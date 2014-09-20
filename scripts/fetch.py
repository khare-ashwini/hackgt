import urllib2
import json

def findItemsByKeywords(keyword):
	url = """http://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findItemsByKeywords&
																					SERVICE-VERSION=1.12.0&
																					SECURITY-APPNAME=GeorgiaI-927c-4229-856a-e1ec1717d0b9&
																					RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD&
																					outputSelector(0)=SellerInfo&
																					outputSelector(1)=StoreInfo&
																					keywords=""" + keyword
	response = urllib2.urlopen(url)
	data = json.load(response)
	count = int(data["findItemsByKeywordsResponse"][0]['searchResult'][0]['@count'])
	return data, count

def getUserInfo(username):
	url = """http://open.api.ebay.com/shopping?callname=GetUserProfile&
												responseencoding=JSON&
												appid=GeorgiaI-927c-4229-856a-e1ec1717d0b9&siteid=0
												&version=525&
												UserID=""" + username
	response = urllib2.urlopen(url)
	data = json.load(response)
	userdata = data["user"]
	return userdata

def findUser(keyword):
	data, count = findItemsByKeywords(keyword)
	userlocation = {};
	for i in range(count):
		username = data["findItemsByKeywordsResponse"][0]['searchResult'][0]['item'][i]['sellerInfo'][0]['sellerUserName'][0]
		userdata = getUserInfo(username)
		location = data["findItemsByKeywordsResponse"][0]['searchResult'][0]['item'][i]['location'][0]