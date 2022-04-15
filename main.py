#!/bin/python

import optparse
import os
import sys

MAX_PORT = 65536
MIN_PORT = 0

HELP = """
webscan is a simple port scanner

Syntax: python webscan <-h host> <-p port>
-h | --help     Show this message and exit
-H | --host     Set hosts ip or domain name
-P | --port     Set port / ports using syntax: exact value(s) 4,5,6,7, range 4-7, combined 4,6,8-20 or use - for 0-65535 range
                Additionally you can specify a part of full range e.g. 10000- means 10000-65535, 1,2,3-5,100- is equal [1,2,3,4,5,100,101,102,...,65535]

Examples:
python webscan -h
python webscan -H 127.0.0.1 -P 10
python webscan -H localhost -P 80
python webscan -H www.google.com -P 80,443


Scanner proceeds only one host per run.
"""

"""
Port resolver rewrites port sequences and ranges to port list used in scan
"""
def resolvePorts(ports_list):
    # divide PORT string to
    port_packets = ports_list.split(",")
    # initialize array of ports and set them 'not used'
    result = [False] * MAX_PORT

    # if port number occurs more than once raise overwrite warning
    overwrite_warning = False
    overwrite_occurrences = 0

    for port_packet in port_packets:
        try:
            # look for range
            if port_packet.__contains__("-"):
                range_bounds = port_packet.split("-")
                # possible AttributeError occurrence (range can have maximum 2 bounds)
                if len(range_bounds) > 2:
                    raise AttributeError("Maximum one '-' per port range allowed")

                # possible TypeError occurrence while casting to integer
                start = 0
                if range_bounds[0] != "":
                    start = int(range_bounds[0])
                    if start > MAX_PORT or start < MIN_PORT:
                        raise AttributeError("Values in range %d - %d allowed" % (MIN_PORT, MAX_PORT))
                end = 65535
                if range_bounds[1] != "":
                    end = int(range_bounds[1])
                    if end > MAX_PORT or end < MIN_PORT:
                        raise AttributeError("Values in range %d - %d allowed" % (MIN_PORT, MAX_PORT))
                end += 1

                for i in range(start, end):
                    if result[i] is True:
                        overwrite_warning = True
                        overwrite_occurrences += 1
                    result[i] = True

            else:
                # possible TypeError occurrence while casting to integer
                specified_port = int(port_packet)
                if specified_port > MAX_PORT or specified_port < MIN_PORT:
                    raise AttributeError("Values in range %d - %d allowed" % (MIN_PORT, MAX_PORT))

                if result[specified_port] is True:
                    overwrite_warning = True
                    overwrite_occurrences += 1
                result[specified_port] = True


        except (AttributeError, ValueError) as e:
            print("[!] There is an error in port: '%s'. %s" % (port_packet, e))
            choice = input("[?] Do you want to skip this element and continue? [y/N] ")
            if choice == 'n' or choice == 'N' or choice == "":
                return None

    if overwrite_warning is True:
        print("[!] %d port numbers occurred more than once while resolving port ranges" % (overwrite_occurrences))


    # rewrite result array to exact values list

    result_array = []
    for i in range(MIN_PORT, MAX_PORT):
        if result[i] is True:
            result_array.append(i)

    return result_array


if __name__ == '__main__':
    try:
        # constructor argument is usage hint
        parser = optparse.OptionParser("python webscan -H <host> -P <port>" + HELP)
        # set HOST options
        parser.add_option('-H', '--host', dest='host', type='string', help='Target host')
        # parser.add_option('--host', dest='host', type='string', help='Target host')
        # set PORT options
        parser.add_option('-P', '--port', dest='port', type='string', help='Target port(s)')
        # parser.add_option('--port', dest='port', type='string', help='Target port(s)')

        # parse arguments
        (options, args) = parser.parse_args()

        # check if required parameters are set
        host = options.host
        port = options.port

        if host is None or port is None:
            print("[!!!] Error. Required 2 parameters, usage: " + parser.usage)
            sys.exit(0)

        # resolve ports
        port = resolvePorts(port)

        print("[i] Port list contains %d element(s)" % len(port))
        if len(port) == 0:
            print("[!!!] No ports to scan. Abort")



    except KeyboardInterrupt as e:
        print("[i] Ctrl+C means Good Bye!")
        exit(0)





