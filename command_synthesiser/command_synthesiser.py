from flask import Flask
import requests
import json
import time
import subprocess

##########################################################################################
# The functions to be done by command synthesizer is the following things:
#    1. Receive the recognized text and then parsing it 
#	2. Determine if the text is a meaningful command by comparing it to the list of \
#          commands in the config.json file or some other array of commands that are to be performed.
#	3. Determine the target application the command should be sent. 
#	4. Create the command.json file with the attributes like what is the command ?, \
#          where it should be executed ?, what type of handler(is it REST, SOAP or ARINC 429) \
#          to use for the target device.
#	5. Send the command.json through the REST api call.   
###########################################################################################

# check and make directory if doesn't exist
import os
if not os.path.exists('logs'):
    os.makedirs('logs')

# Creates the log files for different methods
def log_generator(filename,text):
	timestr = time.strftime("%Y%m%d-%H%M%S")
	with open(filename, 'a+') as f:    
       			f.write("\nThe received text is "+text+" at time of receiving is "+timestr)

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
			subprocess.Popen(["bash play_tts.sh %s" % (cmd)], shell=True)

def find_target(text,target):
	if target in text:
		print ("target found")
		return  1
	else:
		print ("No target found")
		return -1

# Finds if valid command is present in the text
def find_command(text,cmd):
	if cmd in text:
		print ("command found")
		return  1
	else:
		#print ("command Not found for ")
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
        try:
        	res = requests.post('http://127.0.0.1:5000/', json=s).json()
        except (ConnectionError,NameError) as e:
                print("port 5000 is not open")

	print(res['code'])

def live_audio():
    	count=0
        subprocess.call("bash play_intro.sh", shell=True)
	while True:
		try:
			print ("Press Ctrl+C to stop listening")
			subprocess.call("./kaldi.sh 1", shell=True)	
			live_audio_log = 'logs/live_audio_log'
			text = open("asr_out.parsed", 'r').readlines()[0].split('\n')[0]
                        if not text:
                            break
			print ("print in command synthesizer:",text)
			checktext(text)
                        subprocess.call("sleep 2", shell=True)
			log_generator(live_audio_log,text)
		except Exception as e:
			count+=1
			if count >3:
				textip=input("Enter the Text as i/p within quotes\":")
				text_ip_log = 'logs/text_ip_log'	
				checktext(textip)
				log_generator(text_ip_log,textip)
			print("\nNo command from the NLP engine, exception occured",e)
			print(" \nAfter 3 attempts you will be prompted to enter text as command ")		
                        #subprocess.Popen(["bash play_tts.sh"], shell=True)

def test_audio():	
	while True:
            try:
                        #Insted of live audio from mic use the test audio file 
			print ("Press Ctrl+C to stop execution")
			filename= input("enter the audiofile name:")
			subprocess.call("./kaldi.sh 2", shell=True)
			record_audio_log = 'logs/recorded_audio_log'
			audio_text = open("asr_out.parsed", 'r').readlines()[0].split('\n')[0]
			print ("print in command synthesizer:",audio_text)			 
			checktext(audio_text)
			log_generator(record_audio_log,audio_text)
	    except Exception as e:
			print ("Audio file decoding interupted due to the following exception:",e)

if __name__ == "__main__":
	try:
		print("1.Live audio mode\n 2.Testaudio mode")
		choice=str(input("enter the mode to run code(1 or 2):"))
		if choice == '1':
			live_audio()
		if choice == '2':
			test_audio()
	except KeyboardInterrupt:
			print ("The command synthesizer is stopped")
