# python tool to Generate sample log file of 1000000 random lines, with the following format:
# date time source-ip dest-ip port protocol username action
# and with some constraints on each column in this log file.

# @author Rehab Abdel Wahab Ahmed
# @date: Nov. 16, 2019

#this line to import division library updates from python 3 as i use python 2
#if u use python 3, you can remove it 
from __future__ import division
from array import *
from random import randrange
from datetime import datetime
from datetime import time
from faker import Faker
import datetime
import numpy
import random
import string
import argparse
import math

class generator(object):
	#read from user n parameter represent the number of lines it will generate 
	#it helps to generate less than 1000000 line for test
	parser = argparse.ArgumentParser(__file__, description="Log Generator")
	parser.add_argument("--num", "-n", dest='num_lines', help="Number of lines to generate (0 for infinite)", type=int, default=1)
	args = parser.parse_args()
	linesCount = args.num_lines

	#to use faker library which helps in generating random data in any data type formate
	faker = Faker()

	#create and open a .txt file to write the generated logs in it 
	outFileName = 'generated_logs.txt'
	f = open(outFileName,'w')

	#generate random 500 username, apply the required useres count limit constraints 
	users = []
	for x in range(0, 4):
	#assume username length is 8 digits limit
	#apply the constraints that username is a alphanumeric word doesn't start with a digits
	#generate one single char in a lowercase from a-z 
		username = ''.join(random.choice(string.ascii_lowercase) for _ in range(1)) 
	#concatenate the first char to an other 7 random alphanumeric word	
		username += ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(7))  
		users.append(username)

	#generate random sourceIps, apply the required source ips count limit constraints 
	sourceIps = []
	for x in range(0, 3):
		sourceIp = faker.ipv4()
		sourceIps.append(sourceIp)

	Dict1 = {}
		
	#generate array with length of 70% of the whole lines number contains requests happens between 9:00 AM and  06:00 PM  	
	#get 70% of the total number of generated lines 
	requestsCount = linesCount * 0.7
	newrequestsCountInDay = math.floor(requestsCount)
	#array has random times in day 
	requestsInDay = []
	for x in range(0, int(newrequestsCountInDay)-1):
	#generate random time between 9:00 AM and  6:00 PM  which means (from 9:00 to 5:59) which is (9 ->17)
		requestInDay = datetime.time(faker.random_int(9,17), faker.random_int(0,59),faker.random_int(0,59))
		requestsInDay.append(requestInDay)

	#generate array with length of 30% of the whole lines number contains requests happens in the rest of the day from 1:00 AM to 9:00 AM	
	#get 30% of the total number of generated lines 
	requestsCount = linesCount * 0.3
	newrequestsCountNotInDay = math.floor(requestsCount)
	#array has random times not in day
	requestsNotInDay = []
	for x in range(0, int(newrequestsCountNotInDay)-1):
	#generate random time between 1:00 AM and  9:00 AM  which means (from 1:00 to 8:59)  
		requestNotInDay = datetime.time(faker.random_int(1,8), faker.random_int(0,59),faker.random_int(0,59))
		requestsNotInDay.append(requestNotInDay)

	#fixed values arrays for protocols and actions 
	protocol = ["TCP","UDP"]
	action = ["Allow", "Deny", "Bypass", "Log-only"]

	#calculate action probabilities regards to the constraints
	flag = True
	while(flag):	
	#Less than 50% of the entries should be Allow
		allowProp = faker.random_int(1, 49) / 100
	#Less than 10% of the traffic should be Deny
		denyProp = faker.random_int(1, 9) / 100
	#At least 15% of the entries should be Bypass
		bypassProp = faker.random_int(15, 100) / 100
	#and the rest of 100% is for the 4th type log only which is  = 1 (sum of all probabilities) - [sum of 3 probabilities]
		if((allowProp + denyProp + bypassProp) < 1):
			logonlyProp = 1 - (allowProp + denyProp + bypassProp)
			flag = False
		else:
			flag = True

	#matrix initialized with strings contains zeros
	usersIpsDictionary = []
	for j in range(500):
			column = []
			for i in range(3):
				column.append("0")
			usersIpsDictionary.append(column)



