import urllib
import urllib2
import json

def getSearchKeywordsRecommendation(keyword):
	url = { 'OPERATION-NAME' : 'getSearchKeywordsRecommendation', 
			'SERVICE-VERSION' : '1.12.0',
			'SECURITY-APPNAME' : 'GeorgiaI-927c-4229-856a-e1ec1717d0b9',
			'RESPONSE-DATA-FORMAT' : 'JSON'}

	url['keywords'] = keyword

	payload = urllib.urlencode(url)
	dest = "http://svcs.ebay.com/services/search/FindingService/v1?" + payload
	response = urllib2.urlopen(dest)
	data = json.load(response)
	if data['getSearchKeywordsRecommendationResponse'][0]['ack'][0] == 'Success':
		return data['getSearchKeywordsRecommendationResponse'][0]['keywords'][0]
	else:
		return keyword

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
	keyword.replace (" ", "+")
	#print keyword
	#print "\n"
	recommendedKeyword = getSearchKeywordsRecommendation(keyword)
	recommendedKeyword.replace(" ","+")
	#print recommendedKeyword
	#print "\n\n"
	data, count = findItemsByKeywords(recommendedKeyword)
	user = {}
	userItem = {}
	categoryItem = {}
	starUser = {}
	for i in range(count):
		item = {}		
		item["id"] = data["findItemsByKeywordsResponse"][0]['searchResult'][0]['item'][i]["itemId"][0]
		item["title"] = data["findItemsByKeywordsResponse"][0]['searchResult'][0]['item'][i]["title"][0]

		category = {}
		category["id"] = data["findItemsByKeywordsResponse"][0]['searchResult'][0]['item'][i]["primaryCategory"][0]["categoryId"][0]
		category["name"] = data["findItemsByKeywordsResponse"][0]['searchResult'][0]['item'][i]["primaryCategory"][0]["categoryName"][0]

		username = data["findItemsByKeywordsResponse"][0]['searchResult'][0]['item'][i]['sellerInfo'][0]['sellerUserName'][0]
		location = data["findItemsByKeywordsResponse"][0]['searchResult'][0]['item'][i]['location'][0]
		topRatedSeller = data["findItemsByKeywordsResponse"][0]['searchResult'][0]['item'][i]['sellerInfo'][0]['topRatedSeller'][0]
		userdata = getUserInfo(username)		
		feedbackRatingStar = userdata["FeedbackRatingStar"]
		userdata['location'] = location
		userdata['topRatedSeller'] = topRatedSeller

		if username not in user:
			user[username] = userdata

		if username not in userItem:
			userItem[username] = [item]
		else:
			userItem[username].append(item)

		if category["name"] not in categoryItem:
			categoryItem[category["name"]] = [item]
		else:
			categoryItem[category["name"]].append(item)

		if feedbackRatingStar not in starUser:
			starUser[feedbackRatingStar] = [username]
		else:
			starUser[feedbackRatingStar].append(username)

	return user, userItem, categoryItem, starUser

'''user, userItem, categoryItem, starUser = findData("hrry putter")

print user['easygoing182']
print "\n"

print userItem['easygoing182']
print "\n"

print categoryItem['Necklaces & Pendants']
print "\n"

print starUser'''


