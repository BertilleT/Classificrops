import csv 

#we suppose that JECAM is already translated into french language. 
#goal : to associate french crop into a JECAM group
#table_source_path looks like ../../data/FR/FR_2020.csv
#country looks like FR
def converter(table_source_path, country): 
    #open and read the origin data from France into a dictionnary
    genericPath = 'path/to/data'
    with open(table_source_path, newline='') as sourceFile
    sourceDict = csv.DictReader(sourceFile)
    #create a dictionnary with those data
    # ...
    # to be done 
    # ...

    #open and read the target classes from JECAM into a dictionnary
    with open(genericPath + 'JECAM/JECAM_fr', newline='') as JECAMFile
    JECAMDict = csv.DictReader(JECAMFile)
    #create a dictionnary with those data
    # ...
    # to be done 
    # ...

    #create the conversion table into the folder of the country/region we are working with
    genericFileName = 'conversionTable'
    ext = '.csv'
    specificPath = country + '/' + genericFileName + '_' + country + ext
    path = genericPath + specificPath
    f = open(path, 'w')
    #add columns name
    writer = csv.writer(f)
    header = ['ID_CROPS_FR', 'ID_GROUP_JECAM']
    writer.writerow(header)
    
    result = NULL
    levels = ['GROUP', 'CROP', 'SUB-CROP', 'SUB-SUB-CROP']
    #for each crop from French classification
    for c in sourceDict:
        #for each word of the crop. For example if we have "blé tendre", we will scan first "blé". If we do not match any class for "blé", then we will scan "tendre". 
        for word in c["CROPS_FR"]:
            #matching step : first we try to match each w to a group (level 0). If there is no match, we go deeper, and try to match each w to each JECAM crop etc until the last level which is third one (sub-sub-crop). 
            for i in range(i, len(levels)-1 )

                result = select distinct GROUP_ID FROM JECAM_UE WHERE w in levels[i]+'_'+c
                if result !== NULL
                break
            break
        writer.writerow([c["ID_CROPS_FR"],result])

    return "The conversion table to convert classes from " + country + " to JECAM classes has been successfully created. Please follow the following path to download it : " + path


#the code below was written to avoid nested loops with recursivity
            '''
            i == 1
            if key_JECAM_group(country, i, w) !== NULL
                return key_JECAM_group(country, i, w)
            else 
                return key_JECAM_group(country, i+1, w)

def key_JECAM_group(c, i, w): 
    t = levels[i]+'_'+c
    result = c.execute('select distinct GROUP_ID FROM JECAM_UE WHERE w in t', t)
    return result

result = select distinct group_id from jecam where crop in group_lg
if result is null
    result = select distinct group_id from jecam where crop in crop_lg'''