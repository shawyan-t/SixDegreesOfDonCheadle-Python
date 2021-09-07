# Webscrape / 6 Degrees


from bs4 import BeautifulSoup
import requests
import re
import sys

# ------------------------------ Return Links Here

def filter_links(href):
    # returns true for an internal-to-wiki link, false otherwise 
    if href:
        if re.compile('^/wiki/').search(href):
            if not re.compile('/\w+:').search(href):
            	if not re.compile('#').search(href):
            		return True
    return False  

# ------------------------------ Return Links Here



global r 
r = requests.get('https://en.wikipedia.org/wiki/Special:Random')


page = BeautifulSoup(r.text, 'html.parser')
pageTitle = page.find('h1', id="firstHeading").string
print("The page title is", pageTitle)

# ------------------------------------------------Find Main body here

mainBody = page.find(id="bodyContent")
mainBody.find_all('a', href=filter_links)

mainUrls = []					# Storage of all links found on first page (random)
base = "https://en.wikipedia.org"

for link in mainBody.find_all('a', href=filter_links): # Here, we acquire all valid strings on page and assign to mainUrls[]
	#print("The link is",base+link.get('href'))			
	if ((link.string) == None):
		pass
	else:
		wikiUrl = base+link.get('href')
		mainUrls.append(wikiUrl)
# ------------------------------------------------Find Main body here

# ------------------------------------------------Beginning of Search


visited = []
targetLink = base+"/wiki/Don_Cheadle"
									
#for i in mainUrls:
#	print(i)

def huntLink():	
	pageNum = 1;
	hops = 0;		
	for links in mainUrls:							# mainUrls is all urls from SEED page
		
		if(links == targetLink):
			print("\nWe got Don Cheadle on the first jump!")	# This only occurs if the seed contains the link to Don Cheadle on its page
			break

		#print("\n\nThe link being read from the mainUrls[] (SEED) list is: "+links)
													# Traverses through each link from Seed page
		#print("\n\n\nHop Page "+str(pageNum), "links ------------------------------\n\n\n")

		#visited.append(links)        

		newRequest = requests.get(links)
		newPage = BeautifulSoup(newRequest.text, 'html.parser')
		newTitle = newPage.find('h1', id="firstHeading").string
	
		
		newBody = newPage.find(id="bodyContent")
		newBody.find_all('a', href=filter_links)

		newUrls = []								# Stores all links per page we hop to

		for link in newBody.find_all('a', href=filter_links): 
			if ((link.string) == None):
				pass
			else:
				wikiUrl = base+link.get('href')
				newUrls.append(wikiUrl)				# newUrls contains all urls of the new page
		pageNum = pageNum + 1;

		found = False
		for i in newUrls:		# **
			numOf = 2
			if (i == targetLink):
				print('We got Don Cheadle in Two hops!')	# 2st Hop
				break
			if ((huntDeep(newUrls, numOf)) == True):
				print("We found Don Cheadle in Deephunt")
				found = True
				break
			else:
				numOf = numOf + 1	
		
		if found == False:		
			print("No Path to Don Cheadle was Found from random Link: "+str(r.url))


# -------------------------------------------------------------Recursive
def huntDeep(theLinks,num):
	pageNum = 1;
	hops = 0;		
	for links in theLinks:							
		if links == targetLink:
			print("\nWe got Don Cheadle")	

		#print("\n\nThe link being read from the mainUrls[] (SEED) list is: "+links)
													# Traverses through each link from Seed page
		#print("\n\n\nHop Page "+str(pageNum), "links ------------------------------\n\n\n")

	visited.append(links)        

	newRequest = requests.get(links)
	newPage = BeautifulSoup(newRequest.text, 'html.parser')
	newTitle = newPage.find('h1', id="firstHeading").string
	
		
	newBody = newPage.find(id="bodyContent")
	newBody.find_all('a', href=filter_links)

	newUrls = []								# Stores all links per page we hop to

	for link in newBody.find_all('a', href=filter_links): 
		if ((link.string) == None):
			pass
		else:
			wikiUrl = base+link.get('href')
			newUrls.append(wikiUrl)				# newUrls contains all urls of the new page

	for links in newUrls:
		if links == targetLink:
			print("We found Don Cheadle in "+num+" hops\n\n")
			return True

			pageNum = pageNum + 1;		



huntLink()