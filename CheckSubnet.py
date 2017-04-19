from netaddr import IPNetwork

# Ask for the CIDR
Cidr_check = raw_input("What is the range you want to view? ")

for ip in IPNetwork(Cidr_check):
    print '%s' % ip
