# -*- coding: utf-8 -*-
"""
Created on Tue May 10 21:23:02 2022

@author: kphillip
"""

def get_climate_zone(stat_file):
    """ get climate zone for stat file
    
    input stat_file: Statistics Report of the annual weather data .STAT file
    output: string - ASHRAE Climate Zone 
    """   
    with open(stat_file, 'r') as f:
           lines = f.readlines()
    
    # assign value for test
    climate_zone = "nope"
    
    for line in lines:
        #if "ASHRAE Standard 196-2006 Climate Zone" in line:
         if "Climate type" and "Climate Zone" in line:   
            x = line.index('\"')
            climate_zone = line[x+1:x+3]
            break
    
    return climate_zone

def match_climate_zone_to_city(climate_zone):
    """ get closest city to climate zone 
    
    input climate_zone: ASHRAE climate zone code
    output: String - city matching climate zone
    """   
    
    climate_dict = {
        "4B": "Albuquerque",
        "3A": "Atlanta",
        "5A": "Buffalo",
        "5B": "Denver",
        "0B": "Dubai",
        "3B": "ElPaso",
        "8": "Fairbanks",
        "6B": "GreatFalls",
        "0A": "HoChiMinh",
        "1A": "Honolulu",
        "7": "InternationalFalls",
        "1B": "NewDelhi",
        "4A": "NewYork",
        "5C": "PortAngeles",
        "6A": "Rochester",
        "3C": "SanDiego",
        "4C": "Seattle",
        "2A": "Tampa",
        "2B": "Tucson"
        }

    match_city = climate_dict[climate_zone]

    return match_city


stat_file = r"C:\Users\kphillip\Downloads\USA_GA_Marietta-Dobbins.AFB.722270_TMY3\USA_GA_Marietta-Dobbins.AFB.722270_TMY3.stat"

climate_zone = get_climate_zone(stat_file)
best_match_city = match_climate_zone_to_city(climate_zone)

print(climate_zone)
print(best_match_city)


code_standard = "ASHRAE901"
building_type = "OfficeLarge"
code_year = "STD2019"

idf_match = ("{}_{}_{}_{}.idf").format(code_standard,building_type,code_year,best_match_city)

print(idf_match)

