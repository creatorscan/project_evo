from flask import Flask
import requests
import json
import time
import subprocess

''' The functions to be done by command synthesizer is the following things:
    1. Receive the recognized text and then parsing it 
	2. Determine if the text is a meaningful command by comparing it to the list of commands in the config.json file or some other array of commands that are to be performed.
	3. Determine the target application the command should be sent. 
	4. Create the command.json file with the attributes like what is the command ?, where it should be executed ?, what type of handler(is it REST, SOAP or ARINC 429) to use for the target device.
	5. Send the command.json through the REST api call.   
'''
# find the source for copying files
'''
def find_source(text,source):
	if (text.find(source)== -1):
		return 1	
	else:
		return -1	
	#return source
# find the destination to copy files to
def find_destination(text, destination):
	if (text.find(destination)== -1):
		return 1	
	else:
		return -1
	#return destination'''
# check if the recognized text has the keywords to create the command
def checktext(text): 
	with open ('config.json' ,'r') as f:
		config_dict = json.load(f)
	for config in config_dict:
		cmd = str(config['cmd'])
		calltype = str(config['type'])
		target = str(config['target'])
		if find_command(text,cmd)==1:
			print ("The Given text is a valid text , now creating command")
			print ("The cmd word present is ",cmd,"and the target word present is", target)
			send_command(cmd,target,calltype)
                        subprocess.Popen(["bash -x play_tts.sh %s" % (cmd)], shell=True)
		#else:
	        #	print ("command and target not found")
def find_target(text,target):
	if text == target:
		print ("target found")
		return  1
	else:
		print ("No target found")
		return -1
# Finds if valid command is present in the text
def find_command(text,cmd):
	if text == cmd:
		print ("command found")
		return  1
	else:
		print ("command Not found")
		return -1
def send_command(command,target,calltype):
	print ("Inside the send_command function")
        data =[{
		'cmd' :str(command),
		'target': str(target),
		'type': str(calltype),
		'security':str("allowed")
	}]
	s = json.dumps(data)
	res = requests.post('http://127.0.0.1:5000/', json=s).json()   
	print(res['code'])

def live_audio():
	'''	
	print ('Inside main function')	
	text=subprocess.check_output(['./nnet3_online.sh'])
	#text = subprocess.call(['./nnet3_online.sh'])	
	print ("The got text is",text)
	print (type(text))
	'''

        #subprocess.call("./play_intro.sh", shell=True)
	while True:
		count=0
                subprocess.call("./command_synthesizer.sh 1", shell=True)
                text = open("asr_out.parsed", 'r').readlines()[0].split(' ')[0]
		#text=live_recognizer()
		timestr = time.strftime("%Y%m%d-%H%M%S")
		textlog = 'textlog'+timestr
		print ("print in command synthesizer:",text)
		if text != None:
			with open(textlog, 'w') as f:    
       				f.write("\n"+text) 
			checktext(text)
                else:
         		print ('/n No command found in recognized text, say again:\n')
		count+=1
		if count >3:
			textip=input("Enter the Text as i/p:")
			checktext(textip)
def test_audio():	
	while True:
	#Insted of live audio from mic use the test audio file 
		filename= input("enter the audiofile name:")
                subprocess.call("./command_synthesizer.sh 2", shell=True)
                text = open("asr_out.parsed", 'r').readlines()[0].split(' ')[0]
		#text = test_wavs(filename)
		timestr = time.strftime("%Y%m%d-%H%M%S")
		textlog = 'textlog'+timestr
		print ("print in command synthesizer:",text)
		if text != None:
			with open(textlog, 'w') as f:    
       				f.write("\n"+text) 
			checktext(text)

print("1.Live audio mode\n 2.Testaudio mode")
choice=str(input("enter the mode to run code(1 or 2):"))
if choice == '1':
	live_audio()
if choice == '2':
	test_audio()
