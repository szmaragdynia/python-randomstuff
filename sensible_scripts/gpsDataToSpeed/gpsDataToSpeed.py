# this file shall merge (or improve and merge) previous approaches, and be used as one standalone script,without demanding from user any previous action on the gpx files
# this script is for cleaning up data from gps, in order for it to work somehow in after effects

# Todos not necessarily in any particular order EXCEPT FIRST ONE 
# Todo: make it into separate modules. (this code begs refactorization)
    # This is utterly awful. But I want to merge it all first, so that it at least works - heavy problems should not occur since I have had logic already done from previous files. Should heavy issues arise, I will refactor code then.
# Todo: do this using pandas. I tried to do that, but it was overkill, I prioretise finishing this, and I already have "classic" logic - no need to waste time for learning pandas right now
# Todo: how I format indentation in print to file seems to be done in a bad manner. What is help of what I do, if I still need to calculate the length of string I want to indent? My design is probably choosen badly.
# Todo: replace "quit" with real error handling
# Todo: use next() or mere for loop - mixing measure with measures[i+1] is utterly poor style
# Todo: either look-ahead or look-backwards. I am mixing approaches with no reason (maybe there will come out one, but as of now, this is by accident (as far as I remember))

# perhaps should have used virtual environment
import time
time_start = time.time()
from datetime import timedelta, datetime
from auxiliary.utils import logger
logger(datetime.fromtimestamp(time_start))
import copy, math, numpy as np
from geopy import distance
# ----------------
from auxiliary import utils
from auxiliary.constants import tab
from auxiliary import constants
import auxiliary.gpxFunctions as gpxFunctions
from auxiliary import duplicatesProcessingFunctions as duplicates

logger("\n\n~< ------------------------reading and parsing gpx for further use------------------------")
time_start_gpx = time.time()


measures_list = gpxFunctions.makeDictFromGpx(range=30)
# saving at this stage, so that I can take a peek at what is going on
utils.saveDictListAsCsv(measures_list, constants.output_filename_step1_csv)

time_end_gpx = time.time()
logger("\n\n~< ------------------------REMOVING DUPLICATES------------------------") # ~<  is for my defined language in notepad++, which allows me to fold text
duplicates.collect(measures_list)
time_end_collecting_dupes = time.time()

duplicates.showIndexesToDelete(measures_list)

time_start_o2 = time.time()
duplicates.checkIndexesToDeleteAgainstOriginalList(measures_list)
time_end_o2 = time.time()
    
duplicates.remove(measures_list)

utils.saveDictListAsCsv(measures_list, constants.output_filename_step2_csv)
           
time_end_everything_dupes = time.time()
# -------------------------------------------- populating missing data --------------------------------------------
# After effects expects data every second. I need data every second, even if data is empty or fake. We will copy previous values
logger("~< ------------POPULATING MISSING DATA------------") 

measures_list_populated = copy.copy(measures_list)
added_entries_so_far = 0                                            # necessary to know how many items were added so far, for keeping proper indexes in output dictionary
                                                                    # I could go backwards...but I had gone forwards previously and now I will just reuse the logic.                                                               
