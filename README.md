# subreddit-bot-tools
Collection of miscellaneous Reddit tools by /u/Elaeagnifolia.

## Requirements

* Python 3. Specific version used for development of these tools is 3.9.4.
* PRAW. Quick start and installation can be found here: https://praw.readthedocs.io/en/stable/

## MegathreadPostUpdater.py
For a given post, users can specify flairs to generate subsections with lists of submissions for the given flair. By default, also generates a list of the given Megathreads with the latest posts for that type of Megathread.

**TO-DO**: Add functionality for it to edit the Wiki as well (index, sidebar, etc.)

**praw.ini Variables**
```
[site]
user_agent=
redirect_uri=
client_id=
client_secret=
password=
username=
subreddit=
comment_id=
post_limit=
```

**Usage**
```
Usage:
  MegathreadPostUpdater.py [site] [flairs] [headers] [megathreads]

Arguments:
  site          The praw.ini site identifier
  flairs        Comma-separated list of flairs to make subsections for
  headers       Comma-separated list of header names for flair subsections
  megathreads   Semicolon-separated list of general megathread names
```

**Examples**
* /r/MrLove - `MegathreadPostUpdater.py mrlove_bot "Event,Meta,Pinned" "Current Events,Game News/Information,Other Pinned Posts" "Weekly General Help/Questions Megathread;Monthly Pull, Achievements, and Salt Megathread;Monthly Friend Request Megathread;Free Talk Weekend Weekly Megathread;Self Promotion Megathread"`
    * Link: https://www.reddit.com/r/MrLove/comments/f29nzo/read_me_subreddit_rules_megathreads_flairs_and/fhb3qyk/
* /r/TearsOfThemis - `MegathreadPostUpdater.py tot_bot "Pinned,Event,News,Subreddit News" "Pinned,Current Events,Game News/Information,Subreddit News/Information" "Weekly General Help/Questions Megathread;Weekly Progress, Pulls, and Collection Megathread;Monthly Friend UID Megathread"`
    * Link: https://www.reddit.com/r/TearsOfThemis/comments/mzrhe5/read_me_subreddit_rules_megathreads_flairs_and/
