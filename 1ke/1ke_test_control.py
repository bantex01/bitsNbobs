#!/usr/bin/python

import os
import re
import sys
import json
import time
import base64
import urllib2
import urllib
from collections import defaultdict

def gather_tests(test_type):

	print "In gather test with test type of "+str(test_type)
	url=baseurl + str(test_type) + ".json"
	print "so url is "+str(url)

	# build request
	request = urllib2.Request(url)
	request.add_header("Content-Type",'application/json')
	request.add_header("Accept",'application/json')
	request.add_header("Authorization", "Basic %s" % base64string)
	response = urllib2.urlopen(request)
	print "response is "+str(response)
	for msg in response:
		#body_json = json.loads(msg.body)
		print msg
		test_json = json.loads(msg)
		for test in test_json['test']:
			print "test is \n"+str(test)
			
			print "found test for "+str(test['testName'])
			TEST_DICT[test['url']]["test_id"]=test['testId']
      
      
def read_urls(input_file):

	print "in read urls"
	input_file = open(input_file, 'r')

	for line in input_file:
		print "line is "+str(line)
		splitter=line.split(",")
		file_url=splitter[1].rstrip()
		print "file url is "+str(file_url)
		file_url="https://"+file_url
		stack=splitter[0].rstrip()

		# Let's add the whitelist check here

		whitelist_array = [whiteline.rstrip('\n') for whiteline in open("whitelist.csv")]
		print "Checking to see if "+str(stack) + " is in whitelist"

		if (stack in whitelist_array):
			print "stack "+str(stack) + " found in whitelist, moving on"
			continue
		else:
			print "stack "+str(stack) + " not found in whitelist"

		# let's check to see if test exists

		if (file_url in TEST_DICT.keys()):
			print "test exists for "+str(file_url) + " test id is "+str(TEST_DICT[file_url]['test_id'])

			# modes are either "all" or "update" - all will delete tests and recreate, update will just create new tests found

			if (mode != "update"):
				print "mode is not update so we need to delete and recreate"
				# we need to delete the test and recreate
				delete_test(file_url)
				print "back from delete test for "+str(file_url)
				stack, sh_type = create_test_details(line)
				print "returned from create_test_details " +str(stack) +str(sh_type) +str(file_url)
				create_test(stack, sh_type, file_url)

			else:
				# we need to just move on, test found and we're just updating with new tests this run
				print "test found and we're not updating, so moving on"
				continue

		else:
			print "cant find existing test for "+str(file_url) + " , we need to create"
			stack, sh_type = create_test_details(line)
			create_test(stack, sh_type, file_url)


def delete_test(file_url):

	print "In delete test, been passed "+str(file_url)
	# let's get test_id
	test_id = TEST_DICT[file_url]['test_id']
	print "got test_id of "+str(test_id)
	
	deleteurl=baseurl +str(testType) +"/" +str(test_id) +"/delete.json"
	print "delete url is "+str(deleteurl)
	body={}
	request = urllib2.Request(deleteurl, data=json.dumps(body))
	request.add_header("Content-Type",'application/json')
	request.add_header("Authorization", "Basic %s" % base64string)
	response = urllib2.urlopen(request)
	print "response is "+str(response)


def create_test_details(line):

	print "In create test details"		

	print "line is "+str(line)
	splitter=line.split(",")
	file_url=splitter[1].rstrip()

	stack=splitter[0].rstrip()
	type_attr=file_url.split(".")
	sh_type=type_attr[0]

	if sh_type == stack:
		print "this is a normal url " +str(file_url)
		sh_type="standard"
	else:
		print "this is a proper sh type "+str(file_url)
		splitter=sh_type.split("-")
		sh_type=splitter[0]

	return(stack,sh_type)


def create_test(stack,sh_type,url):

	print "In create test with url "+str(url) + " and stack of " +str(stack)
	#testType="http-server"
	# http-server test

	if ".lol" in url or ".stg" in url:
		verifyCertificate=0
	else:
		verifyCertificate=1
	
	loginurl=url
	testName="stack=" + stack + " id=" + sh_type + " metric=web_check testname=web_check~"+str(url) 
	print "testname is "+str(testName) 

	body={ "interval": 60,
		"agents": [
		{"agentId": agentId}
		],
		"testName": testName,
        "contentRegex": "some string",
	    "url": loginurl,
	    "alertsEnabled": 0,
		"bgpMeasurements": 0,
		"networkMeasurements": 0,
	    "verifyCertificate": verifyCertificate
	}

	print "test type is "+str(testType)
	print "body is "+ str(body)

    # build request
	createurl=baseurl+testType+"/new.json"
	request = urllib2.Request(createurl, data=json.dumps(body))
	request.add_header("Content-Type",'application/json')
	request.add_header("Accept",'application/json')
	request.add_header("Authorization", "Basic %s" % base64string)
	response = urllib2.urlopen(request)
	print "response is "+str(response)
 

def process_args():

	if (len(sys.argv) != 3):
		print "Script requires two arguments - input file and mode (all or update)"
		sys.exit(2)
	else:
		global input_file, mode
		input_file = sys.argv[1]
		mode = sys.argv[2]
		if (mode == "all"):
			string = " - tests will be deleted and recreated"
		else:
			if (mode == "update"):
				string = " - only new tests will be created, existing tests will be left"
			else:
				print "Unknown mode found "+str(mode) + " - accepted modes are all or update - exiting"
				sys.exit(2)

		print "Input file is "+str(input_file) + " - mode is "+str(mode) + " " +str(string)


##############################################################################################
# Main Body
##############################################################################################


base64string = base64.b64encode('%s:%s' % ("1ke_user", "1ke_token"))
baseurl="https://api.thousandeyes.com/v6/tests/"
agentId="14410"
testType="http-server"
TEST_DICT = defaultdict(dict)

process_args()
gather_tests("http-server")

#for key in TEST_DICT:
#	print "test is "+str(key) + " and attributes are " +str(TEST_DICT[key])

read_urls(input_file)
