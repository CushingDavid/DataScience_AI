# Import system level functionality.
import logging, os, sys, subprocess, pathlib, time, socket, pickle
import json, xmltodict, pprint, glob

#  Remove new_dictionary.txt file if it exists

from cryptography.fernet import Fernet  # Import Crytography functions
from Functions import external_functions  # Retrieve external functions.
from Functions.external_functions import Program_Info

#  info = Program_Info("the name",the version,)
data = Program_Info("CSCK541 Software in Development Group Project", "1.0", "May 2022",
                    "C.Beeby, D. Cushing, D. Lambert ",
                    "D.Lambert", "email", "Dlambert3@Liverpool.ac.uk", "Computer Science MSc")

# initialize the log settings.
logging.basicConfig(filename='Server_app.log', filemode='w', level=logging.DEBUG)  # Set logging options.

# Trash any previous file instances - for clean start
## List of files to be removed can be edited in files list

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
with open('Server_app.log', 'w') as f:
    f.write(' ')

# Enable this section to test logging is functioning
try:
    test_val1 = 1
    test_val2 = 0
    print(test_val1 / test_val2)
except Exception as e:
    logging.error("Logging confirmed as active", exc_info=True)
time.sleep(2)

# Define all internal functions to be called within the program.

# Body Part 1 - Title Screen

#  Display Title Page
external_functions.clear()  # Clear existing screen contents
external_functions.title_page(data.program_name, data.version, data.release, data.author,
                              data.contact_name, data.contact_type, data.contact_data, data.info_string)

print("\t" + "Waiting 10 seconds before continuing")
time.sleep(10)

external_functions.clear()
file_count = 0

# Body Part 2 - Configure Server to Receive two Files

# device's IP address
SERVER_HOST = "0.0.0.0"  # Allow receipt on any IP the machine has
SERVER_PORT = 81
# receive 4096 bytes each time
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

# create the server socket
# TCP socket
s = socket.socket()

# bind the socket to our local address
s.bind((SERVER_HOST, SERVER_PORT))

# enabling our server to accept connections
# 5 here is the number of unaccepted connections that
# the system will allow before refusing new connections

# Set loop start point

s.listen(5)
print("waiting for Files to be transferred, two files are expected ")
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

# accept connection if there is any
while file_count != 2:
    if file_count != 2:
        client_socket, address = s.accept()
        # if below code is executed, that means the sender is connected
        print(f"[+] {address} is connected.")

        # receive the file infos
        # receive using client socket, not server socket
        received = client_socket.recv(BUFFER_SIZE).decode()
        filename, filesize = received.split(SEPARATOR)
        # remove absolute path if there is
        filename = os.path.basename(filename)
        # convert to integer
        filesize = int(filesize)

        # start receiving the file from the socket
        # and writing to the file stream

        with open(filename, "wb") as f:
            while True:
                # read 1024 bytes from the socket (receive)
                bytes_read = client_socket.recv(BUFFER_SIZE)
                if not bytes_read:
                    # nothing is received
                    # file transmitting is done
                    break
                # write to the file the bytes we just received
                f.write(bytes_read)
        file_count += 1
        client_address = {address}
# close the client socket
client_socket.close()
# close the server socket

print(f"All files from " + str(client_address) + " have been received")

s.close()

# Determine what type of file was received
file_present = "mt"  # declare file_present variable

def filetype():
    file_dict = {pathlib.Path(r"datafile.xml"):"nx", pathlib.Path(r"datafile.bin"):"nb", pathlib.Path(r"datafile.json"): "nj", 
                    pathlib.Path(r"edatafile.xml"):"ex", pathlib.Path(r"edatafile.bin"):"eb", pathlib.Path(r"edatafile.json"):"ej" }
    for x in file_dict.keys():
        if x.exists():
            file_pres = file_dict[x]
    return file_pres

file_present = filetype()
print (file_present)

# If files type is encrypted
# Decrypt and create non-encrypted version preserving encoding
# load key for use

with open('filekey.key', 'rb') as filekey:
    key = filekey.read()

fernet = Fernet(key)

if file_present == "eb":
    fileopen = ['edatafile.bin', 'datafile.bin', 'nb']     
elif file_present == "ej":
    fileopen = ['edatafile.json', 'edatafile.json', 'nj']
elif file_present == "ex":
    fileopen = ['edatafile.xml', 'edatafile.xml', 'nx']
else:
    print('None of the expected files have been sent')

def decrypt(fileopen): 
    #  Decrypt encrypted binary file to a standard binary file
    # open the encrypted file
    with open(fileopen[0], 'rb') as enc_file:
        encrypted = enc_file.read()
    # Decrypt file
    decrypted = fernet.decrypt(encrypted)
    # Open file in write mode and
    # write decrypted data
    with open(fileopen[1], 'wb') as dec_file:
        dec_file.write(decrypted)
    return fileopen[2]

file_present = decrypt(fileopen)
Output_type = " "
print(file_present)

## Unit test for the dictionary creation
## and the file output type ... 

if file_present == "nb":
    dfile = ['datafile.bin', 'pickle.load']
elif file_present == "nj":
    dfile = ['datafile.json', 'json.load']
elif file_present == "nj":
    dfile = ['datafile.xml', 'xmltodict.parse']    

# Create dictionary fromfile
def dict_create(dfile):
    f = open(dfile[0], 'rb')
    dictionary_new = dfile[1](f)
    # close the file
    f.close()

def output_type():
    while Output_type.lower() == " ":
        Output_type = input("Do you wish to output to screen or file (S/F) : ")
        if Output_type.lower() == "s":
            for key, value in dictionary_new.items():
                print(key, ':', value)
        elif Output_type.lower() == "f":
            for key, value in dictionary_new.items():
                f = open('new_dictionary.txt', 'a+')
                file_content = f.read()
                f.write(f"{key} : {value}")
                f.close()
        else :
            print("Please enter 'S' or 'F' ")

dict_create(dfile)
output_type()

# Tidy up
# Trash any previous file instances - for clean start

df_remove()

# Ask User if they want to start over
query_again = "mt"

while query_again != "n":
    go_again = input("\nWould you like to restart?  y/n: ")

    if go_again.lower() == "y":  # Will restart the program y is entered.
        print("Please ensure the server is in a wait state..")
        subprocess.call([sys.executable, os.path.realpath(__file__)] + sys.argv[1:])

    if go_again.lower() == "n":
        print("Thank you for playing with our programs")
        break
