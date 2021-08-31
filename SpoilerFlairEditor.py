'''
For a given post, remind users and allow users to limitedly edit the flair through the bot.

Usage:
	FlairEditor.py [site]

Arguments:
	site          The praw.ini site identifier

Author: Elaeagnifolia | /u/Elaeagnifolia
'''

import praw
import prawcore
import argparse
import datetime

def get_spoiler_posts(reddit):
	subreddit = reddit.config.custom['subreddit']
	posts = reddit.subreddit(subreddit).new(limit=int(reddit.config.custom['flair_edit_post_limit']))

	spoiler_posts = []

	for submission in posts:
		if submission.spoiler == True and '[' not in submission.link_flair_text and submission.link_flair_text != "Future Content":
			spoiler_posts.append(submission)

	return spoiler_posts

def bot_has_posted_reminder(submission, username):
	for comment in submission.comments:
		if comment.author.name == username and comment.removed is False:
			return True
	return False

def post_reminders(reddit, posts):
	for submission in posts:
		if not bot_has_posted_reminder(submission, reddit.config.username):
			reminder_comment = submission.reply(reddit.config.custom['spoiler_edit_flair_reminder'])
			reminder_comment.mod.distinguish(how="yes")

def is_set_spoiler_comment(comment):
	FLAIR_ADDITION_MAX_LIMIT = 35

	comment_split = comment.split('=', 1)
	if comment_split[0].strip().lower() == 'spoiler' and len(comment_split[1]) < FLAIR_ADDITION_MAX_LIMIT:
		return True
	return False

def edit_spoiler_flairs(reddit, posts):
	for submission in posts:
		for comment in submission.comments.list():
			if comment.is_submitter and is_set_spoiler_comment(comment.body):
				current_flair_id = submission.link_flair_template_id
				current_flair_text = submission.link_flair_text
				new_flair_text = current_flair_text + ' | ' + comment.body.split('=', 1)[1].strip()
				submission.flair.select(current_flair_id, new_flair_text)

def main():
	## Parse the command line arguments
	parser = argparse.ArgumentParser(description='Get inputs for building README Megathread section')
	parser.add_argument('site', help='The praw.ini site identifier')
	args = parser.parse_args()

	## Initialize PRAW Reddit
	reddit = praw.Reddit(args.site)
	reddit.validate_on_submit = True

	print("[" + str(datetime.datetime.now()) + "] Bot is running...")
	print("[" + str(datetime.datetime.now()) + "] Updating Spoiler post flairs...")

	spoiler_posts = get_spoiler_posts(reddit)
	post_reminders(reddit, spoiler_posts)
	edit_spoiler_flairs(reddit, spoiler_posts)

	print("[" + str(datetime.datetime.now()) + "] Spoiler posts updated.")

if __name__ == '__main__':
	main()