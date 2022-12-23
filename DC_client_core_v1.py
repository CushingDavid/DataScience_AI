# Import system level functionalities.
import logging  # Import Logging module to capture errors in log.file.
import os  # Import OS to allow calls to Operating System
import sys  # Import sys to allow system command - restart
import subprocess  # Import Subprocess to allow restarts
import socket  # Import sockets for Network Transfers
import pickle  # Import pickle function for serialization.
import json  # Import Json functionality to create json files
import time  # Import time function to allow sleep
from xml.etree.ElementTree import Element, tostring  # Import xml functions
from cryptography.fernet import Fernet  # Import Crytography functions
from Functions import external_functions  # Retrieve external functions.
from Functions.external_functions import Program_Info  # Import class type for title page

transfer_file = " "  # Declare variable as empty until required

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096  # send 4096 bytes each time step

#  info = Program_Info("the name",the version,)
data = Program_Info("CSCK541 Software in Development Group Project", "1.0", "May 2022",
                    "C.Beeby, D. Cushing, D. Lambert "
                    )

# initialize the log settings.
logging.basicConfig(filename='client_app.log', filemode='w', level=logging.DEBUG)  # Set logging options.

# Trash any previous file instances - for clean start
def df_remove(): 
    files = ['datafile.xml', 'datafile.bin', 'datafile.json', 'edatafile.xml', 'edatafile.bin', 'edatafile.json', 'filekey.key']
    # for f in glob.glob(files):
    for f in files:
        if os.path.exists(f):
            print(f"Removing file {f}")
            os.remove(f)
        else:
            print(f"The system cannot find the file {f} to remove")

df_remove()

# Create or Empty Existing App.log file.
with open('client_app.log', 'w') as f:
    f.write(' ')

# Enable this section to test logging is functioning
try:
    test_val1 = 1
    test_val2 = 0
    print(test_val1 / test_val2)
except ZeroDivisionError as e:
    logging.error("Logging confirmed as active", exc_info=True)

# Define all internal functions to be called within the program.


# Body Part 1 - Title Screen

#  Display Title Page
external_functions.clear()  # Clear existing screen contents
external_functions.title_page(data.program_name, data.version, data.release, data.author,
                              data.contact_name, data.contact_type, data.contact_data, data.info_string)

print("\t" + "Waiting 10 seconds before continuing")
time.sleep(10)

external_functions.clear()

# Body Part 2 - Create Dictionary from text file

d = {}
with open("dictionary.txt") as f:
    for line in f:
        (key, val) = line.split(':')
        d[str(key)] = val

#  Encode file as Bin, JSON or XML depending on user response

encoding_type = input("Enter how you wish to encode your data"
                      "\n B - Binary, J - JSON, X - XML : ")
if encoding_type.lower() == "b":
    ofile = open('datafile.bin', 'wb')
    transfer_file = 'datafile.bin'
    pickle.dump(d, ofile)
    ofile.close()
elif encoding_type.lower() == "j":
    ofile = open('datafile.json', 'w')
    transfer_file = 'datafile.json'
    json.dump(d, ofile)
    ofile.close()
elif encoding_type.lower() == "x":
    root_node = Element('Country_List')
    transfer_file = 'datafile.xml'
    for key, value in d.items():
        child_node = Element(key)
        child_node.text = value
        root_node.append(child_node)

    xml_data = tostring(root_node)
    # print(xml_data)

    with open('datafile.xml', 'wb') as file:
        file.write(xml_data)

# Body Part 4 - Ask user if they want to encrypt the data

encrypt = input("Do you wish to encrypt the file before sending? (Y/N) : ")
if encrypt.lower() == "y":
    print("Encryption Requested" +
          "\n\nPlease wait while file is encrypted")

    # Encrypting
    #  Key generation
    key = Fernet.generate_key()

    # string the key in a file
    with open('filekey.key', 'wb') as filekey:
        filekey.write(key)

    # open the key

    with open('filekey.key', 'rb') as filekey:
        key = filekey.read()

    # use the generated key
    fernet = Fernet(key)

    if transfer_file == "datafile.bin":
        # opening the binary file to encrypt
        with open('datafile.bin', 'rb') as file:
            original = file.read()

        # encrypt the file
        encrypted = fernet.encrypt(original)

        # writing the encrypted data
        with open('edatafile.bin', 'wb') as encrypted_file:
            encrypted_file.write(encrypted)

        os.remove('datafile.bin')
        transfer_file = "edatafile.bin"
        print("File has been encrypted...")

    if transfer_file == "datafile.json":
        # opening the json file to encrypt
        with open('datafile.json', 'rb') as file:
            original = file.read()

        # encrypting the file
        encrypted = fernet.encrypt(original)

        # writing the encrypted data
        with open('edatafile.json', 'wb') as encrypted_file:
            encrypted_file.write(encrypted)

        os.remove('datafile.json')
        transfer_file = "edatafile.json"

        print("File has been encrypted...")

    if transfer_file == "datafile.xml":
        # opening the original file to encrypt
        with open('datafile.xml', 'rb') as file:
            original = file.read()

        # encrypting the file
        encrypted = fernet.encrypt(original)

        # writing the encrypted data
        with open('edatafile.xml', 'wb') as encrypted_file:
            encrypted_file.write(encrypted)
        os.remove('datafile.xml')
        transfer_file = "edatafile.xml"
        print("File has been encrypted...")

#  Encryption not selected, provide an indicator to the Server it isn't

if encrypt.lower() == "n":
    no_encryption = "File not encrypted"
    with open('filekey.key', 'w') as not_encrypted_file:
        not_encrypted_file.write(no_encryption)

#  Transfer files to Server

host = input("\nPlease provide hostname or IP \n"
             "Hint.... if both server and client are "
             "\non the same machine use localhost : ")

print("\nTransfering to: " + host)  # Confirm to user the host they specified

# Use port 81 - noted as an Unassigned TCP/IP at www.iana.org
port = 81
# Send the key file first
filename = 'filekey.key'

# get the file size
filesize = os.path.getsize(filename)
# create the client socket
s = socket.socket()
print(f"[+] Connecting to {host}:{port}")
s.connect((host, port))
print("[+] Connected.")

s.send(f"{filename}{SEPARATOR}{filesize}".encode())

with open(filename, "rb") as f:
    while True:
        # read the bytes from the file
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            # file transmitting is done
            break
        # we use sendall to assure transmission in
        # busy networks
        s.sendall(bytes_read)
# close the socket
s.close()

# Send data file
filename = transfer_file

# get the file size
filesize = os.path.getsize(filename)
# create the client socket
s = socket.socket()
s.connect((host, port))

# send the filename and filesize
s.send(f"{filename}{SEPARATOR}{filesize}".encode())

with open(filename, "rb") as f:
    while True:
        # read the bytes from the file
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            # file transmitting is done
            break
        # we use sendall to assure transmission in
        # busy networks
        s.sendall(bytes_read)
# close the socket
s.close()

print("All Required files have been sent to " + host)
query_again = "mt"

while query_again != n:
    go_again = input("\nWould you like to restart?  y/n: ")

    if go_again.lower() == "y":  # Will restart the program y is entered.
        print("Please ensure the server is in a wait state..")
        subprocess.call([sys.executable, os.path.realpath(__file__)] + sys.argv[1:])
    elif go_again.lower() == "n":
        print("Thank you for playing with our programs")
        break
