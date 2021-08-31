'''
Generates a list of desired threads and megathreads automatically in a given comment.
Acts as a way to get around Reddit's only 2 pinned posts.

Usage:
  MegathreadPostUpdater.py [site] [flairs] [headers] [megathreads]

Arguments:
  site          The praw.ini site identifier
  flairs        Comma-separated list of flairs to make subsections for
  headers       Comma-separated list of header names for flair subsections
  megathreads   Semicolon-separated list of general megathread names

Author: Elaeagnifolia | /u/Elaeagnifolia
'''

import praw
import pprint
import datetime
import time
import prawcore
import argparse

### Formatting Helpers
def generate_link(text, link):
	return '[' + text + '](' + link + ')'

def generate_header_title(header, text):
	if header not in range (1,5):
		return

	header_markup = ''
	for i in range(header):
		header_markup = header_markup + '#'

	return header_markup + ' ' + text

### Post Checking Helpers
def is_active_post(submission, post_type):
	## Convert to array so that we can support multiple flair checks
	if not isinstance(post_type, list):
		post_type = [post_type]
		
	if ((submission.link_flair_text in post_type) and submission.locked == False):
		return True
	return False

def is_megathread(submission):
	if (submission.link_flair_text == 'Megathread'):
		return True
	return False

### Post Content Generation Helpers
def generate_section(posts, section_title):
	if len(posts) == 0:
		return ''

	post_content = generate_header_title(3, section_title) + '\n'
	for submission in posts:
		post_content = post_content + '* ' + generate_link(submission.title, submission.permalink) + '\n'
	return post_content

def get_recent_megathread_link(subreddit, title, posts):
	for submission in posts:
		if title in submission.title and submission.link_flair_text == 'Megathread':
			return 'https://www.reddit.com' + submission.permalink
	return 'https://www.reddit.com/r/' + subreddit + '/search/?q=' + title.replace(" ", "+") + '&sort=new&restrict_sr=on&t=all'

def generate_general_megathread_section(subreddit, megathreads, posts):
	general_megathread_post_content = generate_header_title(3, 'General Megathreads') + '\n'

	for megathread in megathreads:
		general_megathread_post_content = general_megathread_post_content + '* ' + generate_link(
			megathread,
			get_recent_megathread_link(subreddit, megathread, posts)
		) + '\n'

	return general_megathread_post_content

def generate_megathread_section(reddit, flair_subsections, subsection_headers, megathreads):
	## Initialize the dictionary that will track the various subsection posts
	## By default, there will always have a Megathread subsection.
	sorted_posts = {
		'Megathread': []
	}
	for subsection in flair_subsections:
		sorted_posts[subsection] = []

	## Get all the posts we'll be sorting through
	subreddit = reddit.config.custom['subreddit']
	posts = reddit.subreddit(subreddit).new(limit=int(reddit.config.custom['post_limit']))

	## Sort the posts based on flair
	for submission in posts:
		if (is_active_post(submission, flair_subsections)):
			sorted_posts[submission.link_flair_text].append(submission)
		if (is_megathread(submission)):
			sorted_posts['Megathread'].append(submission)

	## Generate the post content
	post_content = generate_header_title(1, 'Megathreads') + '\n'

	for index,subsection in enumerate(flair_subsections):
		post_content = post_content + generate_section(
			sorted_posts[subsection],
			subsection_headers[index]
		) + '\n\n'

	return post_content + generate_general_megathread_section(subreddit, megathreads, sorted_posts['Megathread'])

def main():
	## Parse the command line arguments
	parser = argparse.ArgumentParser(description='Get inputs for building README Megathread section')
	parser.add_argument('site', help='The praw.ini site identifier')
	parser.add_argument('flairs', help='Comma-separated list of flairs to make subsections for', default='')
	parser.add_argument('headers', help='Comma-separated list of header names for the flair subsections', default='')
	parser.add_argument('megathreads', help='Semicolon-separated list of general megathread names')
	args = parser.parse_args()

	flair_subsections = args.flairs.split(',')
	subsection_headers = args.headers.split(',')
	megathreads = args.megathreads.split(';')

	## Initialize PRAW Reddit
	reddit = praw.Reddit(args.site)
	reddit.validate_on_submit = True

	print("[" + str(datetime.datetime.now()) + "] Bot is running...")
	print("[" + str(datetime.datetime.now()) + "] Updating Megathread post...")

	# Generate and edit the Megathread post
	megathread_post = reddit.comment(id=reddit.config.custom['comment_id'])
	megathread_post.edit(
		generate_megathread_section(reddit, flair_subsections, subsection_headers, megathreads)
	)

	print("[" + str(datetime.datetime.now()) + "] Megathread post updated.")

if __name__ == '__main__':
	main()