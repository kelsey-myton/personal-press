import requests

API_KEY= ""

def getNews():
    print("Making API call")
    url= f"https://newsapi.org/v2/everything?domains=techcrunch.com,thenextweb.com&apiKey={API_KEY}"
    response= requests.get(url)
    print(response.json())
    
getNews()
