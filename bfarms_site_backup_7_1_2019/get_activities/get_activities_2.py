import pandas as pand 			# for easy data reading and manipulation from CSV file input || Current call syntax: pand.read_csv()
from datetime import datetime	# for getting current system time (datetime.datetime.now()) || Current call syntax: datetime.now()
from dateutil import tz			# for getting system timezone, other specific timezones, in order to convert datetimes into different timezones for astimezone() || Current call syntax: tz.gettz(), tz.tzlocal()
import csv						# for the reading and editing of geoms CSV file

def main():
	# -- Things that can be changed by the user -- #
	user_report_id = 2598
	api_key = 'Z3p6D3a2rU7HeVp3XOZhKg'
	timezone = 'US/Pacific'
	geomsCSVfilename = 'farm_geoms_and_coloring.csv'
	# -- End -- #

	timezone = tz.gettz(timezone)
	currentTime = datetime.now(tz.tzlocal()).astimezone(timezone) # gets system time with system timezone then converts it to specified timezone

	print('Getting information from AgWorld, please wait...')
	try:
		df = pand.read_csv('https://us.agworld.co/user_reports/{0}/export.csv?api_token={1}'.format(user_report_id, api_key), sep=',', error_bad_lines=False, header=0, index_col=False, dtype='unicode') # gets CSV, pandas turns it into a dataframe
	except:
		print("An error occured: Couldn't fetch this file from the address given.")
		exit()
	print ('Done.')

	df = df[~df['Property'].str.contains('Demo')] # removes all tasks that have a proprty name containing 'Demo'/[[keeps all tasks that don't have a property name of 'Demo']]
	df = df.fillna('None Set') # fills all blanks of dataframe with 'None Set'
	df = df[(df['Date Due'].str.contains(str(currentTime.year))) | (df['Date Due'].str.contains(str(currentTime.year-1))) | (df['Date Due'].str.contains('None Set'))] # this keeps only tasks that are the current year or the year previous (must be converted to strings) or those without a due date, previously set to 'None Set'
	df = df[::-1] # reverses dataframe (as the jobs returned by AgWorld towards the bottom are the more recent)

	try:
		df.to_csv('all_activities.csv', index=False)
	except:
		print("An error occured: Couldn't save file with this file name. Maybe it's open in another process?")

	# -- Gets field and task status statistics -- #
	prop_list_with_status = (df['Property'] + ' ' + df['Paddock'] + '||' + df['Job Status']).value_counts().sort_index() # converts these three rows to a single series to count task statuses of the fields (with a || for easy splitting later), counts number of unique values and sort alphabetically for easier indexing later
	prop_list = (df['Property'] + ' ' + df['Paddock']).value_counts() # total amount of tasks of each field (used for percentage calculation later)

	df2 = pand.DataFrame()
	for i in range(len(prop_list_with_status)):
		percentage_value = prop_list_with_status[i] / prop_list[prop_list_with_status.keys()[i].split("||")[0]] * 100 # gives percentage of tasks in that field with that status / total amount of tasks in that field
		temp_dict = { 'Field Name': [prop_list_with_status.keys()[i].split("||")[0]], 'Task Status': [prop_list_with_status.keys()[i].split("||")[1]], '# Tasks With Status': [prop_list_with_status[i]], 'Percentage': ['{0}'.format(str(percentage_value)[:5])] } # to append this information to df2, needs to be in dictionary format, percentage is accirate to 5 digits
		df2 = df2.append(pand.DataFrame(data=temp_dict, columns=['Field Name', 'Task Status', '# Tasks With Status', 'Percentage']), ignore_index=True) # w/o specifying columns, will alphabetically sort column names, ignore_index prevents dataframe index from being maintained after appended to new dataframe

	print("Writing field statistics, please wait...")
	try:
		df2.to_csv('field_statistics.csv', index=False)
	except:
		print("An error occured: Couldn't save file with this file name. Maybe it's open in another process?")
	print("Done.")
	# -- End -- #

	# -- Change geom stroke colors -- #
	print("Changing geom CSV colors, please wait...")
	try:
		geoms_df = pand.read_csv(geomsCSVfilename, sep=',', error_bad_lines=False, header=0, index_col=False, dtype='unicode')
	except:
		print("An error occured: Couldn't find this file.")

	for i in range(len(geoms_df['stroke'])):
		geoms_df['stroke'][i] = '#00FF00' # change all stroke values to green first

	df3 = df2[(~df2['Task Status'].str.match('Complete')) & (~df2['Task Status'].str.contains('Discarded'))].reset_index() # removes all complete (doesn't remove 'Partially Complete') and discarded tasks, resets index to start from 0 again with new dataframe (use in dfs where rows were gotten from other dfs)
	for i in range(len(df3['Percentage'])): # using df3['Percentage'] because it takes less time since there's less items (already changed all stroke to green [complete] first, so this just changes things that need to be changed from green to yellow
		if float(df3['Percentage'][i]) >= 15.00:
			try:
				location_in_geoms_df = geoms_df['field_name'].where(geoms_df['field_name'] == df3['Field Name'][i]).dropna().keys()[0] # gets index of CSV file where the field name is
				geoms_df['stroke'][location_in_geoms_df] = '#D7DF01'
			except:
				continue
			#if df3['Task Status'][i] == 'In Progress':
			#	color = '#D7DF01' # change to dark yellow if in-progress, partially
			#elif df3['Task Status'][i] == 'To-Do':
			#	color = '#87CEFA' # change to blue if todo
			#elif df3['Task Status'][i] == 'Partially Complete':
			#	color = '#D7DF01' # change to dark yellow if partially complete (considering this to be a form of in-progress)
			#else:
			#	color = '#848484' # change to gray if nothing else

	#geoms_temp_df = pand.DataFrame() # to be appended to geoms_df, gives the task status breakdown (percentages)
	#for i in range(len(geoms_df['stroke'])): # need to preallocate dataframe with all 0.00, with the same amount of rows that geoms_df has
	#	temp_dict = { 'Complete': [0.00], 'To-Do': [0.00], 'In Progress': [0.00], 'Partially Complete': [0.00] }
	#	geoms_temp_df = geoms_temp_df.append(pand.DataFrame(data=temp_dict, columns=['Complete', 'To-Do', 'In Progress', 'Partially Complete']), ignore_index=True)

	#for i in range(len(geoms_df['stroke'])):
	#	try:
	#		location_in_df2 = df2['Field Name'].where(df2['Field Name'] == geoms_df['field_name'][i]).dropna().keys() # gets array of indices of where the field is (as each row is an individial task status for that field)
	#		for j in range(len(location_in_df2)):
	#			try:
	#				#print(df2['Field Name'][([location_in_df2][j])])
	#				print(geoms_df['field_name'].where(geoms_df['field_name'][i] == df2['Field Name'][ ([location_in_df2][j])]).dropna())
	#				location_in_geoms_df = geoms_df['field_name'].where(geoms_df['field_name'] == df2['Field Name'][ ([location_in_df2][j]) ]).dropna().keys()[0] # gets index of CSV file where the field name is, to write to geoms_temp_df (as merging them requires that the indices stay the same)
	#				print(location_in_geoms_df)
	#				geoms_temp_df[ df2 ['Task Status'] [([loction_in_df2][j])] ][location_in_geoms_df] = df2['Percentage'][ ([location_in_df2][j]) ]

					#geoms_temp_df[df2['Task Status'][([location_in_df2][j])]][location_in_geoms_df] = df2['Percentage'][([location_in_df2][j])] # hard to read, but for instance, it's geoms_temp_df['Complete'][location_in_geoms] =
	#			except:
	#				continue
	#			except:
	#		continue
	#print (geoms_temp_df)

	geoms_df.to_csv(geomsCSVfilename, index=False)
	print("Done.")
	# -- End -- #

	overall_job_statuses = df['Job Status'].value_counts()
	print('Stats of Tasks {0}-{1}: '.format(currentTime.year-1, currentTime.year))
	for i in range(len(overall_job_statuses)):
		print('{0}: {1}% ({2}/{3})'.format(overall_job_statuses.keys()[i], str(overall_job_statuses[i]/df.shape[0] * 100)[:5], overall_job_statuses[i], df.shape[0])) # prints task status, percetange accurate to 5 digits
	# -- End -- #

	exit() # allevaiates the 'TypeError: 'NoneType' object is not callable' error that sometimes shows up

if __name__ == '__main__':
	main()
