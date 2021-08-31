# subreddit-bot-tools
Collection of miscellaneous Reddit tools by /u/Elaeagnifolia.

These all use PRAW. Quick start and installation can be found here: https://praw.readthedocs.io/en/stable/

## MegathreadPostUpdater.py
Generates a list of desired threads and megathreads automatically in a given comment. Acts as a way to get around Reddit's only 2 pinned posts.

praw.ini Variables
```
user_agent
redirect_uri
client_id
client_secret
password
username
subreddit
comment_id
post_limit
```

**Examples**
* /r/MrLove: https://www.reddit.com/r/MrLove/comments/f29nzo/read_me_subreddit_rules_megathreads_flairs_and/fhb3qyk/
* /r/TearsOfThemis: https://www.reddit.com/r/TearsOfThemis/comments/mzrhe5/read_me_subreddit_rules_megathreads_flairs_and/
