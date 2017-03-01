####
## script to take a snapshot using a snapshot url for foscam cameras and upload the file to slack

from slacker import Slacker
#import os
import sys
#from datetime import datetime
#import logging
#import time
#import requests
import urllib.request
import yaml

configdir = "/config"
#configdir = "x:\\hass-config"

with open('{}/secrets.yaml'.format(configdir), 'r') as sf:
    secrets = yaml.load(sf)
slack_cams_api_key = secrets["slack_cams_api_key"]

if len(sys.argv) > 1:
    #set variables
    slack = Slacker(slack_cams_api_key)
    cam = str(sys.argv[1])
    #filename = ("C:\\temp\\{}.jpg").format(cam)
    filename = ("{}/shell_command_scripts/{}.jpg").format(configdir,cam)

    if cam == "garagecam":
        user = secrets["bi_garagecam_user"]
        pw = secrets["bi_garagecam_pass"]
        garagecam_url = secrets["bi_garagecam_url"]
        url = "{}/CGIProxy.fcgi?cmd=snapPicture2&usr={}&pwd={}".format(garagecam_url,user,pw)
    elif cam == "jackcam":
        url = ""
    elif cam == "ryancam":
        url = ""
    else:
        url = ""

    #download the snapshot
    if url != "":
        urllib.request.urlretrieve(url, filename)
        slack.files.upload(filename,'','','','','','#notifications')
    else:
        print("camera not on my list...")
else:
    print("no camera provided")
