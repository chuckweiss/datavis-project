from tkinter import filedialog as fd
import os
import pandas as pd


def parse_ProjectData(pathname):
    def list_files(dirpath, files=[]):
        for (curdir, dirs, filenames) in os.walk(dirpath):
            for file in filenames:
                files.append((file, curdir))
            if(len(dirs) > 0):
                for dir in dirs:
                    list_files(dir, files)
        return files

    def parse_data(files, keyword):
        data = {}
        for filename, dirpath in files:
            if filename == keyword:
                subject_id = os.path.basename(dirpath)
                if subject_id in data:
                    data[subject_id].append(dirpath)
                else:
                    data[subject_id] = [dirpath]
        return data

    files = list_files(pathname)

    return parse_data(files, 'summary.csv')


def build_DataFrames(data):
    result = {}
    for subject_id in data:
        dataframes = []
        for pathname in data[subject_id]:
            dataframes.append(pd.read_csv(pathname + '\\summary.csv'))
        result[subject_id] = pd.concat(dataframes, ignore_index=True, axis=0)
    return result


def dataSelect():
    dirname = fd.askdirectory()
    parsed_data = parse_ProjectData(dirname)
    dataframes = build_DataFrames(parsed_data)
    return dataframes
