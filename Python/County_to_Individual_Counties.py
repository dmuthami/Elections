#-------------------------------------------------------------------------------
# Name:        Bulls Ring Module
# Purpose:
#
# Author:      dmuthami
#
# Created:     26/09/2014
# Copyright:   (c) dmuthami 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

#Import arcpy module
import os, sys
import arcpy
import traceback
from arcpy import env
import numpy

##Define local functions

def createFC (featureClass,countyName):

    #variable pointer to the in-memory feature layer
    featureLayer = featureClass + '_lyr'

    # Make a layer from stores feature class
    arcpy.MakeFeatureLayer_management(featureClass, featureLayer)

    #collegiate definition
    featureClassFieldwithDelimeter = arcpy.AddFieldDelimiters(env.workspace,"COUNTY_NAM")

    # Select  Bulls eye records
    #strr2 =str(row[3]).replace("'", "''")
    featureClassSQLExp =  featureClassFieldwithDelimeter + " = " + "'"+str(countyName).replace("'", "''")+"'"
    print('Expression : {}'.format(featureClassSQLExp))

    #make a fresh selection here
    arcpy.SelectLayerByAttribute_management(featureLayer, "NEW_SELECTION", featureClassSQLExp)

    #Create feature class from selection
    #strr2 =strr2.replace(" ", "_")
    arcpy.CopyFeatures_management(featureLayer,str(countyName).replace(" ", "_").replace("'", ""))

    #delete the in memory feature layer just in case we need to recreate
    # feature layer or maybe run script an additional time
    arcpy.Delete_management(featureLayer)

    return ""

def loopThruFeatures(fc):
    # Use SearchCursor to access state name and the population count
    #
    strr = ""
    strr2 = ""
    with arcpy.da.SearchCursor(fc, '*') as cursor:
        for row in cursor:
            # Access and print the row values by index position.
            #   County Name: row[3] = "COUNTY_NAM"
            #

            createFC(fc,row[3])
            strr =str(row[3]).replace("'", r"\'")
            print('County Name : {}'.format(strr))


    return ""

def executeFeaturesToFeatureClasses():
    try:
        env.workspace = r'E:\GIS Data\Elections\GIS\elections.gdb\IEBCElectoralDistricts'

        ## Set overwrite in workspace to true
        env.overwriteOutput = True

        #variable pointer to the in-memory feature layer
        BR_storesFeatureClass = 'Counties'

        ##Loop through the county feature class
        loopThruFeatures (BR_storesFeatureClass)

        #Back=up intitial stores feature layer
        #backupInitialStoresFC (BR_workspace,BR_storesFeatureClass, BR_collegiateField, BR_BRMDL)

    except:
        ## Return any Python specific errors and any error returned by the geoprocessor
        ##
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        pymsg = "PYTHON ERRORS:\nTraceback Info:\n" + tbinfo + "\nError Info:\n    " + \
                str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"
        msgs = "Geoprocesssing  Errors :\n" + arcpy.GetMessages(2) + "\n"

        ##Add custom informative message to the Python script tool
        arcpy.AddError(pymsg) #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).
        arcpy.AddError(msgs)  #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).

        ##For debugging purposes only
        ##To be commented on python script scheduling in Windows
        print pymsg
        print "\n" +msgs
        ##Try except contract is in the loop

    return ""
##---End of definition for local functions

def main():
    pass

if __name__ == '__main__':
    main()

    #Run executor
    executeFeaturesToFeatureClasses()