from flask import Flask
from flask import request
import json
from send_cmd import *
app =Flask(__name__)

@app.route('/',methods=['POST'])
def get_command():
	jsondata = request.get_json()
	data = json.loads(jsondata)
	if validate_command(data)== True: 
		if find_type(data)== 'REST-API':
			send_rest(data)
			result={'code':"Rest command sent to end-device"}
			return json.dumps(result)
		elif find_type(data)=='SOAP':
			send_soap(data)
			result={'code':"SOAP command sent to end-device"}
			return json.dumps(result)
		else:
			send_a429(data)
			result={'code':"ARINC 429 label sent to end-device"}
			return json.dumps(result)
	else :
		result={'code':"Command authentication failed"}
		return json.dumps(result)
def validate_command(received_json):
	temp = received_json
	#print (temp)
	#print (type(temp))
	for i in temp:
		got_cmd = i['cmd']
		got_target = i['target']
		got_sec = i['security']
		with open ('security.json' ,'r') as f:
			sec_dict = json.load(f)
			for data in sec_dict:
				cmd = data['cmd']
				target = data['target']
				security = data['security']
				if got_sec == security:
					print ("Command's security verified")
					return True
				else:
					print ("Do not have the appropriate credentials to perform action")
					return False 
def find_type(received_json):
	temp1=received_json
	for i in temp1:
		got_type =i['type']
	return got_type
if __name__=='__main__':
	app.run(debug=True)
