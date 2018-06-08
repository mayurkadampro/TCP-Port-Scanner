import socket
from datetime import datetime
import threading
from queue import Queue


# a print_lock is what is used to prevent "double" modification of shared variables.
print_lock = threading.Lock()

## Enter Host to scan
host = input("Enter a remote host to scan: ")
ip = socket.gethostbyname(host) # Translate a host name to IPv4 address format

#This is just a nice touch that prints out information on which host we are about to scan
print("-" * 80)
print("              Please wait, scanning the host --------> ", ip)
print("-" * 80)

## Check what time the scan started
t1 = datetime.now()

## Using the range function to specify ports (here it will scans all ports between 1 and 1024)
## We also put in some error handling for catching errors
def scan(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #it use for Creates a stream socket
        result = sock.connect_ex((ip, port))
        if result == 0:
            ## if a socket is listening it will print out the port number 
            print("\n Port %d Is Open!!!!!!!!!!!!!" %(port))
            sock.close()
        else:
            print("\n Port %d Is Close :( " %(port))
            
    except:
        pass

# The threader thread pulls an worker from the queue and processes it
def threader():
    while True:
        # gets an worker from the queue
        worker = q.get()

        # Run the example job with the avail worker in queue (thread)
        scan(worker)

        # completed with the job
        q.task_done()



# Create the queue and threader 
q = Queue()

# how many threads are we going to allow for
for x in range(60):
     t = threading.Thread(target=threader)

     # classifying as a daemon, so they will die when the main dies
     t.daemon = True

     # begins, must come after daemon definition
     t.start()

for worker in range(1,100):
    q.put(worker)

# wait until the thread terminates.
q.join()

## Checking the time again
t2 = datetime.now()
## Calculates the difference of time, to see how long it took to run the script
total = t2 - t1
## Printing the information to screen
print('Scanning Completed in: ', total)
