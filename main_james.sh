#! /usr/bin/env zsh

# NOTE: for james's mac only
source ~/.tab.bash

# bc_proxy_server
tab "python bc_proxy_server.py";

# static
tab "python static_server.py";

# hospitals
tab "python hospital_proxy_server.py hospital_1";
tab "python hospital_proxy_server.py hospital_2";
tab "python hospital_proxy_server.py hospital_3";

# physicians
tab "python physician_proxy_client.py bob";
tab "python physician_proxy_client.py alice";
tab "python physician_proxy_client.py jane";

# patients
tab "python patient_proxy_client.py sally";
tab "python patient_proxy_client.py eric";
tab "python patient_proxy_client.py joe";
