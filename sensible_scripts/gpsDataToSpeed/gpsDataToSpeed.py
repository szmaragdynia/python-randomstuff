# this file shall merge (or improve and merge) previous approaches, and be used as one standalone script,without demanding from user any previous action on the gpx files

# this script is for cleaning up data from gps and calculating speed, so its useful in After Effects
# CSVs are saved after every stage, so that I can take a peek at what is going on

# Todos not necessarily in any particular order
# Todo: code in seperate modules needs further refactorization
# Todo: how I format indentation in print to file seems to be done in a bad manner. What is help of what I do, if I still need to calculate the length of string I want to indent? My design is probably choosen badly.
# Todo: replace "quit" with real error handling
# Todo: use next() or mere for loop - mixing measure with measures[i+1] is utterly poor style
# Todo: either look-ahead or look-backwards. I am mixing approaches with no reason (maybe there will come out one, but as of now, this is by accident (as far as I remember))
# Todo: do this using pandas. I tried to do that, but it was overkill, I prioretise finishing this, and I already have "classic" logic - no need to waste time for learning pandas right now

import time
import json
from datetime import timedelta, datetime
# ----------------
from auxiliary import utils
from auxiliary.utils import logger
from auxiliary import constants
import auxiliary.gpxFunctions as gpxFunctions
from auxiliary import duplicatesProcessingFunctions as duplicates
from auxiliary.populatingData import populateMissingData
from auxiliary.speedCalculation import calculateAndAssign
import auxiliary.graphing as graphs

time_start = time.perf_counter()
logger(datetime.fromtimestamp(time.time()))

# logger("\n\n~< ------READING AND PARSING GPX-----") # ~<  is for my defined language in notepad++, which allows me to fold text
# measures_list = gpxFunctions.makeDictFromGpx()  #input range end or leave empty for all
# utils.saveDictListAsCsv(measures_list, constants.output_filename_step1_csv)




# # this is separetely from gpx, because of semantics
# logger("\n\n ------OFFSETTING TIME-----") #
# utils.offsetTime(measures_list, delta_hours=3, delta_minutes=0, delta_seconds = 0) # writing arguments with zero as reminder for future myself that I made these possible to set up



# logger("\n\n~< -----REMOVING DUPLICATES-----")
# returned = duplicates.collect(measures_list)
# if returned != "NoEntriesToDelete":
#   duplicates.showIndexesToDelete(measures_list)
#   duplicates.checkIndexesToDeleteAgainstOriginalList(measures_list)   
#   duplicates.remove(measures_list)
# utils.saveDictListAsCsv(measures_list, constants.output_filename_step2_csv)

# gpxFunctions.saveDictToGPX(measures_list, constants.gpx_out_file_no_duplicates)


# logger("~< -----POPULATING MISSING DATA-----") 
# measures_list_populated = populateMissingData(measures_list)
# utils.saveDictListAsCsv(measures_list_populated, constants.output_filename_step3_csv)

# gpxFunctions.saveDictToGPX(measures_list_populated, constants.gpx_out_file_populated)
                           
           
# logger("~< -----CALCULATING SPEED-----")
# measures_list_populated = calculateAndAssign(measures_list_populated)

# utils.saveDictListAsCsv(measures_list_populated, constants.output_filename_step4_csv)

# logger("~< -----MAKING PROPER JSONs-----")
# #dividing for AE (max 3hours)
# n_files = (len(measures_list_populated)//10800) + 1 # 10800 is seconds in 3 hours. I truncate and add one.

# for n in range(1, n_files+1):
#   range_start = 0 + 10800 * (n - 1)
#   range_end = 10799 + 10800 * (n - 1) + 1
#   with open(f"{constants.path_to_files_dir}{constants.output_filename_step5_json}-{n}of{n_files}.json", 'w') as f:
#     json.dump(measures_list_populated[range_start : range_end], f, indent=2)


#this below is a mess, I am tired and I want it working right now. My apologies to your eyes.

# logger("~< -----GRAPHING-----")
n_files = 4
# for n in range(1, n_files+1):
#   graphs.save_speeds_graph(f"{constants.path_to_files_dir}{constants.output_filename_step5_json}-{n}of{n_files}.json")


path_to_kubas = r"E:\NOWE SERCE ŻYCIA\Menu życia\F Outdoorsy\zepp life i strava do after effects\kuby\podejscie 2 full automacja\\"
path_to_mine = r"E:\NOWE SERCE ŻYCIA\Menu życia\F Outdoorsy\zepp life i strava do after effects\moje, strava\podejscie 2 full automacja\\"

for n in range(1, n_files+1):
  utils.logger(f"------------------------------------------------")
  utils.logger(f"json file number {n}")
  last_file = False
  if n == n_files:
    last_file = True
  graphs.save_speeds_graphs(f"{path_to_kubas}kubaORG__5-{n}of{n_files}.json", 
                            f"{path_to_mine}Przehyba_z_Kuba_rower__5-{n}of{n_files}.json",
                            is_last_file = last_file)

#graphs.save_speeds_graph(f"{constants.path_to_files_dir}Przehyba_z_Kuba_rower__5-1of4.json")
#graphs.save_speeds_graphs(f"{constants.path_to_files_dir}Przehyba_z_Kuba_rower__5-1of4.json",)






logger("\n\n------------FINISHED------------") 
time_end = time.perf_counter()
elapsed_time_all =  timedelta(seconds=time_end - time_start)
logger("{0:<{1}}{2}".format('', 40, "[H:MM:SS.microsec]")) 
logger("{0:<{1}}{2}".format("Elapsed time:", 40, elapsed_time_all)) 



