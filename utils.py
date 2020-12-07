import pandas as pd
from collections import deque

def load_data(filename):
    df = pd.read_csv(filename, sep=',')
    return df

def create_queue(df, num=0, randomize=True):
    d = deque()
    df_cp = df.copy(deep=True)
    if randomize:
        df_for_set = df_cp.sample(frac=1).reset_index(drop=True)
    else:
        df_for_set = df_cp

    if num <= 0 or num > len(df_for_set.index):
        for i in df_for_set.index:
            d.append(df_for_set.loc[i,])
    else:
        for i in range(num):
            d.append(df_for_set.loc[i,])

    return d

def flagstring_to_bool(flag):
    dic = {"on": True, "off": False}
    return dic[flag]
