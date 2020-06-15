import socket
import sys
import threading
import json
import time

#client - two threads - listen and send to all clients
HOST = '10.130.7.146'
PORT = 8083

threads = []
pos = []
num = 0
numofclients = 2
lastmessage = ''
snakedictionary = []

def thread(ip, port, cl, clientno):
    global threads
    global pos 
    global num
    global lastmessage
    global snakedictionary
    global numofclients
    active = True
    #print('client: ', clientno)
    #for x in threads:
    #    print(x)

    cl.sendall(str(clientno).encode('ascii')) #sending client number

    while (len(threads) < numofclients): #waiting for two players to join
        continue

    snake = json.loads(cl.recv(1024)) #recieiving self ki body
    item = {"id": clientno, "body": snake}
    print(item)
    print('Appending to ', snakedictionary)
    snakedictionary.append(item)

    while(len(snakedictionary) < numofclients): #waiting till both snakes have sent initial positions
        time.sleep(0.2)
        continue

    #sending initial positions to the respective clients
    print('Sending ', snakedictionary, ' to all clients')
    cl.sendall((json.dumps(snakedictionary)).encode('ascii'))
    print('Sent')

    while active:
        try: 
            d = json.loads(cl.recv(1024).decode('ascii')) #client dictionary 
            lastmessage = d

            print('Recieved: ', d)
            ID = d['id']
            key = d['move']

            if key == 0:
                print('Connection lost')
                for i in threads:
                    iid = i["clientno"]
                    if int(iid) == int(ID):
                        threads.remove(i)

            if key == 5:
                print('Connection lost')
                for x in threads:
                    xid = x["clientno"]
                    if int(xid) == int(ID): 
                        threads.remove(x)
            
                d2 = json.loads(cl.recv(1024).decode('ascii')) #client dictionary 
                lastmessage = d2
                print('Recieved: ', d2)
                secID = d2['id']
                seckey = d2['move']

                for x in threads:
                    xid = x["clientno"]
                    if int(xid) == int(secID): 
                        threads.remove(x)

                for i in threads:
                    print('Sending: ', d2)
                    icl = i["client"]
                    icl.sendall(json.dumps(d2).encode('ascii'))


            for i in threads:
                print('Sending: ', d)
                icl = i["client"]
                icl.sendall(json.dumps(d).encode('ascii'))

            if key == 0 or key == 5:
                break

        except Exception as e: 
            break

    print(lastmessage)

    """if cl in threads: #removing that client
        threads.remove(cl)"""

    snakedictionary = []
    print('Connection closed')
    cl.close()

    for i in threads:
        print(i)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        s.bind((HOST, PORT))
    except:
        print('Bind failed. Error: ' + str(sys.exc_info()))
        sys.exit()

    s.listen(2)
    print("The server is ready to recieve")

    while True:
        try:
            c,info = s.accept()
            ip, port = str(info[0]), str(info[1])
            print('Connected with ' + ip + ': ' + port)  
            num = len(threads)

            try:    
                item = {"clientno": num, "client": c}
                threads.append(item)    
                t = threading.Thread(target = thread, args = (ip, port, c, num))
                print('The thread has started')
                t.start()
            except:
                print('Thread did not start')
                traceback.print_exc()
        except:
            print("Server shut down")
            sys.exit()

    s.close()

if __name__ == "__main__":
    main()