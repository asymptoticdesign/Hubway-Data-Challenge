"""
Title: etsylib
Author: nathan lachenmyer
Description: A python library that parses data acquired from etsy's web API
Usage:
Date Started: 2012 Sept
Last Modified: 2012 Oct
"""
import MySQLdb as mdb
import sys
import urllib
import json
import time
import oauth2 as oauth
import urlparse
import re

consumerKey = 'rlc50qqzm6vye52aj6ve9zhv'
consumerSecret = 's50aqzkrqe'
tokenKey = '9ffec2dc7fb946b09eb28ef4587b69'
tokenSecret = 'aff086b862'

requestTokenURL = 'http://openapi.etsy.com/v2/oauth/request_token?scope=email_r%20listings_r%20transactions_r%20billing_r'
accessTokenURL = 'http://openapi.etsy.com/v2/oauth/access_token'
authorizeURL = 'https://www.etsy.com/oauth/signin'

def MySQLcommand(command,host='localhost',user='root',pw='q1SWE#fr',database='nervoussystem'):
    conn = None

    try:
        conn = mdb.connect(host,user,pw,database)
        cur = conn.cursor()
        cur.execute(command)
    
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)

    finally:
        if conn:
            conn.commit()
            conn.close()

def MySQLquery(command,host='localhost',user='root',pw='q1SWE#fr',database='nervoussystem'):
    conn = None

    try:
        conn = mdb.connect(host,user,pw,database)
        cur = conn.cursor()
        cur.execute(command)
        rows = cur.fetchall()
#        for row in rows:
#            print row
    
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)

    finally:
        if conn:
            conn.commit()
            conn.close()

    return rows

def decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = decode_list(item)
        elif isinstance(item, dict):
            item = decode_dict(item)
        rv.append(item)
    return rv
        
def decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = decode_list(value)
        elif isinstance(value, dict):
            value = decode_dict(value)
        rv[key] = value
    return rv

def formatParams(paramDictionary):
    """
    Formats a dictionary to the appropriate http query format.
    """
    paramString = '?'
    for key in paramDictionary.keys():
        paramString += '&' + key + '=' + paramDictionary[key]
    return paramString

def requestInfo(request, params={'api_key':consumerKey,'limit':'5'},baseurl='http://openapi.etsy.com/v2'):
    """
    Request data from the etsy server.  request is in the form of an URI as described by the etsy documentation; params is a dictionary of the format {'parameter':'value'}
    """
    paramString = formatParams(params)
    url = baseurl+request+paramString
    urlobj = urllib.urlopen(url)
    data = urlobj.read()
    parsedData = json.loads(data,object_hook=decode_dict)
    return parsedData

def oauth_req(url, key, secret, http_method="GET", post_body='',http_headers=None):
    consumer = oauth.Consumer(key=consumerKey, secret=consumerSecret)
    token = oauth.Token(key=tokenKey, secret=tokenSecret)
    client = oauth.Client(consumer, token)
    resp, content = client.request(
        url,
        method=http_method,
        body=post_body,
        headers=http_headers,
        )
    return resp,content

def requestAuthInfo(request,params={'limit':'10'},baseurl='http://openapi.etsy.com/v2'):
    """
    Request authorized information from etsy via oauth tokens.
    """
    paramString = formatParams(params)
    url = baseurl+request+paramString
    info,data= oauth_req(url,tokenKey,tokenSecret)
    parsedData = json.loads(data,object_hook=decode_dict)
    return parsedData

class ListingsList:
    """
    A wrapper that formats the list of listings
    """
    
    def __init__(self,listingQuery):
        """
        Pass the result from a listings query here.  The class then formats it so its easy to use and read.
        """
        self.results = listingQuery['results']
        self.count = listingQuery['count']
        self.shopid = listingQuery['params']['shop_id']
        self.listings = []

    def formatListings(self):
        """
        Formats the listings.  listings holds the listings objects, while items holds the titles for human-readable identifications.
        """
        for listing in self.results:
            self.listings.append(Listing(listing))

    def showItems(self):
        itemNo = 1
        print 'ItemNo \t Item Title'
        for item in self.listings:
            print str(itemNo) + '\t' + item.title
            itemNo += 1

