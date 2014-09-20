import urllib2
import json

response = urllib2.urlopen("http://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findItemsByKeywords&SERVICE-VERSION=1.12.0&SECURITY-APPNAME=GeorgiaI-927c-4229-856a-e1ec1717d0b9&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD&keywords='pre-CBS'%22&outputSelector(0)=SellerInfo&outputSelector(1)=StoreInfo")
data = json.load(response)   

#Count of the item searched by that keyword
count = int(data["findItemsByKeywordsResponse"][0]['searchResult'][0]['@count'])

#Seller Info for each of the item. This may be repated
for i in range(count):
	print data["findItemsByKeywordsResponse"][0]['searchResult'][0]['item'][i]['sellerInfo']
	print "\n"