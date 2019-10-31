import pandas as pd
from paths import fulltext_dir
from os.path import listdir

def get_pid_series(pickfrompath=fulltext_dir):
    paperfns = listdir(pickfrompath)
    pids = pd.Series(paperfns)
