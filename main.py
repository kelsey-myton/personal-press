import sendgrid
import os
from sendgrid.helpers.mail import *
import requests
# from dotenv import load_dotenv
import datetime

# Load API key from .env file
# load_dotenv()

NEWS_API_KEY= ""
EMAIL_API_KEY= ""

today = datetime.date.today()
email= ""

def getNews():
    print("Making API call")
    url= f"https://newsapi.org/v2/everything?domains=techcrunch.com,thenextweb.com&apiKey={NEWS_API_KEY}"
    response= requests.get(url)
    print(response.json())
    
def sendEmail():
    try:
        sg = sendgrid.SendGridAPIClient(api_key=EMAIL_API_KEY)
        fromEmail = Email(email)
        toEmail = To(email)
        subject = "Personal Press Summary: " + today.strftime("%m/%d/%Y")
        content = Content("text/html", "<div><h1>Personal Press</h1></div>")
        mail = Mail(fromEmail, toEmail, subject, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        print(response.status_code)
        print(subject)
    except SendGridException as e:
        print(e.message)
    
getNews()
sendEmail()
