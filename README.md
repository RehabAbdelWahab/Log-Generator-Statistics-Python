# Generator tool 
This script generates fake logs. with the following format:
date time source-ip dest-ip port protocol username action

It writes log lines in  "generated_logs.txt" file.
It mainly uses Faker library (https://github.com/joke2k/faker/) to generate realistic ip's, ports etc.

# Requirements
* Python 2.7 at least

* and to install the required libraries run this cmd:

$ pip install -r required_libraries.txt

# Usage
run this cmd:

$ python generator.py -n [number_or_lines]

example to generate 1000000 log lines into a generated_logs.txt file

$ python generator.py -n 1000000 

you will find a new created file in the same path called generated_logs.txt having the logs lines 
  
##################################################################

# Statistics Extractor
This script extracts some statistice from the generated_logs.txt file
And writes the results to the statistics.txt 

# Requirements
* Python 2.7 at least


# Usage
run this cmd:

$ python statistics_extractor.py

you will find a new created file in the same path called statistics.txt having the results
