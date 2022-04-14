import pandas as pd
import seaborn as sns
sns.set()


def build_plot(df):
    return [
        sns.lineplot(x='Datetime (UTC)', y='Acc magnitude avg', data=df),
        sns.lineplot(x='Datetime (UTC)', y='Eda avg', data=df),
        sns.lineplot(x='Datetime (UTC)', y='Temp avg', data=df),
        sns.lineplot(x='Datetime (UTC)', y='Movement intensity', data=df),
    ]


def buildPlots(dataframes):
    plots = {}
    for subject_id in dataframes:
        plots[subject_id] = build_plot(dataframes[subject_id])
    return plots
