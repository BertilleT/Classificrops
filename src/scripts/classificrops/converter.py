import csv 
import pandas as pd
import deepl
from fuzzywuzzy import fuzz, process
import numpy as np

##My global variables
matchingList = [] 
resultDf = pd.DataFrame()
resultDf = pd.DataFrame()
srcClasses = []
compareList = []

def classes(df):
    global srcClasses
    columns = list(df)
    for col in columns:
        if 'ID' not in col: 
            srcClasses.append(col)
    return srcClasses

def filter(df, col, filters):
    mydict = {f'(?i){word}':'' for word in filters}
    df[col+'_filtered'] = df[col].replace(mydict, regex=True)
    df[col+'_filtered'] = df[col+'_filtered'].str.replace(r'[^\w\s]+', '', regex=True)
    df[col+'_filtered'] = df[col+'_filtered'].str.replace('   ', ' ')
    df[col+'_filtered'] = df[col+'_filtered'].str.replace('  ', ' ')
    df[col+'_filtered'] = df[col+'_filtered'].str.strip()
    return df[col+'_filtered']

def translateWord(translator, word, language):
    result = translator.translate_text(word, target_lang=language)
    return result

def translateICC(df, lg):
    DEEPL_AUTH_KEY="47c6c989-9eaa-5b30-4ee6-b2e4f1ebd530:fx"
    translator = deepl.Translator(DEEPL_AUTH_KEY)
    df['label_'+lg.lower()+'_filtered'] = df['label_en_filtered'].apply(lambda crop: translateWord(translator, crop, lg) if (pd.notna(crop)) else crop)
    return df['label_'+lg.lower()+'_filtered']

def parserICCCode(x):
    return "".join(x.split('.'))
   
def matchRow(c,idS,src,trg,idT,threshold): 
    global matchingList
    #nb = 0
    if type(src) == str and type(trg) == str:
        '''srcA = src.split()
        length = len(srcA)
        trgA = trg.split()
        myList=[]
        for w in srcA:
            for x in trgA:
                myList.append([srcA.index(w),fuzz.ratio(w,x)])
        cols = ['index', 'sim']
        myDf = pd.DataFrame(myList, columns=cols)
        r = myDf.groupby('index')['sim'].max().reset_index()
        total = r['sim'].sum()
        nb = total / length'''
        nb = fuzz.token_set_ratio(src,trg)
        if nb > threshold: 
            matchingList.append([c,idS, src, trg, idT, nb])

def matchDf(srcDf,iccDf,threshold):
    for c in srcClasses: 
        srcDf2 = srcDf.drop_duplicates(subset = ['ID_' + c])
        srcDf2.apply(lambda x:iccDf.apply(lambda y: matchRow(c, x['ID_' + c],x[c],y.label_fr_filtered,y.group_code,threshold), axis=1), axis=1)

    cols = ['class_level_src', 'id_src',' words_src', 'words_trg', 'id_trg', 'similarity']
    mDf = pd.DataFrame(matchingList, columns=cols)
    idx = mDf.groupby(['id_src'])['similarity'].transform(max) == mDf['similarity']
    return mDf[idx]
    #return mDf

def spreadMatch(id_src,id_trg,sim):
    global resultDf
    resultDf.loc[resultDf.ID_GROUP_FR == id_src, 'ID_GROUP_ICC'] = id_trg
    resultDf.loc[resultDf.ID_GROUP_FR == id_src, 'similarity'] = sim


def incDepth(x): 
    global matchingDf
    ID_C = x.ID_CROPS_FR
    ID_G = x.ID_GROUP_ICC
    sim = x.similarity
    i = matchingDf.loc[matchingDf['id_src'] == ID_C]
    if len(i.index) != 0:
        if pd.isna(ID_G) or sim < i.similarity.iloc[0]:
            ID_G = i.id_trg.iloc[0]
    return ID_G

def spreadSim(id_src,sim):
    global resultDf
    resultDf.loc[resultDf.ID_CROPS_FR == id_src, 'similarity'] = sim

