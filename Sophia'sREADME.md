## Approach
I utilized `datetime` and `zoneinfo` to format the dates and keep track of timezones. I translated which days of the 
week the date range corresponded to and then stepped through the availability for those days in 30 min increments. I 
checked to see if each slot was in the exception time window and blocked it if it was. Then, I took the list of slots 
and filtered out the already made appointments. I then checked for all of the time slots within the users preferred
 time of day. Coding the solution for this challenge took 
me around 2 hours, as I needed to get familiar with handling timezones. 

## How to Run
run `example.py` in command line via `python3 example.py` or via IDE. You can also run `appointment_scheduler.py` 
directly. Inside those files you can change which input file the code reads by updating `inputs/level1_input.json` 
along with which output file the code writes to by updating `outputs/L1_output.json` Please note the output files 
provided didn't match the requirements for the code challenge, thus were not the accurate outputs. Tests for this code, 
which runs through 1 case for each level, can be found in `test_appointment_scheduler.py`

