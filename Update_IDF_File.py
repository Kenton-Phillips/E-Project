# -*- coding: utf-8 -*-
"""
@author: kphillip
"""
import subprocess
import sys
import os
import webbrowser
import shutil


def check_idf_ep_version(idf_file):
    """ get ep version from idf file
    
    input idf_file: file path for Energy Plus run file 
    output: string for EP version 
    """   
    with open(idf_file, 'r') as f:
           lines = f.readlines()
           
    for line in lines:
        if "Version," in line:
            x = line.index(',')
            ep_version = line[x+1:len(line)-2]
            break
    
    #Format ep_version for idf update function 
    ep_version = ep_version.replace(".","-") + "-0"
    
    
    return ep_version


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


def get_shortname_from_stat (stat_file):
    with open(stat_file, 'r') as f:
           lines = f.readlines()
    
    # assign value for test
    loc_short_name = "nope"
    
    for line in lines:
        #if "ASHRAE Standard 196-2006 Climate Zone" in line:
         if "Location --" in line:   
            x = line.index('--')
            loc_short_name = line[x+3:len(line)-3]
            break
    
    loc_short_name = loc_short_name.split(" ")[0]
    
    return loc_short_name


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


def open_EPW_Weather_url():
    url = 'https://energyplus.net/weather'
    webbrowser.open(url, new=2)
    

def run_idf_file(idf_file, epw_file):
    """ Runs a E+ using the idf and epw files
    
    input idf_file: Energy Plus Input Data File (idf) 
    input epw_file: Enegy Plus Westher File 
    output: none
    """
        
    # current hard set
    #NOTE - need to set to user E+ version
    ep_idd_path = "C:\EnergyPlusV9-1-0\Energy+.idd"
    ep_exe_path = "C:\EnergyPlusV9-1-0\energyplus.exe"
    
    idf_file_directory, idf_file_name = os.path.split(idf_file)
    idf_file_directory += "\\"
    
    #make new folder
    newpath = idf_file_directory + "run"
    if not os.path.exists(newpath):
        os.makedirs(newpath)
        
    
    script = []
    script.append('cd ' + '"' + idf_file_directory + '"')
    script.append('copy ' + '"' + idf_file_name + '" ' + "run\\in.idf") 
    script.append('cd ' + '"' + idf_file_directory + "run" + '"')
    script.append('"{}" -w "{}" -i "{}: -x'.format(ep_exe_path,epw_file, ep_idd_path))
    
    with open(idf_file_directory + "run\in.bat", 'w') as f:
        for line in script:
            f.write(line+'\n')
    
    print("running update")
    #run batch (.bat) file
    batch_file2 = idf_file_directory + "run\in.bat"
    #os.startfile('"{}"'.format(batch_file2))
    os.system('"{}"'.format(batch_file2))
    #subprocess.run(batch_file2, shell=True) 
    print("complete")


def update_idf_file(ep_path, idf_file, start_ver, end_ver):
    """Updates the given IDF to the goal version.

    input ep_path: Path string to the energy plus idf verision updater files. Should be something like C:\EnergyPlusVx-x-x\PreProcess\IDFVersionUpdater
    input idf_file: Path sting of idf file that will be updated. Include directory and filename.
    input start_ver: String of E+ version of starting/beginning idf file. See ep_versions list below for format.
    input end_ver: String of E+ version for ending/goal idf file. See ep_versions list below for format.
    output: None
    """
    
    idf_file_directory, idf_file_name = os.path.split(idf_file)
    idf_file_directory += "\\"
    
   
    #NOTE: When new EnergyPlus versions come out, add to front of list
    ep_versions = [
        "9-1-0",
        "9-0-0",
        "8-9-0",
        "8-8-0",
        "8-7-0",
        "8-6-0",
        "8-5-0",
        "8-4-0",
        "8-3-0",
        "8-2-0",
        "8-1-0",
        "8-0-0",
        "7-2-0"
    ]  
        
    ep_versions.sort()
    try: 
        start_index = ep_versions.index(start_ver)
    except ValueError:
        sys.exit("Start Verision is not in list of EP versions")
    
    try: 
        end_index = ep_versions.index(end_ver)
    except ValueError:
        sys.exit("End Verision is not in list of EP versions")
    
    ## Start Bat file creation
    #hold lines of script for bat file
    script = [] 
    script.append('cd ' + idf_file_directory)
    #back up original file
    script.append('copy ' + idf_file_name + " " + "old_"+idf_file_name) 
    script.append('cd ' + ep_path)
    # Loop through each verision of ep idf udpater that needs to be called
    for i in range(start_index,end_index):
        script_line = "Transition-V{}-to-V{}".format(ep_versions[i],ep_versions[i+1])
        script.append(script_line + ' "' + idf_file_directory + idf_file_name + '"')    
    
    # write lines to file
    write_batch_file(idf_file_directory + "IDF_update.bat",script)
    print("running update")
    #run batch (.bat) file
    #subprocess.run(["IDF_update.bat"], shell=True) 
    os.system('"{}"'.format(idf_file_directory + "IDF_update.bat"))
    #os.startfile(idf_file_directory + "IDF_update.bat")
    #os.system("start /wait cmd /c {}".format(idf_file_directory + "IDF_update.bat"))
    print("complete")


