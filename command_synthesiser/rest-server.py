from flask import Flask
import requests
import sys
import json
from deepspeech_parser import *
''' The functions to be done by command synthesizer is the following things:
    1. Receive the recognized text and then parsing it 
	2. Determine if the text is a meaningful command by comparing it to the list of commands in the config.json file or some other array of commands that are to be performed.
	3. Determine the target application the command should be sent. 
	4. Create the command.json file with the attributes like what is the command ?, where it should be executed ?, what type of handler(is it REST, SOAP or ARINC 429) to use for the target device.
	5. Send the command.json through the REST api call.   
'''
# find the source for copying files
def find_source(text,source):
	if (text.find(source)== -1):
		#print ("copy source found")
		return 1	
	else:
		#print ("copy source found")
		return -1	
	#return source
# find the destination to copy files to
def find_destination(text, destination):
	if (text.find(destination)== -1):
		#print ("destination found")
		return 1	
	else:
		#print ("destination Not found")
		return -1
	#return destination
#text = "Print the log in Evo"
# check if the recognized text has the keywords to create the command
def checktext(text): 
	print ("The Given text is :",text)
	with open ('config.json' ,'r') as f:
		config_dict = json.load(f)
	for config in config_dict:
		cmd = config['cmd']
		#print (cmd)
		calltype = config['type']
		target = config['target']
		#print ("The text found is:",text)
		if find_command(text,cmd)==1 and find_target(text,target)==1:
			print ("The Given text is a valid text , now creating command")
			print ("The cmd word present is ",cmd,"and the target word present is", target)
			send_command(cmd,target,calltype)
		#else:
			#print ("command and target not found not found")
def find_target(text,target):
	if (text.find(target)!= -1):
		#print ("target found")
		return  1
	else:
		#print ("No target found")
		return -1
# Finds if valid command is present in the text
def find_command(text,cmd):
	if (text.find(cmd)!= -1):
		#print ("command found")
		return  1
	else:
		#print ("command Not found")
		return -1
def send_command(command,target,calltype):
	#print ("Inside the send_command function")
	data =[{
		'cmd' :command,
		'target': target,
		'type': calltype,
		'security':"allowed"
	}]
	s = json.dumps(data)
	res = requests.post('http://127.0.0.1:5000/', json=s).json()   
	print(res['code'])

while True:
	#text=main()
	filename= input("enter the filename:")
	text = test_wavs(filename)

	#print ("print in command synthesizer:",text)
	if text != None:
		with open('spoken.txt', 'a') as f:    
       			f.write("\n"+text) 
		checktext(text)
#textip=input("Enter the command:")
#checktext(textip)