#########################################################################################
								#start log lines generation
#########################################################################################

	flag = True
	# var represents number of lines (counter)
	linesIndex = 0
	while (flag):
	#generate random dates with the constraint that log covers the duration between 2019-10-20 and 2019-10-30  
		date = datetime.date(faker.random_int(2019,2019), faker.random_int(10,10),faker.random_int(20,30))
	#choose random source ip from the array we generated it before having 650 ips	
		sourceIp = numpy.random.choice(sourceIps)
	#generate random destenation ip 	
		destIp = faker.ipv4()
	#assume the port numbers range from 1025 to 65535	
		port = faker.random_int(1025, 65535)
	#choose randomly the protocol from the fixed array above ["TCP","UDP"]
		protocolProp = numpy.random.choice(protocol)
	#choose one username from the array generated before	
		username = numpy.random.choice(users)
	#choose the action from the fixed array action depends on the probabilities generated before 
	#["Allow" => "Less than 50%" , "Deny" => "Less than 10%", "Bypass" => "At least 15%", "Log-only" => "the rest"]
		actionProp = numpy.random.choice(action,p=[allowProp, denyProp, bypassProp, logonlyProp])
	#applying the constraint that 70% of the requests happen during the day (between 09:00-18:00)	
		linesIndex += 1
		if(linesIndex <= newrequestsCountInDay):
	#fill the first 70% line with a time from the array newrequestsCountInDay having times (between 09:00-18:00)
			time = numpy.random.choice(requestsInDay)
		else:
	#then the rest 30% take times from the other array	requestsNotInDay having times (between 01:00-09:00)
			time = numpy.random.choice(requestsNotInDay)
		
		# apply constraint that user can't have more than 2 distinct source ip
		# create matrix act as a dictionary for user and its source ips
		#check if the user has one ip, give him the other new one, else give him one of the existing 2

###########################################################################3		
#optimization for adding 2 distinct source ips for each user to enhance the complexty.
		# userSourceIps=[]
		# currentUserIps=[]
		# if username in Dict1.keys():
			# print (username)
			# currentUserIps = Dict1[username]
			# if sourceIp in currentUserIps:
				# break
			# else:
				# if(len(currentUserIps)==1):
					# currentUserIps.append(sourceIp)
					# Dict1[username] = currentUserIps
				# else:
					# sourceIp = currentUserIps[0]
			
		# else:
			# userSourceIps.append(sourceIp)
			# Dict1[username]= userSourceIps
###########################################################################3		


		isNewUser = 0
		index = 0	
		for i in range(0, 499):
			if(usersIpsDictionary[i][0] == "0"):
				index = i
				break
			else:
				if(usersIpsDictionary[i][0] == username):
					isNewUser = 1
					if(usersIpsDictionary[i][1] == sourceIp or usersIpsDictionary[i][2] == sourceIp):
						break
					else:
						if(usersIpsDictionary[i][2] == "0" and usersIpsDictionary[i][1] != "0"):
							usersIpsDictionary[i][2]= sourceIp
							break
						else:
							sourceIp = usersIpsDictionary[i][1]
				

		if(isNewUser == 0):	
			usersIpsDictionary[index][0]= username
			usersIpsDictionary[index][1]= sourceIp

	#write in the generated_logs.txt file in the formate 
	# date time source-ip dest-ip port protocol username action

		f.write('%s %s %s %s %s %s %s %s\n' % (date, time, sourceIp, destIp, port, protocolProp, username, actionProp))
		f.flush()

		linesCount = linesCount - 1
		flag = False if linesCount == 0 else True
		
