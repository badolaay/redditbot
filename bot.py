import praw
import requests
import configparser

config = configparser.RawConfigParser()
config.read('config.ini')


def printComments(subreddit):
    mailBody = "<br>Heres some posts from <a href=""reddit.com/r/" + subreddit.display_name + """>""" + subreddit.display_name
    mailBody += "</a><br><br>"
    i = 0
    try:
        for submission in subreddit.hot(limit=int(config.get('reddit', 'postsToFetch'))):
            if not submission.stickied and i < int(config.get('reddit', 'maxPostsToEmail')):
                i += 1
                mailBody += "<strong>Title:</strong> " + submission.title + "<br>"
                if submission.selftext != '':
                    mailBody += "<strong>Text:</strong> " + submission.selftext + "<br>"
                mailBody += "<strong>Score:</strong> " + str(submission.score) + "<br>"
                j = 0
                mailBody += "<strong>Comments:</strong><br>"
                comments = submission.comments._comments
                if len(comments) == 0:
                    mailBody += "<i>This post has no comments</i><br><br>"
                while j < int(config.get('reddit', 'commentsToEmail')) and len(comments) > j:
                    mailBody += comments[j].body + "<br><br>"
                    j += 1

                mailBody += "---------------------------------<br>"
    except:
        pass
    return mailBody


reddit = praw.Reddit('redditDigesttbot')

messages = reddit.inbox.all()
for message in messages:
    m = message.body.split(";")
    if (len(m) > 1):
        email = m[0]
        text = ''
        for i in range(1, len(m)):
            text += printComments(reddit.subreddit(m[i]))
        text += "<br>Explore some random subreddits:<br>"
        text += printComments(reddit.subreddit(config.get('reddit', 'randomSubreddit')))
        # send email
        requests.post(
            config.get('mail', 'url'),
            auth=("api", config.get('mail', 'key')),
            data={"from": config.get('mail', 'from'),
                  "to": email,
                  "subject": "Digest",
                  "html": text})