def write_batch_file(filename,lines):
    """Writes a .txt or .bat file
    
    intput filename: Filname with extenstion type i.e. IDF_update.bat or new.idf
    intput lines: List of Lines that will be written to the .bat file
    output: None
    """
    print(filename)
    with open(filename, 'w') as f:
        for line in lines:
            f.write(line+'\n')
     


if __name__ == "__main__":
    
    print("start")
    
    #Inputs not set by user
    ep_path_test = "C:\EnergyPlusV9-1-0\PreProcess\IDFVersionUpdater"
    end_ver_test = "9-1-0"
    get_weather_files = False
    code_standard = "ASHRAE901"
    building_type = "OfficeLarge"
    code_year = "STD2019"
    idf_repo_dir = "C:\Github\E-Project\IDF_repo\OfficeLarge"
    
    
    idf_file_test = r"C:\Users\kphillip\Desktop\JHU bench mark check\RefBldgMediumOfficePre1980_v1.4_7.2_1A_USA_FL_MIAMI.idf"
    
    #Inputs set by user
    epw_file_test = r"C:\Users\kphillip\Desktop\JHU bench mark check\USA_CA_Los.Angeles.Intl.AP.722950_TMY3.epw"
    stat_file = r"C:\Users\kphillip\Desktop\JHU bench mark check\USA_CA_Los.Angeles.Intl.AP.722950_TMY3.stat"
    
    
    #Get EPW and STAT file if requested
    if get_weather_files == True:
        open_EPW_Weather_url()
    
    
        
    ###############################
    climate_zone = get_climate_zone(stat_file) #find climate zone from .stat file
    best_match_city = match_climate_zone_to_city(climate_zone) #match climate zone to DOE protoype city
    
    idf_match_file_name = ("{}_{}_{}_{}.idf").format(code_standard,
                                                     building_type,
                                                     code_year,
                                                     best_match_city) #find correct idf file
    
    idf_match_file = ("{}\{}").format(idf_repo_dir,idf_match_file_name) #create path for idf file
    
    #move copy of idf_match to epw directory
    epw_file_directory, epw_file_name = os.path.split(epw_file_test)
    
    loc_short_name = get_shortname_from_stat(stat_file)
    print(loc_short_name)
    
    destination_idf = str(("{}\{}_{}_{}_{}.idf").format(epw_file_directory,
                                                        code_standard,
                                                        building_type,
                                                        code_year,
                                                        loc_short_name))
   
    src = idf_match_file
    dst = destination_idf
    
    print(src)
    print(dst)
    shutil.copyfile(src, dst)
        
    # Check starting idf ep version    
    start_ver_test = check_idf_ep_version(destination_idf)
    
    # #Update IDF File Version to v91
    print("Updating IDF File")
    update_idf_file(ep_path_test, destination_idf, start_ver_test, end_ver_test)
    print("Updating IDF File - Complete")
    
    #Run IDF File with selected epw file
    print("running IDF File")
    run_idf_file(destination_idf, epw_file_test)
    print("running IDF File - complete")
    print("end")

