import requests, json 
import base64
from imgurpython import ImgurClient
import config 
import os 

#uploads the img to imgur and returns the link
def get_link(image): 
    url = "https://api.imgur.com/3/image" #the link that it posts the img to 

    #reads the image and encodes it in b64 
    f = open(image, "rb")
    image_data = f.read()              
    b64_image = base64.standard_b64encode(image_data)

    payload={'image': image_data}
    files=[]
    headers = {
    'Authorization': config.imgurID() 
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    # print(response.text)
    link = response.text[437:471]
    return link

print (get_link('figure.png'))

# os.remove('figure.png')