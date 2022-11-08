import json
import requests
import re
from requests.auth import HTTPBasicAuth
from exp_info import primary_exp, delay, tcpdump
import time


def cluster_api(fqdn, user, passwd):
    """Run /cluster/peers API to create a dictionary per cluster including all the peers and credentials"""

    peers_dict = {"nodes": [], "creds": []}
    url = "https://" + fqdn + "/api/v1/provisioning/common/cluster/peers"
    try:
        response = (requests.get(url, auth=HTTPBasicAuth(user, passwd)))
        if response.status_code == 200:
            response = response.json()
            port = fqdn.split(":", 1)
            for i in response:
                peers_dict["nodes"].append(i["PeerAddress"] + ":" + port[1])
            peers_dict["creds"].append(user)
            peers_dict["creds"].append(passwd)
            return peers_dict
    except requests.exceptions.ConnectionError as err:
        print("Error Connecting:", err)
        exit()
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
        exit()


def diaglog_api(fqdn, user, passwd, mode):
    """Diagnostic logging API to star/stop/collect/download"""

    diag_log = "https://" + fqdn + "/api/v1/provisioning/common/diagnosticlogging"

    if mode == "start":
        payload = json.dumps({"Mode": mode, "TCPDump": tcpdump})
    else:
        payload = json.dumps({"Mode": mode})

    try:
        response = (requests.put(diag_log, data=payload, auth=HTTPBasicAuth(user, passwd)))
        if response.status_code == 200 and mode == "download":
            filename = get_filename_from_cd(response.headers.get('content-disposition'))
            with open(filename, 'wb') as f:
                f.write(response.content)
            print("Request to " + mode + " diagnostic logs was successful on node:  " + fqdn)
        elif response.status_code == 200:
            print("Request to " + mode + " diagnostic logs was successful on node:  " + fqdn)
        elif response.status_code == 400:
            response = response.json()
            print("Request to " + mode + " with the error message:   " + response["Message"])
            exit()
    except requests.exceptions.ConnectionError as err:
        print("Error Connecting:", err)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)


def get_filename_from_cd(cd):
    """Get filename from content-disposition"""

    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0].replace('"', '')


if __name__ == "__main__":
    clusters = []
    for i in primary_exp:
        clusters.append(cluster_api(i["fqdn"], i["user_exp"], i["passwd_exp"]))
    print("Clusters:")
    print(clusters)

    for i in primary_exp:
        diaglog_api(i["fqdn"], i["user_exp"], i["passwd_exp"], mode="start")

    if delay == 0:
        ready = input("Type Y and hit Enter to stop the logs:   ")
        if ready == "Y":
            print("Stopping the logs")
    else:
        time.sleep(delay)
        print("Stopping the logs")

    for i in primary_exp:
        diaglog_api(i["fqdn"], i["user_exp"], i["passwd_exp"], mode="stop")
    time.sleep(10)
    for i in clusters:
        for j in i["nodes"]:
            diaglog_api(j, i["creds"][0], i["creds"][1], mode="collect")
    time.sleep(20)
    for i in clusters:
        for j in i["nodes"]:
            diaglog_api(j, i["creds"][0], i["creds"][1], mode="download")
