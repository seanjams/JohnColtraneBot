import logging
from prawcore.exceptions import ResponseException
from praw.models import MoreComments

from db import JobRun, JobStatus
from config import REDDIT_USERNAME, LOGGING_VERBOSE
from reddit import reddit

log = logging.getLogger(__name__)

def log_submission(submission):
    if LOGGING_VERBOSE:
        log.info("*" * 32)
        log.info("--Post--")
        log.info(f"Author: {submission.author}")
        log.info(f"Title: {submission.title}")

def log_comment(comment):
    if LOGGING_VERBOSE:
        log.info("-" * 32)
        log.info("--Reply--")
        log.info(f"Author: {comment.author}")
        log.info(f"Body: {comment.body}")

def check_for_john_coltranes():
    log.info("Checking for new comments...")

    subreddit = reddit.subreddit("jazzcirclejerk")
    comments_created = []

    try:
        for submission in subreddit.new(limit=10):
            submission.comments.replace_more(limit=None)
            # store comments for replies
            pending_replies = {}

            title = submission.title.lower()
            selftext = submission.selftext.lower()
            add_comment_conditions = (
                ("johncoltranebot" in title, "John Coltrane"),
                ("johncoltranebot" in selftext, "John Coltrane"),
                ("john coltrane" in title, "John Coltrane"),
                ("john coltrane" in selftext, "John Coltrane"),
                ("a love supreme" in title, "A love supreme"),
                ("a love supreme" in selftext, "A love supreme"),
            )

            for condition, text in add_comment_conditions:
                if condition:
                    pending_replies[submission.id] = (submission, text)
                    break

            # iterate over all comments and replies in breadth first order
            for comment in submission.comments.list():
                if isinstance(comment, MoreComments):
                    continue

                author = comment.author
                body = comment.body.lower()

                # if we have already replied to this comment,
                # we can remove the parent ID from the queue
                if author.name == REDDIT_USERNAME:
                    # parent id looks like t1_kc2kr2t, so split it
                    parent_id = comment.parent_id.split("_")[1]
                    pending_replies.pop(parent_id, None)
                    continue
                
                # if the comment matches the criteria, add its ID to queue
                reply_comment_conditions = (
                    ("john coltrane" in body, "John Coltrane"),
                    ("johncoltranebot" in body, "John Coltrane"),
                    ("a love supreme" in body, "A love supreme"),
                )

                for condition, text in reply_comment_conditions:
                    if condition:
                        pending_replies[comment.id] = (comment, text)
                        break

            if not pending_replies:
                continue

            # leave replies on candidate comments
            log_submission(submission)
            for comment, reply in pending_replies.values():
                # Write reply to Reddit
                comment.reply(reply)

                # Log result
                log_comment(comment)
                comments_created.append({
                    "submission_id": submission.id,
                    "submission_author": submission.author.name,
                    "submission_title": submission.title,
                    "parent_id": comment.id,
                    "parent_author": comment.author.name,
                    "parent_body": comment.body,
                    "reply_author": REDDIT_USERNAME,
                    "reply_body": reply,
                })

        msg = f"John Coltraned {len(comments_created)} faces."
        job_status = JobStatus.success
    except ResponseException as e:
        msg = f"Error John Coltraning everyone: {e.response.content}"
        job_status = JobStatus.error
    except Exception as e:
        log.exception(e)
        msg = f"Unexpected error John Coltraning everyone"
        job_status = JobStatus.error

    # save new job run to DB
    run = JobRun(
        name="check_for_john_coltranes",
        status=job_status,
        data={
            "comments_created": comments_created,
            "message": msg
        }
    )
    run.save()

    # log output
    log.info("Checking for new comments complete.")
    log.info(msg)
