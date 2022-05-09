##### IMPORT #################################

import requests
from bs4 import BeautifulSoup, SoupStrainer
import re
from random import choice
from urllib.parse import urlparse
import openai
from dotenv import dotenv_values


##### SETUP #################################

# url_current = 'https://cernst.flounder.online'
url_current = input("Please enter start URL: ")

# jumps = 5
jumps = int(input("How many jumps? "))
print("---Jumping", jumps, "times, starting at", url_current+".")

forbidden_urls = ['google', 'facebook', 'twitter', 'linkedin', 'instagram', 'wikipedia', 'youtube', 'pinterest', 'apple']

keyword_previous = "Rainbows"
keyword_current = "Dolphins"


##### FUNCTIONS ###############################

def jumping_to(url_current):

	global page
	page = requests.get(url_current)
	print("---Jumping to", url_current+".")

def gpt3_prompt(keyword_previous, keyword_current):

	config = dotenv_values(".env")
	openai.api_key = config["API_KEY"]

	# restart_sequence = "."

	response = openai.Completion.create(
	  engine="text-davinci-002",
	  prompt="Write a short story with "+keyword_previous+" and "+keyword_current+".",
	  temperature=0.8,
	  max_tokens=500,
	  top_p=1,
	  frequency_penalty=0.8,
	  presence_penalty=1.5
	)

	print("---Prompt:")
	print("Write a short story with '"+keyword_previous+"' and '"+keyword_current+"'.")
	print("---Response:")

	for item in response.choices:
		print(item.text)

	print()

	#######################################

def get_keywords():

	soup = BeautifulSoup(page.content, 'html.parser')

	global keyword_previous
	global keyword_current

	try:
		keyword_previous = keyword_current
		keyword_current = (soup.h2.get_text())
		print("---New keyword:", keyword_current)

	except Exception as e:
		# print(e)
		print("---No keywords here")
		pass

def choose_link(url_current):

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

	if vetted_urls:
		print("---Links found:", len(vetted_urls))
		return choice(vetted_urls)

	else:
		print("---Zero links found.")
		return


##### EXECUTE #################################

for i in range(1,jumps):
	jumping_to(url_current)
	get_keywords()
	gpt3_prompt(keyword_previous, keyword_current)

	##### IF FALSE
	url_next = choose_link(url_current)
	if not url_next:
		print("---Aborting after", i, "jumps.")
		break
	else:
		url_current = url_next









