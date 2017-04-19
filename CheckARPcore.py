#Global imports
from netmiko import ConnectHandler
from datetime import datetime
import csv, os.path
from netaddr import IPNetwork
#Local imports
import credentials

# Begin timing the script
start_time = datetime.now()

# Define the primary function (to be moved to a separate module some day...)
def nc(username, password, secret, customer, subnet, ticketnum):
    with open(customer, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        # Now iterate through every row in the CSVfile and make dictionaries
        for row in reader:
            hostname = row['SysName']
            device_type = row['device_type']
            ip = row['IP_Address']
            switch = {
                'device_type': device_type,
                'ip': ip,
                'username': username,
                'password': password,
                'secret': secret,
                'verbose': False,
            }
            # This is your connection handler for commands from here on out
            net_connect = ConnectHandler(**switch)
            # Insert your commands here
            net_connect.enable()
            # Send log for beginning
            net_connect.send_command('send log "Beginning ARP check ticket {}"'.format(ticketnum))
            # Now make it pretty
            print "\n\n>>>>>>>>> Device {0} <<<<<<<<<".format(row['SysName'])
            for ip in IPNetwork(subnet):
                sh_arp = net_connect.send_command("show arp | include %s" % ip)
                if sh_arp != "":
                    print "%s found" % ip
                else:
                    pass
            print "\n>>>>>>>>> End <<<<<<<<<"
            # Finish logging
            net_connect.send_command('send log "Completing ARP check ticket {}"'.format(ticketnum))
            # Disconnect from this session
            net_connect.disconnect()

# Grab the Customer name to search
customer = raw_input('Customer name: ') + ".csv"
# Grab the subnet to check for
subnet = raw_input('Subnet to check for in slash notation: ')
# Flesh out these variables using the credentials.cred_csv module
username, password, secret = credentials.cred_csv()
# Enter ticket number for SW change logging
ticketnum = raw_input('Ticket #: ')
# command_string = "write mem" # can be passed to nc...
# Run the primary function in this program
nc(username, password, secret, customer, subnet, ticketnum)


end_time = datetime.now()
# How long did it run?
total_time = end_time - start_time
print "\nTotal time for script: \n" + str(total_time)
