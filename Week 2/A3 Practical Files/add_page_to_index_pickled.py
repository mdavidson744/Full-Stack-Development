import urllib.request
import pickle
 
def get_page_text(url):

	response = urllib.request.urlopen(url)
	html = str(response.read())

	page_text, page_words = "", []
	html = html[html.find("<body") + 5:html.find("</body>")]

	finished = False
	while not finished:
		next_close_tag = html.find(">")
		next_open_tag = html.find("<", next_close_tag + 1)
		if next_open_tag > -1:
			content = " ".join(html[next_close_tag + 1:next_open_tag].strip().split())
			page_text = page_text + " " + content
			html = html[next_open_tag + 1:]
		else:
			finished = True
			
	for word in page_text.split():
		if word.isalnum() and word not in page_words:
			page_words.append(word)
				
	return page_words


def add_word_to_index(index, keyword, url):
	for entry in index:
		if entry[0] == keyword:
			entry[1].append(url)
			return
	index.append([keyword, [url]])


def add_page_to_index(index, url):
	page_words = get_page_text(url)
	for word in page_words:
		add_word_to_index(index, word, url)	


index = []
url = "http://www.ulster.ac.uk/campuses/belfast"
add_page_to_index(index, url)		
print(index)

fout = open("index.txt", "wb")
pickle.dump(index, fout)
fout.close()

print("------------")

fin = open("index.txt", "rb")
new_index = pickle.load(fin)
fin.close()
print(new_index)		