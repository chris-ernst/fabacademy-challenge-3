import requests
from bs4 import BeautifulSoup, SoupStrainer
import re
from random import choice
from urllib.parse import urlparse

###

import openai
import json
from dotenv import dotenv_values


##### DEFINE START URL & JUMPS

# url_current = 'https://www.wikipedia.org'
# url_current = 'https://uroulette.com/visit/owtqw'

# url_current = 'https://cernst.flounder.online'
jumps = 5

url_current = input("Please enter start URL (starting with 'https://'): ")
# jumps = (input("How many jumps?")
# jumps = int(jumps)
# print(jumps)

print("jumping to: "+url_current)

###### FORBIDDEN

forbidden_urls = ['google', 'facebook', 'twitter', 'linkedin', 'instagram', 'wikipedia', 'youtube', 'pinterest', 'apple']

### Placeholder Headlines
headline_previous = "Rainbows"
headline_current = "Doplhins"


###### FINE-TUNING LINKS ARRAY

for i in range(1,jumps):

	page = requests.get(url_current)



	###### Extract headline_current

	soup = BeautifulSoup(page.content, 'html.parser')

	try:

		### rotate out headlines, parse H2
		headline_previous = headline_current
		headline_current = (soup.h2.get_text())


		###### GPT3 #################################

		### AUTH
		config = dotenv_values(".env")
		API_KEY = config["API_KEY"]
		openai.api_key = API_KEY


		### GPT-3 Request
		# restart_sequence = "."

		response = openai.Completion.create(
		  engine="text-davinci-002",
		  prompt="Write a short story with "+headline_previous+" and "+headline_current+".",
		  temperature=0.8,
		  max_tokens=500,
		  top_p=1,
		  frequency_penalty=0.8,
		  presence_penalty=1.5
		)

		print("---Prompt:")
		print("Write a short story with '"+headline_previous+"' and '"+headline_current+"'.")
		print("---Response:")

		for item in response.choices:
			print(item.text)

		print()

		#######################################

	except Exception as e:
		print(e)
		
	######






	all_urls = []
	vetted_urls = []

	###### Extract Domain

	current_forbidden = urlparse(url_current).netloc

	if len(current_forbidden.split('.')) <= 3:
		current_forbidden = current_forbidden.split('.')[-2]
		forbidden_urls.append(current_forbidden)
		# print('current_forbidden:', current_forbidden)

	else:
		current_forbidden = current_forbidden.split('.')[-3]
		forbidden_urls.append(current_forbidden)
		# print('current_forbidden:', current_forbidden)

	###### Parse all URLs

	for url in BeautifulSoup(page.content, parse_only=SoupStrainer('a'), features="html.parser"):
		if url.has_attr('href'):
			all_urls.append(url['href'])

	###### Check URLs against 'forbidden' URLs

	for url in all_urls: 
		contains_forbidden = any(forbidden_url in url for forbidden_url in forbidden_urls)
		if not contains_forbidden:
			if url.startswith("https"):
				vetted_urls.append(url)

	###### Choose URL
	if not vetted_urls:
		print("---zero links")
		print("---aborting after", i, "jumps")
		break
	else:
		url_current = choice(vetted_urls)
		print('---url_current:', url_current)


print('---loop complete')












