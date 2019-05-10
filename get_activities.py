# Prereq: Python 3 (sudo apt install python3)
#		  Python3-pip (sudo apt install python3-pip)
# 		  Python3 requests (sudo pip3 install requests)
#		  Python3 dateutil (sudo pip3 install python-dateutil)
#		  Python3 datetime (sudo pip3 install datetime)

from requests import get as web_get 			#requests.get(), for CURL requests || Current call syntax: web_get()
from json import loads as json_parser 			#json.loads(), for parsing CURL response || Current call syntax: json_parser()
from dateutil.parser import parse as date_parse # dateutil.parser.parse(), for converting str from AgWorld to date objects || Current call syntax: date_parse()
from datetime import datetime					# for getting current system time (datetime.datetime.now()), also needed for time comparison and astimezone (tz conversion for mismatched tz timestamps) || Current call syntax: datetime.now(), obj.astimezone()
import csv										# for the creation of fileOut CSV file and editing of fileCSV CSV file. || Current call syntax:
from dateutil import tz							# for getting system timezone, other specific timezones, in order to convert datetimes into different timezones for astimezone() || Current call syntax: tz.gettz(), tz.tzlocal()


def main():
	# ---- THESE ARE THE ONLY VARIABLE VALUES ANY USER REALLY NEEDS TO CHANGE, EVERYTHING ELSE IS HANDLED WITH THIS INFORMATION AND DOESN'T NEED TO BE TOUCHED ---- #
	fileOut = "things.csv"
	fileCSV = "geoms.csv"
	timezone = tz.gettz("US/Pacific") # for timestamp conversion to US/Pacific time (as Agworld returns -6:00 timezone, but Bowles farms are in the US/Pacific timezone)
	apiKey = "wFdJRAHjwzylncYDdwrcKw"
	# ---- END ---- #

	counter = 1 # for counting pages/knowing which page to fetch from AgWorld, starting with page 1
	print ("Getting page {0} of data, please wait...".format(counter))
	response = web_get('https://us.agworld.co/user_api/v1/activities?api_token={0}&page[number]={1}&page[size]=100'.format(apiKey, counter), headers={"Content-Type":"application/vnd.api+json", "Accept":"application/vnd.api+json"}) # gets 100 item chunks at a time
	each_result = json_parser(response.text)

	fileOut_open = open(fileOut, "w") # need to specify a variable to open a file (rather than it being inline with csv.writer) in order to properly close the file when finished with the program, as csv.writer has no close() function
	outfile = csv.writer(fileOut_open, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL)
	#outCSV = open(fileCSV, "w")

	# note: forcing everything that is a known string to encode as utf-8 as Python fallsback to ASCII which is limited to 127 characters and causes the error: UnicodeEncodeError: 'ascii' codec can't encode character u'\u201c' in position 28: ordinal not in range(128)
	# doing this will resolve the error and (theoretically) prevent it from happening ever again
	outfile.writerow(["Activity ID".encode("utf-8"), "Task Name".encode("utf-8"), "Due At".encode("utf-8"), "Completed At".encode("utf-8"), "Farm Name".encode("utf-8"), "Field Name".encode("utf-8"), "Field ID".encode("utf-8"), "Job Status".encode("utf-8")]) # first row (header) of CSV file

	while len(each_result['data']) > 0: # what the following loop does is that while the length of result['data'] > 0, then keep fetching from agworld (because we need to continuously fetch 100 [the maximum allowed at a time, also hence why page[size]=100] at a time until each_result['data']'s length is 0 (aka is []))
		print ("Writing page {0} of data to '{1}', please wait...".format(counter, fileOut))
		for i in range(len(each_result['data'])): # inside the loop, we take the current chunk of agworld data and fetch the important bits and save it to a CSV file
			activity_id = each_result['data'][i]['id']
			task_name = each_result['data'][i]['attributes']['title'].encode("utf-8") # from tracebacks, this was apparently the problem variable that caused that encode error
			due_at = "" # will hold (more readable version) of the due date than what AgWorld returns
			completed_at = "" # will hold (more readable version) of the completed time than what AgWorld returns
			status = "" # will hold complete-on-time/complete-late/incomplete-late/etc. based on time comparisons

			# if the thing is none, apparently it's type NoneType (not string like what I originally thought)
			# need .__name__ because that gets the name of type alone rather than < class 'TYPE' >
			if type(each_result['data'][i]['attributes']['due_at']).__name__ != "NoneType" and type(each_result['data'][i]['attributes']['completed_at']).__name__ != "NoneType": # if due date isn't none and completed at isn't none, then completed?? ||If there is a Due Date and a Complete Date, task_status = complete
				dtDueAt = date_parse(each_result['data'][i]['attributes']['due_at']).astimezone(timezone)
				dtCompAt = date_parse(each_result['data'][i]['attributes']['completed_at']).astimezone(timezone) 

				status = "COMPLETE"
				if dtCompAt <= dtDueAt:
					status = status + "-ON-TIME"
				else:
					status = status + "-LATE"

				due_at = dtDueAt.strftime("%b-%d-%Y %H:%M:%S") # both due date and completed time as they exist, rewriting it to make it more user-readable in CSV file (and the resulting website)
				due_at = due_at + " US/Pac"
				completed_at = dtCompAt.strftime("%b-%d-%Y %H:%M:%S")
				completed_at = completed_at + " US/Pac"

			elif type(each_result['data'][i]['attributes']['due_at']).__name__ != "NoneType" and type(each_result['data'][i]['attributes']['completed_at']).__name__ == "NoneType": # if due isn't none but completed is then in progress || If there is a Due Date but NO Complete Date, task_status = in progress
				dtDueAt = date_parse(each_result['data'][i]['attributes']['due_at']).astimezone(timezone)
				currentTime = datetime.now(tz.tzlocal()).astimezone(timezone) # gets system time with system timezone then converts it to specified timezone

				status = "IN-PROGRESS"
				if currentTime <= dtDueAt:
					status = status + "-GOOD"
				else:
					status = status + "-LATE"

				due_at = dtDueAt.strftime("%b-%d-%Y %H:%M:%S") # only due because there's no completed time
				due_at = due_at + " US/Pac"
				completed_at = "Task in progress"

			else: #else there isn't a due date set
				status = each_result['data'][i]['attributes']['job_status'].replace(" ", "-").upper() # makes the AgWorld data look like the format we have for job status by replacing spaces with - and making the entire string uppercase
				status = status + "-NO-DUE-DATE" # we fetch the status of the activity according to AgWorld, but also add that fact that there was no due date set, notifying that we can't tell if it's late or on-time
				due_at = "No due date set"

				if type(each_result['data'][i]['attributes']['completed_at']).__name__ != "NoneType": # however, if there was data on time it was completed
					dtCompAt = date_parse(each_result['data'][i]['attributes']['completed_at']).astimezone(timezone)

					completed_at = dtCompAt.strftime("%b-%d-%Y %H:%M:%S") # then save that completed time
					completed_at = completed_at + " US/Pac"
					
			for j in range(len(each_result['data'][i]['attributes']['activity_fields'])): # because apparantly a single assignment can involve multiple fields/farms
				farm_name = each_result['data'][i]['attributes']['activity_fields'][j]['farm_name'].encode("utf-8")
				field_name = each_result['data'][i]['attributes']['activity_fields'][j]['field_name'].encode("utf-8")
				field_id = each_result['data'][i]['attributes']['activity_fields'][j]['field_id']

				outfile.writerow([activity_id, task_name, due_at.encode("utf-8"), completed_at.encode("utf-8"), farm_name, field_name, field_id, status.encode("utf-8")])
				# this will write a row for each farm name as some tasks involve multiple farms (and it seemed easier to do this for easier CSV file parsing)
				# it works out since we would already have all of the other things to write to the CSV file

		print ("Wrote page {0} to '{1}'".format(counter, fileOut))
		counter = counter + 1	# to get the next 100 or so tasks
		print("Getting page {0} of data, please wait...".format(counter))
		response = web_get('https://us.agworld.co/user_api/v1/activities?api_token={0}&page[number]={1}&page[size]=100'.format(apiKey, counter), headers={"Content-Type":"application/vnd.api+json", "Accept":"application/vnd.api+json"})
		each_result = json_parser(response.text)
	print("Page {0} of data didn't have anything. Everything has been written to '{1}'".format(counter, fileOut))
	fileOut_open.close()
if __name__ == "__main__":
	main()

# ---- CODE GRAVEYARD ---- #
			#-------------------------------------------------------------------------------------------------------
			# the list of things that we've tried that some things in the JSON file have, but not all (as in, exists in some not in all. It's lack of existence breaks this program though)
			#outfile.write("Activity ID [job_activities]: {0}\n".format(each_result['data'][i]['attributes']['job_activities']['activity_id']))
			#outfile.write("Activity Type [job_activities]: {0}\n".format(each_result['data'][i]['attributes']['job_activities']['activity_type']))
			#Type of Category
			#outfile.write("Activity ID: {0}\n".format(each_result['data'][i]['activity_category']))
			#------Unsure on these
			#Who ordered the ActivJob Status: tity (author)
			#outfile.write("Author User Name: {0}\n".format(each_result['data'][i]['attributes']['job_activities']['author_user_name']))
			#outfile.write ("Operator Name: {0}\n".format(each_result['data'][i]['attributes']['operator_users'][0]['name']))
			#-------------------------------------------------------------------------------------------------------
# ---- END GRAVEYARD ---- #
