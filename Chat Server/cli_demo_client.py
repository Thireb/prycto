import socket
from threading import Thread
from datetime import datetime
import json

# server's IP address
# if the server is not on this machine, 
# put the private (network) IP address (e.g 192.168.1.2)
SERVER_HOST = "127.0.254.1"
SERVER_PORT = 5002 # server's port

# initialize TCP socket
s = socket.socket()
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
# connect to the server
s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected.")

# prompt the client for a name
name = input("Enter your name: ")

def listen_for_messages():
    while True:
        message = s.recv(1024).decode()
        # print("\n" + message)
        incoming_json = json.loads(message)
        inc_name = incoming_json['name']
        inc_date = incoming_json['time']
        inc_msg =  incoming_json['msg']
        if (inc_name == name):
            # print(f'Me : {inc_date} : {inc_msg}')
            print('DELIVERED')
            print("\n")
            pass
        else:
            print(f'{inc_name} : {inc_date} : {inc_msg}')
            print("\n")


# make a thread that listens for messages to this client & print them
t = Thread(target=listen_for_messages)
# make the thread daemon so it ends whenever the main thread ends
t.daemon = True
# start the thread
t.start()

while True:
    # input message we want to send to the server
    to_send =  input()

    # add the datetime, name & the color of the sender
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    ## EXP SEND 
    # to_send = f"{client_color}[{date_now}] {name}{separator_token}{to_send}{Fore.RESET}"
    
    # making a dict of things for sending
    msg_dic = dict()
    msg_dic['name']=name
    msg_dic['time']=date_now
    msg_dic['msg']=to_send

    # check for internal app command
    if (msg_dic['msg'].split(" ")[0]=="/app"):
        # if its the exit command / to close the app
        if (msg_dic['msg'].split(" ")[1]=="exit"):
            # close the socket
            s.close()
            # closing the app
            quit()
        # a kind of useful-ish help message
        elif (msg_dic['msg'].split(" ")[1]=="help"):
            # a help screen
            print("[i] Help Screen of app commands using /app thing\n")
            print("[*] help - shows this page\n")
            print("[*] exit - trys to disconnect and kills the client\n")
        else:
            # printing a generic message
            print("[!] Unknow Command\n")
    else:
        # jsonify the message for the next clinet
        msg_send = json.dumps(msg_dic)
        # finally, send the message
        s.send(msg_send.encode())
