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

def findItemsByKeywords(keyword, count):

	url = { 'OPERATION-NAME' : 'findItemsByKeywords', 
			'SERVICE-VERSION' : '1.12.0',
			'SECURITY-APPNAME' : 'GeorgiaI-927c-4229-856a-e1ec1717d0b9',
			'RESPONSE-DATA-FORMAT' : 'JSON', 
			'outputSelector' : 'SellerInfo',
			'paginationInput.entriesPerPage' : count}
			#'paginationInput.pageNumber' : '100'}

	url['keywords'] = keyword

	payload = urllib.urlencode(url)
	dest = "http://svcs.ebay.com/services/search/FindingService/v1?" + payload
	response = urllib2.urlopen(dest)
	data = json.load(response)
	count = int(data["findItemsByKeywordsResponse"][0]['searchResult'][0]['@count'])
	return data, count

#Get Item Info

def getItemInfo(itemID):
	try:
		url = {'callname' : 'GetSingleItem',
			'responseencoding' : 'JSON',
			'appid' : 'GeorgiaI-927c-4229-856a-e1ec1717d0b9', 
			'siteid' : '0',
			'version' : '525',
			'ItemID' : itemID,
			'IncludeSelector' : 'Description,ItemSpecifics'}

		payload = urllib.urlencode(url)
		dest = "http://open.api.ebay.com/shopping?" + payload
		response = urllib2.urlopen(dest)
		itemData = json.load(response)
		return itemData
	except:
		return None

# Returns basic info for username

def getUserInfo(username):
	url = {'callname' : 'GetUserProfile',
			'responseencoding' : 'JSON',
			'appid' : 'GeorgiaI-927c-4229-856a-e1ec1717d0b9', 
			'siteid' : '0',
			'version' : '525',
			'IncludeSelector' : 'Details,FeedbackDetails'}

	url['UserID'] = username
	payload = urllib.urlencode(url)
	dest = "http://open.api.ebay.com/shopping?" + payload
	response = urllib2.urlopen(dest)
	data = json.load(response)
	userdata = data["User"]
	feedbackDetails = data["FeedbackDetails"]

	listImageURL = []

	for entry in feedbackDetails:
		itemData = getItemInfo(entry["ItemID"])
		#print itemData
		if itemData['Ack'] != 'Failure':
			if 'PictureURL' in itemData['Item']:
				listImageURL.append(itemData['Item']['PictureURL'][0])		

	return userdata, feedbackDetails, listImageURL


# Items to be displayed in Search Result
# param {keyword}

def searchData(keyword, count):
	data, count = findItemsByKeywords(keyword, count)
	itemList = []

	for i in range(count):
		itemDict = data["findItemsByKeywordsResponse"][0]['searchResult'][0]['item'][i]

		item = {}		
		item["id"] = itemDict["itemId"][0]
		item["title"] = itemDict["title"][0]
		item["categoryName"] = itemDict["primaryCategory"][0]["categoryName"][0]
		item["galleryURL"] = itemDict["galleryURL"][0]
		item["viewItemURL"] = itemDict["viewItemURL"][0]
		item["sellingState"] = itemDict["sellingStatus"][0]["sellingState"][0]
		item["currentPrice"] = itemDict["sellingStatus"][0]["currentPrice"][0]["__value__"]
		item["location"] = itemDict["location"][0]
		item["user"] = itemDict['sellerInfo'][0]

		if item not in itemList:
			itemList.append(item)

	return itemList

def findData(keyword, count):
	#print "Search for " + keyword
	#keyword.replace (" ", "+")
	#recommendedKeyword = getSearchKeywordsRecommendation(keyword)
	#recommendedKeyword.replace(" ","+")
	#data, count = findItemsByKeywords(recommendedKeyword)

	data, count = findItemsByKeywords(keyword, count)
	user = {}
	categoryItem = {}
	starUser = {}
	itemList = {}
	for i in range(count):

		itemDict = data["findItemsByKeywordsResponse"][0]['searchResult'][0]['item'][i]

		item = {}		
		item["id"] = itemDict["itemId"][0]
		item["title"] = itemDict["title"][0]
		item["categoryName"] = itemDict["primaryCategory"][0]["categoryName"][0]
		item["galleryURL"] = itemDict["galleryURL"][0]
		item["viewItemURL"] = itemDict["viewItemURL"][0]

		if "postalCode" in itemDict:
			item["postalCode"] = itemDict["postalCode"][0]

		item["sellingState"] = itemDict["sellingStatus"][0]["sellingState"][0]
		item["currentPrice"] = itemDict["sellingStatus"][0]["currentPrice"][0]["__value__"]

		category = {}
		category["id"] = itemDict["primaryCategory"][0]["categoryId"][0]
		category["name"] = itemDict["primaryCategory"][0]["categoryName"][0]

		username = itemDict['sellerInfo'][0]['sellerUserName'][0]
		location = itemDict['location'][0]
		topRatedSeller = itemDict['sellerInfo'][0]['topRatedSeller'][0]
		userdata, feedbackDetails = getUserInfo(username)		
		feedbackRatingStar = userdata["FeedbackRatingStar"]
		userdata['location'] = location
		userdata['topRatedSeller'] = topRatedSeller
		userdata['itemsSold'] = [item]		

		for entry in feedbackDetails:
			feedbackItem = {}
			feedbackItem["CommentingUser"] = entry["CommentingUser"]
			feedbackItem["CommentText"] = entry["CommentText"]
			feedbackItem["CommentTime"] = entry["CommentTime"]
			feedbackItem["CommentType"] = entry["CommentType"]
			feedbackItem["ItemID"] = entry["ItemID"]
			if 'feedbackDetails' not in userdata:
				userdata['feedbackDetails'] = [feedbackItem]
			else:
				userdata['feedbackDetails'].append(feedbackItem)

		if username not in user:
			user[username] = userdata
		else:
			user[username]['itemsSold'].append(item)

		if category["name"] not in categoryItem:
			categoryItem[category["name"]] = [item]
		else:
			categoryItem[category["name"]].append(item)

		if feedbackRatingStar not in starUser:
			starUser[feedbackRatingStar] = [username]
		else:
			starUser[feedbackRatingStar].append(username)

		if item["title"] not in itemList:
			itemList[item["title"]] = item

	return user, categoryItem, starUser, itemList

#data = searchData("Harry Potter", 10)
#print data[0]
#user, categoryItem, starUser, itemList = findData("harry potter", 10)

#print user
#print "\n"
#print categoryItem
#print "\n"
#print starUser
#print "\n"
#print itemList
#print "\n"

#print getUserInfo('revant')
