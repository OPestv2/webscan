import optparse


def help:
    print("""
        Simple port simplescanner
        Syntax: python simplescanner <-H host> <-P port>
        --help     Show this message
        -h | --host     Set hosts ip or domain name
        -p | --port     Set port / ports using syntax "4,5,6,7" or "4-7" or combined "4,6,8-20" ( remember to use "" ) or use "-" for 0-65535 range
    
        Examples:
        python simplescanner -help
        python simplescanner -h 127.0.0.1 -p 10
    
    
        Scanner proceeds only one host per run
    """)
    pass


def resolvePorts():
    pass


def resolveHost():
    pass


if __name__ == '__main__':
    parser = optparse.OptionParser('SimpleWebScanner ' + '-H <Host> -P <Port>')
    parser.add_option('-H', dest='host', type)