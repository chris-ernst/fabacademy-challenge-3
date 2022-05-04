import requests
from bs4 import BeautifulSoup, SoupStrainer
import re
from random import choice
from urllib.parse import urlparse


##### DEFINE START URL & JUMPS

# start = 'wikipedia.org'
start = 'cernst.flounder.online'
# start = 'iaac.net'
# start = 'uroulette.com/visit/ospqt'

url = f'https://{start}/'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

jumps = 3


###### FORBIDDEN

forbidden = ['google', 'facebook', 'twitter', 'linkedin', 'instagram', 'wikipedia', 'youtube', 'pinterest']

### Debug Forbidden
forbidden.append('flounder')
forbidden.append('iaac')


###### FINE-TUNING LINKS ARRAY

for i in range(1,jumps):

	all_links = []

	for link in BeautifulSoup(page.content, parse_only=SoupStrainer('a'), features="html.parser"):
		if link.has_attr('href'):
			all_links.append(link['href'])

	def validate_url(url):
		global forbidden
		parsed_uri = urlparse(url).netloc
		sub_urls = url.split(".")
		for u in sub_urls:
			if u in forbidden:
				return False
		return True

	allowed_links = list(filter(validate_url, all_links))

	print(allowed_links)


##### JUMPING

	# choose a random link

	links_count = len(all_links)

	print('   links found:',links_count)
	print('   vetted links:',len(allowed_links))

	# print(list(set(allowed_links)))

	if links_count == 0:
		print('   aborting')
		break
	else:
		url_new = choice(allowed_links)

		### print it
		print('jump:',i)
		print(' url:',url_new)


##### navigate to new URL
		page = requests.get(url_new)
		soup = BeautifulSoup(page.content, "html.parser")

		all_links.clear()
		allowed_links.clear()
		# forbidden.clear()

		### add url_new here 
		current_forbidden = urlparse(url_new).netloc
		print('   current_forbidden1:' + current_forbidden)
		forbidden.append(current_forbidden)

		print(forbidden)
		print('   loop complete after', jumps, 'jumps')


