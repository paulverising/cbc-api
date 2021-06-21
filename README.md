# Use Case
This script allows you to connect to the Carbon Black Cloud instance and see either all of the processes that ran on a single host, or a single process name that ran across the environment.
## Host
The “--host HOSTNAME” option allows you to enter a hostname and the script will return all of the processes that ran on the host. It outputs to a file titled “HOSTNAME_processdata.csv” and contains:
- Hostname
- Process Start Time
- Process Name
- Command Line
- Pid
- Parent Pid
## Process
The “--process PROCESSNAME” option allows you to enter a process name such as, “powershell.exe” and the script will return all of the times that process ran across the entire environment. It outputs a file titled “PROCESS_processdata.csv” and contains:
- Hostname
- Process Start Time
- Process Name
- Command Line
- Pid
- Parent Pid
## Window
The “--window” option allows you to specify the time range for the data. This is an optional flag. Default is 10h. Time window: “2w” where y=year, w=week, d=day, h=hour, m=minute, s=second.
# Setup
## Carbon Black Cloud API Setup
Navigate to the organization's Carbon Black Cloud instance. 
- On the left hand side select Settings > API Access.
    - Take note of the “ORG KEY"
- Click “Add API Key” on the right hand side
- Enter in a Name for the API Key
- Leave the Access Level Type set to “API”
- Click Save and then take note of the “API ID” and “API Secret Key”
## Credential File
### MacOS
Create this file in this location: 
- ~/.carbonblack/credentials.cbc
### Permissions for Directory and File - Only required for MacOS
- chmod 700 ~/.carbonblack
- chmod 600 ~/.carbonblack/credentials.cbc
### Windows
Create this file in this location: 
- C:\Windows\carbonblack\credentials.cbc
### Contents
The contents of the file should look like this:
```
[default]
url=https://{your-instance}.conferdeploy.net
token=APISECRETKEY/APIID
org_key=ORGKEY
ssl_verify=True
```
This is where the API Secret Key, API ID, and ORG KEY will be entered.
## Python Environment Setup
The first step is to make sure to have python 3 installed.

The recommended method for setting up the python environment is through a python virtual environment. The steps will be listed below for how to set this up. If you feel confident in your own setup the only requirements you need to install with pip are: requests and pandas.
### Virtual Environment Setup - MacOS
- Choose a folder where you want to keep this virtual environment on your system
- Create the virtual environment with this command:
    - python3 -m venv PATH-TO-YOUR-DIRECTORY/CBC-API
- Activate the virtual environment with this command:
    - source PATH-TO-YOUR-DIRECTORY/CBC-API/bin/activate
    - You should now see “CBC-API” at the beginning of you terminal line
- Install the requirements for the script with this command:
    - pip install requests
    - pip install pandas
- If you want to leave this python virtual environment simply type this command:
    - deactivate
### Virtual Environment Setup - Windows
- Choose a folder where you want to keep this virtual environment on your system
- Create the virtual environment with this command:
    - python3 -m venv PATH-TO-YOUR-DIRECTORY\CBC-API
- Activate the virtual environment with this command:
    - PATH-TO-YOUR-DIRECTORY\CBC-API\Scripts\activate.bat
    - You should now see “CBC-API” at the beginning of you terminal line
- Install the requirements for the script with this command:
    - pip install requests
    - pip install pandas
- If you want to leave this python virtual environment simply type this command:
    - deactivate
# Running the Script

With the virtual environment running you can type the either of these commands:
- `python cbc-api.py --host HOSTNAME`
- `python cbc-api.py --process PROCESSNAME`
- optionally specifying the `--window WINDOW` flag you can increase or decrease the time range
- `python cbc-api.py --help` to see the same information displayed in your terminal

After you are done running the script, you can deactivate the virtual environment by typing:
- deactivate
# Reusing the Script after Initial Setup
To reuse the script for a different Carbon Black Cloud instance there are a few requirements:
- Create a new API Access Key for the new instance
- Update the credentials.cbc file to reflect the API Access Key and ORG Key
- Enable the virtual environment that you created using the following command:
    - source PATH-TO-YOUR-DIRECTORY/CBC-API/bin/activate
- To disable the virtual environment use the following command:
    - deactivate
