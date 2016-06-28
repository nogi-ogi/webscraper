import bs4, json
import urllib2
from time import sleep

BASE_URL = "http://www.wordplays.com/crossword-clues/"

wordlist = []
print('loading words')
with open('words.txt') as inputfile:
	for line in inputfile:
		wordlist.append(line.strip())

delay = 1 # seconds
min_delay = 1 # second
max_delay = 600 # 10 min

def try_url(url):
	global delay
	if (delay > max_delay):
	delay = max_delay

sleep(delay)
result = ""

try:
	html = urllib2.urlopen(url).read()
	delay = min_delay
	return html
except urllib2.HTTPError, err:
	print(err.code)
	delay = delay * 2
except urllib2.URLError, err:
	print(err.args)
	delay = delay * 2
	return None

def get_clues(word):
	html = try_url(BASE_URL + word)
	if (html is not None):
		soup = bs4.BeautifulSoup(html, "lxml")
		clues = [a.string for a in soup.findAll("td", "clue")]
		return clues
	else:
		return get_clues(word) # try again

fileCount = 0
def save(data):
	global fileCount
	fileCount += 1
	print('saving batch ' + str(fileCount))
	with open('results/result' + str(fileCount) + '.json', 'w') as fp:
	json.dump(data, fp)

batchSize = 25
batchCount = 0
data = {}
print("starting")
for singleWord in wordlist:
	batchCount += 1
	print('looking up: ' + singleWord)
	wordClues = get_clues(singleWord)
	data[singleWord] = wordClues
	if (batchCount % batchSize == 0):
		save(data)
		data = []
		batchCount = 0

if (batchCount > 0):
save(data) 