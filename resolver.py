import re
import sys
import traceback


class Resolver:
    def __init__(self, err_continue, err_stop):
        self.MAX_PORT = 65536
        self.MIN_PORT = 0

        self.MIN_OCTET = 0
        self.MAX_OCTET = 256

        self.MIN_BITS_IP_ADDR = 0
        self.MAX_BITS_IP_ADDR = 32
        self.MIN_AVAILABLE_MASK = 1
        self.MAX_AVAILABLE_MASK = 29

        # final ports array
        self.ports = []
        # array of ports and set them 'not used'
        self.set_pots = [False] * self.MAX_PORT
        # final hosts array
        self.hosts = []

        # if port number occurs more than once warn about duplication
        self.duplication_warning = False
        self.duplication_occurrences = 0

        # error handling style
        # 1. [False/False] just print info and ask what to do
        # 2. [True/False] omit wrong values
        # 3. [False/True] Abort
        # 4. [True/True] WTF?! (kidding, this scenario is avoided)
        self.ERR_CONTINUE = err_continue
        self.ERR_STOP = err_stop

    def __add_port(self, port):
        # if port is already added set warning flag to true and count occurrences
        if self.set_pots[port] is True:
            self.duplication_warning = True
            self.duplication_occurrences += 1
        else:
            self.set_pots[port] = True
            self.ports.append(port)

    def __add_host(self, host):
        self.hosts.append(host)

    def resolve_ports(self, ports):
        ports = self.__remove_white_characters(ports)
        # divide PORT string individual packets and process them
        for port_packet in ports.split(","):
            try:
                # look for range
                if port_packet.__contains__("-"):
                    range_bounds = port_packet.split("-")
                    # possible AttributeError occurrence (range can have maximum 2 bounds)
                    if len(range_bounds) > 2:
                        raise AttributeError("Maximum one '-' per port range allowed")

                    # possible TypeError occurrence while casting the beginning and the end of the range to integer
                    start = self.MIN_PORT
                    if range_bounds[0] != "":
                        start = int(range_bounds[0])
                        if start < self.MIN_PORT or start > self.MAX_PORT:
                            raise AttributeError("Values in range %d - %d allowed" % (self.MIN_PORT, self.MAX_PORT - 1))
                    end = self.MAX_PORT
                    if range_bounds[1] != "":
                        end = int(range_bounds[1]) + 1
                        if end > self.MAX_PORT or end < self.MIN_PORT:
                            raise AttributeError("Values in range %d - %d allowed" % (self.MIN_PORT, self.MAX_PORT - 1))

                    # add ports from given range to final array
                    for i in range(start, end):
                        self.__add_port(i)

                # single value
                else:
                    # possible TypeError occurrence while casting to integer
                    specified_port = int(port_packet)
                    if specified_port > self.MAX_PORT or specified_port < self.MIN_PORT:
                        raise AttributeError("Values in range %d - %d allowed" % (self.MIN_PORT, self.MAX_PORT - 1))

                    # add port to final array
                    self.__add_port(specified_port)

            except (AttributeError, ValueError) as e:
                print("[!] There is an error in port '%s': %s " % (port_packet, e), file=sys.stderr, end="")
                if self.ERR_CONTINUE:
                    choice = 'y'
                    print("[AUTO CONTINUE]", file=sys.stderr)
                elif self.ERR_STOP:
                    choice = 'n'
                    print("[AUTO STOP]", file=sys.stderr)
                else:
                    print("\n[?] Do you want to skip this element and continue? [y/N] ", file=sys.stderr, end="")
                    choice = input()
                if choice == 'n' or choice == 'N' or choice == "":
                    return None

        # warn about duplications
        if self.duplication_warning is True:
            print("[!] Found %d ports duplicated" % self.duplication_occurrences, file=sys.stderr)

        # return final ports array
        return self.ports

    def resolve_hosts(self, hosts):
        hosts = self.__remove_white_characters(hosts)
        # divide HOST string to individual packets and process them
        for host_packet in hosts.split(","):
            try:
                # subnet mask
                if host_packet.__contains__("/"):
                    ip = host_packet.split("/")[0]
                    mask = int(host_packet.split("/")[1])

                    # check if mask is a correct value
                    if mask < self.MIN_AVAILABLE_MASK or mask > self.MAX_AVAILABLE_MASK:
                        raise AttributeError("Values in range %d - %d allowed" % (self.MIN_AVAILABLE_MASK, self.MAX_AVAILABLE_MASK))

                    # if there is a subnet mask check if the IP address is correct
                    correct_ip = re.search(
                        '^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$',
                        ip)
                    if correct_ip is None:
                        raise AttributeError("Incorrect ip address")

                    # add subnet ip addresses
                    # self.__calculate_ip_range_using_subnet_mask(ip,mask)
                    self.hosts += self.__calculate_ip_range_using_subnet_mask(ip, mask)

                else:
                    self.__add_host(host_packet)

            except (AttributeError, ValueError) as e:
                traceback.print_exc()
                print("[!] There is an error in host '%s': %s" % (host_packet, e), file=sys.stderr, end="")
                if self.ERR_CONTINUE:
                    choice = 'y'
                    print("[AUTO CONTINUE]", file=sys.stderr)
                elif self.ERR_STOP:
                    choice = 'n'
                    print("[AUTO STOP]", file=sys.stderr)
                else:
                    print("\n[?] Do you want to skip this element and continue? [y/N] ", file=sys.stderr, end="")
                    choice = input()
                if choice == 'n' or choice == 'N' or choice == "":
                    return None

        return self.hosts

    def __calculate_ip_range_using_subnet_mask(self, ip, mask):
        print("[i] Resolving ip address: %s with subnet mask %d" % (ip, mask))

        ips = []
        # split ip to list of integers
        ip_array = [int(ip_part) for ip_part in ip.split(".")]

        subnet_mask_array = self.__calc_subnet_mask(mask)

        print(f"[i] Subnet mask address is: {self.__array2ips(subnet_mask_array)}")

        # calculate network address
        network_address_array = self.__calc_network_address(ip_array, subnet_mask_array)

        print(f"[i] Network address is: {self.__array2ips(network_address_array)}")

        # broadcast address is last address in subnet
        # negation of 255 value gives 9bit value (-256) it is necessary to make modulo 256 to get '0' value
        broadcast_address = self.__calc_broadcast_address(ip_array, subnet_mask_array)

        print(f"[i] Broadcast address is: {self.__array2ips(broadcast_address)}")

        # increment address using mask
        ip_bit_array = "".join(self.__dec2bins(octet) for octet in network_address_array)

        # divide ip to static part (network) and variable part (hosts)
        network_part = ip_bit_array[:mask]
        hosts_part = ip_bit_array[mask:]
        # create last possible host address and set as final, it is reserved broadcast address
        hosts_limit = "".join("1" for i in range(self.MAX_BITS_IP_ADDR - mask))

        # omit first address, it is reserved network address
        hosts_part = self.__increment_binary(hosts_part)

        while hosts_part != hosts_limit:
            result_ip = self.__ipsequence2addr(network_part + hosts_part)
            ips.append(result_ip)
            hosts_part = self.__increment_binary(hosts_part)
        return ips

    def __increment_binary(self, subject_binstr, ingredient_binstr="1"):
        return(bin(int(subject_binstr, 2) + int(ingredient_binstr, 2)))[2:].zfill(len(subject_binstr))

    def __ipsequence2addr(self, sequence):
        # create list of ip pieces
        ip = []
        # cast every next 8 bits to int and add to list
        for i in range(4):
            ip.append(int(sequence[i*8:i*8+8], 2))
        # then convert this list to ip string
        return self.__array2ips(ip)

    # function converts int array to ip string
    def __array2ips(self, array):
        return str(array[0]) + "." + str(array[1]) + "." + str(array[2]) + "." + str(array[3])

    # function converts decimal value to binary string
    def __dec2bins(self, val):
        bins = ""
        for exponent in range(7, -1, -1):
            power = 2 ** exponent
            if val - power >= 0:
                bins += "1"
                val -= power
            else:
                bins += "0"
        return bins

    def __calc_broadcast_address(self, ip_array, subnet_mask_array):
        return [(ip_oct | (~mask_oct % 256)) for ip_oct, mask_oct in zip(ip_array, subnet_mask_array)]

    def __calc_network_address(self, ip_array, subnet_mask_array):
        return [(ip_oct & mask_oct) for ip_oct, mask_oct in zip(ip_array, subnet_mask_array)]

    def __calc_subnet_mask(self, mask):
        # create subnet mask list of integers
        # initially fill array with '255's if mask is multiple of 8 (contains 8, 16, 24 or 32 bits set to 1)
        subnet_mask_array = [255] * int(mask / 8)
        # leave the rest of the division
        mask = mask % 8
        # incomplete '255', value with bits 1s and 0s
        val = 0
        # add power of 2 appropriate to bit's position, from most left to right
        # these values are [128, 64, 32, 16, 8, 4, 2, 1]
        # bit's position     7   6   5   4   3  2  1  0
        # now 'mask' is a position where 1s sequence ends and 0s begin to appear in 8bit sequence (n-th octet)
        for exponent in range(7, 7 - mask, -1):
            val += 2 ** exponent

        # when mask % 8 != 0 it is necessary to add value to array, otherwise
        # zeros will be added in the 'while' below
        if val != 0:
            subnet_mask_array.append(val)

        # fill array with zeros to achieve 4 pieces of ip address in array
        while len(subnet_mask_array) < 4:
            subnet_mask_array.append(0)

        return subnet_mask_array

    def __remove_white_characters(self, string):
        # replace \n to ,
        string = string.replace("\n", ",")
        # remove spaces, tabulations and 'returns'
        string = string.replace(" ", "")
        string = string.replace("\t", "")
        string = string.replace("\r", "")
        return string
