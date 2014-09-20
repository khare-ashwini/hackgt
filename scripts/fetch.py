import urllib
import urllib2
import json

def findItemsByKeywords(keyword):

	url = { 'OPERATION-NAME' : 'findItemsByKeywords', 
			'SERVICE-VERSION' : '1.12.0',
			'SECURITY-APPNAME' : 'GeorgiaI-927c-4229-856a-e1ec1717d0b9',
			'RESPONSE-DATA-FORMAT' : 'JSON', 
			'outputSelector' : 'SellerInfo'}

	url['keywords'] = keyword

	payload = urllib.urlencode(url)
	dest = "http://svcs.ebay.com/services/search/FindingService/v1?" + payload
	response = urllib2.urlopen(dest)
	data = json.load(response)
	count = int(data["findItemsByKeywordsResponse"][0]['searchResult'][0]['@count'])
	return data, count

def getUserInfo(username):
	url = {'callname' : 'GetUserProfile',
			'responseencoding' : 'JSON',
			'appid' : 'GeorgiaI-927c-4229-856a-e1ec1717d0b9', 
			'siteid' : '0',
			'version' : '525'}

	url['UserID'] = username
	payload = urllib.urlencode(url)
	dest = "http://open.api.ebay.com/shopping?" + payload
	response = urllib2.urlopen(dest)
	data = json.load(response)
	userdata = data["User"]
	return userdata

def findData(keyword):
	data, count = findItemsByKeywords(keyword)
	user = {}
	userItem = {}
	categoryItem = {}
	for i in range(count):
		item = {}		
		item["id"] = data["findItemsByKeywordsResponse"][0]['searchResult'][0]['item'][i]["itemId"][0]
		item["title"] = data["findItemsByKeywordsResponse"][0]['searchResult'][0]['item'][i]["title"][0]

		category = {}
		category["id"] = data["findItemsByKeywordsResponse"][0]['searchResult'][0]['item'][i]["primaryCategory"][0]["categoryId"][0]
		category["name"] = data["findItemsByKeywordsResponse"][0]['searchResult'][0]['item'][i]["primaryCategory"][0]["categoryName"][0]

		username = data["findItemsByKeywordsResponse"][0]['searchResult'][0]['item'][i]['sellerInfo'][0]['sellerUserName'][0]
		userdata = getUserInfo(username)
		location = data["findItemsByKeywordsResponse"][0]['searchResult'][0]['item'][i]['location'][0]
		userdata['location'] = location

		if username not in user:
			user[username] = userdata

		if username not in userItem:
			userItem[username] = [item]
		else:
			userItem[username].append(item)

		if category["name"] not in categoryItem:
			categoryItem["name"] = [item]
		else:
			categoryItem["name"].append(item)

	return user, userItem, categoryItem

user, userItem, categoryItem = findData("Harry")


