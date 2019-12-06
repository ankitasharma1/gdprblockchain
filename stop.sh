#! /usr/bin/env zsh

# bc_proxy_server
lsof -ti tcp:1025 | xargs kill

# hospital
lsof -ti tcp:1024 | xargs kill
lsof -ti tcp:2000 | xargs kill
lsof -ti tcp:3000 | xargs kill

# physicians
lsof -ti tcp:4000 | xargs kill
lsof -ti tcp:5000 | xargs kill
lsof -ti tcp:6000 | xargs kill

# patients
lsof -ti tcp:7000 | xargs kill
lsof -ti tcp:8000 | xargs kill
lsof -ti tcp:9000 | xargs kill

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
