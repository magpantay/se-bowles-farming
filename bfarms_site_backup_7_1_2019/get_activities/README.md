# Get Activities Python Script
A Python script to get activities of Bowles Farming from AgWorld and output CSV files for the dashboarding website

# Preinstallation Requirements
You need a Python interpreter (on Linux is preferred, the following commands are for Linux):
- Python 3
  - `sudo apt install python3`
- Python 3 Pip
  - `sudo apt install python3-pip`
- Python Pandas
  - `sudo pip3 install pandas`
- Python Dateutil
  - `sudo pip3 install python-dateutil`
- Python Datetime
  - `sudo pip3 install datetime`
There are probably equivalent installers/packages for other OSes such as Windows, but I don't have documentation for that.

## Running the Python Script
- Edit the first few variables in the first few lines of the main() function to your liking (the default values seem to be fine for the current purpose)
  - This is clearly marked with the comment line "# -- Things that can be changed by the user -- #"
- Run `python3 get_activities_2.py`

## Outputs of the Python Script
Based on the default values of the script, these are the outputs of the Python script:
- 'all_activities.csv': All of the activities from AgWorld for Bowles Farming (at least, what info is accessible with the given API key)
- 'farm_geoms_and_coloring.csv': Used in Carto to draw the map and the appropriate coloring of the fields based on task statuses
- 'field_statistics.csv': Statistics of task completion in the fields at Bowles Farms
