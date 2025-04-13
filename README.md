# personal-press

A personalized news aggregator that fetches articles from APIs based on user defined preferences.
- Automated the creation of responsive HTML email content with Python and delivered curated news via SendGrid.
- Integrated OpenAI to summarize and categorize news articles, enhancing relevance and readability for users.
- Scheduled daily execution with Windows Task Scheduler, ensuring reliable and hands-free operation.

## Installation

1. Clone the repo:
git clone https://github.com/kelsey-myton/personal-press.git

2. Install dependencies:
pip install -r requirements.txt

## Usage

Run the main script:
python main.py

Update user perferences:
python userPreferences.py

## APIs used

News API: https://newsapi.org/docs/get-started 
Sendgrid: https://www.twilio.com/docs/sendgrid/for-developers
OpenAI: https://platform.openai.com/docs/overview
