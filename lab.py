import arcpy
from arcpy import env
from arcpy.sa import *
arcpy.CheckOutExtension('Spatial')

# Set environment settings
workspace = "C:\data"
env.cellSize = r"data\landcover"
env.extent = r"data\landcover"
env.workspace = r"data\data.gdb"
print "My workspace", env.workspace
env.overwriteOutput = True
blockgroups = "BlockGroups"
landcover = "landcover"

# Step 2
print("Converting Block Groups from Polygon to Raster")
#Convert Block Group to Polygon on Population Field, output popu10
arcpy.PolygonToRaster_conversion(BlockGroups, "POP10", "popu10")


# Step 3
print("Reclassifying landcover raster")
print("Setting local variables")
inRaster = landcover
reclassField = "VALUE"
# See README for more information on the following step
remap = RemapValue([[1, 15], [2, 65], [3, 5], [4, 10], [5, 5], [6, 0]])

print("Executing reclassify")
rdensity = Reclassify(inRaster, reclassField, remap, "NODATA")
print("Saving...")

rdensity.save(r"C:\data\data.gdb\rdensity")
print("Done saving.")

# Step 4
print("Tabulating Blockgroups Area")
# FIPS is the ID of each block group.
TabulateArea(BlockGroups, "FIPS", landcover, "VALUE", "lctab")

# Step 5

fields = ["Total", "P1", "P2", "P3", "P4", "P5", "E"]
print("Adding [ {} ] fields to lctab".format(', '.join(fields)))
for field in fields:
	arcpy.AddField_management("lctab", field, "DOUBLE")

# Step 6
expression = "!VALUE_1! + !VALUE_2! + !VALUE_3! + !VALUE_4! + !VALUE_5!"
print("Calculating totals")
arcpy.CalculateField_management("lctab", "Total", expression, "PYTHON_9.3")

# Step 7
expression1 = "!VALUE_1! / !Total!"
arcpy.CalculateField_management("lctab", "P1", expression1, "PYTHON_9.3")

expression2 = "!VALUE_2! / !Total!"
arcpy.CalculateField_management("lctab", "P2", expression2, "PYTHON_9.3")

expression3 = "!VALUE_3! / !Total!"
arcpy.CalculateField_management("lctab", "P3", expression3, "PYTHON_9.3")

expression4 = "!VALUE_4! / !Total!"
arcpy.CalculateField_management("lctab", "P4", expression4, "PYTHON_9.3")

expression5 = "!VALUE_5! / !Total!"
arcpy.CalculateField_management("lctab", "P5", expression5, "PYTHON_9.3")

# Step 8
expression6 = "!P1! * 15 + !P2! * 65 + !P3! * 5 + !P4! * 10 + !P5! * 5"
arcpy.CalculateField_management("lctab", "E", expression6, "PYTHON_9.3")

# Step 9

try:
    print "Trying to join..."
	# FIPS would be the ID of each Block Group.
    arcpy.JoinField_management(BlockGroups, "FIPS", "lctab", "FIPS")

except BaseException as e:
    print "Somehow that is throwing an execption. Moving on..."

print "Done joining."

# Step 10
arcpy.PolygonToRaster_conversion(BlockGroups, "Total", "total_ra")
arcpy.PolygonToRaster_conversion(BlockGroups, "E", "e_ra")

# Step 11
#------------------------
cellpopu = Raster("rdensity") * Raster("popu10") * 133.058 * (133.058 / (Raster("e_ra") * Raster("total_ra")))
cellpopu.save(r"C:\data\data.gdb\cellpopu")
