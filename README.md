# LinuxAdminTools

## Summary

This is an attempt at making a collection of generic Linux Troubleshooting tools
/scripts that aims to make troubleshooting easier and faster for experienced and
amateur admins alike.

## apt_install_history.py

This is meant to ease the pain of sifting through dpkg logs and making long
1-liners to sift info. Will take the contents of /var/log/dpkg.log.* and output
to stdout.

./apt_install_history.py [-a|-c|-s] [-n <int>]

flags:  
  -a, --all :  
  		Prints every line of every dpkg.log file  
  -c, --command_code :  
  		Prints every line of an action (install|remove|purge)  
  -f, --from_date :  
      Prints entries starting at this YYYY-MM-DD date  
  -s, --status_code :  
  		Prints every line of package status (installed|not-installed)  
  -n, --number :  
  		Number of lines to print (starting from most recent)  
  -u, --until :  
      Prints entries until this YYYY-MM-DD date  
