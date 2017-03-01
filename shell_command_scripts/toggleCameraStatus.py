#####
## script to toggle jackcam and ryancam (disabled/enabled)

import json
import requests
import hashlib
import sys
from datetime import datetime
import logging
import time
import yaml

configdir = "/config"
#configdir = "x:\\hass-config"

with open('{}/secrets.yaml'.format(configdir), 'r') as sf:
    secrets = yaml.load(sf)

bi_server = secrets["bi_server"]
bi_user = secrets["bi_user"]
bi_pass = secrets["bi_pass"]

if sys.argv[1] == "disabled":
	enabled = False
elif sys.argv[1] == "enabled":
	enabled = True
else:
	quit

url = "http://{}:81/json".format(bi_server)
data = {'cmd':'login'}
r = requests.post(url,json.dumps(data))
session = r.json()['session']
#print(session)

if session != "":
	str = "{0}:{1}:{2}".format(bi_user,session,bi_pass)
	m = hashlib.md5()
	m.update(str.encode('utf-8'))
	hash = m.hexdigest()
	data = {'cmd':'login','session':session,'response':hash}
	print(json.dumps(data))
	r = requests.post(url,json.dumps(data))

	if r.json()['result'] == 'success':
		data = {'cmd':'status','session':session}
		print(json.dumps(data))
		r = requests.post(url,json.dumps(data))
		if r.json()['result'] == 'success':
			cams = "ryancam","jackcam"
			time.sleep(3)
			for cam in cams:
				#enabled = "false"
				data = {'camera':cam,'enable':enabled,'session':session,'cmd':'camconfig'}
				print(json.dumps(data))
				r = requests.post(url,json.dumps(data))
				#time.sleep(3)
				#print(r.json()['result'])
