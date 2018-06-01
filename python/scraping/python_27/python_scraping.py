# library imports
import arcpy
import csv
from misc_functions import *
import ntpath

#activate licenses
arcpy.CheckOutExtension("Spatial")

##########IF FILES EXIST, PUT True, else False.############
permit_range_files_exist = False
water_agency_files_exist = False
clipped_agency_files_exist = False
csv_files_exist = False
csv_files_test_exist = False



###import files###
repo_base_path = parent_path(3).replace("\\", "/") + "/"

#name file imports
list_location = repo_base_path + "data/name_lists/"
file_name_list = [
    'friant_kern_county_contractors_list',
    'i15_2014_commodity_list',
    'kern_county_water_Agency_districts_list',
    'other_water_districts_list',
    'permitting_commodity_list'
    ]
name_dict = {}  # dictionary with all names of commodities, water districts
# accessing all CSV files and adding all names to the dictionary
for name in file_name_list:
    file_name = list_location + name + '.csv'
    with open(file_name, 'rb') as f:
        reader = csv.reader(f)
        your_list = list(reader)
    name_dict[name] = your_list

#setting paths to kerm_permit_data
kern_permit_location = repo_base_path + "data/kern_county_permit_data/"

#establishing range of data from 1997 to 2017
permit_range = range(1997, 2018)

#convert dictionary into list
permitting_commodity_list = name_dict['permitting_commodity_list']
i15_2014_commodity_list = name_dict['i15_2014_commodity_list']

#create lists of all water districts
kern_county_water_Agency_districts_list = name_dict['kern_county_water_Agency_districts_list']
other_water_districts_list = name_dict['other_water_districts_list']
friant_kern_county_contractors_list = name_dict['friant_kern_county_contractors_list']

water_districts_overall = [friant_kern_county_contractors_list, kern_county_water_Agency_districts_list, other_water_districts_list]
water_district_names = ['friant_kern_county_contractors_list', 'kern_county_water_Agency_districts_list', 'other_water_districts_list']
all_district_names = []
for i in range(len(water_districts_overall)):
    for k in range(len(water_districts_overall[i])):
        all_district_names.append(repo_base_path + "output/water_district_boundaries/" + water_district_names[i] + "/" +
                                  str(water_districts_overall[i][k]).replace("[", "").replace("'", "").replace("-", "").replace(" ", "_")
                                    )


for i in range(len(water_districts_overall)):
    if water_agency_files_exist == True:
        pass
    else:
        arcpy.env.workspace = repo_base_path + \
            "output/water_district_boundaries/" \
            + water_district_names[i] + "/"

        print water_district_names[i]

        for k in range(len(water_districts_overall[i])):
            print str(water_districts_overall[i][k]).replace("[", "").replace("]", "").replace("'", "").replace(" ", "_").replace("-","")

            arcpy.env.workspace = repo_base_path + \
                "output/water_district_boundaries/" \
                + water_district_names[i] + "/"

            in_layer_or_view = arcpy.MakeFeatureLayer_management(
                in_features= repo_base_path + "data/water_district_shape_files/WaterDistricts20180108.shp",
                out_layer=str(water_districts_overall[i][k]).replace("[", "").replace("]", "").replace("'", "").replace(" ", "_").replace("-","") + "i"
                )

            # select based on name of the water district
            where_clause = "AGENCYNAME ='" + str(water_districts_overall[i][k]).replace("[", "").replace("]", "").replace("'", "").replace("-","") + "'"

            print where_clause

            arcpy.SelectLayerByAttribute_management(
                in_layer_or_view=in_layer_or_view,
                selection_type='NEW_SELECTION',
                where_clause=where_clause
                )

            #write to a new featureclass, outputs to a shapefile called test with the clipped data
            file_output_name = repo_base_path + "output/water_district_boundaries/" \
                + water_district_names[i] + "/" + str(water_districts_overall[i][k]).replace("[", "").replace("]", "").replace("'", "").replace("-","").replace(" ", "_")

            #create output of this water district shapefile
            arcpy.CopyFeatures_management(
                in_features=str(water_districts_overall[i][k]).replace("[", "").replace("]", "").replace("'", "").replace(" ", "_").replace("-","") + "i",
                out_feature_class=repo_base_path + \
                    "output/water_district_boundaries/" + \
                    str(water_districts_overall[i][k]).replace("[", "").replace("]", "").replace("'", "").replace(" ", "_").replace("-","")
                )


























