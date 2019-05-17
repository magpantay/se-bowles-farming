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
	geomsCSVfilename = "geoms.csv"
	timezone = tz.gettz("US/Pacific") # for timestamp conversion to US/Pacific time (as Agworld returns -6:00 timezone, but Bowles farms are in the US/Pacific timezone)
	apiKey = "wFdJRAHjwzylncYDdwrcKw"
	# ---- END ---- #

	counter = 1 # for counting pages/knowing which page to fetch from AgWorld, starting with page 1
	print ("Getting page {0} of data, please wait...".format(counter))
	response = web_get('https://us.agworld.co/user_api/v1/activities?api_token={0}&page[number]={1}&page[size]=100'.format(apiKey, counter), headers={"Content-Type":"application/vnd.api+json", "Accept":"application/vnd.api+json"}) # gets 100 item chunks at a time
	each_result = json_parser(response.text)

	fileOut_open = open(fileOut, "w") # need to specify a variable to open a file (rather than it being inline with csv.writer) in order to properly close the file when finished with the program, as csv.writer has no close() function
	outfile = csv.writer(fileOut_open, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL)

	fields_in_progress_good = [] # list of all fields with in-progress tasks that are good (or have no due date)
	fields_in_progress_late = [] # list of all fields with in-progress tasks that are late
	# for the rest of the fields, we can assume they're complete since we got all of the in-progress possibilities

	# note: forcing everything that is a known string to encode (then decode) as utf-8 as Python fallsback to ASCII which is limited to 127 characters and causes the error: UnicodeEncodeError: 'ascii' codec can't encode character u'\u201c' in position 28: ordinal not in range(128)
	# doing this will resolve the error and (theoretically) prevent it from happening ever again
	outfile.writerow(["Activity ID", "Task Name", "Due At", "Completed At", "Farm Name", "Field Name", "Field ID", "Job Status", "Author Name"]) # first row (header) of CSV file

	while len(each_result['data']) > 0: # what the following loop does is that while the length of result['data'] > 0, then keep fetching from agworld (because we need to continuously fetch 100 [the maximum allowed at a time, also hence why page[size]=100] at a time until each_result['data']'s length is 0 (aka is []))
		print ("Writing page {0} of data to '{1}', please wait...".format(counter, fileOut))
		for i in range(len(each_result['data'])): # inside the loop, we take the current chunk of agworld data and fetch the important bits and save it to a CSV file
			activity_id = each_result['data'][i]['id']
			task_name = each_result['data'][i]['attributes']['title'].encode("utf-8").decode("utf-8") # from tracebacks, this was apparently the problem variable that caused that encode error
			due_at = "" # will hold (more readable version) of the due date than what AgWorld returns
			completed_at = "" # will hold (more readable version) of the completed time than what AgWorld returns
			status = "" # will hold complete-on-time/complete-late/incomplete-late/etc. based on time comparisons
			author_name = each_result['data'][i]['attributes']['author_user_name'].encode("utf-8").decode("utf-8")


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
				farm_name = each_result['data'][i]['attributes']['activity_fields'][j]['farm_name']
				field_name = each_result['data'][i]['attributes']['activity_fields'][j]['field_name']
				field_id = each_result['data'][i]['attributes']['activity_fields'][j]['field_id']

				outfile.writerow([activity_id, task_name, due_at, completed_at, farm_name, field_name, field_id, status, author_name])
				# this will write a row for each farm name as some tasks involve multiple farms (and it seemed easier to do this for easier CSV file parsing)
				# it works out since we would already have all of the other things to write to the CSV file
				if status == "IN-PROGRESS-GOOD" or status == "IN-PROGRESS-NO-DUE-DATE":
					fields_in_progress_good.append("{0}||{1}".format(farm_name, field_name))
				elif status == "IN-PROGRESS-LATE":
					fields_in_progress_late.append("{0}||{1}".format(farm_name, field_name))

		print("Wrote page {0} to '{1}'".format(counter, fileOut))
		counter = counter + 1	# to get the next 100 or so tasks
		print("Getting page {0} of data, please wait...".format(counter))
		response = web_get('https://us.agworld.co/user_api/v1/activities?api_token={0}&page[number]={1}&page[size]=100'.format(apiKey, counter), headers={"Content-Type":"application/vnd.api+json", "Accept":"application/vnd.api+json"})
		each_result = json_parser(response.text)
	print("Page {0} of data didn't have anything. Everything has been written to '{1}'".format(counter, fileOut))
	fileOut_open.close()

	# I was keeping track of the fields that are in progress to change the color of those specific fields in the map
	# every other field not in any of these arrays are assumed complete and will be color green
	fields_in_progress_good = set(fields_in_progress_good) # makes all of the values unique, removes duplicates
	fields_in_progress_late = set(fields_in_progress_late)

	print("Changing {0}, please wait...".format(geomsCSVfilename))

	geomsCSVfileread = open(geomsCSVfilename, "r")
	geomsCSVread = csv.reader(geomsCSVfileread, delimiter=",")
	geoms_csv_contents = list(geomsCSVread)
	geomsCSVfileread.close()

	geomsCSVfilewrite = open(geomsCSVfilename, "w")
	geomsCSVwrite = csv.writer(geomsCSVfilewrite, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL)

	for i in range(1, len(geoms_csv_contents)): # start at 1, set all to green first
		geoms_csv_contents[i][4] = "#00FF00"
		geoms_csv_contents[i][7] = "#00FF00"

	for i in range(1, len(geoms_csv_contents)):
		for good_field_names in fields_in_progress_good:
			if good_field_names.split("||")[1].find("Block") == -1: # split with || because that's the format I chose for writing the strings to the array
				if good_field_names.split("||")[0] == geoms_csv_contents[i][1] and good_field_names.split("||")[1].split(" #")[0] == geoms_csv_contents[i][2]: # if the farm name and field name maatch the farm name, field name of the csv file, for the # split, it is because the geoms file and AgWorld's field name are slightly different in format (example: Agworld: Lone Tree T-10 #02 vs. geoms: Lone Tree T-10)
					geoms_csv_contents[i][4] = "#D7DF01" # change the value of stroke to dark yellow
					geoms_csv_contents[i][7] = "#D7DF01" # change the value of fill to dark yellow
			else: # for some oddd reason, except for fields that have the word 'Block' in them, those are the same across the both files
				if good_field_names.split("||")[0] == geoms_csv_contents[i][1] and good_field_names.split("||")[1] == geoms_csv_contents[i][2]:
					geoms_csv_contents[i][4] = "#D7DF01" # change the value of stroke to dark yellow
					geoms_csv_contents[i][7] = "#D7DF01" # change the value of fill to dark yellow
		for late_field_names in fields_in_progress_late:
			if late_field_names.split("||")[1].find("Block") == -1:
				if late_field_names.split("||")[0] == geoms_csv_contents[i][1] and late_field_names.split("||")[1].split(" #")[0] == geoms_csv_contents[i][2]: # if the farm name and field name maatch the farm name, field name of the csv file, for the # split, it is because the geoms file and AgWorld's field name are slightly different in format (example: Agworld: Lone Tree T-10 #02 vs. geoms: Lone Tree T-10)
					geoms_csv_contents[i][4] = "#FF0000" # change the value of stroke to red
					geoms_csv_contents[i][7] = "#FF0000" # change the value of fill to red
			else: # for some oddd reason, except for fields that have the word 'Block' in them, those are the same across the both files
				if late_field_names.split("||")[0] == geoms_csv_contents[i][1] and late_field_names.split("||")[1] == geoms_csv_contents[i][2]:
					geoms_csv_contents[i][4] = "#FF0000" # change the value of stroke to red
					geoms_csv_contents[i][7] = "#FF0000" # change the value of fill to red

	for row in geoms_csv_contents: # time to write with the changed colors
		geomsCSVwrite.writerow(row)
	geomsCSVfilewrite.close()

if __name__ == "__main__":
	main()
