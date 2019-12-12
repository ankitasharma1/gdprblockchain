import subprocess

child_processes = []

"""
print("Kicking off static_server")
p = subprocess.Popen(["python", "static_server.py"])
child_processes.append(p)
"""

print("Kicking off bc_proxy_server")
p = subprocess.Popen(["python", "bc_proxy_server.py"])
child_processes.append(p)

print("Kicking off hospital_proxy_server hospital_1")
p = subprocess.Popen(["python", "hospital_proxy_server.py", "hospital_1"])
child_processes.append(p)

"""
print("Kicking off hospital_proxy_server hospital_2")
p = subprocess.Popen(["python", "hospital_proxy_server.py", "hospital_2"])
child_processes.append(p)

print("Kicking off hospital_proxy_server hospital_3")
p = subprocess.Popen(["python", "hospital_proxy_server.py", "hospital_3"])
child_processes.append(p)

print("Kicking off physician_proxy_client bob")
p = subprocess.Popen(["python", "physician_proxy_client.py", "bob"])
child_processes.append(p)

print("Kicking off physician_proxy_client alice")
p = subprocess.Popen(["python", "physician_proxy_client.py", "alice"])
child_processes.append(p)

print("Kicking off physician_proxy_client jane")
p = subprocess.Popen(["python", "physician_proxy_client.py", "jane"])
child_processes.append(p)

print("Kicking off patient_proxy_client sally")
p = subprocess.Popen(["python", "patient_proxy_client.py", "sally"])
child_processes.append(p)

print("Kicking off patient_proxy_client eric")
p = subprocess.Popen(["python", "patient_proxy_client.py", "eric"])
child_processes.append(p)
"""

print("Kicking off patient_proxy_client joe")
p = subprocess.Popen(["python", "patient_proxy_client.py", "joe"])
child_processes.append(p)

for cp in child_processes:
    cp.wait()
    

