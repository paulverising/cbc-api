import requests
import pandas as pd
import time
import argparse
import sys
from os.path import expanduser

start_time = time.time()

# Handle the parameters that are passed into the program
def getArgs(argv=None):
    parser = argparse.ArgumentParser(
        description="Use cbr-api.py to see all processes on a specific host or search for a process across the environment."
    )
    group1 = parser.add_mutually_exclusive_group(required=True)
    group1.add_argument(
        "--host",
        type=str,
        help="Enter in the name of the host you want to see all the processes on.",
    )
    group1.add_argument(
        "--process", type=str, help="Enter in the name of the process you want to search."
    )
    parser.add_argument(
        "--window",
        type=str,
        required=False,
        help="OPTIONAL: Default is 10h. Time window: “2w” where y=year, w=week, d=day, h=hour, m=minute, s=second",
    )
    args = parser.parse_args(argv)
    return args

def getConfig():
    """
    Function reads the contents of the credential file and returns the configuration data 
    to connect to the API of a specific org. Returns the headers for the api request, the 
    org id, and the domain name to connect to.
    """
    if sys.platform == "Windows":
        cred_file = "C:\\Windows\\carbonblack\\credentials.cbc"
    else:
        home = expanduser("~")
        cred_file = f"{home}/.carbonblack/credentials.cbc"

    with open(cred_file) as file:
        datafile = file.readlines()
        for line in datafile:
            if "url" in line:
                address = line.split("=")[1]
            elif "token" in line:
                auth_token = line.split("=")[1]
            elif "org" in line:
                org = line.split("=")[1]
        auth_token = str(auth_token).strip("\n")
        headers = {
            "X-Auth-Token": auth_token,
            "Content-Type": "application/json",
            "accept": "application/json",
        }
    return (address, headers, org)


def get_job_id(domain, org_key, headers, hostname="*", process="*", window="10h"):
    """
    Function takes in the domain, org_key, headers, hostname, and timeframe to generate 
    the initial query an retrieve the job id of that query returns job_id
    """
    url = f"{domain}/api/investigate/v2/orgs/{org_key}/processes/search_jobs"
    print(url)
    if hostname == "*":
        query_payload = {
            "query": "process_name:" + process,
            "fields": [
                "device_name",
                "process_start_time",
                "process_cmdline",
                "process_name",
                "process_pid",
                "parent_pid",
            ],
            "sort": [{"field": "device_timestamp", "order": "asc"}],
            "start": 0,
            "rows": 10000,
            "time_range": {"window": "-" + window},
        }
    else:
        query_payload = {
            "criteria": {"device_name": [hostname]},
            "query": "process_name:" + process,
            "fields": [
                "device_name",
                "process_start_time",
                "process_cmdline",
                "process_name",
                "process_pid",
                "parent_pid",
            ],
            "sort": [{"field": "device_timestamp", "order": "asc"}],
            "start": 0,
            "rows": 10000,
            "time_range": {"window": "-" + window},
        }
    print("")
    response = requests.post(url, headers=headers, json=query_payload).json()
    job_id = response.get("job_id")
    print("Query sent to Carbon Black Cloud")
    return job_id


def check_status(domain, org_key, job_id, headers):
    """
    Takes in the domain, org_key, job_id, and headers as input and generates a new request 
    that runs until "contacted" == "completed", this indicates that the query has finished 
    running and we can now retrieve results returns the bool True when complete
    """
    url = f"{domain}/api/investigate/v1/orgs/{org_key}/processes/search_jobs/{job_id}"
    contacted = ""
    completed = "1"
    print("Checking to see if query has completed...")
    while contacted != completed:
        response = requests.get(url, headers=headers).json()
        contacted = response.get("contacted")
        completed = response.get("completed")
    print("Query has completed.")
    return True


def get_results(domain, org_key, job_id, headers):
    """
    Takes in domain, org_key, job_id, and headers as input and retrieves the reults in the 
    proper format. Function returns a dataframe.
    """
    print("Retrieving the results. Please stand by...")
    all_df = pd.DataFrame()
    url = f"{domain}/api/investigate/v2/orgs/{org_key}/processes/search_jobs/{job_id}/results"
    for i in range(0, 10000, 1000):
        payload = {"start": i, "rows": 1000}
        response = requests.get(url, headers=headers, params=payload).json()
        results = response.get("results")
        r_df = pd.DataFrame.from_dict(results)
        all_df = all_df.append(r_df, ignore_index=True)
        del r_df
    return all_df


def df_to_csv(results, param):
    """
    Takes in the dataframe and argument parameter input and writes it to a csv.
    """
    output_file = f"{param}-process.csv"
    results.to_csv(
        output_file,
        index=False,
        columns=[
            "device_name",
            "process_start_time",
            "process_cmdline",
            "process_name",
            "process_pid",
            "parent_pid",
        ],
    )


if __name__ == "__main__":
    args = getArgs()
    config = getConfig()
    domain = str(config[0]).strip("\n")
    headers = config[1]
    org_key = str(config[2]).strip("\n")
    if args.host:
        hostname = args.host
        param = args.host
        if args.window:
            window = args.window
            job_id = get_job_id(
                domain, org_key, headers, hostname=hostname, window=window
            )
        else:
            job_id = get_job_id(domain, org_key, headers, hostname=hostname)
    elif args.process:
        process = args.process
        param = args.process
        if args.window:
            window = args.window
            job_id = get_job_id(
                domain, org_key, headers, process=process, window=window
            )
        else:
            job_id = get_job_id(domain, org_key, headers, process=process)
    status = check_status(domain, org_key, job_id, headers)
    if status == True:
        results = get_results(domain, org_key, job_id, headers)
        print(results)
    df_to_csv(results, param)
    print("--- %s seconds ---" % (time.time() - start_time))
