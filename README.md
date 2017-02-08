This script uses a dasymetric mapping technique to disaggregate population data and create a map of population density. Please read Holloway et al. (1997) Dasymetric Mapping Using Arc/Info for methods.

This specific script is was hardcoded to use the 2006 landcover map derived from Landsat imagery (MRLC) and 2010 census block group data from Beaverton, Oregon. Input included a landuse dataset that had 6 values for land use. The landuse dataset included (1) low density residential, (2) high density residential, (3) commercial/industrial, (4) agriculture, (5) natural, and (6) water/wetland. Each used a weighted relative density, which can be found in step 3 of the script, as follows: (1) = 15%, (2) = 65%, (3) = 5%, (4) = 10%, (5) = 5%, and (6) = 0%.

The lab that this script is based on was written by the Portland State University Geography Department.
