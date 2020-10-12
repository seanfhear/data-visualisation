import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

FILENAME = '/home/seanh/Code/data-visualisation/A1.2/data/total-number-of-people-aged-15-with-no-education-in-millions-by-continent-1970-2050.csv'


def get_data(filename):
    df = pd.read_csv(filename)
    df.rename(columns={'Total number of people aged 15+ with no education (millions) (IIASA (2015))': 'Num People (million)'}, inplace=True)
    return df


def scatter(df):
    sns.scatterplot(data=df, x="Year", y="Num People (million)", size="Entity")


def main():
    df = get_data(FILENAME)
    print(df.head())

    scatter(df)

    plt.show()


if __name__ == '__main__':
    main()
