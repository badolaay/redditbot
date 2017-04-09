import praw
import requests
import configparser

config = configparser.RawConfigParser()
config.read('config.ini')


def printComments(subreddit):
    text = "Heres some posts from <a href=""reddit.com/r/" + subreddit.display_name + """>""" + subreddit.display_name
    text += "</a><br><br>"
    i = 0
    try:
        for submission in subreddit.hot(limit=3):
            if (not submission.stickied and i < 5):
                i += 1
                text += "<strong>Title:</strong> " + submission.title + "<br>"
                if (submission.selftext != ''):
                    text += "<strong>Text:</strong> " + submission.selftext + "<br>"
                text += "<strong>Score:</strong> " + str(submission.score) + "<br>"
                j = 0
                text += "<strong>Comments:</strong><br>"
                comments = submission.comments._comments
                while (j < 5 and len(comments) > j):
                    text += comments[j].body + "<br><br>"
                    j += 1

                text += "---------------------------------<br>"
    except:
        pass
    return text


def send_simple_message(to, text):
    return requests.post(
        config.get('mail', 'url'),
        auth=("api", config.get('mail', 'key')),
        data={"from": config.get('mail', 'from'),
              "to": to,
              "subject": "Hello",
              "html": text})


reddit = praw.Reddit('testbot')

messages = reddit.inbox.all()
for message in messages:
    m = message.body.split(";")
    if (len(m) > 1):
        email = m[0]
        text = ''
        for i in range(1, len(m)):
            subreddit = reddit.subreddit(m[i])
            text += printComments(subreddit)
        text += "<br>Explore some random subreddits:<br>"
        text += printComments(reddit.subreddit("random"))
        send_simple_message(email, text)

# subreddit = reddit.subreddit("random")
# subreddit = reddit.subreddit("random")
# subreddit = reddit.subreddit("random")
