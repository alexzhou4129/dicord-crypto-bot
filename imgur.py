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
    'Authorization': os.getenv("imgurID")
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    
    #the link returned has back slashes for some reason, which discord doesn't like, this loop filters it out
    unformattedLink = response.text[437:471] 
    formattedLink = ""
    for i in range (len(unformattedLink)):
        if (unformattedLink[i] != '\\'):
            formattedLink+=unformattedLink[i]

    return formattedLink



print (get_link('figure.png'))

# os.remove('figure.png')