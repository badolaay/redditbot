import praw

reddit = praw.Reddit('bot1')

subreddit = reddit.subreddit("programming")


def printComments():
    print("Heres some posts from " + subreddit.display_name)
    i = 0
    for submission in subreddit.hot(limit=5):
        if (not submission.stickied and i < 1):
            i += 1
            print("Title: ", submission.title)
            if (submission.selftext != ''):
                print("Text: ", submission.selftext)
            print("Score: ", submission.score)
            i = 0
            comments = submission.comments._comments
            while (i < 1 and len(comments) > i):
                print(comments[i].body)
                i += 1

            print("---------------------------------\n")


printComments()
subreddit = reddit.subreddit("random")
subreddit = reddit.subreddit("random")
subreddit = reddit.subreddit("random")
printComments()
