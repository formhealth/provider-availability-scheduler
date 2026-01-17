## Approach
I utilized datetime and ZoneInfo to format the dates and keep track of timezones. I got the days of the week the dates
corresponded to and then stepped through the availability in 30 min increments. I then checked to see if the slot was
in the exception time window. After I got the list of slots, I filtered out the already made appointments and then
checked for all of the time slots within the users time of day preference. Coding the solution for this challenge took 
me around 2 hours, as I needed to get familiar with handling timezones. 

## How to Run
run `example.py` by 
in command line via
`python3 example.py` or via IDE. 
Inside `example.py` you can change which input file the code reads by updating `inputs/level1_input.json` along with 
which output file the code writes to by updating `outputs/L1_output.json` Please note the output files provided didn't match the requirements for the code 
challenge. 

