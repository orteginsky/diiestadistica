import pandas as pd

def anti_join(df1, df2, left_on, right_on):
    inner_join = pd.merge(df1, df2, left_on=left_on, right_on=right_on, how='inner')
    return df1[~df1[left_on].isin(inner_join[left_on])]
