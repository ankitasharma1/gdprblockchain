#!/bin/bash

# bc_proxy_server
xterm -title "bc_proxy_server" -e "python bc_proxy_server.py" &

# hospital
xterm -title "hospital_proxy_server 1" -e "python hospital_proxy_server.py hospital_1" &
xterm -title "hospital_proxy_server 2" -e "python hospital_proxy_server.py hospital_2" &
xterm -title "hospital_proxy_server 3" -e "python hospital_proxy_server.py hospital_3" &

# physicians
xterm -title "physician_proxy_client bob" -e "python physician_proxy_client.py bob &" &
xterm -title "physician_proxy_client alice" -e "python physician_proxy_client.py alice" &
xterm -title "physician_proxy_client jane" -e "python physician_proxy_client.py jane" &

# patients
xterm -title "patient_proxy_client sally" -e "python patient_proxy_client.py sally" &
xterm -title "patient_proxy_client eric" -e "python patient_proxy_client.py eric" &
xterm -title "patient_proxy_client joe" -e "python patient_proxy_client.py joe" &

