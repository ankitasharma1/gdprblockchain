### Privacy-First Infrastructure Design for Hospital Record Management

## Description

This project is a proof-of-concept for a system of blockchains (both public and private) for making reading, writing, removing, and transferring patient medical data more secure.

The ecosystem of our project is derived from 'config.yaml.' The configuration file specifies the entities involved and their contact information (ip address and port number). 

Each entity runs its own proxy server:

hospital_proxy_server.py
patient_proxy_client.py
bc_proxy_server.py
physician_proxy_client.py


To try out our project, you will run a startup script that will kick-off all of the required servers for the demo. Go to 'localhost:8080' and play around!

## Usage

###Install `Python 2.x.x`

### Linux: Starting up: ./main_anx.sh

### Mac: Starting up: ./main_james.sh
### Requires 'iTerm2'

### Cleaning up: ./stop.sh

## Notes

- All hospitals have the same hash function
- One card is generated per user
- Patients are associated with only one hospital at a time


## Bug

- We have found that when a physician enters in a large note, this results in a 'plaintext too large error'

## WIP

Physician_Transfer() - the backend is implemented for this but the frontend is currently a WIP.
