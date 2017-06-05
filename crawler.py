import sys
import json
import signal
import urllib.request
import time
import lxml.html as html

FLAG = True
HOSTNAME = "http://archiveofourown.org"
GENERIC_QUERY = "http://archiveofourown.org/works/search?utf8=%E2%9C%93&work_search%5Bquery%5D=&work_search%5Btitle%5D=&work_search%5Bcreator%5D=&work_search%5Brevised_at%5D=&work_search%5Bcomplete%5D=0&work_search%5Bsingle_chapter%5D=0&work_search%5Bword_count%5D=&work_search%5Blanguage_id%5D=&work_search%5Bfandom_names%5D=&work_search%5Brating_ids%5D=&work_search%5Bcharacter_names%5D=&work_search%5Brelationship_names%5D=&work_search%5Bfreeform_names%5D=&work_search%5Bhits%5D=&work_search%5Bkudos_count%5D=&work_search%5Bcomments_count%5D=&work_search%5Bbookmarks_count%5D=&work_search%5Bsort_column%5D=created_at&work_search%5Bsort_direction%5D=asc&commit=Search"

def get(url):
	time.sleep(1)
	print(time.ctime(), url, file=sys.stderr)
	return urllib.request.urlopen(url).read()

def parse(string):
	return html.fromstring(string)

def last_page(tree):
	return tree.find(".//ol[@title='pagination']/li[last()-1]/a").attrib["href"]

def previous_page(tree):
	return tree.find(".//li[@title='previous']/a").attrib["href"]

def get_works(tree):
	return tree.findall(".//ol[@class='work index group']/li")

def get_fandoms(tree):
	return [i.text.strip() for i in tree.findall(".//h5[@class='fandoms heading']/a")]

def get_date(tree):
	return tree.find(".//p[@class='datetime']").text.strip()

def get_id(tree):
	return tree.find(".//h4[@class='heading']/a[1]").attrib["href"].split("/")[-1]

def mine(tree):
	for work in get_works(tree):
		yield {
			"id": get_id(work),
			"date": get_date(work),
			"fandoms": get_fandoms(work)}

def exit_gracefully(*args):
	global FLAG
	FLAG = False

def main():
	url = sys.argv[1] if len(sys.argv) > 1 else HOSTNAME + last_page(parse(get(GENERIC_QUERY)))
	amount = sys.argv[2] if len(sys.argv) > 2 else 10000
	i = 0
	while i < amount and FLAG:
		tree = parse(get(url))
		for thing in mine(tree):
			print(json.dumps(thing))
		url = HOSTNAME + previous_page(tree)
		i += 1
	with open("/var/tmp/lastpage", "a") as fil:
		fil.write(url + "\n")
	print("Done", file=sys.stderr)

if __name__ == "__main__":
	signal.signal(signal.SIGINT, exit_gracefully)
	signal.signal(signal.SIGTERM, exit_gracefully)
	main()
