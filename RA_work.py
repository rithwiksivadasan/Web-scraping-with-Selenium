#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 00:15:51 2022

@author: rithwiksivadasan
"""
#notes

'''new line characters in biography that are not getting filtered out '''

'''In case of some Athletes, athlete page captures followers as 0 while social_url 
has different value eg: chris williams hence code retirves 0 while the link to profile 
lands on public page with details, inst handle to be used to get the followers.'''

''' Unable to use fuzzywuzzy modlue and levenshtein distance for matching with thresholds'''
'''Have to try using Jaro wrinkler' '''

'''athlete profiles are scrapped from top 50 pages'''



# fuzzy logic to be checked for name matching 
#names to be stitched together - done
#biography as well to be extracted - done
#name discrepancies to be mentioned in new column, namechange = 1
#additional column for instagram and twitter handles - done


#'no account' in case of Null values- done but not 100% accurate


import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import difflib 



url = "https://opendorse.com/"

first_name=[]
last_name=[]
instagram_reach=[]
twitter_reach=[]
current_team=[]
profile_link=[]
instagram_handle=[]
twitter_handle=[]
biography=[]
page_num="page="
prev_page="page=1"



for i in range (1,200):

    page_num=page_num+str(i)
    
    url=re.sub(prev_page,page_num,url)

    
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    
    #print(soup.prettify())
    
    #table = soup.find('div')#, attrs = {'id':'firstName'}) 
    
    row = soup.find_all(('script'), attrs = {'type':'application/json'})
    
    line=row[0]
    st=str(line)
    
    list1 =st.split('}')
    
    
    
    for i in range(0,len(list1)):
         if 'firstName' in list1[i]:
             sample_list=[]
             #print(re.findall('(?<=\"firstName\":\").*?(?=\")',list1[i]))
             key= str(re.findall('(?<=\"firstName\":\").*?(?=\")',list1[i]))
             special_characters=[']','[',"'"]
             for i in special_characters:
                 key=key.replace(i,"")
             
             first_name.append(key)
     
    
    for i in range(0,len(list1)):
         if 'lastName' in list1[i]:
             sample_list=[]
             
             key= str(re.findall('(?<=\"lastName\":\").*?(?=\")',list1[i]))
             special_characters=[']','[',"'"]
             for i in special_characters:
                 key=key.replace(i,"")
             
             last_name.append(key)
             
             
    for i in range(0,len(list1)):
        if 'lastName' in list1[i]:
            key= str(re.findall('(?<=\"currentTeams\":\[\").*?(?=\")',list1[i]))
            special_characters=[']','[',"'"]
            for i in special_characters:
                key=key.replace(i,"")
            current_team.append(key)
                   
      
    for i in range(0,len(list1)):
         if 'lastName' in list1[i]:
             sample_list=[]
             
             key= str(re.findall('(?<=\"twitterReach\":).*?(?=\,)',list1[i]))
             #print(key)
             special_characters=[']','[',"'"]
             for i in special_characters:
                 key=key.replace(i,"")
             if 'null' not in key:
                 key=int(key)
             else:
                 key='No Account'
                 
             twitter_reach.append(key)          
    
    
    
    for i in range(0,len(list1)):
         if 'lastName' in list1[i]:
             sample_list=[]
             
             key= str(re.findall('(?<=\"instagramReach\":).*?(?=\,)',list1[i]))
             #print(key)
             special_characters=[']','[',"'"]
             for i in special_characters:
                 key=key.replace(i,"")
             if 'null' not in key:
                 key=int(key)
             else:
                 key='No Account'
                 
             instagram_reach.append(key)                         
             
                   
    
        
    prof= soup.find_all(('div'), attrs = {'id':'__next'})             
    list2=str(prof[0]).split('</a>')
    list2=list2[4:]
        
    
    for i in range(0,32):
         if 'href' in list2[i]:
             sample_list=[]
             
             key= str(re.findall('(?<=href=\").*?(?=\")',list2[i]))
             #print(key)
             special_characters=[']','[',"'",'\n']
             for i in special_characters:
                 key=key.replace(i,"")
            
                 
             #profile_link.append(key)
             
             link='https://opendorse.com' + key
             
             profile_link.append(link)
             
             ath_page=BeautifulSoup(requests.get(link).content, "html.parser")
             
             ath_page_contend=str(ath_page.find_all('body'))
             
             inst_url=str(re.findall('(?<="instagramUrl\":\").*?(?=\")',ath_page_contend))
             
             for i in special_characters:
                 inst_url=inst_url.replace(i,"")
             instagram_handle.append(inst_url)
             
             twit_url=str(re.findall('(?<="twitterUrl\":\").*?(?=\")',ath_page_contend))
             
             for i in special_characters:
                 twit_url=twit_url.replace(i,"")
             twitter_handle.append(twit_url)
             
             
             bio=str(re.findall('(?<="biography\":\").*?(?=\")',ath_page_contend))
             
             for i in special_characters:
                 bio=bio.replace(i,"")
             biography.append(bio)
                
    
    prev_page=page_num
    page_num="page="

    

    
ath = {'first_name':first_name,'last_name':last_name,'current_team':current_team,'InstagramReach':instagram_reach,'twitterReach':twitter_reach,'instagramHandle':instagram_handle,'twitterHandle':twitter_handle,'biography':biography,'profileLink':profile_link}
        
df= pd.DataFrame(ath)

df['full_name']=df['first_name']+" " +df['last_name']


df.to_csv('scrapped2.csv', index=False)





















#men_file=pd.read_csv('menWithRace.csv')






















































#script=row.script id="__NEXT_DATA__" nonce="EMAid3tzbU6YKH/ZDci5cg==" type="application/json"

#y=json.dumps(row)

#data = json.loads(row)


#for line in row:
 #   print(line)

# for row in soup.find_all_next('div', attrs = {'class':'sc-e90ee035-0 doZzSQ'}):
#     print(row)
#     quote = {}
#     quote['first_name'] = row.h5.text
#     quote['last_name'] = row.a['href']
#     quote['inst_reach'] = row.img['src']
#     quote['twitter_reach'] = row.img['alt'].split(" #")[0]
   
#     profile.append(quote)






#print(re.findall(r'^.*? InstagramReach',doc))


#result = doc.find_all("__NEXT_DATA__" ,nonce="b0Ep2YiC1Ah0Oaa8IOH02w==" type="application/json")

#inst = doc.find_all(text="athletes")

#print(result)

#parent=inst.parent

#print(parent)

#tag=soup.find_all("InstagramReach")

#print(tag)


#tags to be found 
#firstname
#lastname
#twitterReach

#"instagramReach"

