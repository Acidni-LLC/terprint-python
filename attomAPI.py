import http.client 
import urllib.parse

conn = http.client.HTTPSConnection("api.gateway.attomdata.com") 

headers = { 
    'accept': "application/json", 
    'apikey': "3e01f43183c0ba23eec5713eb6be66d6", 
} 
address1 ="126 Elderberry Ln"
address2 =", Palatka, FL"
address1 =  urllib.parse.quote(address1)
address2 =  urllib.parse.quote(address2)
attomid = 162317237
urlproperty ="/propertyapi/v1.0.0/property/detail?address1=" + address1 + "&address2=" + address2   
urlowner ="/propertyapi/v1.0.0/property/detailowner?attomid="+ str(attomid)
#conn.request("GET", urlproperty, headers=headers) 

conn.request("GET", urlowner, headers=headers) 

res = conn.getresponse() 
data = res.read() 
print (urlowner)
print(data.decode("utf-8"))