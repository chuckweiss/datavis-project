import pandas as pd

def buildDataFrames(data):
    result = {}
    for subject_id in data:
        dataframes = []
        for pathname in data[subject_id]:
            dataframes.append(pd.read_csv(pathname + '\\summary.csv'))
        result[subject_id] = pd.concat(dataframes)
    return result
