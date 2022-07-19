# python script to parse through JSON files to obtain counts above/below voltage ranges 
# the script will convert the JSON file to a csv output (with counts), provided the correct format of JSON.
#
# ---- TO DO BEFORE RUNNING ------
# delete "Metadata" Section before running
# add "retrieved_data" label at the beginning of the file (and fix bracket inconsistency)
#
# @author Miiyu Fujita 
# Last modified: July 5th, 2022

from locale import normalize
import pandas as pd
import csv

# dictionary to store RangeA count, RangeB count, RangeAThresholdPassedCount, RangeBThresholdPassedCount
# dictionary looks like this: {meter_1:{'above_range_A':'value','below_range_A':'value',...}
#                              meter_2:{'above_range_A':'value','below_range_A':'value',...}
#                              ... }
individual_counts = {}

# -------- helper functions ------------

def count_rangeA_above(nested_list):
    """
    counts total range A violations (above)
    """
    count = 0
    for list in nested_list:
        count += list[22]
    return count

def count_rangeA_below(nested_list):
    """
    counts total range A violations (below)
    """
    count = 0
    for list in nested_list:
        count += list[23]
    return count

def count_rangeB_above(nested_list):
    """
    counts total range B violations (above)
    """
    count = 0
    for list in nested_list:
        count += list[24]
    return count

def count_rangeB_below(nested_list):
    """
    counts total range B violations (below)
    """
    count = 0
    for list in nested_list:
        count += list[25]
    return count

# load JSON file (change path to JSON file depending on use)
# pdObj = pd.read_json('billing_meter_metrics_collector_output_base_winter.json')
pdObj = pd.read_json('billing_meter_metrics_collector_output_ieee_123.json')
# convert JSON file to pandas dataframe (rows: timesteps during simulation, columns: meters)
meters_over_time = pd.json_normalize(pdObj['retrieved_data'])
print(meters_over_time)
# total_count = 0
# iterate over each column (each meter) and update count dictionary 
for meter in meters_over_time:
    list_meter = meters_over_time[meter].tolist()
    range_A_count_above = count_rangeA_above(list_meter)
    range_A_count_below = count_rangeA_below(list_meter)
    range_B_count_above = count_rangeB_above(list_meter)
    range_B_count_below = count_rangeB_below(list_meter)
    individual_counts[meter] = {'above_rangeA': range_A_count_above, 'below_rangeA':range_A_count_below, 'above_rangeB':range_B_count_above, 'below_rangeB':range_B_count_below}
#    range_A_threshold_count = count_rangeA_threshold(list_meter) (we can add different performance indicators if we wish)
#    range_B_threshold_count = count_rangeB_threshold(list_meter)
#    total_count += range_A_count_above 
    print(meter, individual_counts[meter]) # print check

# export to CSV
meter_labels = ['meter', 'above_rangeA', 'below_rangeA', 'above_rangeB', 'below_rangeB'] # csv headers 
with open('output_ieee_123.csv', 'w') as csvfile: # change csv file for each case
    writer = csv.DictWriter(csvfile, fieldnames=meter_labels)
    writer.writeheader()
    for key,val in individual_counts.items():
        row = {'meter': key}
        print(row)
        row.update(val) # val is a dictionary
        writer.writerow(row)