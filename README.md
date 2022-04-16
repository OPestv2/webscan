Webscan is a python script used to scan given hosts' ports. 
It returns ports states like open / closed.

Syntax: 
`webscan [-h | --help] -H hosts -P ports [-T time | --timeout=time] [-c | --show-closed] [-o | --hide-open]`

| Argument                      | Description                             |
|-------------------------------|-----------------------------------------|
| -h, --help                    | Show help and quit                      |
| -H HOST, --host=HOST          | Set hosts                               |
| -P PORT, --port=PORT          | Set ports                               |
| -T TIMEOUT, --timeout=TIMEOUT | Set single connection timeout           |
| -c, --show-closed             | Print list of closed ports              |
| -o, --hide-open               | Don't print list of open ports          |
|                               |                                         |
| **Not supported yet**         | --------------------------------------- |
| -W FILE, --write=FILE         | Write output to file                    |
| -R FILE, --read=FILE          | Read hosts and ports from file          |
| -v, --use-ipv6                | Specify hosts using IPv6 notation       |



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


#### Hosts can be specified as a single value, sequence, range, subnet mask or combined
| Type                | Example                  |
|---------------------|--------------------------|
| single value        | www.google.com           |
| sequence            | 127.0.0.1,www.github.com |
| range               | 13.14.16.17-20.19.18.16  |
| subnet mask         |                          |
| combined            |                          |

#### Reading hosts and ports from file
File should contain list of hosts (first) and ports only **separated by one empty line**. Specification rules can be applied. 
For example:
```text
localhost
10.0.12.5
10.1.15.34
100.0.0.1-100.0.0.10
192.168.0.0\24

10-100
``` 
First 5 lines are ip addresses, then empty line and ports. Make sure You have permission to read the input file.

Console output
---
#### Output (logs) type is described by one of the following signs

| Logging syntax | Description                                  |
|----------------|----------------------------------------------|
| [i]            | information                                  |
| [?]            | question; answer using one of options in [ ] |
| [!]            | warning; it does not terminate the program   |
| [!!!]          | critical; it does terminate                  |
| [+]            | success                                      |
| [-]            | failure                                      |

Additional features
---
#### Handling mistakes
In case of incorrectly specified hostname/IP or port, when script finds that, there is option to omit this value and continue.

***
> Script created using Python 3.9

> Script supports IPv4 addresses only (at this moment)

Created by OPest [GitHub](https://github.com/OPestv2 "OPest Github").
###### Feel free to use and modify if You find it useful