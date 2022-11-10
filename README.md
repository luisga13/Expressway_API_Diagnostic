# Expressway_API_Diagnostic

Cisco Expressway introduced the ability to Start/Stop/Collect/Download diagnostic logs using API requests, this is an extremely important feature when you are troubleshooting a multiple cluster deployment. This repository includes a single script that builds and sends the API requests neccesary to run and download diagnostic logs from multiple clusters. 

The DiagnosticAPI.py script will pull the primary node from each of your clusters and credentials from the exp_info.py file, it will use this information to find the FQDN for each node in the clusters. Then it will orchestrate the API requests needed to gather the diagnostic logs. 

## Dependencies:

- Python 3.9
- pip install requests

## Instructions to run the script: 

1. Install Python 3.9 

2. Download the repository "Expressway_API_Diagnostic" to a directory. 

3. Install a virtual environment or use an existing one.

4. Install the requests package: 
```
pip install requests
```

5. Update the exp_info.py file. These are the parameters you need to update:

        * The primary_exp is a list of dictionaries, you need to add a dictionary for each of your clusters with the primary node information. Example:
                primary_exp = [{'fqdn': 'exp-e01.example.com:7443', 'user_exp': 'apiuser', 'passwd_exp': 'cisco'},{'fqdn': 'exp-c01.example.com:443', 'user_exp': 'apiuser', 'passwd_exp': 'cisco'}]
                
        * TCPDump. Allowed values are "on" or "off", defines if you want to collect packet captures when running the diagnostic logs. 
        
        * Delay. Time delay in seconds between the start and stop of the logs. If you specify the value 0, the script will ask you when to stop the logs. 

 6. Run the script DiagnosticAPI.py: 
```
python3 DiagnosticAPI.py
```

## Limitations: 

1. All the nodes within the same cluster need to use the same credentials. If the "admin" credentials are different on each node, create the same administrator account with API access on each node. 
2. Cluster peers most be defined with a FQDN instead of an IP. API requests in this script are setup to be secured, meaning that it will verify the host in the url against the certificate. 