class Listing:
    """
    A listing class that allows easy access of the Listing fields.  See the etsy API for more information.

    http://www.etsy.com/developers/documentation/reference/listing
    """

    def __init__(self,dict_entry):
        """
        Unwrap all of the categories from a dictionary to local variables.
        """
        self.itemid = dict_entry['listing_id']
        self.state = dict_entry['state']
        self.user = dict_entry['user_id']
        self.category = dict_entry['category_id']
        self.title = dict_entry['title']
        self.description = dict_entry['description']
        self.creationDate = time.ctime(dict_entry['creation_tsz'])
        self.modifiedDate = time.ctime(dict_entry['last_modified_tsz'])
        self.price = dict_entry['price']
        self.quantity = dict_entry['quantity']
        self.tags = dict_entry['tags']
        self.materials = dict_entry['materials']
        self.views = dict_entry['views']
        self.url = dict_entry['url']
        self.rank = dict_entry['featured_rank']
        self.style = dict_entry['style']
        self.shipping = dict_entry['shipping_profile_id']

class Transactions:
    """
    A transactions class that allows for easy access of transaction data.
    """
    def __init__(self,transactionQuery):
        """pass the result from a listings query here.  The class then formats it so its easy to use and read.
        """
        self.count = transactionQuery['count']
        self.results = transactionQuery['results']
        self.transactions = []

    def formatTransactions(self):
        """
        Formats the transactions.
        """
        for transaction in self.results:
            self.transactions.append(Transaction(transaction))

    def formatBuyers(self):
        for transaction in self.transactions:
            transaction.getBuyerInfo()

    def formatShipping(self):
        for transaction in self.transactions:
            transaction.getShippingInfo()

    def showTransactions(self):
        transactionNo = 1
        print 'Transaction ID \t Quantity \t Desc'
        for transaction in self.transactions:
            print str(transaction.id) + '\t\t' + str(transaction.quantity) + '\t' + transaction.title + '\t' + str(transaction.receiptid) + '\t' + str(transaction.listingid)
            transactionNo += 1

    def showBuyers(self):
        transactionNo = 1
        print 'Transaction ID \t User ID \t Date \it Item'
        for transaction in self.transactions:
            print str(transaction.id) + '\t' + str(transaction.buyerid) + '\t' + str(transaction.transactionDate) + '\t' + str(transaction.title)
            transactionNo += 1

class Transaction:
    """
    A transaction class that allows easy access of the transaction fields.  See the etsy API for more information.

    http://www.etsy.com/developers/documentation/reference/transaction
    """

    def __init__(self,dict_entry):
        """
        Unwrap all of the categories from a dictionary to local variables.
        """
        self.id = dict_entry['transaction_id']
        self.listingid = dict_entry['listing_id']
        self.title = dict_entry['title']
        self.description = dict_entry['description']
        self.productid = returnProductID(self.description)
        self.sellerid = dict_entry['seller_user_id']
        self.buyerid = dict_entry['buyer_user_id']
        self.price = dict_entry['price']
        self.date = time.ctime(dict_entry['creation_tsz'])
        self.paidDate = dict_entry['paid_tsz']
        self.shippedDate = dict_entry['shipped_tsz']
        self.quantity = dict_entry['quantity']
        self.shippingCost = dict_entry['shipping_cost']
        self.receiptid = str(dict_entry['receipt_id'])
        self.status = "PENDING"

    def getBuyerInfo(self):
        """
        Use the receipt ID to pull out the buyer info.
        """
        receiptQuery = requestAuthInfo('/receipts/'+str(self.receiptid))
        results = receiptQuery['results']
        self.buyer = str(results[0]['name'])
        self.email = str(results[0]['buyer_email'])
        addressLine = str(results[0]['first_line'])
        secondLine = results[0]['second_line']
        if secondLine:
            addressLine += ' '+secondLine
        self.address = addressLine
        self.city = results[0]['city']
        self.state = results[0]['state']
        self.zipcode = str(results[0]['zip'])
        self.country = results[0]['country_id']                                       
        countryQuery = requestAuthInfo('/countries/'+str(self.country))
        results = countryQuery['results']
        self.country = results[0]['name']

    def getShippingInfo(self):
        listingQuery = requestAuthInfo('/listings/'+str(self.listingid))
        self.shippingprofileid = listingQuery['results'][0]['shipping_profile_id']
        self.shippingprofile = requestAuthInfo('/shipping/profiles/'+str(self.shippingprofileid))['results'][0]['name']    

#Create listings
def showInventory(numItems):
    listingsQuery = requestInfo('/shops/nervoussystem/listings/active',params={'api_key':consumerKey,'limit':str(numItems)})
    listOfListings = ListingsList(listingsQuery)
    listOfListings.formatListings()
    listOfListings.showItems()

def showTransactions(numTransactions):
    transactionsQuery = requestAuthInfo('/shops/nervoussystem/transactions',params={'limit':str(numTransactions)})
    listOfTransactions = Transactions(transactionsQuery)
    listOfTransactions.formatTransactions()
    listOfTransactions.showTransactions()

