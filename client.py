import socket
import time
import random

HEADER = 64              # Package that is sent containing information
PORT = 5050             # Random port chosen on PC, hopefully is not in use
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT THE CLIENTS"
SERVER = "192.168.1.16" # Server we are trying to connect to
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Set up the client socket
client.connect(ADDR)

def send(msg):
    yerp = str(msg)     # Converts numbers into a string
    message = yerp.encode(FORMAT)   # Encodes them so we can send them
    msg_length = len(message)       # Gathers the length of the message
    send_length = str(msg_length).encode(FORMAT)    # Encodes the length of the message
    send_length += b' ' * (HEADER - len(send_length))   # Fills up the send length so that there are 64 characters
    client.send(send_length)    # Sends header to Server so it can get ready for message
    client.send(message)        # sends the message after
    received = client.recv(2048).decode(FORMAT) # Prints out what was sent back by the server on Patient terminal
    print(received)




#Random numbers to simulate the sensor for the heart rate and temperature

input()             # Waits on an enter input from the user in the command line
time.sleep(3)       # Waits 3 seconds

on = 50
while on > 0 :
    time.sleep(1)
    heartr = random.uniform(59, 101)
    if heartr < 60 or heartr > 100:
        send("HEART BEAT WARNING")
    else:
        heartr =  round(heartr, 3)
        heartr = str(heartr) + " PATIENT HEART BEAT"
        send(heartr)
    temp = random.uniform(36.0, 38.0)
    if  temp > 37.5:
        send("TEMPERATURE WARNING")
    else:
        temp =  round(temp, 3)
        temp = str(temp) + " PATIENT TEMPERATURE"
        send(temp)
    on = on - 1


#In the actual device, this would be sensor information being read in
# import csv


# file = open('patient_data.csv')
# csv_reader = csv.reader(file)
# next(csv_reader)    

# e = 10
# while e > 0:
#     for row in csv_reader:
#         time.sleep(0.2)
#         value = int(row[0])
#         if value < 50 or value > 100:
#             send("HEART BEAT WARNING")
#         else:
#             send(row[0])

#     e = e-1


send(DISCONNECT_MESSAGE)

