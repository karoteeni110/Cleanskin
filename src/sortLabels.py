import pandas as pd
from paths import data_path, results_path
from os.path import join

def read_one_result(result_txt_path):
    with open(result_txt_path, 'r') as f:
        df = pd.read_csv(f, sep=" ", index_col='heading',names=['heading','label'], dtype=str)
    return df # dict(zip(df.heading, df.label)) 

def merge_to_three_cols(df1, df2, df3):
    """
    >>> print(x)
                                     label_x       label_y         label
    heading                                                                 
    introduction                    introduction  introduction  introduction
    conclusion                        conclusion    conclusion    conclusion
    related_work                    related_work  related_work  related_work
    conclusions                       conclusion    conclusion    conclusion
    experiments                          results       results       results
    ...                                      ...           ...           ...
    achievability_proof_of_theorem       methods       methods       methods
    notation_and_basic_definitions    background    background    background
    numerical_algorithm                  methods       methods       methods
    system_modeling                      methods       methods       methods
    open_challenges                   conclusion    conclusion    conclusion

    [1013 rows x 3 columns]
    """
    x = pd.merge(df1,df2,on='heading',how='inner')
    x = pd.merge(x,df3,on='heading',how='inner')
    x.label = x.label.str.cat([x.label_x,x.label_y],sep=',')
    x = x.drop(['label_x','label_y'],axis=1)
    x.label = 
    return x

if __name__ == "__main__":
    ay_path, al_path, do_path = join(data_path, 'AY_RESULTS.txt'), join(data_path, 'ALAN_RESULTS.txt'), join(data_path, 'DOROTA_RESULTS.txt')
    ay_df, al_df, do_df = read_one_result(ay_path), read_one_result(al_path), read_one_result(do_path)
    print()