def showBuyers(numBuyers):
    transactionsQuery = requestAuthInfo('/shops/nervoussystem/transactions',params={'limit':str(numBuyers)})
    listOfTransactions = Transactions(transactionsQuery)
    listOfTransactions.formatTransactions()
    listOfTransactions.showBuyers()

def returnProductID(description):
    """
    Returns a product ID given the description of an etsy listing.
    """
    #convert to lowercase so no case-matching is needed
    description = description.lower()
    if 'item no' in description:
        #if the item is in our new inventory system (with product id listed)
        index = description.rfind('item no')
        productid = description[index:]
        productid = productid.split()[-1]
        return productid
    else:
        #if the item is pre-inventory, return 'null' string.
        return 'NULL'

def returnShippingInfo(receiptid):
    """
    Given a receiptid, returns the shipping address of a buyer.
    """
    receiptQuery = requestAuthInfo('/receipts/'+str(receiptid),params={'limit':'1'})
    results = receiptQuery['results']
    addressLine = str(results[0]['first_line'])
    secondLine = results[0]['second_line']
    if secondLine:
        addressLine += ' '+secondLine
    city = results[0]['city']
    zipcode = str(results[0]['zip'])
    return addressLine, city, zipcode

def getNewOrders():
    """
    Updates a MySQL database based on data ripped from the etsy api.
    """
    #First -- query etsy for information on all transactions
    transactionsQuery = requestAuthInfo('/shops/nervoussystem/transactions',params={'limit':'10'})
    transactions = Transactions(transactionsQuery)
    transactions.formatTransactions()
    transactions.formatBuyers()
    transactions.formatShipping()

    #make container lists
    order_etsy = []
    order_etsy_product = []

    #Make a list of receipts that currently exist in the database
    receiptList = []
    receiptQuery = MySQLquery("SELECT receipt_id FROM orders_etsy;")
    for receipt in receiptQuery:
        receiptList.append(receipt[0])

    #select the latest item in the database, and save its date
    latestEntry = MySQLquery("SELECT date FROM orders_etsy ORDER BY receipt_id DESC;")
    latestDate = latestEntry[0][0]
    
    for transaction in transactions.transactions:
        #only add new transactions to the queue
        if transaction.receiptid not in receiptList and time.strptime(transaction.date) > time.strptime(latestDate):
            order_etsy.append([transaction.receiptid, transaction.buyer, transaction.email, transaction.address, transaction.city, transaction.state, transaction.zipcode, transaction.country, transaction.shippingprofile, transaction.status, transaction.date])
            receiptList.append(transaction.receiptid)
        if time.strptime(transaction.date) > time.strptime(latestDate):
            order_etsy_product.append([transaction.receiptid, transaction.productid, transaction.listingid, transaction.quantity, transaction.price, transaction.title, transaction.date])

        #iterate through the list of undocumented transactions and add them to the database
    for item in order_etsy:
        order_etsy_string = "INSERT INTO orders_etsy VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8],item[9],item[10])
        #print order_etsy_string,'\n'
        MySQLcommand(order_etsy_string)

    for item in order_etsy_product:
        order_etsy_products_string = "INSERT INTO orders_products_etsy VALUES ('%s','%s','%s','%s','%s','%s','%s')" %(item[0],item[1],item[2],item[3],item[4],item[5],item[6])
        #print order_etsy_products_string,'\n'
        MySQLcommand(order_etsy_products_string)

def updateShippingInfo():
    etsyQuery = requestAuthInfo('/shops/nervoussystem/receipts',{'limit':'50','offset':'0'})
    #make container list
    receipts = []
    #add the first 50 items, determine total number of items
    for receipt in etsyQuery['results']:
        receipts.append(receipt)
    count = etsyQuery['count']
    offsetNo = 50

    #iterate until all items are accounted for
    while offsetNo < count:
        #retrieve the next 50 items
        etsyQuery = requestAuthInfo('/shops/nervoussystem/receipts',{'limit':'50','offset':str(offsetNo)})
        for receipt in etsyQuery['results']:
            receipts.append(receipt)
        offsetNo += 50

#    print "Total count is",count
#    print "Retrieved",len(receipts),"records"
    for receiptIndex in range(len(receipts)):
        wasShipped = receipts[receiptIndex]['was_shipped']
        commandString = "UPDATE orders_etsy SET status = 'SHIPPED' WHERE receipt_id = '"+str(receipts[receiptIndex]['receipt_id'])+"';"
        if wasShipped:
            MySQLcommand(commandString)

def updateDatabase():
    getNewOrders()
    updateShippingInfo()
    logFile = open('etsy.log','w')
    logFile.write("Databased updated at "+str(time.ctime(time.time())))
    logFile.close()
