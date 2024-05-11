# TODO
# iterate over comments in a way that is sure not to miss a MoreComments instance
# try to load MoreComments into the list.
# This was a random script I used to fix an issue where JohnColtraneBot left
# infinite comments on some guy due to the MoreComments result not having an author,
# or something like that. Anyways, might be useful later.

# Should experiment with this parent_id which led the issue the first time around:
# - kf7wb9o
# ex for fetching objects:
#  comment = [j for j in reddit.info(fullnames=["t1_kf7wb9o"])][0]
#  submission = comment.submission

# Then just repeat the above logic in the shell and try to fix

import datetime
import time
from praw.models import MoreComments
from reddit import reddit

from config import REDDIT_USERNAME

def fix_comments(parent_id: str):
    comment = [j for j in reddit.info(fullnames=[f't1_{parent_id}'])][0]
    comment.refresh()

    process_comments = []
    extra_comments = []
    for r in comment.replies:
        if isinstance(r, MoreComments):
            for c in r.comments():
                if c.author == REDDIT_USERNAME:
                    extra_comments.append(c)
        elif r.author == REDDIT_USERNAME:
            process_comments.append(r)

    return process_comments, extra_comments

def delete_comments(comments_list):
    count = 0
    for comment in comments_list:
        if count >= 90:
            time.sleep(60)
            count = 0
            print(f"[{datetime.datetime.utcnow()}] Sleeping...")

        print(f"[{datetime.datetime.utcnow()}] Deleting comment: {comment.id}")
        comment.delete()
        count += 1
