# Bowles Farming Software Engineering Project (Group 13)
Voted best Bowles Farming project and finalist in UC Merced's Mobile App Challenge 2019!

# Important Notice
This project is no longer actively under development, as the Innovate To Grow final submission date has passed; however, Kyran has migrated the website (HTML, CSS, JS, etc.), Python script, and CSV files in its current form to another Github repository and website.
As a result, the commit that edits this README.md file (super meta) will be the last commit to this repository, and this repository will be archived shortly after.

## Project Details
Taken from the [Innovate to Grow website](https://innovatetogrow.ucmerced.edu/project-submissions/2019-01-spring-cse):
### Background
Bowles Farming Company is a sixth generation family farm out of Los Banos, CA. Bowles continuously strives to implement new technology to improve processes and activities around the farm.
### Problem
AgWorld is a modern farm management program that allows operations to plan and track jobs and costs associated in one program. We will be using AgWorld for task assignment and data collection. AgWorld has a very robust API which allows programs to extract as much information as needed about jobs in the database. Although a large amount of data is logged in AgWorld, it is not presented as well as it could be.
### Objectives
A step toward making AgWorld data presentable is to have a dashboard showing upcoming and completed jobs while highlighting overdue jobs. This data would be presented on TVs or as web platforms for users around the farm to get updated about what is going on and what has happened. This communication tool will help get everyone on the same page about what operations has done and what's coming up.

# Website
During the development of this project, the website was hosted [here](https://www.kyran.xyz/agworld-test/), but now that it's past the main development stages, it has been moved to [bfarms.github.io](https://bfarms.github.io/) as to make it more official (and to move away from using Kyran's personal website as a host).

## Information of the files
A lot of these files (the HTML files, JS files, and CSS files) are self-explanatory, so the remaining files will be covered.
### Get Activities Python Script
A Python script to get activities of Bowles Farming from AgWorld and output CSV files for the dashboarding website
### Preinstallation Requirements
You need a Python interpreter (on Linux is preferred, the following commands are for Linux):
- Python 3
  - `sudo apt install python3`
- Python 3 Pip
  - `sudo apt install python3-pip`
- Python Requests
  - `sudo pip3 install requests`
- Python Dateutil
  - `sudo pip3 install python-dateutil`
- Python Datetime
  - `sudo pip3 install datetime`
There are probably equivalent installers/packages for other OSes such as Windows, but I don't have documentation for that.
### Running the Python Script
- Edit the first few variables in the first few lines of the main() function to your liking (the default values seem to be fine for the current purpose)
  - This is clearly marked with the comment line "# ---- THESE ARE THE ONLY VARIABLE VALUES ANY USER REALLY NEEDS TO CHANGE, EVERYTHING ELSE IS HANDLED WITH THIS INFORMATION AND DOESN'T NEED TO BE TOUCHED ---- #")
- Run `python3 get_activities.py`
### Outputs of the Python Script
Based on the default values of the script, these are the outputs of the Python script:
- 'all_activities.csv': All of the activities from AgWorld for Bowles Farming (at least, what info is accessible with the given API key)
- 'farm_geoms_and_coloring.csv': Used in Carto to draw the map and the appropriate coloring of the fields based on task statuses
