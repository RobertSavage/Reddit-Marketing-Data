import praw
import requests
import bs4
from prawcore.exceptions import Forbidden
from time import sleep
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import Counter
import commonwords as CW
import subred
import os
import datetime as dt

'''
what dos this need to do
-find people with a list of subreddits
-make it a unique list of people
-look up the people and pull their tweets and make a list of words from them
-make a list of 25 most used words 
'''

client_id = '#####'
client_secret = '#####'
username = '#####'
password = '#####'
user_agent = 'pulling_models_test'
reddit = praw.Reddit(client_id=client_id,client_secret=client_secret,username=username,password=password,user_agent=user_agent)
print('---SCRAPE START---')
print('TIME: ',dt.datetime.now())

def users(subredd):
	x = reddit.subreddit(subredd)
	y = x.new(limit=10000)
	users = []
	try:
		for post in y:
			#looks through post
			try:
				users.append(post.author)
				sleep(0.3)
			except:
				print(f'{subredd}bad g')
				sleep(5)
				continue
			#looks through comments
			for comment in post.comments:
				try:
					users.append(comment.author)
					sleep(0.3)
				except:
					print(f'{subredd}bad g')
					sleep(5)
					continue
		Text_file = open('users.txt','a', encoding='utf-8')
		for word in set(users):
			Text_file.write(str(word)+"\n")

		print('----------------------------------------')
		print(subredd,' TIME: ',  datetime.now())
		print('----------','DONE: ',subredd,'----------')
		sleep(20)
	except:	
		print(f'BIG BOI MESSED UP ALL DIS BITCH {subredd}')
		sleep(20)
		pass

def data(user):
	#for user in Text_file:
	try:
		wordlist = []
		for submission in reddit.redditor(user).submissions.top('all'):
			temp = submission.title
			temp.replace('! ', ' ')
			temp.replace(', ', ' ')
			temp.replace('. ', ' ')
			temp.replace(': ', ' ')
			temp.replace('; ', ' ')
			temp.replace('? ', ' ')
			temp.replace('( ', ' ')
			temp.replace(') ', ' ')
			temp.replace('[ ', ' ')
			temp.replace('] ', ' ')
			split = temp.split(' ')
			for i in split:
				wordlist.append(i.lower())
		for comment in reddit.redditor(user).comments.top('all'):
			com = str(comment.body)
			com1 = com.replace('!', ' ')
			com2 = com1.replace(',', ' ')
			com3 = com2.replace('.', ' ')
			com4 = com3.replace(':', ' ')
			com5 = com4.replace(';', ' ')
			com6 = com5.replace('?', ' ')
			com7 = com6.replace('(', ' ')
			com8 = com7.replace(')', ' ')
			com9 = com8.replace('[', ' ')
			com10 = com9.replace(']', ' ')
			com11 = com10.replace("'", '')
			com12 = com11.replace("’", '')
			split = com12.split(' ')
			for i in split:
				wordlist.append(i.lower())
		newlist = []

		for word in wordlist:
			try:
				if int(word) == True:
					pass
			except ValueError:
				if word+' ' not in CW.common_list and ',' not in word and '.' not in word and '/' not in word and '[' not in word and '-' not in word and '(' not in word and '"' not in word and ')' not in word and word != '' and '!' not in word and '?' not in word:
					newlist.append(word)

		most_common_words= [word for word, word_count in Counter(newlist).most_common(15)]
		#print(str(user)+', '+str(most_common_words)+"\n")
		Text_file = open('data.txt','a', encoding='utf-8')
		Text_file.write(str(most_common_words)+"\n")
		sleep(1)
	except:
		sleep(15)


#users('physics')
"""
subred = subred.sub
processes = []
with ThreadPoolExecutor(max_workers=50) as executor:
	for sub in subred:
		processes.append(executor.submit(users, sub))
"""
#for task in as_completed(processes):
#	print(task.result())
print('---ALL DONE WITH FINDING USERS---')

list_text = []
Text_file = open('users.txt','r', encoding='utf-8')
for i in Text_file:
	list_text.append(i)
processes = []
with ThreadPoolExecutor(max_workers=15) as executor:
	for user in list_text:
		executor.submit(data, user)

print('---ALL DONE WITH WORD SCRAPE---')
print('TIME: ',dt.datetime.now())