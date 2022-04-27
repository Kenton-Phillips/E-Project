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





# def _run_idf_windows(idf_file_path, epw_file_path=None, expand_objects=True, silent=False):
#     """Run an IDF file through energyplus on a Windows-based operating system.
#     A batch file will be used to run the simulation.
#     Args:
#         idf_file_path: The full path to an IDF file.
#         epw_file_path: The full path to an EPW file. Note that inputting None here
#             is only appropriate when the simulation is just for design days and has
#             no weather file run period. (Default: None).
#         expand_objects: If True, the IDF run will include the expansion of any
#             HVAC Template objects in the file before beginning the simulation.
#             This is a necessary step whenever there are HVAC Template objects in
#             the IDF but it is unnecessary extra time when they are not
#             present. (Default: True).
#         silent: Boolean to note whether the simulation should be run silently
#             (without the batch window). If so, the simulation will be run using
#             subprocess with shell set to True. (Default: False).
#     Returns:
#         Path to the folder out of which the simulation was run.
#     """
#     # check and prepare the input files
#     ###directory = prepare_idf_for_simulation(idf_file_path, epw_file_path)
    
#     idf_file_directory, idf_file_name = os.path.split(idf_file_path)
#     idf_file_directory += "\\"
    
    
    
    
    
#     if not silent:  # write a batch file; useful for re-running the sim
#         # generate various arguments to pass to the energyplus command
#         epw_str = '-w "{}"'.format(os.path.abspath(epw_file_path)) \
#             if epw_file_path is not None else ''
        
        
#         idd_str = '-i "{}"'.format(folders.energyplus_idd_path)
#         expand_str = ' -x' if expand_objects else ''
#         working_drive = directory[:2]
#         # write the batch file
#         batch = '{}\ncd "{}"\n"{}" {} {}{}'.format(
#             working_drive, directory, folders.energyplus_exe, epw_str,
#             idd_str, expand_str)
#         batch_file = os.path.join(directory, 'in.bat')
#         write_to_file(batch_file, batch, True)
#         if all(ord(c) < 128 for c in batch):  # just run the batch file as it is
#             os.system('"{}"'.format(batch_file))  # run the batch file
#             return directory
#     # given .bat file restrictions with non-ASCII characters, run the sim with subprocess
#     cmds = [folders.energyplus_exe, '-i', folders.energyplus_idd_path]
#     if epw_file_path is not None:
#         cmds.append('-w')
#         cmds.append(os.path.abspath(epw_file_path))
#     if expand_objects:
#         cmds.append('-x')
#     process = subprocess.Popen(cmds, cwd=directory, shell=silent)
#     process.communicate()  # prevents the script from running before command is done

#     return directory



#run test code
ep_path = "C:\EnergyPlusV9-1-0\PreProcess\IDFVersionUpdater"
ep_idd_path = "C:\EnergyPlusV9-1-0\Energy+.idd"
idf_file = r"C:\Users\kphillip\Desktop\New folder\RefBldgMediumOfficePre1980_v1.4_7.2_1A_USA_FL_MIAMI.idf"
start_ver = "7-2-0"
end_ver = "9-1-0"
epw_path = r"C:\DIVA\WeatherData\USA_CO_Denver.Intl.AP.725650_TMY3.epw"

#update_idf_file(ep_path_test, idf_file_test, start_ver_test, end_ver_test)




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
script.append("C:\EnergyPlusV9-1-0\energyplus.exe -w {} -i {} -x".format(epw_path, ep_idd_path))

with open(idf_file_directory + "run\in.bat", 'w') as f:
    for line in script:
        f.write(line+'\n')

print("running update")
#run batch (.bat) file
batch_file2 = idf_file_directory + "run\in.bat"
os.system('"{}"'.format(batch_file2))
#subprocess.run([idf_file_directory+"\\run.in.bat"], shell=True) 
print("complete")



# C:
# cd "C:\Users\kphillip\Desktop\New folder\run"
# "C:\EnergyPlusV9-1-0\energyplus.exe" -w "C:\DIVA\WeatherData\USA_CO_Denver.Intl.AP.725650_TMY3.epw" -i "C:\EnergyPlusV9-1-0\Energy+.idd" -x

