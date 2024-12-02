import os
from typing import List
from snscrape.modules.twitter import TwitterHashtagScraper
import praw
# from app.configs import print_error, print_log,  print_success
from praw.models import MoreComments

def get_tweets(hashtag):
    scrape = TwitterHashtagScraper(f'{hashtag}')
    i = 0
    items = dict()
    for item in scrape.get_items():
        # items.append(item.content)
        tweet_content = item.content
        items[f"{i}"] = tweet_content.encode('ascii', 'ignore').decode()
        # items[f"{i}"] = re.sub(r'(\\u[0-9A-Fa-f]+)', unescapematch, tweet_content)
        i += 1
        if i == 5:
            break
    return items

def get_subreddit_info(subreddit):
    client_id  = "FejZ17tRaMjIcuacaNUeTA"
    client_secret = "QOkHMXZ0P05Fmhg59MgZh0HL-I4eCg"
    user_agent =  "scraper"
    reddit_link = "https://www.reddit.com/"
    read_only = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
    )
    sub_data = read_only.subreddit(f"{subreddit}")     # minus the "r/"

    # print_success("Data Get Successful")
    # print_log(f"Display name: {sub_data.display_name}")
    # print_log(f'Title: {sub_data.title}')
    # print_log(f'description: {sub_data.description}')
    print('doing shit')
    all_posts = sub_data.top("day")
    posts = list()
    for post in all_posts:
        data = {
            'title': post.title,
            'content': post.selftext,
            'id': post.id,
            'score': post.score,
            'comments': post.num_comments,
            'url': post.url,
            'perma_url': f"{reddit_link}/{post.permalink}",
            'top_comments': [],
            'replies': [],
        }
        try:
            submission = read_only.submission(
                url=data['perma_url']
            )
            i = 10
            for comment in submission.comments:
                if type(comment) == MoreComments:
                    continue
                data['top_comments'].append(comment.body)
                replies = comment.replies.list()
                for reply in replies:
                    data['replies'].append(reply.body)
                i+=1
                if i==10:
                    break
        except:
            pass
        posts.append(data)
    return posts

def raw_data(data) -> List:
    if type(data) == list:
        datalist = list()
        for post in data:
            datalist.append(post['content'])
            for item in post['top_comments']:
                datalist.append(item)
            for item in post['replies']:
                datalist.append(item)
    return _flatten_data(datalist)


def _flatten_data(data):
    raw_string = ''
    for item in data:
        raw_string += item
    return raw_string
    