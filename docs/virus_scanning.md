# Virus Scanning

The DORIS Intranet uses McAfee Endpoint Protection to scan uploads for malicious content. Due to licensing restrictions, the license package cannot be distributed with the codebase.

## Installation Instructions
1. Obtain the latest version of the UVScan Utility from the shared software repository (/development/development_tools/virus_scan/).  
Note: As of this writing the latest version is `20181030-UVScan.tar`
2. Extract the file to your `/vagrant` directory:  
   `tar xvf 20181030-UVScan.tar -C /vagrant/`
   This will extract the files to `/vagrant/VirusScan`
3. Change directory into `/vagrant/VirusScan/vscl`:
   `cd /vagrant/VirusScan/vscl`
4. Install uvscan to a directory of your choosing and follow the prompts (our preferred location is `/vagrant/.uvscan`):  
   `sudo sh ./install-uvscan /vagrant/.uvscan`
5. Change directories into the `/vagrant/VirusScan` directory to install the virus definitions:
   `cd /vagrant/VirusScan`
6. Expand the zip file included in this directory (should be named `avdat-####.zip` where `####` is a 4 digit number):  
   `unzip avvdat-####.zip`
7. Move all the `.dat` files to your uvscan installation directory:  
   `mv *.dat /vagrant/.uvscan`
8. Due to a quirk (not fully understood), UVScan will hang if not run as root at least once. So run the uvscan command as the root user:  
   `sudo /usr/local/bin/uvscan /vagrant/README.txt`

## Updating Virus Definitions
Virus definitions should be updated on a regular basis to ensure the most up-to-date protections possible.

Within the tar file that contains the UVScan utility there is a readme.txt file. Please follow the directions in the section titled "Updating DAT Files" to obtain the latest virus definitions.

Once you have obtained the latest zip file with the updated definitions
1. Expand the zip file (should be named `avdat-####.zip` where `####` is a 4 digit number):  
   `unzip avvdat-####.zip`
2. Move all the `.dat` files to your uvscan installation directory:  
   `mv *.dat /vagrant/.uvscan`