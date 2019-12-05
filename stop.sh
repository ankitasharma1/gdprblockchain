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
