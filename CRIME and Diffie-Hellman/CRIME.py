import requests
import string
import math
import base64


def decode_chiper(response):
    if response[0] == "\"":
        response = response[1:-1]
    missing_padding = len(response) % 4
    if missing_padding:
        response += '=' * (4 - missing_padding)
    return len(base64.b64decode(response))


session = requests.Session()
flag_chars = string.ascii_letters
temp_len = math.inf
flag_temp = ['f','l','a','g',':']
for i in range(10):
    temp_len = math.inf
    print("searching for the next char of flag...")
    for char1 in flag_chars:
        request = 'https://pacific-anchorage-60533.herokuapp.com/ce442/?user=' + ''.join(flag_temp[-5:]) + char1
        response = session.get(request)
        flag_dict = session.cookies.get_dict()
        flag_cipher = flag_dict['flag']
        flag_chiper_length = decode_chiper(flag_cipher)
        #print(flag_chiper_length)
        if (flag_chiper_length < temp_len ):
            temp_len = flag_chiper_length
            temp = char1
    flag_temp.append(temp)
    print("flag until now: " + ''.join(flag_temp))
    print("------------------------------------------------")
    #print(flag_temp)

print("final flag is: " + ''.join(flag_temp))




