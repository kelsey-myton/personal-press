import sendgrid
import os
from sendgrid.helpers.mail import *
import requests
import datetime
from openai import OpenAI
import json

client = OpenAI(
  organization='',
  api_key=''
)

NEWS_API_KEY= ''
EMAIL_API_KEY= ''

# Load the data from the file
with open("userPreferences.json", "r") as f:
    data = json.load(f)
        
today = datetime.date.today()

header="""
            <!DOCTYPE html>
            <html>
                <head>
            <style>
                h1{
                font-family: "Diplomata SC", serif;
                font-weight: 400;
                font-size: 30px;
                font-style: normal;
                text-align: center;
                }
            .header{
                display: flex;
                justify-content: space-between;
            }
            a{
                color: #4A0404;
                border: 1.5px solid #4A0404;;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
            }
            .footer{
                display: flex;
                flex-direction: row;
                gap: 10px;
                text-align: center;
            }
            .footer-lines{
                width:28%;
                margin:auto;
            }
            hr{
                margin:2px;
                color: #4A0404;
            }
            </style>
                </head>
            <body>
                <div class='header'>
                <h6>""" + today.strftime("%B %d, %Y") + """</h6>
                </div>
                <hr>
                <hr>
            <h1>Personal Press Digest</h1>
            """
footer= """       
            <div class='footer'>
                <div class='footer-lines'>
                <hr>
                <hr>
                </div>
                <h6>Your News, Your Way- Delivered Daily.</h6> 
                <div class='footer-lines'>
                <hr>
                <hr>
                </div>
                </div>
                </body></html>"""

def getNews(country='us'):
    url= f"https://newsapi.org/v2/top-headlines?country={country}&pageSize={data['numArticles']}&apiKey={NEWS_API_KEY}"
    response= requests.get(url).json()
    return response['articles']
    
def sendEmail(content):
    try:
        sg = sendgrid.SendGridAPIClient(api_key=EMAIL_API_KEY)
        fromEmail = Email(data['email'])
        toEmail = To(data['email'])
        subject = "Personal Press Digest: " + today.strftime("%m/%d/%Y")
        emailBody= Content("text/html", header + content + footer)
        mail = Mail(fromEmail, toEmail, subject, emailBody)
        response = sg.client.mail.send.post(request_body=mail.get())
    except SendGridException as e:
        print(e.message)
        
def summarizeArticle(url):
        
    prompt = (
        f"Summarize the article at this link: {url}. Use a {data['tone']} and {data['length']}."
    )
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are an editor, summarizing a news article for a digest."},
        {"role": "user", "content": prompt}
        ]
    )
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
        summary= summarizeArticle(article['url'])
        content +=   f"""<div>
                    <hr style='margin:20px;'>
                      <h4>{article['title']}</h4>
                      <h6>{article['source']['name']}</h6>
                      <h6>By {article['author']}</h6>
                      <h6>{summary}</h6>
                      <a href={article['url']}>Read full article</a>
                      </div>"""
    sendEmail(content)

createNewsDigest()