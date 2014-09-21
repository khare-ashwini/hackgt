##HackGT
______

###Tech 

* Ebay API
* Flask


##Application
   This application will be able to for each seller you will be able to get store information, i.e. what item the store will have. You will be able to access information regarding the top sellers across the nation, and across any state.
With the combinations of several different APIs you should be able to search for the users that you want to buy from.

##Usage
   ```python __init__.py```

###Ebay API
____________________

Used Finding API and Shopping API

Methods used for API Calls from Finding API
* getSearchKeywordsRecommendation: Get recommended keywords for search
* findItemsByKeywords: Search items by keywords

Methods used for API Calls from Shopping API
* GetUserProfile: Retrieve eBay user profile and feedback information
* GetSingleItem: Simplified buyer specific view of item data

Useful API Calls

* findItemsByKeywords: Search items by keywords

http://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findItemsByKeywords&SERVICE-VERSION=1.12.0&SECURITY-APPNAME=GeorgiaI-927c-4229-856a-e1ec1717d0b9&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD&keywords=%22pre-CBS%22&outputSelector(0)=SellerInfo&outputSelector(1)=StoreInfo

* GetUserProfile: Retrieve eBay user profile and feedback information

http://open.api.ebay.com/shopping?callname=GetUserProfile&responseencoding=JSON&appid=GeorgiaI-927c-4229-856a-e1ec1717d0b9&siteid=0&version=525&UserID=dudescotty

* getSearchKeywordsRecommendation: Get recommended keywords for search

http://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=getSearchKeywordsRecommendation&SERVICE-VERSION=1.12.0&SECURITY-APPNAME=GeorgiaI-927c-4229-856a-e1ec1717d0b9&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD&keywords=arry+poter+phonix

