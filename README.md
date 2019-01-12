# OwnMap
Simple Python tool that uses Nmap to periodically portscan hosts and detect changes.

## The idea

This tool is intended mostly for blue teams and administrators. The problem that it tries to address is that it is not 
convenient/flexible in general to have a custom bash script that performs port scans, and even the official tool (ndiff)
is not very convenient in tracking changes.

Ownmap should help here by giving a web interface to configure the scans (namely adding/removing hosts, approving
ports etc.) and to retrieve reports. At the same time it would allow to get pretty reports sent to email that give an 
overview of the situation.

## How it works

Ownmap uses a Postgres DB to store data about hosts and about ports. A list of targets to scan is kept, and each host in
this list is scanned using nmap python library. Once the scan is done, a "state" is created, where all the hosts with 
the corresponding ports are added. At this point, the current state is pulled from the database, compared with the one 
just calculated, differences are elicited and the new state is written to the DB, while the old one is archived.
Every port is not approved by default, and an alert (email, slack, more?) is sent everytime a difference in the 
scan result is found or if the scan runs and there are unapproved ports left.
If SSH connection to a host is available, Ownmap can be configured to SSH into the target host and use 
netstat to understand what is actually running on each open port from the perspective of the host. This might be helpful
to catch backdoors.

## Status of development


 - Core
   - [x] Port Abstraction
   - [x] Host Abstraction
   - [x] State Abstraction
- Database
    - [x] Initialization
    - [ ] Load state
    - [x] Save state
    - [x] Load targets
- Scanning
    - [x] Scan single host
    - [x] Multithread scan 
    - [x] Save result to DB
    - [ ] Compute differences
- Reporting
    - [ ] Generate HTML report
    - [ ] Send email
    - [ ] Slack integration
    - [ ] LaTeX + Jinja for PDF report
- Web Frontend
    - [ ] Main dashboard
    - [ ] Add/Remove host functionality
    - [ ] Pull old report functionality
    - [ ] Change scanning configuration
    - [ ] Run manual scan
