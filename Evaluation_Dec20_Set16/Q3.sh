#!/bin/bash

IFACE=$(ip route | awk '/default/ {print $5}')
echo "Interface: $IFACE"

IP_INFO=$(ip addr show "$IFACE" | awk '/inet / && /scope global/')

if echo "$IP_INFO" | grep -q "dynamic"; then
    echo "Result: DHCP"
    echo "Reason: 'dynamic' found in 'scope global' address (ip addr show)"
elif [ -f /var/lib/dhcp/dhclient.leases ] && \
     grep -q "$IFACE" /var/lib/dhcp/dhclient.leases; then
    echo "Result: DHCP (likely)"
    echo "Reason: DHCP lease found in dhclient.leases"
else
    echo "Result: Static IP"
    echo "Reason: No DHCP indicators in ip addr or lease files"
    echo "Justification: Static IPs may not create DHCP lease files"
fi