for i, measure in enumerate(measures_list[:-1]):                    # iterate over all except last, because it does not have the next element
    digs_msr = utils.nDigitsToWriteDownIndex(measures_list)
    logger("{0}/{1:<{2}}=new list index={3}".format(len(measures_list) - 1, i, digs_msr, i+added_entries_so_far))
    
    current_datetime = datetime.fromisoformat(measure["datetimeISO8601"])
    next_datetime = datetime.fromisoformat(measures_list[i+1]["datetimeISO8601"])
    time_difference_in_seconds = (next_datetime - current_datetime).total_seconds()
        #total seconds returns float (Because its datetime/timedelta(seconds=1) under the hood, so you could have ...seconds=3)
        # mere (next_datetime - current_datetime) is of type timedelta, created from two datetime type objects
    if time_difference_in_seconds.is_integer():
            time_difference_in_seconds = int(time_difference_in_seconds)
    else:
        logger("\n\n\nGetting total seconds out of difference between two measures, total seconds resulting came out NOT TO BE integeres. Program will now quit.")
        exit()
    # these work
        #logger(next_datetime.date())
        #logger("{}".format(next_datetime.date()))
    # but neither of these do: 
        #logger(f"{next_datetime.date():>20}")
        #logger("{:>4}".format(next_datetime.date()))
    # I do not need now to inspect and explore this

    logger("{0}{1:<{2}}{3:<{4}} - current element datetime."
           .format(tab, current_datetime.date().isoformat(), 18, current_datetime.time().isoformat(),  16),
           stream="fileOnly") # magic numbers out of string lengths
    logger("{0}{1:<{2}}{3:<{4}} - next element datetime."
           .format(tab, next_datetime.date().isoformat(), 18, next_datetime.time().isoformat(), 16)
           ,stream="fileOnly")
    logger("{0:<{1}}{2} - number of entries added so far."
           .format('', 16, added_entries_so_far), stream="fileOnly") #tab and then the same amount of space as in previous line
    
    if time_difference_in_seconds > 1:
        n_missing_entries = time_difference_in_seconds - 1
        if n_missing_entries < 5:
            logger("{0:<{1}}{2} missing (Time difference bigger than 1 second occured)."
           .format('', 16, n_missing_entries), stream="fileOnly") 
        elif n_missing_entries >=5:
            logger("~< {0:<{1}}{2} missing (Time difference bigger than 1 second occured)."
           .format('', 16, n_missing_entries), stream="fileOnly") 
        for j in range(n_missing_entries):
            insert_before_index = (i + 1) + added_entries_so_far    # with every entries added previously, the index from the dictionary list python is reading from differs from the dictionary list python is writing to. 
            measure_copy = measure.copy()
            logger("~<", stream="fileOnly")
            logger("{0:<{1}}{2}/{3}".format('',16, n_missing_entries, j+1))
            logger("{0:<{1}}Object to be inserted, BEFORE updating its data:".format('',16), stream = "fileOnly")
            logger("{0}{1:<{2}}{3}".format(tab,'', 16, measure_copy), stream = "fileOnly")
            measure_copy["datetimeISO8601"] = (datetime.fromisoformat(measure["datetimeISO8601"]) + timedelta(seconds=1+j)).isoformat()
            measure_copy["original_data"] = False
            logger("{0:<{1}}Object to be inserted, AFTER updating its data:".format('',16), stream = "fileOnly")
            logger("{0}{1:<{2}}{3}".format(tab,'', 16, measure_copy), stream = "fileOnly")
            logger("{0:<{1}}It will be insterted before index: {2}".format('',16, insert_before_index), stream = "fileOnly")
            logger("{0}{1:<{2}} which holds this object:".format(tab, '', 16, ), stream = "fileOnly")
            logger("{0}{1:<{2}}{3}".format(tab,'', 16, measures_list_populated[insert_before_index]), stream = "fileOnly")
            measures_list_populated.insert(insert_before_index, measure_copy)    #insert before (i+1)-th element
            logger("\n{0:<{1}}Now object in the index {2} is: ".format('', 16,insert_before_index-1), stream="fileOnly" )
            logger("{0}{1:<{2}}{3}".format(tab, '', 16, measures_list_populated[insert_before_index-1]), stream = "fileOnly")
            logger("\n{0:<{1}}Now object in the index {2} is: ".format('', 16,insert_before_index), stream="fileOnly" )
            logger("{0}{1:<{2}}{3}".format(tab, '', 16, measures_list_populated[insert_before_index]), stream = "fileOnly")
            logger("\n{0:<{1}}Now object in the index {2} is: ".format('', 16,insert_before_index+1), stream="fileOnly" )
            logger("{0}{1:<{2}}{3}".format(tab, '', 16, measures_list_populated[insert_before_index+1]), stream = "fileOnly")
            logger("~>", stream="fileOnly")
            added_entries_so_far = added_entries_so_far + 1 #keeping track of how many more entries there are in the output dictionary list
        if n_missing_entries >= 5:
            logger("~>",stream = "fileOnly")
    elif time_difference_in_seconds == 0:                                   
            logger("\n\n\nBug, the previous step (deleting duplicates) seems to have failed. Program will now exit.")
            exit()
    elif time_difference_in_seconds < 0:                                   
            logger("\n\n\nSerious bug! Next time is earlier than previous time! Program will now exit.")
            exit()
logger("~>",stream = "fileOnly")


utils.saveDictListAsCsv(measures_list, constants.output_filename_step3_csv)
           
time_end_populating_missing = time.time()
# -------------------------------------------- calculating speed  --------------------------------------------
logger("~< ------------ CALCULATING SPEED ------------")
# latitude and longitude are given each second (Be they fake or real)

