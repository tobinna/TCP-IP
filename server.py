import socket 
import threading
import ssl

CONNS = []
ADDRS = []
HEADER = 64             # Package that is sent containing information
PORT = 5050             # Random port chosen on PC, hopefully is not in use
SERVER = socket.gethostbyname(socket.gethostname())     #Getting the IP4 address of the Server
ADDR = (SERVER, PORT)   # Making a variable that encapsulates both Server and the Port
FORMAT = 'utf-8'        # Used for encoding Unicode characters
DISCONNECT_MESSAGE = "DISCONNECT THE CLIENTS"           # Making a variable for ease of use
HR_WARNING_MESSAGE = "HEART BEAT WARNING"               # ''
TEMP_WARNING_MESSAGE = "TEMPERATURE WARNING"            # ''

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) # Making a new socket of type INET
server.bind(ADDR)       # Binding the Address information of the server to the socket


def handle_client(conn, addr):              # Function that takes in the information from the client
    print(f"[NEW CONNECTION] {addr} connected.") # print the IP4 address of the client that has been connected

    connected = True    # Bool created so that this continues for as long as the client is connected to the server
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT) # Decodes the information coming over from client
        if msg_length:  # If there is any information in the message:
            msg_length = int(msg_length)    # get the integer equivelent of the length
            msg = conn.recv(msg_length).decode(FORMAT)  # Take out the part of the message that is actually being sent
            if msg == DISCONNECT_MESSAGE:   # If we were sent the disconnect message
                CONNS[0].close()            # Disconnecte both clients
                CONNS[1].close()            # CAN REMOVE WHEN USING ACTUAL SENSORS
                dial_numbers(DIAL_NUMBERS)  # And call the carer in case of any emergency
                connected = False           # Leave the loop and disconnect the clients
            elif msg == HR_WARNING_MESSAGE: # If patients hear rate is off:
                dial_numbers(DIAL_NUMBERS)  # Dial emergency contact
                CONNS[0].send("CONTACT YOUR CARER IF YOU ARE NOT IN TROUBLE".encode(FORMAT)) # Send message to client
                CONNS[1].send("CHECK PATIENT HEART RATE".encode(FORMAT)) # Send message to carer

            elif msg == TEMP_WARNING_MESSAGE:# If temp is off in either: 
                CONNS[0].send("\nPOSSIBLE COVID CASE: Your carer has been notified, remain indoors".encode(FORMAT)) # Patient message
                CONNS[1].send("\nPOSSIBLE CLOSE CONTACT: Seek immediate medical attention\nif you have serious symptoms. Always call before visiting your doctor or health facility.".encode(FORMAT))
            elif msg == "CARER TEMPERATURE WARNING":
                CONNS[1].send("\nPOSSIBLE COVID CASE: Seek immediate medical attention\nif you have serious symptoms. Always call before visiting your doctor or health facility.".encode(FORMAT))
            else:
                conn.send(" ".encode(FORMAT)) 
            print(f"[{addr}] {msg}")        # Print on the server
            

    conn.close()


      

def start():                # Our function that constantly updates new clients
    server.listen()         # Can specify number of unaccepted connections its willing to make before it stop accepting anything new
    print(f"[LISTENING] Server is listening on {SERVER}") # Small statement on server,prints the IP
    while True:
        conn, addr = server.accept() # make a new instance of conn and addr for every new client
        CONNS.append(conn)           # add new connections to the CONNS list
        ADDRS.append(addr)           # add new connections to the ADDRS list
        thread = threading.Thread(target=handle_client, args=(conn, addr)) # maintain both running in series
        thread.start()               # start the handle_client function
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}") # Display the amount of clients connected
 


from twilio.rest import Client

#Designated number for the server, it calls the carer from this number
TWILIO_PHONE_NUMBER = "+44 7480 559778"

#Include Phone number of the carer, I have used mine here but you may use your own number
#If you want to try it out, send me your phone number and i can authorise it for testing
DIAL_NUMBERS = ["+353852619421"] # Could make different numbers for differnt severitys

TWIML_INSTRUCTIONS_URL = \
  "http://static.fullstackpython.com/phone-calls-python.xml" # Wedsite that calls phone number of carer


client = Client("AC7d4a599076990c099baf9da1cbd4cb8b", "0bbaffe15045decfbe4e9492429d1300") # The address of the website


def dial_numbers(numbers_list): # Phone call function
    
    for number in numbers_list: # Iterates through all the numbers in the list
        print("Dialing Carer Number: " + number)
        client.calls.create(to=number, from_=TWILIO_PHONE_NUMBER,
                            url=TWIML_INSTRUCTIONS_URL, method="GET")



print("STARTING - server is starting up...")
start()         # Get the server going














#If we had a raspberry pi, we could use this instead!!

# hostMACAddress = '8C-8D-28-FD-63-E8' # The MAC address of a Bluetooth adapter on the server. The server might have multiple Bluetooth adapters.
# port = 5050 
# backlog = 1
# size = 1024
# s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
# s.bind((hostMACAddress,port))
# s.listen(backlog)
# def blutooth():
#     try:
#         client, address = s.accept()
#         while 1:
#             data = client.recv(size)
#             if data:
#                 print(data)
#                 client.send(data)
#     except:	
#         print("Closing socket")	
#         client.close()
#         s.close()





#blutooth()