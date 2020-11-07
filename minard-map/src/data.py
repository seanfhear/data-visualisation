import pandas as pd

FILENAME = "../data/minard-data.csv"
ADV_FILENAME = "../data/minard-data-adv.csv"
RET_FILENAME = "../data/minard-data-ret.csv"


def get_data(filename=FILENAME):
    return pd.read_csv(filename)


def get_troop_data(df, direction=None):
    if direction == 'A':
        df = get_data(ADV_FILENAME)
    elif direction == 'R':
        df = get_data(RET_FILENAME)

    df = df[["LONP", "LATP", "SURV", "DIR", "DIV"]]
    return df[df["LONP"].notna()]


def get_city_data(df):
    df = df[["LONC", "LATC", "CITY"]]
    return df[df["LONC"].notna()]


def get_temp_data(df):
    df = df[["LONT", "TEMP", "DAYS", "MON", "DAY"]]
    df = df[df["LONT"].notna()]

    df['DAY'] = df['DAY'].astype('str').str.strip('.0')
    df['MON'] = df['MON'].astype('str')

    df['DATE'] = df[['DAY', 'MON']].agg(', '.join, axis=1).replace('nan, nan', "")
    df["LABEL"] = df.apply(axis=1, func=lambda row: "{}°  {}".format(str(row[1])[:-2], row[5]))

    return df
