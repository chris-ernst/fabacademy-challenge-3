import requests
from bs4 import BeautifulSoup, SoupStrainer
import re
from random import choice
from urllib.parse import urlparse


##### DEFINE START URL & JUMPS

# start_url = 'https://www.wikipedia.org'
# start_url = 'https://uroulette.com/visit/owtqw'

start_url = 'https://cernst.flounder.online'
print(start_url)



page = requests.get(start_url)
soup = BeautifulSoup(page.content, 'html.parser')

jumps = 3


###### FORBIDDEN

forbidden_urls = ['google', 'facebook', 'twitter', 'linkedin', 'instagram', 'wikipedia', 'youtube', 'pinterest']

### Debug Forbidden
forbidden_urls.append('flounder')
forbidden_urls.append('iaac')

###### FINE-TUNING LINKS ARRAY

for i in range(1,jumps):



	

	all_urls = []
	vetted_urls = []

	###### Parse all URLs

	for url in BeautifulSoup(page.content, parse_only=SoupStrainer('a'), features="html.parser"):
		if url.has_attr('href'):
			all_urls.append(url['href'])

	###### Check URLs against 'forbidden' URLs

	for url in all_urls: 
		contains_forbidden = any(forbidden_url in url for forbidden_url in forbidden_urls)
		# print(contains_forbidden, url)
		if not contains_forbidden:
			vetted_urls.append(url)

	###### Choose URL

	url_new = []
	url_new = choice(vetted_urls)
	print('url_new:', url_new)

	###### Extract Domain

	current_forbidden = urlparse(url_new).netloc

	if len(current_forbidden.split('.')) <= 3:
		current_forbidden = current_forbidden.split('.')[-2]
		forbidden_urls.append(current_forbidden)
		print('current_forbidden:', current_forbidden)

	else:
		current_forbidden = current_forbidden.split('.')[-3]
		forbidden_urls.append(current_forbidden)
		print('current_forbidden:', current_forbidden)


print('forbidden_urls ', forbidden_urls)
print('loop complete')

## For Tomorrow: Set URL navigation in the beginning of the loop to initate organically with start_url











