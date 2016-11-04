#!/bin/sh
#Pradhananga, Prajesh |  prajeshpradhananga@gmail.com  |  04/23/2013 
#Folder location for wsadmin.sh might be different based on configuraiton. Adjust the path if necessary.
sudo sh /opt/IBM/WebSphere/AppServer/profiles/App01/bin/wsadmin.sh -lang jython -f ./AutoDeployment.py ./AutoDeployment.properties