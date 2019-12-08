import socket
import sys
from constants import ADDRESS
from constants import PORT
from parser import Parser
from threading import Thread
from threading import Condition
from physician import Physician
from constants import MESSAGE_SIZE
from constants import TYPE
import constants
import patient_msg
import card_helper
from flask import Flask, request, render_template, jsonify
import json
from requests import post

"""
Supported Commands
"""
EXIT = 'exit'
REGISTER = 'reg'
HOSPITALS = 'hospitals'

"""
Supported Commands Params
"""
NUM_REGISTER_PARAMS = 2 # 'reg [hospital name]'

phys = None
parser = Parser()

PHYSICIAN_TREATMENT_MSGS = []
PHYSICIAN_READ_MSGS = []
GLOBAL_CARD_PATH = None
PHYSICIAN_PORT = {
    'bob': 8008,
    'alice': 8009,
    'jane': 8010
}

app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')


def main():
    """
    Wrapper around the physician class.
    """
    arguments = sys.argv
    if len(arguments) < 2:
        print("ERROR: missing argument - %s" %(parser.get_phys_names_string()))
        return

    physician_name = arguments[1]

    if not parser.valid_phys(physician_name):
        print("ERROR: invalid argument - %s" %(parser.get_phys_names_string()))
        return

    # Construct physician using info. from parser.
    global phys
    phys = Physician(physician_name, parser.get_phys_id(physician_name))
    contact_info = parser.get_phys_contact_info(physician_name)
    address = contact_info[ADDRESS]
    port = contact_info[PORT]

    # Condition variable for clean termination.
    cv = Condition()

    # Condition variable for other thread reading from stdin.
    read_from_stdin = Condition()

    # Create socket object.
    s = socket.socket()
    s.bind(('', port))
    print("Socket binded to %s" %(port))

    # Put the socket into listening mode.        
    s.listen(5)
    print("Socket is listening")

    # Spawn repl thread.
    print("Starting repl for %s." %(physician_name))
    t = Thread(target=repl, args=(s, cv))
    t.daemon = True
    t.start()

    # Spawn connection thread.
    t = Thread(target=handle_connection, args=(s,))
    t.daemon = True
    t.start()

    # Start flask server for frontend
    t = Thread(target=flask_thread(), args=())
    t.daemon = True
    t.start()

    # Wait for termination.
    termination = False    
    cv.acquire()
    while not termination:
        cv.wait()
        termination = True
        cv.release()

def repl(s, cv):
    print("Kicking off REPL\n\n")
    while True:
        commands = sys.stdin.readline().split()
        try:
            command = commands[0]
            if command == EXIT:
                # Close the socket.
                s.close()
                cv.acquire()
                # Notify main thread that user would like to exit.
                cv.notify()
                cv.release()
                return
            elif command == REGISTER:
                if len(commands) != NUM_REGISTER_PARAMS:
                    print( "Usage: reg [hospital name]")
                    continue
                hospital_name = commands[1]
                register(hospital_name)
            elif command == HOSPITALS:
                print(phys.get_hospitals())            
            else:
                print("Supported Commands: [" + EXIT + ", " + HOSPITALS + ", " + REGISTER + "]")
        except Exception, e:
            print(e)

def register(hosp_name):
    if not parser.valid_hosp(hosp_name):
        print("ERROR: invalid hospital - %s" %(parser.get_hosp_names_string()))
        return

    hosp_contact_info = parser.get_hosp_contact_info(hosp_name)
    return phys.register(hosp_name, hosp_contact_info[ADDRESS], hosp_contact_info[PORT])

def handle_connection(s):
    while True:
        try:
            c, addr = s.accept()
            print("Got connection from " + addr[0] + ": " + str(addr[1]))
            # Start a thread for each socket.
            t = Thread(target=listen_on_socket, args=(c,))
            t.daemon = True
            t.start()
        except Exception, e:
            #print(e)
            return

def listen_on_socket(c):
    while True:
        try:
            data = c.recv(MESSAGE_SIZE)
            if data:
                messages = constants.deserialize(data)
                for message in messages:
                    response = handle_message(message)
                    c.send(response)
            else:
                return clean_up(c)
        except Exception, e:
            print(e)
            return clean_up(c)

