'''
For a given post, users can specify flairs to generate subsections
with lists of submissions for the given flair.

By default, also generates a list of the given Megathreads with the
latest posts for that type of Megathread.

Usage:
  MegathreadPostUpdater.py [site]

Arguments:
  site          The praw.ini site identifier

Author: Elaeagnifolia | /u/Elaeagnifolia
'''

import praw
import datetime
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

def generate_megathread_section(reddit, subsection_flairs, subsection_headers, megathreads):
	## Initialize the dictionary that will track the various subsection posts
	## By default, there will always have a Megathread subsection.
	sorted_posts = {
		'Megathread': []
	}
	for flair in subsection_flairs:
		sorted_posts[flair] = []

	## Get all the posts we'll be sorting through
	subreddit = reddit.config.custom['subreddit']
	posts = reddit.subreddit(subreddit).new(limit=int(reddit.config.custom['post_limit']))

	## Sort the posts based on flair
	for submission in posts:
		if (is_active_post(submission, subsection_flairs)):
			sorted_posts[submission.link_flair_text].append(submission)
		if (is_megathread(submission)):
			sorted_posts['Megathread'].append(submission)

	## Generate the post content
	post_content = generate_header_title(1, 'Megathreads') + '\n'

	for index,subsection in enumerate(subsection_flairs):
		post_content = post_content + generate_section(
			sorted_posts[subsection],
			subsection_headers[index]
		) + '\n\n'

	return post_content + generate_general_megathread_section(subreddit, megathreads, sorted_posts['Megathread'])

def main():
	SUBSECTION_FLAIR_CONFIG_PREFIX = 'subsection_flair'
	SUBSECTION_HEADER_CONFIG_PREFIX = 'subsection_header'
	MEGATHREAD_CONFIG_PREFIX = 'megathread'

	## Parse the command line arguments
	parser = argparse.ArgumentParser(description='Get inputs for building README Megathread section')
	parser.add_argument('site', help='The praw.ini site identifier')
	args = parser.parse_args()

	## Initialize PRAW Reddit
	reddit = praw.Reddit(args.site)
	reddit.validate_on_submit = True

	## Parse the custom praw.ini configuration parameters
	subsection_flairs = []
	subsection_headers = []
	megathreads = []

	for setting in sorted(reddit.config.custom):
		if SUBSECTION_FLAIR_CONFIG_PREFIX == setting[:len(SUBSECTION_FLAIR_CONFIG_PREFIX)]:
			subsection_flairs.append(reddit.config.custom[setting])
		if SUBSECTION_HEADER_CONFIG_PREFIX == setting[:len(SUBSECTION_HEADER_CONFIG_PREFIX)]:
			subsection_headers.append(reddit.config.custom[setting])
		if MEGATHREAD_CONFIG_PREFIX == setting[:len(MEGATHREAD_CONFIG_PREFIX)]:
			megathreads.append(reddit.config.custom[setting])

	print("[" + str(datetime.datetime.now()) + "] Bot is running...")
	print("[" + str(datetime.datetime.now()) + "] Updating Megathread post...")

	# Generate and edit the Megathread post
	megathread_post = reddit.comment(id=reddit.config.custom['comment_id'])
	megathread_post.edit(
		generate_megathread_section(reddit, subsection_flairs, subsection_headers, megathreads)
	)

	print("[" + str(datetime.datetime.now()) + "] Megathread post updated.")

if __name__ == '__main__':
	main()
