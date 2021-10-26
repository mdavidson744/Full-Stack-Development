import urllib.request
url = str(input("URL > "))
response = urllib.request.urlopen(url)
html = str(response.read())

links, pos = [], 0
all_found, links_found = False, 0
while not all_found:
	tag_start = html.find("<a href=", pos)
	if tag_start > -1:
		href = html.find('"', tag_start + 1)
		end_href = html.find('"', href + 1)
		url = html[href + 1:end_href]
		if url[:7] == "http://" or url[:8] == 'https://':
			if url[-1] == "/":
				url = url[:-1]
			links.append(url)     
			print(url)
			links_found = links_found + 1
		closeTag = html.find("</a>", tag_start)
		pos = closeTag + 1
	else:
		all_found = True   
print("{} hyperlinks found".format(links_found))
print(links)


 