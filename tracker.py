#!/usr/bin/env python3

import jsonpickle
import sys
import subprocess
import requests
import hashlib
import os
from os.path import expanduser
import logging as log
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

DEF_CONF_LOC='.website-tracker-conf'
CACHE_DIR='.website-tracker'

def setup_logging():
    log.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=log.INFO)

def sha256(plain):
    return hashlib.sha256(plain.encode()).hexdigest()

def abs_path(path):
    home = home_dir()
    return '{}/{}'.format(home,path)

def mkdir_cache():
    path = abs_path(CACHE_DIR)
    if not os.path.exists(path):
        os.makedirs(path)

def home_dir():
    return expanduser("~")

class PropDict(dict):
    __getattr__= dict.__getitem__
    __setattr__= dict.__setitem__
    __delattr__= dict.__delitem__

class MailSender():

    def __init__(self,config):
        self.config = config
        self.__create_con()

    def send(self,sender,receivers,subject,content):
        try:
            receivers = ', '.join(receivers)
            sender = '{} <{}>'.format(sender, self.config.address)
            self.con.sendmail(sender,receivers,self.__create_msg(sender,receivers,subject,content).as_string())
        except:
            log.error('Failed to send mail')

    def __create_con(self):
        self.con = smtplib.SMTP(self.config.smtp_server,self.config.port)
        if self.config.enable_tls:
            self.con.starttls()
        self.con.login(self.config.address,self.config.password)

    def __create_msg(self,sender,receivers,subject,content):
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = receivers
        msg['Subject'] = subject
        msg.attach(MIMEText(content,'plain'))
        return msg

    def close(self):
        self.con.quit() 

class Tracker:

    def __init__(self,data,sender):
        self.data = data
        self.sender = sender
        self.id = sha256(data.url)

    def track(self):
        html = self.__get_website()
        if html == None:
            return
        hash = sha256(html)

        if not os.path.exists(self.__filepath()):
            self.__write_hash(hash)

        prev_hash = self.__read_hash()
        if prev_hash != hash:
            log.info('Website {} changed'.format(self.data.url))
            self.__write_hash(hash)
            self.__on_change()
        else:
            log.info('Website {} has not changed'.format(self.data.url))
        
    def __write_hash(self,hash):
        with open(self.__filepath(),'w') as f:
            f.write(hash)

    def __read_hash(self):
        with open(self.__filepath(),'r') as f:
            return f.read()

    def __filepath(self):
        return abs_path('{}/{}'.format(CACHE_DIR,self.id))

    def __on_change(self):
        log.info('Sending mail [{},{}] to {} as {}'.format(self.data.subject,self.data.content,self.data.to,self.data.alias))
        self.sender.send(self.data.alias,self.data.to,self.data.subject,self.data.content)

    def __get_website(self):
        try:
            resp = requests.get(self.data.url)
            if resp.status_code <200 or resp.status_code >=300:
                raise Exception('failed to get url')
            return resp.text
        except:
            log.error('Failed to GET {}'.format(self.data.url))
            return None

def load_config():
    path = abs_path(DEF_CONF_LOC)
    if len(sys.argv) >= 2:
        path = sys.argv[1]
    try:
        with open(path,'r') as f:
            return PropDict(jsonpickle.decode(f.read()))
    except Exception as e:
        log.error('Failed to read config file: {} - {}'.format(path,e))
        sys.exit(1)

if __name__ == '__main__':
    setup_logging()
    log.info('Running...')
    mkdir_cache()
    config = load_config()
    sender = MailSender(PropDict(config.sender))
    trackers = map(lambda x: Tracker(PropDict(x),sender),config.trackers)
    for t in trackers:
        t.track()

