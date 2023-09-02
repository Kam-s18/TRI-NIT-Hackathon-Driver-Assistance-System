import http.client as httplib
import urllib
import time
from threading import Thread

key = "909C67BRJO1IGCLD"
acc_list=[0.1,0.2,0.6,0.9,-0.1,1.4509]
vel_list=[15,20,9,8,28,25]
brake_list=[0,1,0,1,1,1]
gps_lat=[63.23,63.24,63.25,63.26,63.27,63.29]
gps_long=[10.11,10.22,10.22,10.32,10.34,10.56]

def acc():
    i=0
    while i<6:
        acceleration=acc_list[i]
        
        i+=1
        params =  urllib.parse.urlencode({'field1': acceleration, 'key':key }) 
        headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = httplib.HTTPConnection("api.thingspeak.com:80")
        try:
            conn.request("POST", "/update", params, headers)
            response = conn.getresponse()
            print(acceleration)
            print(response.status, response.reason)
            print("\n")
            data = response.read()
            time.sleep(15)
            conn.close()
        except:
            print("connection failed")
            break

def acc1():
    i=0
    while i<6:
        velocity=vel_list[i]
        i+=1
        params =  urllib.parse.urlencode({'field2': velocity, 'key':key }) 
        headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = httplib.HTTPConnection("api.thingspeak.com:80")
        try:
            conn.request("POST", "/update", params, headers)
            response = conn.getresponse()
            print(velocity)
            print(response.status, response.reason)
            print("\n")
            data = response.read()
            time.sleep(15)
            conn.close()
        except:
            print("connection failed")
            break

def acc2():
    i=0
    while i<6:
        brake=brake_list[i]
        i+=1
        params =  urllib.parse.urlencode({'field3': brake, 'key':key }) 
        headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = httplib.HTTPConnection("api.thingspeak.com:80")
        try:
            conn.request("POST", "/update", params, headers)
            response = conn.getresponse()
            print(brake)
            print(response.status, response.reason)
            print("\n")
            data = response.read()
            time.sleep(15)
            conn.close()
        except:
            print("connection failed")
            break

def acc3():
    i=0
    while i<6:
        gps_la=gps_lat[i]
        i+=1
        params =  urllib.parse.urlencode({'field4': gps_la, 'key':key }) 
        headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = httplib.HTTPConnection("api.thingspeak.com:80")
        try:
            conn.request("POST", "/update", params, headers)
            response = conn.getresponse()
            print(gps_la)
            print(response.status, response.reason)
            print("\n")
            data = response.read()
            time.sleep(15)
            conn.close()
        except:
            print("connection failed")
            break

def acc4():
    i=0
    while i<6:
        gps_lo=gps_long[i]
        i+=1
        params =  urllib.parse.urlencode({'field5': gps_lo, 'key':key }) 
        headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = httplib.HTTPConnection("api.thingspeak.com:80")
        try:
            conn.request("POST", "/update", params, headers)
            response = conn.getresponse()
            print(gps_lo)
            print(response.status, response.reason)
            print("\n")
            data = response.read()
            time.sleep(15)
            conn.close()
        except:
            print("connection failed")
            break

acc()
acc1()
acc2()
acc3()
acc4()
