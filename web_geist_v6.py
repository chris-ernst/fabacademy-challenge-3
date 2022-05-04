import requests
from bs4 import BeautifulSoup, SoupStrainer
import re
import random
import time
from urllib.parse import urlparse

# start = 'wikipedia.org'
# start = 'cernst.flounder.online'
start = 'iaac.net'
# start = 'uroulette.com/visit/ospqt'

url = f'https://{start}/'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

jumps = 5

##### REDIRECTS

print('–––––––––––––––––––––––––––––––––––')

print('checking for redirects')
# import time
# time.sleep(5) 

### get the url after redirect
redirects = page.history
if not redirects:
	print('   no redirects happened')
else:
	print('redirected to:')
	last_redirect = redirects.pop()
	print('',last_redirect.url)


###### UPDATE LINKS ARRAY

for i in range(1,jumps):

	forbidden = []

	forbidden.append('google')
	forbidden.append('facebook')
	forbidden.append('youtube')
	forbidden.append('twitter')
	forbidden.append('pinterest')
	forbidden.append('wikipedia')
	forbidden.append('instagram')
	forbidden.append('linkedin')

	forbidden.append('flounder')
	forbidden.append('iaac')
	
	print(forbidden)


###### FINE-TUNING LINKS ARRAY

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

##### JUMPING

	# choose a random link
	from random import choice

	links_count = len(all_links)

	print('   links found:',len(all_links))
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
		### navigate to new URL
		page = requests.get(url_new)
		soup = BeautifulSoup(page.content, "html.parser")

		all_links.clear()
		allowed_links.clear()
		forbidden.clear()

		### add url_new here 
		current_forbidden = urlparse(url_new).netloc
		# print('  current_forbidden1:' + current_forbidden)

		if len(current_forbidden.split('.')) <= 3:
			current_forbidden = current_forbidden.split('.')[-2]
			# print('  current_forbidden2:' + current_forbidden)
			forbidden.append(current_forbidden)
		else:
			current_forbidden = current_forbidden.split('.')[-3]
			# print('  current_forbidden2:' + current_forbidden)
			forbidden.append(current_forbidden)

		print(forbidden)
		print('   loop complete after', jumps, 'jumps')


