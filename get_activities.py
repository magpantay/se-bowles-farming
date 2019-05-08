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
from dateutil import tz							# for getting timezone, to convert datetimes into different timezones (tz.gettz()) || Current call syntax: tz.gettz()

def main():
	fileOut = "things.csv"
	fileCSV = "bowles_farming_table.csv"
	timezone = tz.gettz("US/Pacific") # for timestamp conversion to US/Pacific time (as Agworld returns -6:00 timezone, but Bowles farms are in the US/Pacific timezone)

	counter = 1 # for counting pages/knowing which page to fetch from AgWorld, starting with page 1
	print ("Getting page {0} of data, please wait...".format(counter))
	response = web_get('https://us.agworld.co/user_api/v1/activities?api_token=wFdJRAHjwzylncYDdwrcKw&page[number]={0}&page[size]=100'.format(counter), headers={"Content-Type":"application/vnd.api+json", "Accept":"application/vnd.api+json"}) # gets 100 item chunks at a time
	each_result = json_parser(response.text)

	outfile = csv.writer(open(fileOut, "w"), delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL)
	#outCSV = open(fileCSV, "w")

	outfile.writerow(["Activity ID", "Activity Type [attrib]", "Task Name", "Due At", "Completed At", "Farm Name", "Field Name", "Field ID", "Job Status"]) # first row (header) of CSV file

	while len(each_result['data']) > 0: # what the following loop does is that while the length of result['data'] > 0, then keep fetching from agworld (because we need to continuously fetch 100 [the maximum allowed at a time, also hence why page[size]=100] at a time until each_result['data']'s length is 0 (aka is []))
		print ("Writing page {0} of data to '{1}', please wait...".format(counter, fileOut))
		for i in range(len(each_result['data'])): # inside the loop, we take the current chunk of agworld data and fetch the important bits and save it to a CSV file
			activity_id = each_result['data'][i]['id']
			activity_type_attrib = each_result['data'][i]['attributes']['activity_type']
			task_name = each_result['data'][i]['attributes']['title']
			due_at = "" # will hold (more readable version) of the due date than what AgWorld returns
			completed_at = "" # will hold (more readable version) of the completed time than what AgWorld returns
			status = "" # will hold complete-on-time/complete-late/incomplete-late/etc. based on time comparisons

			# if the thing is none, apparently it's type NoneType (not string like what I originally thought)
			# need .__name__ because that gets the name of type alone rather than < class 'TYPE' >
			if type(each_result['data'][i]['attributes']['due_at']).__name__ != "NoneType" and type(each_result['data'][i]['attributes']['completed_at']).__name__ != "NoneType": # if due date isn't none and completed at isn't none, then completed?? ||If there is a Due Date and a Complete Date, task_status = complete
				dtDueAt = date_parse(each_result['data'][i]['attributes']['due_at'])
				dtCompAt = date_parse(each_result['data'][i]['attributes']['completed_at'])
				dtDueAt = dtDueAt.astimezone(timezone)
				dtCompAt = dtCompAt.astimezone(timezone)

				status = "COMPLETE"
				if dtCompAt <= dtDueAt:
					status = status + "-ON-TIME"
				else:
					status = status + "-LATE"

				due_at = "{0:02}-{1:02}-{2:04} {3:02}:{4:02}:{5:02} US/Pac".format(dtDueAt.month, dtDueAt.day, dtDueAt.year, dtDueAt.hour, dtDueAt.minute, dtDueAt.second) # both due date and completed time as they exist, rewriting it to make it more user-readable in CSV file (and the resulting website)
				completed_at = "{0:02}-{1:02}-{2:04} {3:02}:{4:02}:{5:02} US/Pac".format(dtCompAt.month, dtCompAt.day, dtCompAt.year, dtCompAt.hour, dtCompAt.minute, dtCompAt.second)

			elif type(each_result['data'][i]['attributes']['due_at']).__name__ != "NoneType" and type(each_result['data'][i]['attributes']['completed_at']).__name__ == "NoneType": # if due isn't none but completed is then in progress || If there is a Due Date but NO Complete Date, task_status = in progress
				dtDueAt = date_parse(each_result['data'][i]['attributes']['due_at'])
				currentTime = datetime.now()
				dtDueAt = dtDueAt.astimezone(timezone)
				currentTime = currentTime.astimezone(timezone)

				status = "IN-PROGRESS"
				if currentTime <= dtDueAt:
					status = status + "-GOOD"
				else:
					status = status + "-LATE"

				due_at = "{0:02}-{1:02}-{2:04} {3:02}:{4:02}:{5:02} US/Pac".format(dtDueAt.month, dtDueAt.day, dtDueAt.year, dtDueAt.hour, dtDueAt.minute, dtDueAt.second) # only due because there's no completed time
				completed_at = "Task in progress"

			else: #else there isn't a due date set
				status = each_result['data'][i]['attributes']['job_status'].replace(" ", "-").upper() # makes the AgWorld data look like the format we have for job status by replacing spaces with - and making the entire string uppercase
				status = status + "-NO-DUE-DATE" # we fetch the status of the activity according to AgWorld, but also add that fact that there was no due date set, notifying that we can't tell if it's late or on-time
				due_at = "No due date set"

				if type(each_result['data'][i]['attributes']['completed_at']).__name__ != "NoneType": # however, if there was data on time it was completed
					dtCompAt = date_parse(each_result['data'][i]['attributes']['completed_at'])
					dtCompAt = dtCompAt.astimezone(timezone)
					completed_at = "{0:02}-{1:02}-{2:04} {3:02}:{4:02}:{5:02} US/Pac".format(dtCompAt.month, dtCompAt.day, dtCompAt.year, dtCompAt.hour, dtCompAt.minute, dtCompAt.second) # then save that completed time

			for j in range(len(each_result['data'][i]['attributes']['activity_fields'])): # because apparantly a single assignment can involve multiple fields/farms
				farm_name = each_result['data'][i]['attributes']['activity_fields'][j]['farm_name']
				field_name = each_result['data'][i]['attributes']['activity_fields'][j]['field_name']
				field_id = each_result['data'][i]['attributes']['activity_fields'][j]['field_id']

				outfile.writerow([activity_id, activity_type_attrib, task_name, due_at, completed_at, farm_name, field_name, field_id, status])
				# this will write a row for each farm name as some tasks involve multiple farms (and it seemed easier to do this for easier CSV file parsing)
				# it works out since we would already have all of the other things to write to the CSV file

		print ("Wrote page {0} to '{1}'".format(counter, fileOut))
		counter = counter + 1	# to get the next 100 or so tasks
		print("Getting page {0} of data, please wait...".format(counter))
		response = web_get('https://us.agworld.co/user_api/v1/activities?api_token=wFdJRAHjwzylncYDdwrcKw&page[number]={0}&page[size]=100'.format(counter), headers={"Content-Type":"application/vnd.api+json", "Accept":"application/vnd.api+json"})
		each_result = json_parser(response.text)
	print("Page {0} of data didn't have anything. Everything has been written to '{1}'".format(counter, fileOut))

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
