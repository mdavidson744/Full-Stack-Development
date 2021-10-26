import urllib.request


def get_page_text():
	urlPrompt = input("Please enter a url to scrape: ")
	return urlPrompt
	
	

urlPrompt = get_page_text()

response = urllib.request.urlopen(urlPrompt)
html = str(response.read())

page_text, page_words = "", []

def ignoreText():
	fin = open("ignorelist.txt", "r")

	word = ""

	for line in fin:
		word = line.strip()


	html = html[html.find("<body") + 5:html.find("</body>")]
	html.split()

	html.replace(word, "")

	return html

	# html = html[html.find("<body") + 5:html.find("</body>")]


html = ignoreText()



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


print(page_words)
print("{} unique words found".format(len(page_words)))