#this definition here is temporary, it will be moved to separate file or will be deleted (it might not be useful even for showcasing)
#source: bing. Checked that with wikipedia.
def haversine(lat1, lon1, lat2, lon2, lib=math):
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(lib.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = lib.sin(dlat / 2) ** 2 + lib.cos(lat1) * lib.cos(lat2) * lib.sin(dlon / 2) ** 2
    if (lib == np):
        c = 2 * lib.arctan2(lib.sqrt(a), lib.sqrt(1 - a))
    else:
        c = 2 * lib.atan2(lib.sqrt(a), lib.sqrt(1 - a))
    r = 6371000 # Radius of the Earth in meters
    distance_m_speed = c * r # this is at the same time speed in m/s, because measures are taken every second
    speed_kmh = distance_m_speed * 3.6 # 3.6 is coefficient for transforming from m/s to km/h
    
    return round(speed_kmh, 1)

def calculate_speeds(lat1, lon1, lat2, lon2):
    return {
        "haversine_math": haversine(lat1, lon1, lat2, lon2, lib=math),
        "haversine_np": haversine(lat1, lon1, lat2, lon2, lib=np),
        "geopy_geodesic": round(distance.distance((lat1, lon1),(lat2, lon2)).meters * 3.6, 1),    #coefficient m/s->kmh/h
        "geopy_great_circle": round(distance.great_circle((lat1, lon1),(lat2, lon2)).meters * 3.6, 1),
        
    }


n_entries = len(measures_list_populated)

speeds = calculate_speeds(0, 0, 0, 0) # dummy value
for key in speeds:
    measures_list_populated[0]['speed_kmh'+'_'+key] = speeds[key]
measures_list_populated[0]['speed_source'] = "dummy value"

i=1
while i < n_entries: #iterate from 2nd because we append speed to second element from pair it was calculated from, and it is convenient in code to look bacwards
    logger(n_entries-1,"/",i, sep='')

    # we need to take care of fake (copied) values, because they make speed constant and just before real value - very large. 
    # we need to take the last real speed value before fake values, and then the first real speed value after fake values, and intepolate (poor man's:linearly) in the fake-value objects, so we have gradual change of speed
    # assumptions: 1. before any fake-entries, there is at least one real one with appriopriate geolocation data 
    #              2. after fake-entries, there are at least TWO real ones with appriopriate geolocation data (two because we want to calculate real speed to interpolate from)

    # I dont understand this comment, I must have been extremely tired. I am leaving this for now - will delete if I finish everything and this will not come in handy:
        # if second entry is false then we would need dummy speed val in the first element, but this might not make sense if began recording while on the move, because then average speed would make more sense.

    if measures_list_populated[i]['original_data'] == True:
        latitude_now = measures_list_populated[i]['latitude_deg']
        longitude_now = measures_list_populated[i]['longitude_deg']
        
        latitude_prev = measures_list_populated[i-1]['latitude_deg']
        longitude_prev = measures_list_populated[i-1]['longitude_deg']
        
        speeds = calculate_speeds(latitude_prev, longitude_prev, latitude_now, longitude_now)
        for key in speeds:
            measures_list_populated[i]['speed_kmh'+'_'+key] = speeds[key]
        measures_list_populated[i]['speed_source'] = "[T->T->T...]"
        logger("{0}[T->T->T...]".format(tab),stream="fileOnly")
        logger("{0}{1}".format(tab,measures_list_populated[i]['datetimeISO8601']),stream="fileOnly")
    elif (measures_list_populated[i])['original_data'] == False:
        #search for first not-fake and determine number of fakes
        j = i
        while (measures_list_populated[j]['original_data'] == False):
            j += 1 
        # after 'while' lopo, j is first not-fake
        # if second element after TRUE exists and if that element is also TRUE [t f f f f {T T}] 
        if (j + 1 < n_entries-1 and measures_list_populated[j+1]['original_data'] == True): 
            # calculate the speed for the second original_data=True basing on first and second original_data=True and insert it into second
            latitude_now = (measures_list_populated[j+1])['latitude_deg']
            longitude_now = (measures_list_populated[j+1])['longitude_deg']
            
            latitude_prev = (measures_list_populated[j])['latitude_deg']
            longitude_prev = (measures_list_populated[j])['longitude_deg']

            speeds = calculate_speeds(latitude_prev, longitude_prev, latitude_now, longitude_now)
            for key in speeds:
                measures_list_populated[j+1]['speed_kmh'+'_'+key] = speeds[key]
            (measures_list_populated[j+1])['speed_source'] = "[T->T->T...]"
            logger("{0}Once for {1}/{2}: [T->T->T...]".format(tab,n_entries,j+1),stream="fileOnly")
            logger("{0}{1}".format(tab,measures_list_populated[j+1]['datetimeISO8601']),stream="fileOnly")

            # now lets interpolate speed for all fake values and first true value
            number_of_fakes = j-i # because j points at first TRUE after last fake [which does not hold instantenous speed value], and i points at first fake [which does not hold instantenous speed value]
            magic_number = 2 # well...it just should be like that.
            speed_change_every_second = {}
            for key in speeds:
                speed_change_every_second['speed_kmh'+'_'+key] = ((measures_list_populated[j+1])['speed_kmh'+'_'+key] - (measures_list_populated[i-1])['speed_kmh'+'_'+key])/(number_of_fakes+magic_number)
            # now insert interpolated speeds
            k=0
            # while the main iterator (i) is not yet the same as  look-ahead-iterator (j), which (j) points to first not fake, which needs interpolated speed as well
            while i <= j:
                logger(n_entries-1,"/",i, sep='')
                for key in speeds:
                    (measures_list_populated[i])['speed_kmh'+'_'+key] = round((measures_list_populated[i-1])['speed_kmh'+'_'+key] + speed_change_every_second['speed_kmh'+'_'+key])
                (measures_list_populated[i])['speed_source'] = "interpolated speed [T T->{F F F F T}-> T]"
                logger("{0}interpolated speed [T T->{{F F F F T}}-> T]".format(tab),stream="fileOnly")
                logger("{0}{1}".format(tab,measures_list_populated[i]['datetimeISO8601']),stream="fileOnly")
                i += 1
            i -= 1 #compensation - we incremented once too much and thanks to that quit 'while', but we want to increment into the next (first unchecked so far) element at the end of the main loop
        # if second element after FALSE is FALSE, despite first being TRUE [t f f f f {T f}]
        # then we dont have enough data points to calculate speed for "T", and simpliest thing we can do is to use average speed throughout the entire false-scope, basing on difference in coordinates between 2 real measures
        # in the future I could interpolate speeds more properly - that is: maybe look at previous true speed values and use them to calculate the speed that must had been kept over the distance that is 'fake'
        elif (j + 1 < n_entries-1 and measures_list_populated[j+1]['original_data'] == False): 
            # j is still first not-fake
            # i is first fake
            # calculate the AVERAGE speed basing on STRAIGHT LINE DISPLACEMENT for each missing element, basing on pre-fake realvalue and on post-fake realvalue and insert it into proper place
            latitude_now = (measures_list_populated[j])['latitude_deg']
            longitude_now = (measures_list_populated[j])['longitude_deg']
            
            latitude_prev = (measures_list_populated[i-1])['latitude_deg']
            longitude_prev = (measures_list_populated[i-1])['longitude_deg']
            speeds = calculate_speeds(latitude_prev, longitude_prev, latitude_now, longitude_now)

            while i <= j:
                logger(n_entries-1,"/",i, sep='')
                for key in speeds:
                    measures_list_populated[i]['speed_kmh'+'_'+key] = speeds[key]
                (measures_list_populated[i])['speed_source'] = "average straight line displacement [{T->(F F F F)->T F}]"
                logger("{0}average straight line displacement [{{T->(F F F F)->T F}}]".format(tab),stream="fileOnly")
                logger("{0}{1}".format(tab,measures_list_populated[i]['datetimeISO8601']),stream="fileOnly")
                i += 1
            i -= 1 #compensation - we incremented once too much and thanks to that quit 'while', but we want to increment into the next (first unchecked so far) element 
    i += 1



utils.saveDictListAsCsv(measures_list_populated, constants.output_filename_step4_csv)

time_end_calculating_speed = time.time()
# ------------------------------------------------------------------------
#with open(path_to_files_dir + output_filename, 'w') as f:
#  json.dump(measures_list, f, indent=2)
# divide for AE!

time_end = time.time()
elapsed_time_all =  timedelta(seconds=time_end - time_start)
elapsed_time_gpx = timedelta(seconds=time_end_gpx - time_start_gpx)
elapsed_time_everything_dupes = timedelta(seconds=time_end_everything_dupes - time_end_gpx)
elapsed_time_collecting_dupes = timedelta(seconds=time_end_collecting_dupes - time_end_gpx)
elapsed_time_o2 = timedelta(seconds=time_end_o2 - time_start_o2)
elapsed_time_populating_missing = timedelta(seconds=time_end_populating_missing - time_end_everything_dupes)
elapsed_time_calculating_speed = timedelta(seconds=time_end_calculating_speed - time_end_populating_missing)


logger("\n\n------------FINISHED------------") 

logger("{0:<{1}}{2}".format('', 40, "[H:MM:SS.microsec]")) 
logger("{0:<{1}}{2}".format("Elapsed time:", 40, elapsed_time_all)) 

logger("{0}{1:<{2}}{3}".format(tab, "....parsing gpx:", 36, elapsed_time_gpx)) 
logger("{0}{1:<{2}}{3}".format(tab, "....processing duplicates:", 36, elapsed_time_everything_dupes)) 
logger("{0}{1:<{2}}{3}".format(2*tab, "....collecting duplicates:", 32, elapsed_time_collecting_dupes)) 
logger("{0}{1:<{2}}{3}".format(2*tab, "....printing o2:", 32, elapsed_time_o2)) 
logger("{0}{1:<{2}}{3}".format(tab,"....populating missing:", 36, elapsed_time_populating_missing)) 
logger("{0}{1:<{2}}{3}".format(tab,"....calculating speed:", 36, elapsed_time_calculating_speed)) 



