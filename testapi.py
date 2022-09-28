import pandas as pd
import requests
from requests.exceptions import HTTPError
from requests.auth import HTTPBasicAuth
import json

#Signin
data = {
"CommandType":"SignIn", 
"CSIOnetID":"csioxml14@broker.edi.csio.com",
"CSIOnetPassword":"abcd1234"
}

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

try:
    #response = requests.post('https://staging.csionet.com/signin', verify = False, auth = HTTPBasicAuth(('csioxml14@broker.edi.csio.com'), getpass()))
    response = requests.post('https://staging.csionet.com/v1/MessageServices.aspx', json = data, headers = headers)
    response.raise_for_status 
except HTTPError as http_err:
    print(f'HTTP error ocurred: {http_err}')

except Exception as err:
    print(f'Other error occurred: {err}')

else:
    print('Success!')


print("SiginIn:", response.json())


j = response.text

with open("signin.json", "w") as outfile:
    outfile.write(j)


f = open('signin.json')

# returns JSON object as
# a dictionary
data = json.load(f)

print("Dictionaty ", data)

# Iterating through the json
# list
for key, value in data.items():
    print(key, '->', value)

s = data['Response']['SessionGUID']
u = data['Response']['UserGUID']

f.close()

print("Extracted SessionGUID",s)

#build the XML request body 
import xml.etree.ElementTree as et

request = et.Element("Request")

commandtype = et.SubElement(request, "CommandType")
commandtype.text = "Send"


sessionguid = et.SubElement(request, "SessionGUID")
sessionguid.text = s


userguid = et.SubElement(request, "UserGUID")
userguid.text = u

toemailaddress = et.SubElement(request, "ToEmailAddress")
toemailaddress.text = "csioxml14@broker.edi.csio.com"


fromemailaddress =  et.SubElement(request, "FromEmailAddress")
fromemailaddress.text = "csioxml14@broker.edi.csio.com"


messagetype =  et.SubElement(request, "MessageType")
messagetype.text = "ACK"


messagesubject =  et.SubElement(request, "MessageSubject")
messagesubject.text = "ACKTestMessage"


attribs = {"count":"2"}


data = et.tostring(request)

print("Request body " data)

#use the XML as a request body 


headers = {'Content-type': 'application/xml', 'Accept': 'text/plain'}

try:
    #response = requests.post('https://staging.csionet.com/signin', verify = False, auth = HTTPBasicAuth(('csioxml14@broker.edi.csio.com'), getpass()))
    response = requests.post('https://staging.csionet.com/v1/MessageServices.aspx', data = data, headers = headers)
    response.raise_for_status 
except HTTPError as http_err:
    print(f'HTTP error ocurred: {http_err}')

except Exception as err:
    print(f'Other error occurred: {err}')

else:
    print('Success!')











