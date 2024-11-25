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
  api_key=''
)

NEWS_API_KEY= ""
EMAIL_API_KEY= ""
email= ""

def getNews(country='us'):
    topArticles= []
    url= f"https://newsapi.org/v2/top-headlines?country={country}&pageSize=5&apiKey={NEWS_API_KEY}"
    response= requests.get(url).json()
    topArticles= response['articles']
    return topArticles
    
def sendEmail(content):
    today = datetime.date.today()
    try:
        sg = sendgrid.SendGridAPIClient(api_key=EMAIL_API_KEY)
        fromEmail = Email(email)
        toEmail = To(email)
        subject = "Personal Press Digest: " + today.strftime("%m/%d/%Y")
        emailBody= Content("text/html", "<h1>Personal Press Digest</h1>" + content)
        mail = Mail(fromEmail, toEmail, subject, emailBody)
        response = sg.client.mail.send.post(request_body=mail.get())
        print(response.status_code)
        print(subject)
    except SendGridException as e:
        print(e.message)
        
def summarizeArticle(content):
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
    
def categorizeArticle(title, description):
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

def createNewsDigest():
    articles= getNews()
    formattedArticles= []
    content=''
    for article in articles:
        # summary= summarizeArticle(article)
        summary= article['description']
        formattedArticles.append(newsArticle(article['title'], summary, article['author'], article['source'], article['url']))
        content +=   f"""<div>
                      <h4>{article['title']}</h4>
                      <h6>{article['source']['name']}</h6>
                      <h6>{article['author']}</h6>
                      <h6>{summary}</h6>
                      <a href={article['url']}>Read full article > </a>
                      </div>"""
    sendEmail(content)

createNewsDigest()