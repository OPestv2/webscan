Webscan is a python script used to scan hosts' ports. 
It returns ports states like open / closed and name of service running on the ports.

Syntax: <br/>
`webscan    [-h | --help] | [-H hosts -P ports [-T time | --timeout=time] 
            [-c | --show-closed] [-o | --hide-open]
            [[-y | --err_continue] | [-n | --err_stop]]]`

| Argument                      | Description                                                  |
|-------------------------------|--------------------------------------------------------------|
| -h, --help                    | Show help and quit                                           |
| -H HOST, --host=HOST          | Set hosts                                                    |
| -P PORT, --port=PORT          | Set ports                                                    |
| -T TIMEOUT, --timeout=TIMEOUT | Set single connection timeout                                |
| -c, --show-closed             | Print list of closed ports                                   |
| -o, --hide-open               | Don't print list of open ports                               |
| -y, --err-continue            | Continue the script when host or port resolving error occurs |
| -n, --err-stop                | Stop the script when host or port resolving error occurs     |
|                               |                                                              |
| **Not supported yet**         | ---------------------------------------                      |
| -v, --use-ipv6                | Specify hosts using IPv6 notation                            |
| -u                            | Use UDP protocol                                             |





Ports and hosts specification
---
#### Ports can be specified as a single value, sequence, range, full range, part of full range or combined.
| Type               | Example             |
|--------------------|---------------------|
| singe value        | 3                   |
| sequence           | 5,8,11              |
| range              | 10-40               |
| full range         | - (dash; 0-65535)   |
| part of full range | -30 (0,1,...,29,30) |
| combined           | -4,7-10,15,100-     |


#### Hosts can be specified as a single value, sequence or as an IP address with subnet mask
| Type                | Example                   |
|---------------------|---------------------------|
| single value        | www.google.com            |
| sequence            | 10.10.0.25,www.github.com |
| subnet mask         | 192.168.2.17/24           |

#### Reading hosts and ports from file
Script does not have an in-built reading input from file mechanism. 
But the best way to achieve this manually is to 'cat' file into parameter.
```bash 
python webscan.py -H $(cat _hosts_filename_ | tr "\n" ",") -P $(cat _ports_filename_ | tr "\n" ",")
```

When values in file are in separate lines use the ```tr``` command to make text a one line, comma separated argument. 
Be sure not to put any whitespaces e.g. spaces, tabulations.

#### Writing console output to file
Script does not have an in-built writing console output to file mechanism. But the best way to achieve this manually is to use redirector ```>```
as shown below
```bash 
python webscan.py -H _hosts_ -P _ports_ > _output_filename_
```

Error messages (about wrong hosts and ports) are printed on **stderr** in console. 
They will not be saved in file and user can manually choose to continue or exit. 
If You want to avoid handling such errors add one of the following flags to the command.

```-y``` or ```--err-continue``` tells script to skip wrong values and continue executing.

```-n``` or ```--err-stop``` tells script to abort execution if wrong values occurs.

You can use this flags while specifying hosts and ports both manually and by using file.

Console output
---
#### Output type is described by one of the following signs

| Syntax | Description                                  |
|--------|----------------------------------------------|
| [i]    | information                                  |
| [?]    | question; answer using one of options in [ ] |
| [!]    | warning; it does not terminate the program   |
| [!!!]  | critical; it does terminate                  |
| [+]    | success                                      |
| [-]    | failure                                      |

Additional features
---
#### Handling user mistakes
In case of incorrectly specified host name/IP or port, when script finds that, there is option to omit this value and continue.

***
> Script created using Python 3.9

> Script supports IPv4 addresses only (at this moment)

> Script does not support scanning hosts connected via VPN 

Created by OPest [GitHub](https://github.com/OPestv2 "OPest Github").
###### Feel free to use and modify if You find it useful