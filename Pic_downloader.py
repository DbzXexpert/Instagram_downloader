import requests,re,json,os,sys
from bs4 import BeautifulSoup as sp
import urllib.request as ur


username = input("Enter the instagram username :   ")          # Targeted Instagram User
website_url = "https://www.instagram.com/"
source = requests.get(website_url+username+"?__a=1").text         # Http request

try :
	js= json.loads(source)       #Parse the JSON response
except Exception :
	print("This account does not exist")
	sys.exit(0)

Query_ID = '' # provide sessionID (Browser developer tools)
idd = ""
end_cursor = ""
pics = []
is_private =  js['graphql']['user']['is_private']    #Private user
nodes = js['graphql']['user']['edge_owner_to_timeline_media']['edges']
i = 1
for node in nodes:
	if not node['node']['is_video']:
		pics.append(node['node']['shortcode'])
	if i == 1:
		idd = node['node']['owner']['id']
		i=2


has_next_page = js['graphql']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
if has_next_page :
	end_cursor = js['graphql']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor'] 


while has_next_page :
	 
	link = "https://www.instagram.com/graphql/query/?query_hash="+Query_ID+"&variables={\"id\":\""+idd+"\",\"first\":50,\"after\":\""+end_cursor+"\"}"
	source = requests.get(link).text
	js= json.loads(source)
	nodes = js['data']['user']['edge_owner_to_timeline_media']['edges']
	for node in nodes:
		if not node['node']['is_video']:
			pics.append(node['node']['shortcode'])
	has_next_page = js['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
	if has_next_page :
		end_cursor = js['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor'] 
if is_private:
	print("this account is private")
else:
	print(len(pics),"Picture retrived wait a few minutes while downloading it !!")

	try:
		os.mkdir(username)
	except Exception:
		pass

	os.chdir(username)

i = 1
for pic in pics:
	soup = sp(requests.get(website_url+'p/' + pic).text,features="lxml")

	for item  in soup.find_all('meta'):
		if item.get('content') and re.match(r'^https://instagram.*\.jpg.*',item.get('content')):
			ur.urlretrieve(item.get('content'),str(i)+'.jpg')
	i+=1














