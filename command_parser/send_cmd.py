import requests
import json
#from arinc429 import *
# Sending an rest request POST to the end device
def send_rest(got_data):
	s = json.dumps(got_data)
        try:
    	    command = requests.post('http://127.0.0.1:8080/command', json=s).json()
    	    print("command sent to evo")
            print(command['code'])
        except ConnectionError as e:
            print(str(e) + " as port 8080 is not open")
# Sending an SOAP request
def send_soap(got_data):
	s = json.dumps(got_data)
	#print ("The dumped data is" s "and the type of dunped data is" type(s))
        try:
            command = requests.post('http://127.0.0.1:8080/command', json=s).json()
            print("command sent to evo")
            print(command['code'])
        except ConnectionError as e:
            print(str(e) + " as port 8080 is not open")
# sending an arinc429 word as a command
def send_a429(got_data):
	s = json.dumps(got_data)
	#print ("The dumped data is" s "and the type of dunped data is" type(s))
        try:
    	    command = requests.post('http://127.0.0.1:8080/command', json=s).json()
	    print("command sent to evo")
	    print(command['code'])
        except ConnectionError as e:
            print(str(e) + "port 8080 is not open")
