# Auth log parser
Little project to eventually visualize what the most scanned users are which bots use to try to access my ssh server.

Source: several rotated auth.log files from my public facing server

## Commonly used usernames in ssh probes
usernames that are probed more than 20 times in this case.
![bar chart of usernames](/img/usernames.png)

## Most common country in ssh probe ips
countries with more than 22 hits in this case
![bar chart of origin](/img/origin.png)

## Next steps
- implement argparse to pass auth.log files into the script
- cache data from ip lookup if it is the same file
