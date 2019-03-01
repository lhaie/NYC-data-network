2015 Yellow Taxi Trip Data | NYC Open Data

Comments about the structure of the code :

To download the full database :
https://data.cityofnewyork.us/view/ba8s-jw6u
Click on "Export" and then "Download"

The python file "main_gzdata.py" is used to make the analysis on the whole database.
However we cut the process when we reached 40 millions trips used out of the 146 millions.

The file "main.py" is used to make the analysis on the 1000 trips sample, 
which is stored in "data.txt" and loaded with "getData.py".
"route.py" is used to encode python objects for the trips in order to facilitate the access to the variables of a trip.