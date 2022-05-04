# -*- coding: utf-8 -*-
"""
@author: kphillip
"""
import subprocess
import sys
import os
import webbrowser

def get_climate_zone(stat_file):
    """ get climate zone for stat file
    
    input stat_file: Statistics Report of the annual weather data .STAT file
    output: string - ASHRAE Climate Zone 
    """   
    with open(stat_file, 'r') as f:
           lines = f.readlines()
           
    for line in lines:
        if "ASHRAE Standard 196-2006 Climate Zone" in line:
            x = line.index('\"')
            climate_zone = line[x+1:x+3]
            break
    
    return climate_zone

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



          


if __name__ == "__main__":
    
    print("start")
    
    #Inputs for test rusn
    ep_path_test = "C:\EnergyPlusV9-1-0\PreProcess\IDFVersionUpdater"
    idf_file_test = r"C:\Users\kphillip\Desktop\JHU bench mark check\ASHRAE901_OfficeMedium_STD2016_NewYork.idf"
    start_ver_test = "9-0-0"
    end_ver_test = "9-1-0"
    epw_file_test = r"C:\Users\kphillip\Desktop\JHU bench mark check\USA_MD_Baltimore-Washington.Intl.AP.724060_TMY3.epw"
    get_weather_files = False
    #stat_file = "add file path"
    
   
    #Get EPW and STAT file
    if get_weather_files == True:
        open_EPW_Weather_url()
    
    # #Lookup best match
    
       
    #Update IDF File Version from v72 to v91
    print("Updating IDF File")
    update_idf_file(ep_path_test, idf_file_test, start_ver_test, end_ver_test)
    print("Updating IDF File - Complete")
    
    #Run IDF File with selected epw file
    print("running IDF File")
    run_idf_file(idf_file_test, epw_file_test)
    print("running IDF File - complete")
    print("end")

