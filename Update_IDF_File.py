# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 21:06:49 2022

@author: kphillip
"""
import subprocess
import sys
import os


def write_batch_file(_lines):
    """
    intput _lines: List of Lines that will be written to the .bat file
    output: creates .bat at current directory
    """
    with open('IDF_update.bat', 'w') as f:
        for line in _lines:
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
    write_batch_file(script)
    print("running update")
    #run batch (.bat) file
    subprocess.run([r"C:\Users\kphillip\.spyder-py3\IDF_update.bat"], shell=True) 
    print("complete")



#run test code
ep_path_ = "C:\EnergyPlusV9-1-0\PreProcess\IDFVersionUpdater"
idf_file_ = r"C:\Users\kphillip\Desktop\New folder\RefBldgMediumOfficePre1980_v1.4_7.2_1A_USA_FL_MIAMI.idf"
start_ver_ = "7-2-0"
end_ver_ = "9-1-0"

update_idf_file(ep_path_, idf_file_, start_ver_, end_ver_)
