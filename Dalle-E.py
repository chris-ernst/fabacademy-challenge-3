
import requests
import base64
import json
import cv2


img_prompt = input("Please enter something: ")
print("Image generating: " + img_prompt)


ID = "https://plenty-cameras-learn-35-247-103-148.loca.lt"
url = f"{ID}//dalle"

headers = {

  # 'authority': 'three-olives-remain-104-154-191-103.loca.lt' , 
  'accept': '*/*' , 
  'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7' , 
  'bypass-tunnel-reminder': 'go' , 
}

payload = {
"text": img_prompt,
"num_images":3
}

r = requests.post(url, headers = headers, json = payload)
response = r.content.decode('utf-8')
print(type(response))
loaded_response = json.loads(response)
print(type(loaded_response))

for i, img in enumerate(loaded_response):
  print(type(img))
  with open("generated"+str(i)+".bmp", 'wb') as fh:
    fh.write(base64.decodebytes(bytes(img, 'utf-8')))

for i, img in enumerate(loaded_response):
  image = cv2.imread("generated"+str(i)+".bmp")
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  cv2.imwrite("generated_grey"+str(i)+".bmp", gray)
  




