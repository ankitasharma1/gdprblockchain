import yaml
CONFIG_FILE = 'config.yaml'

# Parse config.txt and create appropriate classes/kick off/spawn shells

# Clean up if killed
"""
Initialize 
    1. blockchain, 
    2. hospital dbs for all hospitals
    3. hasher
    4. hospitals 
    5. hosptial dns - csv with ip and port
    6. patients

Cleanup
"""

def parse(path):
    with open(path, 'r') as f:
        doc = yaml.load(f)

def clean_up(path):
    close(path)

def main():
    parse(CONFIG_FILE)
    clean_up(CONFIG_FILE)

main()