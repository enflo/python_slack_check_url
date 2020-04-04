# PYTHON CHECK URL SLACK NOTIFIER

A simple script to easily check URLs and notify a Slack channel

## How does it work?
The first thing to do is to start a virtualenv and install the requirements
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

You need to create an .env file with the following entries:
```dotenv
SLACK_API_TOKEN='xoxp-12345...' # Token obtained from https://api.slack.com/custom-integrations/legacy-tokens
SLACK_CHANNEL='CHANELID'
SLACK_USERNAME='USERNAME'
```

Finally add your url in the file landingURL.txt
Now you are ready to run the script
```bash
python httpAssertion.py
```
