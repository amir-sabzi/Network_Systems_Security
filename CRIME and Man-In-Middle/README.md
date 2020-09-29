## Network Security
In this directory I developed two python scripts for implentation of crime and man in middle attacks. Access to resources of the assignment is restricted due to the course policy, But I'll try to provide useful information on it.
### CRIME Attack
This attack is based on the vulnerablity of zlib algorithm that is an extended version of lempel-Ziv. In lempel-ziv algorithm, which is one of the well known methods of source coding,
if a word has been repeated many times, Instead of sending that many times, algorithm will reduce the length of message by sending the number of times that word repeated. So if there
is a way to attach a word to plaintext which was in the cipher, the length of the coded string will NOT increse. Based ON this idea I developed the code [CRIME.py](https://github.com/amir-sabzi/Network_Systems_Security/blob/master/CRIME%20and%20Diffie-Hellman/CRIME.py) 
that can find and decipher contents of a web cookie.

### Man In The Middle Attack
To perform this attack it's needed to have prior knowledge of ARP Poisoning and Diffie–Hellman key exchange. First I poisoned the ARP response to place a malicious host between two
other hosts. Then I extrected pattern of the communication of two host and forge corresponding reponse for each of them. After that, Since we can exchange our public key with two hosts
and also have our own private key, we are able to decipher symmetric key and then find flag. These steps are implmented in [Man_In_Middle.py](https://github.com/amir-sabzi/Network_Systems_Security/blob/master/CRIME%20and%20Diffie-Hellman/Man_In_Middle.py) 
