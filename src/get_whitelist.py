import pandas as pd
import numpy as np
from os import listdir
from kldiv import get_pid2cate_dict, get_acro2cate_dict

code2cat = {                                                                                                                                                                          'cs.LG' : "Machine Learning",                                                                                                                                                     'cs.NE' : "Evolutionary Computing",                                                                                                                                               'cs.NA' : "Numerical Analysis",                                                                                                                                                   'cs.PF' : "Performance",                                                                                                                                                      
    'cs.PL' : "Programming Languages",                                                                                                                                            
    'cs.CC' : "Computational Complexity",                                                                                                                                         
    'cs.RO' : "Robotics",                                                                                                                                                         
    'cs.CL' : "Computation and Language",                                                                                                                                         
    'cs.GR' : "Graphics",                                                                                                                                                         
    'cs.GT' : "Game Theory",                                                                                                                                                      
    'cs.NI' : "Networking and Internet",                                                                                                                                          
    'cs.CE' : "Computational Science",                                                                                                                                            
    'cs.IT' : "Information Theory",                                                                                                                                               
    'cs.CG' : "Computational Geometry",                                                                                                                                           
    'cs.IR' : "Information Retrieval",                                                                                                                                            
    'cs.AI' : "Artificial Intelligence",                                                                                                                                          
    'cs.AR' : "Hardware Architecture",                                                                                                                                            
    'cs.CY' : "Computers and Society",                                                                                                                                            
    'cs.CV' : "Computer Vision",                                                                                                                                                  
    'cs.GL' : "General Literature",                                                                                                                                               
    'cs.CR' : "Cryptography and Security",                                                                                                                                        
    'cs.OH' : "Other Computer Science",                                                                                                                                           
    'cs.MA' : "Multiagent Systems",                                                                                                                                               
    'cs.SY' : "Systems and Control",                                                                                                                                              
    'cs.MM' : "Multimedia",                                                                                                                                                       
    'cs.MS' : "Mathematical Software",                                                                                                                                            
    'cs.LO' : "Logic",                                                                                                                                                            
    'cs.SD' : "Sound",                                                                                                                                                            
    'cs.SE' : "Software Engineering",                                                                                                                                             
    'cs.OS' : "Operating Systems",                                                                                                                                                
    'cs.SC' : "Symbolic Computation",                                                                                                                                             
    'cs.DM' : "Discrete Mathematics",                                                                                                                                             
    'cs.DL' : "Digital Libraries",                                                                                                                                                
    'cs.DC' : "Distributed Computing",                                                                                                                                            
    'cs.DB' : "Databases",                                                                                                                                                        
    'cs.ET' : "Emerging Technologies",                                                                                                                                            
    'cs.DS' : "Data Structures and Algorithms",                                                                                                                                   
    'cs.FL' : "Formal Languages",                                                                                                                                                 
    'cs.HC' : "Human-Computer Interaction",                                                                                                                                       
    'cs.SI' : "Social Networking"                                                                                                                                                 
}
CATEDICT = get_pid2cate_dict(metaxml_list=['Computer_Science.xml'])

def cate_count(catelist):
    a = np.concatenate(catelist.cate.to_numpy())
    a = pd.Series(a)
    return a.value_counts()

def main(threshold):
    print('Reading pids...')
    ft_df = pd.DataFrame(listdir('/home/ad/home/y/yzan/Desktop/Cleanskin/results/cs_lbsec/cs_ft'), 
                columns=['pid'])\
                    .apply(lambda x: x[0][:-4],axis=1,result_type='broadcast')
    catelist = pd.concat([ft_df, ft_df.pid.map(CATEDICT).rename('cate')],axis=1).dropna()
    cate_freq = cate_count(catelist)

    while len(cate_freq[cate_freq>3000]) > 0:
        cate_to_sample, how_many = cate_freq.index[0], cate_freq[0] # the most frequent cate
        cate_blacklist_idx = catelist[catelist.cate.apply(lambda x: cate_to_sample in x)].sample(n=how_many-threshold).index
        catelist = catelist.drop(cate_blacklist_idx) # update catelist
        cate_freq = cate_count(catelist)# update cate_freq
    
    catelist.pid.to_csv('whitelist.txt', index=False)

    for acrocate in pd.Series(code2cat.keys()).apply(lambda x: x[-2:]):
        cate_ids = catelist[catelist.cate.apply(lambda x: acrocate in x)]
        cate_counts = len(cate_ids)
        # if cate_counts > threshold:

    # a= pd.Series(catelist).map(acro2cate)


    acro2cate = get_acro2cate_dict()
    # print(a.value_counts())

if __name__ == "__main__":
    main(threshold=3000)