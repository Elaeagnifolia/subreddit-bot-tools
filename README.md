# subreddit-bot-tools
Collection of miscellaneous Reddit tools by /u/Elaeagnifolia.

## Table of Contents
* [Requirements](#requirements)
* [MegathreadPostUpdater.py](#megathreadpostupdaterpy)
    * [To-Do](#to-do)
    * [praw.ini](#prawini)
        * [Template](#template)
    * [Usage](#usage)
        * [Example](#example)
* [FlairEditor.py](#flaireditorpy)
    * [To-Do](#to-do)

## Requirements

* Register your Reddit App: https://www.reddit.com/prefs/apps/
* Python 3. Specific version used for development of these tools is 3.9.4.
* PRAW. Quick start and installation can be found here: https://praw.readthedocs.io/en/stable/

## MegathreadPostUpdater.py
For a given post, users can specify flairs to generate subsections with lists of submissions for the given flair. By default, also generates a list of the given Megathreads with the latest posts for that type of Megathread.

### To-Do
* Add functionality for it to edit Wiki pages as well (index, sidebar, etc.)

### praw.ini
A lot of the settings used in the program come from custom-defined variables in the praw.ini.

#### Template
```
[site]
# Credentials
user_agent=
redirect_uri=
client_id=
client_secret=
password=
username=

# Post Settings
subreddit=
comment_id=
post_limit=

# Subsections
subsection_header1=
subsection_flair1=
subsection_header2=
subsection_flair2=
...
subsection_headerN=
subsection_flairN=

# Megathreads
megathread1=
megathread2=
...
megathreadN=
```

### Usage
```
Usage:
  MegathreadPostUpdater.py [site]

Arguments:
  site          The praw.ini site identifier
```

#### Examples

##### /r/MrLove

**Link**: https://www.reddit.com/r/MrLove/comments/f29nzo/read_me_subreddit_rules_megathreads_flairs_and/fhb3qyk/

**Command**: `MegathreadPostUpdater.py mrlove_bot`

**praw.ini Example**:
```
# Credentials
...

# Post Settings
subreddit=MrLove
comment_id=fhb3qyk
post_limit=750

# Subsections
subsection_header1=Current Events
subsection_flair1=Event
subsection_header2=Game News/Information
subsection_flair2=Meta
subsection_header3=Other Pinned Posts
subsection_flair3=Pinned

# Megathreads
megathread1=Weekly General Help/Questions Megathread
megathread2=Monthly Pull, Achievements, and Salt Megathread
megathread3=Monthly Friend Request Megathread
megathread4=Free Talk Weekend Weekly Megathread
megathread5=Self Promotion Megathread
```

## FlairEditor.py
For cases where a community wants to allow limited editing of flairs. For example, if a user has a `Game Screenshot` post marked as Spoiler, and they want to add where in the game the post spoils (e.g. Chapter 3), replying to the bot will edit the flair to be `Game Screenshot [Chapter 3]`.

This allows users to add in this information without needing to have their post deleted/repost and also doesn't completely give users access to flair editing.

### To-Do
* 