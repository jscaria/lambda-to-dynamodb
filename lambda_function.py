import urllib2
import urllib
from bs4 import BeautifulSoup
import config
import json
import logging

def get_list(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', config.USER_AGENT)
	resp = urllib2.urlopen(req)
	f = urllib.urlopen(url) 
	soup = BeautifulSoup(resp, 'html.parser')

	results = []

	table = soup.find("table", attrs={"id": config.TABLE_ID})
	rows = table.find_all('tr')

	row_number = 1
	for row in rows:
		cells = row.find_all('td')
		entry = {}

		if len(cells) == 4:
			if cells[0].string is None:
				entry[config.KEY_NAMES[0]] = row_number
				sub_tags = cells[0].find_all(config.SUB_TAG)
				if len(sub_tags) == 1:
					entry[config.KEY_NAMES[1]] = sub_tags[0][config.SUB_TAG_ATTRIBUTE]
				else:
					entry[config.KEY_NAMES[1]] = None
			else:
				entry[config.KEY_NAMES[0]] = cells[0].string
				entry[config.KEY_NAMES[1]] = None
			entry[config.KEY_NAMES[2]] = cells[1].string
			entry[config.KEY_NAMES[3]] = cells[3].string if cells[3].string is not None else None
			row_number += 1
			results.append(entry)

	return results

def lambda_handler(event, context):
	results = []
	for local_url in config.get_all_urls():
		results.append(get_list(local_url))

	# write results to dynamo-db
	return True


if __name__ == '__main__':
    lambda_handler(None, None)