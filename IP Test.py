import os
import socket
import fcntl
import struct
import picamera
import picamera.array
import io
import time

PiName = 'RP1'
HostList = []
ip = ''


# Find local Hosts that you could potentially connect to
def FindHosts():
    x = 2
    while x <= 14:
        Response = os.system('ping -c 1 '+str(ip+str(x)))
        #print(str(Response)
        if Response == 0:
            HostList.append(ip+str(x))
        x = x+1


# Removes end characters until a '.' is found
def Trim(str):
    newstr = str
    while len(newstr)>0:
        end = newstr[-1:]
        if end == '.':
            return newstr
        newstr = newstr[:len(newstr)-1]



def GetIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(),0x8915, struct.pack('256s','wlan0'[:15]))[20:24])



def SendCapture(sock):
    camera = picamera.PiCamera()
    stream = io.BytesIO()
    time.sleep(2)
    
    camera.resolution = (640,480)
    camera.framerate = 10
    camera.capture(stream,format='jpeg',use_video_port=True)
    
    connection = sock.makefile('wb')
    try:
        time.sleep(2)
        stream.seek(0)
        connection.write(struct.pack('<L',stream.tell()))
        time.sleep(2)
        connection.flush()
        stream.seek(0)
        stream.truncate()
        time.sleep(2)
    finally:
        stream.seek(0)
        stream.truncate()
        camera.close()
    
    



#ip = socket.gethostbyname(socket.getfqdn())
ip = GetIp()
print('My IP : '+ip)
ip = Trim(ip)
print('Range : '+ip)


FindHosts()

print('')
print('==== Hosts Found ====')
for Host in HostList:
    print(Host)


print('')
print('==== Attempting Client Connect ====')
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
Connection = False
for Host in HostList:
    #sock.setdefaulttimeout(3)
    try :
        sock.connect(('192.168.0.13',9001))
        #sock.create_connection((Host,9001),timeout=3)
        Connection = True
        break
    except:
        print(Host+' : No Connection')
        sock.close()


if Connection:

    # Send Name
    sock.send(PiName)


    # Begin Polling For Commands
    Listening = True
    while Listening:
        data = sock.recv(24)
        print('Server : '+data)
        if data == '<GetVideo>':
           SendCapture(sock) 
        elif data == 'Shutting Down Host':
            sock.close()
            Listening = False
            break



