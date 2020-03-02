from flask import Flask
from flask import request
import json
import requests
import shutil
import subprocess
import os
from os import path

app =Flask(__name__)

@app.route('/command',methods=['POST'])
def command():
	jsondata = request.get_json()
	data = json.loads(jsondata)
	if execute_command(data)== True:
		result={'code':"Command executed in enddevice"}
		return json.dumps(result)
	else :
		result={'code':"execution failed"}

def execute_command(recv_cmd):
	temp = recv_cmd
	#print (temp "and the type of temp is " type(temp))
	for i in temp:
		if i['cmd']== 'switch':
		    print("The switch command is received")
		    return True
		if i['cmd']== 'delete':
		    print("The delete command is received")
                    if i['target'] == 'evo':
    		        src = '/home/natrinai/kaldi/egs/wsj/s5/test.browsing'
                        subprocess.Popen(['rm %s' % (src)], shell=True)
		    return True
		if i['cmd'] == 'copy':
		    # code for copying files from one directory to usb
		    print ("Inside copy command")
                    if i['target'] == 'evo':
		        src = '/home/natrinai/kaldi/egs/wsj/s5/test.log'
		        dest = '/media/natrinai/SREE/'
                        # sanity checks
                        if path.exists(src):
                            if path.isfile(src):
                                print(src, " log is a file")
                            elif path.isdir(src):
                                print(src, " log is a directory")
                            if path.exists(dest):
                                size_src = int(path.getsize(src))
                                size_dest = int(path.getsize(dest))
                                if size_src < size_dest:
                                    subprocess.Popen(['cp -r %s %s' % (src, dest)], shell=True)
                                    print("Copy completed")
                                else:
                                    print("Not sufficient memory space")
                            else:
                                print("No USB connected, Please connect the USB and perform copy")
                                break
                        else:
                            print(src, " log path does not exist, try another path")
		        #if copytree(src,dest) == True:
		    return True

def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
        	shutil.copytree(s, d, symlinks, ignore)
	    #return True
        else:
        	shutil.copy2(s, d)
        	return True
if __name__=='__main__':
	app.run(host ='127.0.0.1',port = 8080 ,debug=True)
