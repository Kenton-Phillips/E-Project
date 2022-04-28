# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 21:06:49 2022

@author: kphillip
"""
import subprocess
import sys
import os


def write_batch_file(filename,lines):
    """Writes a .txt of .bat file when a list of strings
    
    intput filename: Filname with extenstion type. for example IDF_update.bat or new.idf
    intput lines: List of Lines that will be written to the .bat file
    output: None
    """
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
        
    #'IDF_update.bat    
    write_batch_file("IDF_update.bat",script)
    print("running update")
    #run batch (.bat) file
    subprocess.run([r"C:\Users\kphillip\.spyder-py3\IDF_update.bat"], shell=True) 
    print("complete")

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
    script.append('cd ' + idf_file_directory)
    script.append('copy ' + idf_file_name + " " + "run\\in.idf") 
    script.append('cd ' + idf_file_directory + "run")
    script.append("{} -w {} -i {} -x".format(ep_exe_path,epw_file, ep_idd_path))
    
    with open(idf_file_directory + "run\in.bat", 'w') as f:
        for line in script:
            f.write(line+'\n')
    
    print("running update")
    #run batch (.bat) file
    batch_file2 = idf_file_directory + "run\in.bat"
    #os.system('"{}"'.format(batch_file2))
    subprocess.run(batch_file2, shell=True) 
    print("complete")


if __name__ == '__main__':

    #Inputs for test rusn
    ep_path = "C:\EnergyPlusV9-1-0\PreProcess\IDFVersionUpdater"
    idf_file = r"C:\Users\kphillip\Desktop\New folder\RefBldgMediumOfficePre1980_v1.4_7.2_1A_USA_FL_MIAMI.idf"
    start_ver = "7-2-0"
    end_ver = "9-1-0"
    epw_file = r"C:\DIVA\WeatherData\USA_CO_Denver.Intl.AP.725650_TMY3.epw"
    
    
    #Update IDF File Version from v72 to v91
    update_idf_file(ep_path, idf_file, start_ver, end_ver)
    
    #Run IDF File with selected epw file
    run_idf_file(idf_file, epw_file)






