# import socket programming library 
import socket 

# import thread module 
from _thread import *
from threading import *
import threading 
import sys
import time
import json
import requests
import csv
import socket
from signal import signal, SIGINT
from sys import exit

sem=Semaphore(4)
ip=requests.get('https://api.ipify.org').text #public ip
iptable=[]
ips=['13.72.82.119','52.186.143.155','13.68.207.73','40.88.6.7']
avail=[1,1,1,1]

print_lock = threading.Lock() 

def handler(signal_received,frame):
    data = {}
    f = open('sample.json',)
    d = json.load(f)
    f.close()
    d['count']=d['count']+1
    # temp = "IP-Login-"+str(d['count'])
    num = d['count']
    temp = 'IP-Login-' + str(num)
    d[temp]=[]
    print("\nCurent IPTABLE before Terminating the Program:")
    ind=1
    print("Index\t\t\t","IPs")
    print("----------------------------------------------------------------------------")
    if not iptable:
        print("IPTABLE IS EMPTY!!!")
    else:
        for x in iptable:
            d[temp].append({
                'Index':ind,
                'IP No.':x
                })
            print(str(ind),"\t\t\t",x)
            ind+=1
    with open('sample.json', 'w') as outfile:
        json.dump(d, outfile)
    sys.exit()




def check():
    index=-1
    global avail
    for i in range(len(avail)):
        if (avail[i] == 1):
            avail[i]=0
            return i
    return index

def serverconnect(ipt):
    s = socket.socket()
    port=12347
    s.connect((ipt, port))
    ip=requests.get('https://api.ipify.org').text #public ip
    s.send(str(ip).encode())
    api_response=s.recv(1024).decode()
    s.close()
    return api_response

# thread function 
def threaded(c,addr):

    global iptable,ips

    sem.acquire()
    index=check()
    iptable.append([addr,ips[index]])
    info=serverconnect(ips[index])
    c.send(str(info).encode())
    time.sleep(5)
    avail[index]=1
    sem.release()
    c.close()


def Main(): 
	host = "" 

	# reverse a port on your computer 
	# in our case it is 12345 but it 
	# can be anything 
	port = 9020
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	s.bind((host, port)) 
	print("socket binded to port", port) 

	# put the socket into listening mode 
	s.listen(5) 
	print("socket is listening") 

	# a forever loop until client wants to exit 
	while True: 

		# establish connection with client 
		c, addr = s.accept() 

		# lock acquired by client 

		print('Connected to :', addr[0], ':', addr[1]) 

		# Start a new thread and return its identifier 
		start_new_thread(threaded, (c,addr)) 
	s.close() 


if __name__ == '__main__':
    signal(SIGINT,handler)
    Main()
