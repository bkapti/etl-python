# Instructions
first run

`docker build -t python-app .`

then run

`docker run -it -v $(pwd)/excel_files:/usr/src/app/excel_files --rm --name my-running-app python-app`


You'll be asked to provide an input for the year you would like to get the weather data for.

Then you'll be asked to select the exercise number, either 1 or 2. 

Results are hardcoded for "TORONTO CITY"

If you run exercise 2, you'll receive the output immediately. 

If you run exercise 1, you'll have the output file in the excel_files folder.