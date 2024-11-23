import sendgrid
import os
from sendgrid.helpers.mail import *
import requests
# from dotenv import load_dotenv
import datetime
from openai import OpenAI

# Load API key from .env file
# load_dotenv()

client = OpenAI(
  organization='',
  api_key='',
)

NEWS_API_KEY= ""
EMAIL_API_KEY= ""
email= ""

def getNews():
    print("Making API call")
    url= f"https://newsapi.org/v2/everything?domains=techcrunch.com,thenextweb.com&apiKey={NEWS_API_KEY}"
    response= requests.get(url)
    print(response.json())
    
def sendEmail():
    today = datetime.date.today()
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
        
def summarize_article(content):
    prompt = (
        f"Summarize this article: {content}"
    )
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant that summarizes articles."},
        {"role": "user", "content": prompt}
        ]
    )
    print(response.choices[0].message)
    summary = response.choices[0].message.content
    return summary
    
def categorize_article(title, description):
    prompt = (
        f"Here is an article:\n\nTitle: {title}\nContent: {description}\n\n"
        "Assign it to one of these categories: Technology, Health, Business, Sports, Entertainment, or Politics."
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an assistant that assigns categories to news articles."},
            {"role": "user", "content": prompt}
        ]
    )
    category = response.choices[0].message.content
    return category

# getNews()
# sendEmail()
# summarize_article()
