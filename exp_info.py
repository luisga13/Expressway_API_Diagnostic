
# Add all the primary Expressway servers to the list. 'FQDN:port' format is required.

primary_exp = [{'fqdn': 'exp-e01.example.com:7443', 'user_exp': 'apiuser', 'passwd_exp': 'cisco'},
               {'fqdn': 'exp-c01.example.com:443', 'user_exp': 'apiuser', 'passwd_exp': 'cisco'}]

delay = 20

tcpdump = "on"