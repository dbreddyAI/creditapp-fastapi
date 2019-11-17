import pandas as pd


class MyEncoder(object):
    columns = []

    def fit(self, columns=[]):
        self.columns = columns
        return self

    def fit_transform(self, dataframe=pd.DataFrame(), columns=[]):
        dataframe = dataframe.copy()
        for column in columns:
            dataframe[column] = dataframe[column].apply(
                lambda x: 1 if x is True else 0
            )
        return dataframe

    def transform(self, dataframe=pd.DataFrame()):
        dataframe = dataframe.copy()
        for column in self.columns:
            dataframe[column] = dataframe[column].apply(
                lambda x: 1 if x is True else 0
            )
        return dataframe
