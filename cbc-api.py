# from cbc_sdk.helpers import *
from cbc_sdk.platform import *
from cbc_sdk.rest_api import *
import argparse
import csv
import json

parser = argparse.ArgumentParser(description='Use cbr-api.py to see all processes on a specific host or search for a process across the environment.')
group1=parser.add_mutually_exclusive_group()
group1.add_argument('--host', type=str, help="Enter in the name of the host you want to see all the processes on.")
group1.add_argument('--process', type=str, help="Enter in the name of the process you want to search.")

args = parser.parse_args()

cb = CBCloudAPI(profile='default')

def host_timeline(host):
    query = "device_name: " + host
    host_query = cb.select(Process).where(query).set_fields(["*", "process_cmdline", "process_start_time"])
    file_output = host + '_processdata.csv'
    with open(file_output, 'w') as csv_file:
        csv_file.write("Process Start Time, Name, CMDline, pid, Ppid\n")
        for proc in host_query:
            try:
                start_time = proc.process_start_time
            except:
                start_time = "NO DATA"
            try:
                cmdline = str(proc.process_cmdline)
            except:
                cmdline = "NO DATA"
            try:
                name = str(proc.process_name)
            except:
                name = "NO DATA"
            # hash = proc.process_hash
            try:
                pid = str(proc.process_pid)
            except:
                pid = "NO DATA"
            try:
                ppid = str(proc.parent_pid)
            except:
                ppid = "NO DATA"
            line = '{}, {}, {}, {}, {}\n'.format(start_time, name.replace(',', ''), cmdline.replace(',', ''), pid, ppid)
            csv_file.write(line)

def stacking(process):
    query = "process_name: " + process
    process_query = cb.select(Process).where(query).set_fields(["*", "process_cmdline", "process_start_time"])
    file_output = process + '_processdata.csv'
    with open(file_output, 'w') as csv_file:
        csv_file.write("Hostname, Name, CMDline, pid, Ppid\n")
        for proc in process_query:
            try:
                start_time = proc.process_start_time
            except:
                start_time = "NO DATA"
            try:
                cmdline = str(proc.process_cmdline)
            except:
                cmdline = "NO DATA"
            try:
                hostname = proc.device_name
            except:
                hostname = "NO DATA"
            try:
                name = str(proc.process_name)
            except:
                name = "NO DATA"
            # md5 = proc.process_md5
            try:
                pid = str(proc.process_pid)
            except:
                pid = "NO DATA"
            try:
                ppid = str(proc.parent_pid)
            except:
                ppid = "NO DATA"
            line = '{}, {}, {}, {}, {}, {}\n'.format(start_time, hostname, name.replace(',', ''), cmdline.replace(',', ''), pid, ppid)
            csv_file.write(line)

if __name__ == '__main__':
    if args.host:
        host_timeline(args.host)
    elif args.process:
        stacking(args.process)