def compare(pathHandMade,computed,threshold):
    handmade = pd.read_csv(pathHandMade)
    compare = handmade.copy()
    compare.rename(columns={'ID_GROUP_ICC':'ID_GROUP_ICC_handmade'}, inplace=True)
    compare['ID_GROUP_ICC_computed'] = computed['ID_GROUP_ICC']
    compare2=compare.copy()

    booleanSerie = compare.apply(lambda x : True if (x.ID_GROUP_ICC_handmade==x.ID_GROUP_ICC_computed) else False,axis=1)
    booleanSerie2 = compare2.apply(lambda x : True if not (np.isnan(x.ID_GROUP_ICC_computed)) and (x.ID_GROUP_ICC_handmade!=x.ID_GROUP_ICC_computed)  else False,axis=1)
    booleanDf = booleanSerie.to_frame()
    booleanDf2 = booleanSerie2.to_frame()
    booleanDf = booleanDf.rename(columns = {0:'bool'})
    booleanDf2 = booleanDf2.rename(columns = {0:'bool'})

    tot = len(compare)
    match = booleanDf['bool'].sum()
    error = booleanDf2['bool'].sum()
    per = round((match*100)/tot)
    err = round((error*100)/tot)

    print('The conversion table computed with the threshold = ' + str(threshold) + ', fits to the expected output at ' + str(per) + '%.')
    print('The conversion script made '+str(err)+'%'+' of errors.')
    return (threshold,per)

def converter(pathCsv, lg, srcDepth, threshold):
    global resultDf
    global matchingDf
    global compareList
    ##Loading
    srcDf = pd.read_csv(pathCsv)
    iccDf = pd.read_csv('../../../data/ICC/ICC.csv')

    ##Listing
    classes(srcDf)

    ##Filtering1
    englishFilters=['other','crops',' and',' or','n.e.c.', 'spp','n.e.c']
    iccDf['label_en_filtered'] = filter(iccDf,'label_en',englishFilters)
    iccDf.replace('',np.nan,regex = True,inplace=True)
        
    iccDf.to_csv('../../../data/ICC/ICC.csv', index=False)

    ##Filtering2
    frenchFilters = ['autres','autre',' et ',' ou ']
    for c in srcClasses:
        srcDf[c] = filter(srcDf,c,frenchFilters)

    ##Translating
    if 'label_'+lg.lower()+'_filtered' not in list(iccDf.columns):
        iccDf['label_'+lg.lower()+'_filtered'] = translateICC(iccDf, lg)
        iccDf.to_csv('../../../data/ICC/ICC.csv', index=False)

    ##Formating
    iccDf['code'] = iccDf['code'].apply(lambda code:parserICCCode(code))
    iccDf['code'] = iccDf['code'].astype('int')
    iccDf['group_code'] = iccDf['code'].astype('str').str[:1].astype('int')

    ##Initializing
    resultDf = srcDf[['ID_CROPS_FR', 'ID_GROUP_FR']]

    ##Matching all
    matchingDf = matchDf(srcDf,iccDf,threshold)

    ##Spreading
    rows = matchingDf.loc[matchingDf['class_level_src'] == 'GROUP_FR']
    rows2 = rows.copy()
    rows2.apply(lambda x: spreadMatch(x.id_src, x.id_trg,x.similarity), axis=1)

    ##Incrementing depth   
    cp = matchingDf.copy()
    cp.apply(lambda x: spreadSim(x.id_src, x.similarity), axis=1)
    print(resultDf.head(50))
    resultDf['ID_GROUP_ICC'] = resultDf.apply(lambda x: incDepth(x), axis=1)

    #Writting result
    resultDf.to_csv('../../../data/FR/conversionTable_FR_scriptMade.csv', index=False)
    matchingDf.to_csv('../../../data/FR/matchingDf_FR_scriptMade.csv', index=False)
    resultDf['ID_GROUP_ICC'] = resultDf.loc[:, ['ID_GROUP_ICC']].astype(float)
    compareList.append(compare('../../../data/FR/conversionTable_FR_handMade.csv',resultDf,threshold))

converter('../../../data/FR/FR_2020.csv', 'FR', 1,99)