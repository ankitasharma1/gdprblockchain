#! /usr/bin/env zsh

# bc_proxy_server
lsof -ti tcp:1025 | xargs kill

# hospital
lsof -ti tcp:1024 | xargs kill
lsof -ti tcp:2000 | xargs kill
lsof -ti tcp:2100 | xargs kill

# physicians
lsof -ti tcp:2200 | xargs kill
lsof -ti tcp:2300 | xargs kill
lsof -ti tcp:2400 | xargs kill

# patients
lsof -ti tcp:2500 | xargs kill
lsof -ti tcp:2600 | xargs kill
lsof -ti tcp:2700 | xargs kill

# static
lsof -ti tcp:8080 | xargs kill

# blockchain
lsof -ti tcp:8001 | xargs kill

# hospital
lsof -ti tcp:8002 | xargs kill
lsof -ti tcp:8003 | xargs kill
lsof -ti tcp:8004 | xargs kill

# patients
lsof -ti tcp:8005 | xargs kill
lsof -ti tcp:8006 | xargs kill
lsof -ti tcp:8007 | xargs kill

# physicians
lsof -ti tcp:8008 | xargs kill
lsof -ti tcp:8009 | xargs kill
lsof -ti tcp:8010 | xargs kill
