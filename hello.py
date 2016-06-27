import bs4, json
from urllib2 import urlopen
from time import sleep

BASE_URL = "http://www.wordplays.com/crossword-clues/"

wordlist = []
with open('sample.txt') as inputfile:
	for line in inputfile:
		wordlist.append(line.strip())

def get_clues(word):
	html = urlopen(BASE_URL + word).read()
	soup = bs4.BeautifulSoup(html, "lxml")
	clues = [a.string for a in soup.findAll("td", "clue")]
	return { word: clues}

data = [];
for singleWord in wordlist:
	wordClue = get_clues(singleWord)
	data.append(wordClue)
	sleep(1)

print(data[0])
print(data[1])

with open('result.json', 'w') as fp:
	json.dump(data, fp)