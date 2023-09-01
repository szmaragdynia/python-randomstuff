# this file shall merge (or improve and merge) previous approaches, and be used as one standalone script,without demanding from user any previous action on the gpx files

# this script is for cleaning up data from gps and calculating speed, so its useful in After Effects
# CSVs are saved after every stage, so that I can take a peek at what is going on

# Todos not necessarily in any particular order EXCEPT FIRST ONE 
# Todo: make it into separate modules. (this code begs refactorization)
    # This is utterly awful. But I want to merge it all first, so that it at least works - heavy problems should not occur since I have had logic already done from previous files. Should heavy issues arise, I will refactor code then.
# Todo: do this using pandas. I tried to do that, but it was overkill, I prioretise finishing this, and I already have "classic" logic - no need to waste time for learning pandas right now
# Todo: how I format indentation in print to file seems to be done in a bad manner. What is help of what I do, if I still need to calculate the length of string I want to indent? My design is probably choosen badly.
# Todo: replace "quit" with real error handling
# Todo: use next() or mere for loop - mixing measure with measures[i+1] is utterly poor style
# Todo: either look-ahead or look-backwards. I am mixing approaches with no reason (maybe there will come out one, but as of now, this is by accident (as far as I remember))


import time
from datetime import timedelta, datetime
# ----------------
from auxiliary import utils
from auxiliary.utils import logger
from auxiliary import constants
from auxiliary.constants import tab
import auxiliary.gpxFunctions as gpxFunctions
from auxiliary import duplicatesProcessingFunctions as duplicates
from auxiliary.populatingData import populateMissingData
from auxiliary.speedCalculation import calculateAndAssign

time_start = time.perf_counter()
logger(datetime.fromtimestamp(time.time()))

logger("\n\n~< ------reading and parsing gpx for further use-----") # ~<  is for my defined language in notepad++, which allows me to fold text
measures_list = gpxFunctions.makeDictFromGpx(40)  #input range end or leave empty for all
utils.saveDictListAsCsv(measures_list, constants.output_filename_step1_csv)

logger("\n\n~< -----REMOVING DUPLICATES-----")
duplicates.collect(measures_list)
duplicates.showIndexesToDelete(measures_list)
duplicates.checkIndexesToDeleteAgainstOriginalList(measures_list)   
duplicates.remove(measures_list)
utils.saveDictListAsCsv(measures_list, constants.output_filename_step2_csv)

logger("~< -----POPULATING MISSING DATA-----") 
measures_list_populated = populateMissingData(measures_list)
utils.saveDictListAsCsv(measures_list, constants.output_filename_step3_csv)
           
logger("~< -----CALCULATING SPEED-----")
measures_list_populated = calculateAndAssign(measures_list_populated)

utils.saveDictListAsCsv(measures_list_populated, constants.output_filename_step4_csv)
# ------------------------------------------------------------------------
#with open(path_to_files_dir + output_filename, 'w') as f:
#  json.dump(measures_list, f, indent=2)
# divide for AE!

logger("\n\n------------FINISHED------------") 
time_end = time.perf_counter()
elapsed_time_all =  timedelta(seconds=time_end - time_start)
logger("{0:<{1}}{2}".format('', 40, "[H:MM:SS.microsec]")) 
logger("{0:<{1}}{2}".format("Elapsed time:", 40, elapsed_time_all)) 