def handle_message(message):
    type = message.get(TYPE)
    if type == patient_msg.SEEK_TREATMENT:
        global PHYSICIAN_TREATMENT_MSGS
        card_path = message.get(patient_msg.CARD_PATH)
        phys_port = PHYSICIAN_PORT[phys.name]
        resp = post('http://127.0.0.1:%s/dashboard/physician/%s' % (phys_port, phys.name), data={'seek_treatment': card_path} )

        if resp.text == 'None':
            return patient_msg.seek_treatment_msg_response(False)
        else:
            PHYSICIAN_TREATMENT_MSGS.append(resp.text)
            return patient_msg.seek_treatment_msg_response(True)
    elif type == patient_msg.PHYS_READ:
        global PHYSICIAN_READ_MSGS
        card_path = message.get(patient_msg.CARD_PATH)
        card = card_helper.get_card_object(card_path)
        print("-------> Request to read medical records for %s" % card.patient_name)
        PHYSICIAN_READ_MSGS.append("-------> Request to read medical records for %s" % card.patient_name)
        # API Call #
        hosp_contact_info = parser.get_hosp_contact_info(card.hospital_name)
        success, records = phys.read_patient_record(card_path, hosp_contact_info[ADDRESS], hosp_contact_info[PORT])
        if success:
            resp = patient_msg.phys_read_response_msg(True)
            for r in records:
                PHYSICIAN_READ_MSGS.append(r)            
            return resp
        PHYSICIAN_READ_MSGS.append("-------> Could not read medical records for %s" % card.patient_name)            
        resp = patient_msg.phys_read_response_msg(False)
        return resp
    elif type == patient_msg.PHYS_TRANSFER:
        card_path = message.get(patient_msg.CARD_PATH)
        card = card_helper.get_card_object(card_path)
        src_hospital = message.get(patient_msg.SRC_HOSPITAL)
        print("-------> Request to transfer medical records for %s" %(card.patient_name))
        # TODO: Don't hardcode this.
        dest_hospital = "hospital_3"  

        # Validate params before making API call.
        if not parser.valid_hosp(dest_hospital):
            print("ERROR: invalid hospital - %s" %(parser.get_hosp_names_string()))
            return patient_msg.phys_transfer_response_msg(False)   

        src_hosp_contact_info = parser.get_hosp_contact_info(src_hospital)
      
        # API Call #
        if phys.transfer(card_path, src_hospital, src_hosp_contact_info[ADDRESS], src_hosp_contact_info[PORT], dest_hospital):
            return patient_msg.phys_transfer_response_msg(True)
        return patient_msg.phys_transfer_response_msg(False)   
    else:
        print("ERROR: unknown type %s" %(type))

def clean_up(c):
    print("Closing connection")
    c.close()


@app.route('/dashboard/physician/' + sys.argv[1], methods=['GET', 'POST'])
def dashboard():
    global GLOBAL_CARD_PATH
    global PHYSICIAN_READ_MSGS
    global PHYSICIAN_TREATMENT_MSGS
    global phys
    if request.method == 'GET':
        return render_template('dashboard.html', entity_type='physician', name=phys.name)
    elif request.method == 'POST':
        if 'physician_id' in request.form:
            response = phys.physician_id
        elif 'hospitals' in request.form:
            response = parser.get_hosp_names_string()
        elif 'register' in request.form:
            hospital_name = request.form.get('register')
            if register(hospital_name):
             response = "Registration successful"
            else:
                response = "Error registering"
        elif 'affiliated_hospitals' in request.form:
            response = phys.get_hospitals()
        elif 'read' in request.form:
            response = PHYSICIAN_READ_MSGS
        # TODO: Finish physician APIs by hooking into the handle_message def
        elif 'seek_treatment' in request.form:
            if GLOBAL_CARD_PATH:
                response = None
            else:
                # card path set above via handle_message()
                GLOBAL_CARD_PATH = request.form['seek_treatment']
                card = card_helper.get_card_object(GLOBAL_CARD_PATH)
                if card:
                    response = "-------> Request for treatment from %s" % card.patient_name
                else:
                    response = None
        elif 'submit_treatment' in request.form:
            if GLOBAL_CARD_PATH:
                card = card_helper.get_card_object(GLOBAL_CARD_PATH)
                hosp_contact_info = parser.get_hosp_contact_info(card.hospital_name)
                notes = request.form['submit_treatment']
                if phys.seek_treatment(GLOBAL_CARD_PATH, notes, hosp_contact_info[ADDRESS], hosp_contact_info[PORT]):
                    patient_msg.seek_treatment_msg_response(True)
                    GLOBAL_CARD_PATH = None
                    response = "Successfully wrote to hospital db for %s" % card.patient_name
                else:
                    patient_msg.seek_treatment_msg_response(False)
                    GLOBAL_CARD_PATH = None
                    response = "Unsuccessful update."                   
            else:
                response = "Error: missing patient consent for treatment"
        elif 'update_phys_treatment_msgs' in request.form:
            response = PHYSICIAN_TREATMENT_MSGS
        else:
            response = ["Error: Flask request not recognized"]
        return jsonify(response)


def flask_thread():
    # TODO: disable debug
    app.run(port=PHYSICIAN_PORT[phys.name])

main()
