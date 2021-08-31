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
* [SpoilerFlairEditor.py](#spoilerflaireditorpy)
    * [To-Do](#to-do-1)
    * [praw.ini](#prawini-1)
        * [Template](#template)
    * [Usage](#usage)
        * [Example](#example)

## Requirements

* Register your Reddit App: https://www.reddit.com/prefs/apps/
* Python 3. Specific version used for development of these tools is 3.9.4.
* PRAW. Quick start and installation can be found here: https://praw.readthedocs.io/en/stable/

## MegathreadPostUpdater.py
For a given post, users can specify flairs to generate subsections with lists of submissions for the given flair. By default, also generates a list of the given Megathreads with the latest posts for that type of Megathread.

Submissions will fall off the list when: 1) They are no longer pulled due to going past the specified `post_limit` 2) If the submission is Locked.

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

#### Example

##### /r/MrLove

**Link**: https://www.reddit.com/r/MrLove/comments/f29nzo/read_me_subreddit_rules_megathreads_flairs_and/fhb3qyk/

**Command**: `py MegathreadPostUpdater.py mrlove_bot`

**praw.ini Example**:
```
[mrlove_bot]
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

## SpoilerFlairEditor.py
For cases where a community wants to allow limited editing of flairs specifically for spoiler posts. For example, if an OP of a post has a `Game Screenshot` post marked as Spoiler, and they want to add where in the game the post spoils (e.g. Chapter 3), replying to the bot will edit the flair to be `Game Screenshot [Chapter 3]`.

This allows users to add in this information without needing to have their post deleted/repost and also doesn't completely give users access to flair editing.

A bot will only edit a flair once per post to prevent flair editing abuse.

### To-Do
* The currenct check to see if a bot has already edited a post's flair isn't great. Improve it.
* Some parts of the script may be too specific to the subreddit this was initially intended for (/r/TearsOfThemis). Refactor to make it applicable across more subreddits.

### praw.ini
SpoilerFlairEditor.py needs a few custom-defined variables in praw.ini

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

# Custom Settings
subreddit=
flair_edit_post_limit=
spoiler_edit_flair_reminder=
```

### Usage
```
Usage:
  SpoilerFlairEditor.py [site]

Arguments:
  site          The praw.ini site identifier
```

#### Example

**Link**: https://www.reddit.com/r/TearsOfThemis/comments/pcgghp/episode_5_iii_walkthrough_and_rec_power_levels/

**Command**: `py SpoilerFlairEditor.py tot_bot`

```
[tot_bot]
# Credentials
...

# Post Settings
subreddit=TearsOfThemis
flair_edit_post_limit=50
spoiler_edit_flair_reminder=Your post has been detected as a **Spoiler** post.

  It is recommended to let other users know what content this spoils by leaving a comment that says `spoiler=<Spoiler Content>`. This will then append the spoiler content to your post flair (e.g. `Guide [Main Story 05-01]`).

  Some examples might be:

  * Main Story: `spoiler=Main Story 05-01`
  * Character Story: `spoiler=Luke 02-04`
  * Card Story: `spoiler=Artem "Atmospherics"`
  * Event: `spoiler=Lost Gold`

  **If your post title already clearly states the content your post spoils, then you may ignore this message.**
```
