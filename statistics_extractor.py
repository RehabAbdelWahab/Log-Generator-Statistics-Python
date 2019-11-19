# python tool to extract some statistics from the generated_logs.txt file 
# and write the results to the statistics.txt file 

# @author Rehab Abdel Wahab Ahmed
# @date: Nov. 18, 2019

from __future__ import division
import numpy as numpy
from collections import OrderedDict
from collections import Counter
import pprint

class statisticsExtractor(object):

	filepath = 'generated_logs.txt'
	file = open(filepath,'r')

	#create dictionary to fill the top 10 allowed source ips, key: source ip , value: number or repeat
	Dict1 = {}
	#create dictionary2 to fill the top 10 denied usernames ips, key: username , value: number or repeat
	Dict2 = {}
	#create counter for the bypass TCP 
	counter=0
	#create dictionary3 to fill the top 5 services (ports), key: port , value: number or repeat
	Dict3 = {}
	#create dictionary4 to fill the top 5 dest ips for each user, key: user , value: array of dest ips
	Dict4 = {}

	linesCounter=0
	for line in file:
	#read all lines from the log file
		fields = line.split(" ")
	#for each line get every columb data and put it in a variable	 
		date = fields[0]
		time = fields[1]
		sourceIP = fields[2]
		destIP = fields[3]
		port = fields[4]
		protocol = fields[5]
		username = fields[6]
		action = fields[7]

	##################################################################################			

		if(action == "Allow\n"):
	#check if the action statues is allow
			if sourceIP in Dict1:
	#if the sourceip is in dictionary before increment the value
				Dict1[sourceIP] += 1
			else:
	#if not add the source ip to the dictionary		
				Dict1[sourceIP] = 1	
				
	##################################################################################			

		if(action == "Deny\n"):
	#check if the action statues is deny
			if username in Dict2:
	#if the username is in dictionary before increment the value
				Dict2[username] += 1
			else:
	#if not add the username to the dictionary		
				Dict2[username] = 1				
				
	#array to store each user destination ips		
		userDestIps=[]	
	#read the logs file again to start from its begining, to start from line 1	
		file2 = open(filepath,'r')
	#loop on each line and get the user ip 	
		for line in file2:
			fields2 = line.split(" ")
	#read the username and the destinatio ip		
			destIP2 = fields2[3]
			username2 = fields2[6]
	#check if the username is the current username i am holding it  
			if(username == username2):
	#so add the dest ip to the user array 		
				userDestIps.append(destIP2)
		file2.close()	
	#count how many each user use this dest ip	
		Counter(userDestIps)
		#print (Counter(userDestIps))
	#sort the array dessending to get the top 5 ips	
		userDestIpsSorted = sorted(Counter(userDestIps), key=Counter(userDestIps).get, reverse=True)
		top5UserDestIpsSorted = userDestIpsSorted[:5]
	#append the array of each user having his top 5 dest ips to the dict4	
		Dict4[username] =  top5UserDestIpsSorted
				
	##################################################################################						

		if(action == "Bypass\n" and protocol == "TCP"):
	#check if the action statues is Bypass and the protocol is TCP
			counter+=1		
			
		if port in Dict3:
	#if the port is in dictionary before increment the value
			Dict3[port] += 1
		else:
	#if not add the port to the dictionary		
			Dict3[port] = 1					
			
	##################################################################################					

		linesCounter+=1
	#end of loop
	file.close()		

	################################################################
	#Requirment 1
	################################################################

	#sort the dictionary values dessending and put the corresponding keys (source ips) in an array  	
	allowedSourceIps = sorted(Dict1, key=Dict1.get, reverse=True)
	#get the first 10 element from the array 
	top10AllowedSourceIps = allowedSourceIps[:10]
	#the top 10 Allowed Source Ips requirements No. 1  
	#print(top10AllowedSourceIps)
	#write results to the file
	outFileName = 'statistics.txt'
	f = open(outFileName,'w')
	f.write("Top 10 Allowed Source Ips:\n")
	f.write('%s \n\n' % (top10AllowedSourceIps))

	################################################################
	#Requirment 2
	################################################################

	#part A
	#sort the dictionary values dessending and put the corresponding keys (usernames) in an array  	
	deniedUsernames = sorted(Dict2, key=Dict2.get, reverse=True)
	#get the first 10 element from the array 
	top10deniedUsernames = deniedUsernames[:10]
	#the top 10 denied usenames requirements No. 2  
	#print(deniedUsernames)
	#write results to the file
	f.write("Top 10 Denied Usernames:\n")
	f.write('%s\n\n' % (top10deniedUsernames))

	#part B
	#pprint.pformat(Dict4)
	#write results to the file
	f.write("Top 5 destination IPs for each user:\n")
	f.write('%s\n\n' % (pprint.pformat(Dict4)))

	################################################################
	#Requirment 3
	################################################################

	#part A	
	percentage=(counter/linesCounter)*100
	#print(percentage)
	#write results to the file
	f.write("Percentage of Bypassed TCP services:\n")
	f.write('%s %s\n' % (percentage," %\n"))

	#part B
	#sort the dictionary values dessending and put the corresponding keys (ports) in an array  	
	ports = sorted(Dict3, key=Dict3.get, reverse=True)
	#get the first 5 element from the array 
	top5ports = ports[:5]
	#the top 5 ports
	#print(top5ports)
	#write results to the file
	f.write("Top 5 Services:\n")
	f.write('%s\n\n' % (top5ports))

	f.flush()
