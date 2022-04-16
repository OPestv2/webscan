
class Resolver:
    def __init__(self):
        self.MAX_PORT = 65536
        self.MIN_PORT = 0

        self.MIN_OCTET = 0
        self.MAX_OCTET = 256

    """
    resolve_ports rewrites port sequences and ranges to port list used in scan
    """

    def resolve_ports(self, ports):
        # divide PORT string to
        port_packets = ports.split(",")
        # initialize array of ports and set them 'not used'
        result = [False] * self.MAX_PORT

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
                    start = self.MIN_PORT
                    if range_bounds[0] != "":
                        start = int(range_bounds[0])
                        if start > self.MAX_PORT or start < self.MIN_PORT:
                            raise AttributeError("Values in range %d - %d allowed" % (self.MIN_PORT, self.MAX_PORT))
                    end = self.MAX_PORT
                    if range_bounds[1] != "":
                        end = int(range_bounds[1]) + 1
                        if end > self.MAX_PORT or end < self.MIN_PORT:
                            raise AttributeError("Values in range %d - %d allowed" % (self.MIN_PORT, self.MAX_PORT))

                    for i in range(start, end):
                        if result[i] is True:
                            overwrite_warning = True
                            overwrite_occurrences += 1
                        result[i] = True

                else:
                    # possible TypeError occurrence while casting to integer
                    specified_port = int(port_packet)
                    if specified_port > self.MAX_PORT or specified_port < self.MIN_PORT:
                        raise AttributeError("Values in range %d - %d allowed" % (self.MIN_PORT, self.MAX_PORT))

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
            print("[!] %d port(s) occurred more than once while resolving" % overwrite_occurrences)

        # rewrite result array to exact values list

        result_array = []
        for i in range(self.MIN_PORT, self.MAX_PORT):
            if result[i] is True:
                result_array.append(i)

        return result_array


    def resolve_hosts(self, hosts):
        # divide PORT string to
        host_packets = hosts.split(",")
        # initialize array of ports and set them 'not used'
        result = []

        # if port number occurs more than once raise overwrite warning
        overwrite_warning = False
        overwrite_occurrences = 0

        for host_packet in host_packets:
            try:
                # look for range
                if host_packet.__contains__("-"):
                    start = [int(octet) for octet in host_packet.split("-")[0].split(".")]
                    end = [int(octet)+1 for octet in host_packet.split("-")[1].split(".")]


                    for oct1 in range(start[0], end[0]):
                        for oct2 in range(start[1] if oct1==start[0] else self.MIN_OCTET, end[1] if oct1==end[0] else self.MAX_OCTET):
                            for oct3 in range(start[2] if oct1==start[1] else self.MIN_OCTET, end[2] if oct1==end[1] else self.MAX_OCTET):
                                for oct4 in range(start[3] if oct1==start[2] else self.MIN_OCTET, end[3] if oct1==end[2] else self.MAX_OCTET):



                    # range_bounds = host_packet.split("-")
                    # # possible AttributeError occurrence (range can have maximum 2 bounds)
                    # if len(range_bounds) > 2:
                    #     raise AttributeError("Maximum one '-' per port range allowed")
                    #
                    # # possible TypeError occurrence while casting to integer
                    # start = MIN_PORT
                    # if range_bounds[0] != "":
                    #     start = int(range_bounds[0])
                    #     if start > MAX_PORT or start < MIN_PORT:
                    #         raise AttributeError("Values in range %d - %d allowed" % (MIN_PORT, MAX_PORT))
                    # end = MAX_PORT
                    # if range_bounds[1] != "":
                    #     end = int(range_bounds[1]) + 1
                    #     if end > MAX_PORT or end < MIN_PORT:
                    #         raise AttributeError("Values in range %d - %d allowed" % (MIN_PORT, MAX_PORT))
                    #
                    # for i in range(start, end):
                    #     if result[i] is True:
                    #         overwrite_warning = True
                    #         overwrite_occurrences += 1
                    #     result[i] = True
                # subnet mask
                elif host_packet.__contains__("/"):
                    pass

                else:
                    duplicated = False
                    for host in result:
                        if host == host_packet:
                            overwrite_warning = True
                            overwrite_occurrences += 1
                            duplicated = True
                            break
                    if duplicated is False:
                        result.append(host_packet)

            except (AttributeError, ValueError) as e:
                print("[!] There is an error in host: '%s'. %s" % (host_packet, e))
                choice = input("[?] Do you want to skip this element and continue? [y/N] ")
                if choice == 'n' or choice == 'N' or choice == "":
                    return None

        if overwrite_warning is True:
            print("[!] %d host(s) occurred more than once while resolving" % overwrite_occurrences)
