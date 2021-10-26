import urllib.request

def get_all_new_links_on_page(page, prev_links):

	response = urllib.request.urlopen(page)
	html = str(response.read())

	links, pos, all_found = [], 0, False
	while not all_found:
		tag_start = html.find("<a href=", pos)
		if tag_start > -1:
			href = html.find('"', tag_start + 1)
			end_href = html.find('"', href + 1)
			url = html[href + 1:end_href]
			if url[:7] == "http://":
				if url[-1] == "/":
					url = url[:-1]
				if url not in links and url not in prev_links:
					links.append(url)     
					print(url)
			close_tag = html.find("</a>", tag_start)
			pos = close_tag + 1
		else:
			all_found = True   
	return links

to_crawl = ["http://adrianmoore.net/com661/test_index.html"]
crawled = []
while to_crawl:
	url = to_crawl.pop()
	crawled.append(url)
	new_links = get_all_new_links_on_page(url, crawled)
	to_crawl = list( set(to_crawl) | set(new_links) )
	
print(crawled)	