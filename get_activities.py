from requests import get as web_get 	#requests.get(), for CURL requests
from json import loads as json_parser 	#json.loads(), for parsing CURL response
import csv

def main():
	filename = "things.txt"

	counter = 1
	print ("Getting page {0} of data, please wait...".format(counter))
	response = web_get('https://us.agworld.co/user_api/v1/activities?api_token=wFdJRAHjwzylncYDdwrcKw&page[number]={0}&page[size]=100'.format(counter), headers={"Content-Type":"application/vnd.api+json", "Accept":"application/vnd.api+json"}) # gets 100 item chunks at a time
	each_result = json_parser(response.text)
	
	outfile = open(filename, "w")
	
	#what the following loop does is that while the length of result['data'] > 0, then keep fetching from agworld (because we need to continuously fetch 100 [the maximum allowed at a time, also hence why page[size]=100] at a time until each_result['data']'s length is 0 (aka is []))
	while len(each_result['data']) > 0:
		print ("Writing page {0} of data to '{1}', please wait...".format(counter, filename))
		for i in range(len(each_result['data'])): # inside the loop, we take the current chunk of agworld data and fetch the important bits and save it to a txt file (the filename above)
			outfile.write("Activity ID: {0}\n".format(each_result['data'][i]['id']))
			outfile.write("Task Name: {0}\n".format(each_result['data'][i]['attributes']['title']))
			#print ("Foreman: {0}\n".format(each_result['data'][i]['attributes']['operator_users'][0]['name']))
			for j in range(len(each_result['data'][i]['attributes']['activity_fields'])): # because apparantly a single assignment can involve multiple fields/farms
				outfile.write("Farm Name: {0}\n".format(each_result['data'][i]['attributes']['activity_fields'][j]['farm_name']))
				outfile.write("Field Number: {0}\n".format(each_result['data'][i]['attributes']['activity_fields'][j]['field_name']))
			outfile.write("Job Status: {0}\n".format(each_result['data'][i]['attributes']['job_status']))
			outfile.write("\n")
		print ("Wrote page {0} to '{1}'".format(counter, filename))
		counter = counter + 1	# to get the next 100 or so tasks
		print("Getting page {0} of data, please wait...".format(counter))
		response = web_get('https://us.agworld.co/user_api/v1/activities?api_token=wFdJRAHjwzylncYDdwrcKw&page[number]={0}&page[size]=100'.format(counter), headers={"Content-Type":"application/vnd.api+json", "Accept":"application/vnd.api+json"})
		each_result = json_parser(response.text)
	print("Page {0} of data didn't have anything. Everything has been written to '{1}'".format(counter, filename))
if __name__ == "__main__":
	main()