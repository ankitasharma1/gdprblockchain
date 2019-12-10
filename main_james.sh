#! /usr/bin/env bash

# NOTE: for james's mac only
[ `uname -s` != "Darwin" ] && echo "Cannot run on non-macosx system." && exit

function tab () {
    local cdto="$PWD"
    local args="$@"

    if [ -d "$1" ]; then
        cdto=`cd "$1"; pwd`
        args="${@:2}"
    fi

    osascript -i <<EOF
        tell application "iTerm2"
                tell current window
                        create tab with default profile
                        tell the current session
                                write text "cd \"$cdto\" && $args"
                        end tell
                end tell
        end tell
EOF
}

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
