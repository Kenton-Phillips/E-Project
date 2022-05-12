# -*- coding: utf-8 -*-
"""
Created on Wed May 11 21:33:20 2022

@author: kphillip
"""

def get_shortname_from_stat (stat_file):
    with open(stat_file, 'r') as f:
           lines = f.readlines()
    
    # assign value for test
    loc_short_name = "nope"
    
    for line in lines:
        #if "ASHRAE Standard 196-2006 Climate Zone" in line:
         if "Location --" in line:   
            x = line.index('--')
            loc_short_name = line[x+3:len(line)]
            break
    
    return loc_short_name



path = r"C:\Users\kphillip\Desktop\JHU bench mark check\USA_VA_Arlington-Ronald.Reagan.Washington.Natl.AP.724050_TMY3.stat"

print(get_shortname_from_stat(path))
