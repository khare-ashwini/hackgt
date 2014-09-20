HackGT
______

###Tech 

Flask
ebay and their sucky API

##Application
   This application will be able to for each seller you will be able to get store information, i.e. what item the store will have. You will be able to access information regarding the top sellers across the nation, and across any state.
With the combinations of several different APIs you should be able to search for the users that you want to buy from.

##Usage
   cd flask
   python index.py

##Ebay API

Getting Seller Info and Store Info

http://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findItemsByKeywords&SERVICE-VERSION=1.12.0&SECURITY-APPNAME=GeorgiaI-927c-4229-856a-e1ec1717d0b9&RESPONSE-DATA-FORMAT=XML&REST-PAYLOAD&keywords=%22pre-CBS%22&outputSelector(0)=SellerInfo&outputSelector(1)=StoreInfo

GetUserProfile using the seller username obtained in the above url

http://developer.ebay.com/DevZone/shopping/docs/CallRef/GetUserProfile.html#samplebasic

http://open.api.ebay.com/shopping?callname=GetUserProfile&responseencoding=JSON&appid=GeorgiaI-927c-4229-856a-e1ec1717d0b9&siteid=0&version=525&UserID=dudescotty

