#Pradhananga, Prajesh |  prajeshpradhananga@gmail.com  |  04/23/2013
import sys
import java
from java.util import Properties
from java.io import FileInputStream
import time

def appinstallinsandbox(ApplicationName,ApplicationPath,Node,Server):
 global AdminApp
 global AdminConfig
 
 print " Getting Cell Name .."
 cell = AdminControl.getCell()
 print " Cell name is --> " +cell
 print " ----------------------------------------------------------------------------------------- "
 print "Application update started for "+ApplicationName
 AdminApp.update(''+ApplicationName+'', 'app', '[  -operation update -contents '+ApplicationPath+'  -nopreCompileJSPs -installed.ear.destination $(APP_INSTALL_ROOT)/'+cell+' -distributeApp -nouseMetaDataFromBinary -deployejb -createMBeansForResources -noreloadEnabled -nodeployws -validateinstall warn -noprocessEmbeddedConfig -filepermission .*\.dll=755#.*\.so=755#.*\.a=755#.*\.sl=755 -noallowDispatchRemoteInclude -noallowServiceRemoteInclude -asyncRequestDispatchType DISABLED -nouseAutoLink -noenableClientModule -clientMode isolated -novalidateSchema -MapModulesToServers [[ "MBO EJB Module" mboejb.jar,META-INF/ejb-jar.xml WebSphere:cell='+cell+',node='+Node+',server='+Server+' ][ "MAXIMO Web Application" maximouiweb.war,WEB-INF/web.xml WebSphere:cell='+cell+',node='+Node+',server='+Server+' ][ "MBO Web Application" mboweb.war,WEB-INF/web.xml WebSphere:cell='+cell+',node='+Node+',server='+Server+' ][ "MEA Web Application" meaweb.war,WEB-INF/web.xml WebSphere:cell='+cell+',node='+Node+',server='+Server+' ][ "REST Web Application" maxrestweb.war,WEB-INF/web.xml WebSphere:cell='+cell+',node='+Node+',server='+Server+' ]]]' )
 AdminApp.edit(''+ApplicationName+'', '[  -MapWebModToVH [[ "MAXIMO Web Application" maximouiweb.war,WEB-INF/web.xml maximo_host ][ "MBO Web Application" mboweb.war,WEB-INF/web.xml maximo_host ][ "MEA Web Application" meaweb.war,WEB-INF/web.xml maximo_host ][ "REST Web Application" maxrestweb.war,WEB-INF/web.xml maximo_host ]]]' )
 AdminConfig.save()
#####################Waiting for the application to expand and then starting the server################
 print " Sleeping for 30 seconds after deploying application " +ApplicationName
 time.sleep(30)
 return None

def appinstallincluster(ApplicationName,ApplicationPath,Cluster):

 global AdminApp
 global AdminConfig
 
 print " Getting Cell Name .."
 cell = AdminControl.getCell()
 print " Cell name is --> " +cell
 print " ----------------------------------------------------------------------------------------- "

###############################################################################################
 print "Application update started for " +ApplicationName
 AdminApp.update(''+ApplicationName+'', 'app', '[-operation update -contents '+ApplicationPath+'  -nopreCompileJSPs -installed.ear.destination $(APP_INSTALL_ROOT)/'+cell+' -distributeApp -nouseMetaDataFromBinary -deployejb -createMBeansForResources -noreloadEnabled -nodeployws -validateinstall warn -noprocessEmbeddedConfig -filepermission .*\.dll=755#.*\.so=755#.*\.a=755#.*\.sl=755 -noallowDispatchRemoteInclude -noallowServiceRemoteInclude -asyncRequestDispatchType DISABLED -nouseAutoLink -MapModulesToServers [[ "MBO EJB Module" mboejb.jar,META-INF/ejb-jar.xml WebSphere:cell='+cell+',cluster='+Cluster+' ][ "MAXIMO Web Application" maximouiweb.war,WEB-INF/web.xml WebSphere:cell='+cell+',cluster='+Cluster+' ][ "MBO Web Application" mboweb.war,WEB-INF/web.xml WebSphere:cell='+cell+',cluster='+Cluster+' ][ "MEA Web Application" meaweb.war,WEB-INF/web.xml WebSphere:cell='+cell+',cluster='+Cluster+' ][ "REST Web Application" maxrestweb.war,WEB-INF/web.xml WebSphere:cell='+cell+',cluster='+Cluster+' ]]]' )
# Editing the vitual host for all the webmodule to maximo_host 
 AdminApp.edit(''+ApplicationName+'', '[  -MapWebModToVH [[ "MAXIMO Web Application" maximouiweb.war,WEB-INF/web.xml maximo_host ][ "MBO Web Application" mboweb.war,WEB-INF/web.xml maximo_host ][ "MEA Web Application" meaweb.war,WEB-INF/web.xml maximo_host ][ "REST Web Application" maxrestweb.war,WEB-INF/web.xml maximo_host ]]]' )
#Save the changes after the application is updated
 AdminConfig.save()
#####################Waiting for the application to expand and then starting the server################
 print " Sleeping for 30 seconds after deploying application " +ApplicationName
 time.sleep(30)
 return None	

#Parsing the property file 
propFile=sys.argv[0]
properties=Properties();
properties.load(FileInputStream(propFile))
print " ----------------------------------------------------------------------------------------- "
print "Succesfully read property file "+propFile
ApplicationPath1 = str(properties.getProperty("ApplicationPath1"))
Cluster1 = str(properties.getProperty("Cluster1"))
ApplicationName1 = str(properties.getProperty("ApplicationName1"))

ApplicationPath2 = str(properties.getProperty("ApplicationPath2"))
Cluster2 = str(properties.getProperty("Cluster2"))
ApplicationName2 = str(properties.getProperty("ApplicationName2"))

ApplicationPath3 = str(properties.getProperty("ApplicationPath3"))
Cluster3 = str(properties.getProperty("Cluster3"))
ApplicationName3 = str(properties.getProperty("ApplicationName3"))

ApplicationPath = str(properties.getProperty("ApplicationPath"))
ApplicationName = str(properties.getProperty("ApplicationName"))
Node = str(properties.getProperty("Node"))
Server = str(properties.getProperty("Server"))
###############################################################################################
#Calling methods based on properties file.
#Application1 in a cluster
if (ApplicationPath1!='None' and Cluster1!='None' and ApplicationName1!='None'):
 appinstallincluster(ApplicationName1,ApplicationPath1,Cluster1)
#Application2 in a cluster
if (ApplicationPath2!='None' and Cluster2!='None' and ApplicationName2!='None'):
 appinstallincluster(ApplicationName2,ApplicationPath2,Cluster2)
#Application3 in a cluster
if(ApplicationPath3!='None' and Cluster3!='None' and ApplicationName3!='None'):
 appinstallincluster(ApplicationName3,ApplicationPath3,Cluster3)
#Standalone Application
if (ApplicationName!='None'and ApplicationPath!='None'and Node!='None'and Server!='None'):
 appinstallinsandbox(ApplicationName,ApplicationPath,Node,Server)
###############################################################################################
#Syncing the Nodes after installation
#This will cause the application to restart if it is running
if (ApplicationPath1!='None' or ApplicationPath2!='None' or ApplicationPath3!='None' or ApplicationName!='None'):
 NodeList=AdminTask.listManagedNodes()
 NodeListParsed= NodeList.split("\n") 
 for nodes in NodeListParsed:
  AdminNodeManagement.syncNode(''+nodes+'')
  time.sleep(30)
 print "Application updated"
else:
 print 'Not Enough Information Provided'
sys.exit()