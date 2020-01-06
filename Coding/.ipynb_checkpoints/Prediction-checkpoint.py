import pandas as pd
from influxdb import DataFrameClient, InfluxDBClient
import seaborn as sns
import datetime
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats as spstats


df_prediction = pd.read_csv("./influxdb-1.7.8-1/data/messwerte_mythenquai_2007-2018.csv", index_col=0)
df_pred = df_prediction
df_pred.index = pd.to_datetime(df_pred.index)
df_pred = df_pred.loc["2018-01-01":"2018-12-31"]

def get_values_in_grouped_days(df, column, group_string, group_int):
    """
    Splits distributions in separate lists of days together as new list of values. This DF is always used as reference to determine temperature of next day.
    Input: df = vector or dataframe, column = specific column index, group_string = "3D", "D", group_int = integer days want to group
    """

    df.index = pd.to_datetime(df.index)  ## Index conversion to datetime

    df1 = df.iloc[:, column]

    grouped_df = df1.resample(group_string).aggregate(lambda tdf: tdf.tolist())  # Creates new df by grouping days
    grouped_df = pd.DataFrame(grouped_df)

    df2 = df.iloc[:, column]

    grouped_df_max = df2.resample("D").aggregate(lambda tdf: tdf.max())
    grouped_df_max = pd.DataFrame(grouped_df_max)
    grouped_df_max = grouped_df_max[::group_int].iloc[1:]  ## takes each third row and drops the first one

    new_df = pd.concat([grouped_df, grouped_df_max], axis=1)
    new_df = new_df.shift(-1).dropna()
    new_df.columns = ["grouped_values", "Temp_next_day"]

    return new_df


sample_df = get_values_in_grouped_days(df_pred, 0, "1D", 1)
sample_df.head()


def prediction_ks_test(df_for_test, sample_df):
    """Predicts the value of next day by using the statistical KS-Test of Scipy package. It's used to compare the distributions of two
    test samples. The higher the probability value the better is the fit.
    Input: df_for_test: dataframe of one day to perform the test / sample_df: specific sample df as reference
    Returns: fitting maximum temperature of next day
    """
    KS_p_val_to_compare = 0
    fitting_temp_next_day = 0
    iterations = 0  ## length not equal of sample df

    for row in range(0, len(sample_df)):

        KS_stat, KS_p_val = spstats.ks_2samp(df_for_test.iloc[:, 0], sample_df.iloc[row, 0])  # Perform t-test

        if KS_p_val > KS_p_val_to_compare:
            KS_p_val_to_compare = KS_p_val
            fitting_temp_next_day = sample_df.iloc[row, 1]

        iterations = iterations + 1

        # print("P-Wert: {} / Iterations: {} / Fitting Temp.: {}".format(KS_p_val_to_compare, iterations, fitting_temp_next_day))

    return fitting_temp_next_day





