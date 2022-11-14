# SURE2022

This repository contains files relevant to the analysis of the effect of DERs on an electricity distribution network. The hope is that the scripts included can facilitate subsequent research done using GridLAB-D. 

## Python Scripts
There are 2 Python scripts included in the repo, each to be used after simulating a network using GridLAB-D software:
1. `JSON_to_CSV.py`
2. `voltage_unbalance_calculator.py`

> Make sure you have all the necessary libraries installed before running your files! 

### JSON_to_CSV.py

This file takes in a __*JSON file*__ as input, and outputs a __*CSV file*__.
The script parses through the JSON file to retrieve the number of times voltage values at any meter in the network go outside the ANSI range (above or below). 
The network violation occurences will be stored as a csv file, where the output will look like this:


|meter |	above_rangeA |	below_rangeA |	above_rangeB |	below_rangeB |
|--- | --- | --- | --- | --- |
| meter_1 |	0.0 |	1.0 |	0.0 |	1.0 |
| meter_10 | 1.0 |	0.0 |	1.0 |	0.0 |
| meter_100 |	1.0 |	0.0 |	2.0 |	0.0 |
...

> Exponential values are sometimes obtained in the output (of the simulation and therefore in the output csv), but I think these are outliers (to be handled)

### voltage_unbalance_calculator.py

This file takes __*csv files (one for each phase)*__ as input, and performs matrix multiplications necessary to determine any voltage unbalance occurences. (Fortescue's transformation) 
The script will count the number of voltage unbalance occurences, and __*print the result to the console*__ wherever the program is being run. (If using an IDE, it should print to the corresponding console window). It will print a python `dict`.
