import socket
import time
import random

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT THE CLIENTS"
SERVER = "192.168.1.16"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    yerp = str(msg)
    message = yerp.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    received = client.recv(2048).decode(FORMAT)
    print(received)


input()
time.sleep(3)

#Random heart rate and temp to simulate the sensor
on = 50
while on > 0 :
    time.sleep(1)
      
    temp = random.uniform(36.0, 38.0)
    if temp > 37.5:

        send("CARER TEMPERATURE WARNING")
    else:
        temp =  round(temp, 3)
        temp = str(temp) + " CARER TEMPERATURE"
        send(temp)
    on = on - 1



#In the actual device, this would be sensor information being read in
# import csv
# file = open('patient_data.csv')
# csv_reader = csv.reader(file)
# next(csv_reader)

#If i wanted to parse from the excel file
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

