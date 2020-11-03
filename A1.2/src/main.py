import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

FILENAME = '/home/seanh/Code/data-visualisation/A1.2/data/data.csv'
LEGEND_FONTSIZE = 'x-small'
LEGEND_SCALE = 0.6


def get_data(filename):
    df = pd.read_csv(filename)
    df.rename(columns={'Total number of people aged 15+ with no education (millions) (IIASA (2015))': 'Num People (million)'}, inplace=True)

    return df


def set_titles(axs):
    axs[0, 0].set_title('C1', pad=0)
    axs[1, 0].set_title('C2', pad=0)
    axs[2, 0].set_title('C3', pad=0)
    axs[3, 0].set_title('C4', pad=0)
    axs[4, 0].set_title('C5', pad=0)

    axs[0, 1].set_title('Q1', pad=0)
    axs[1, 1].set_title('Q2', pad=0)
    axs[2, 1].set_title('Q3', pad=2)
    axs[3, 1].set_title('Q4 (2020)', pad=-10)
    axs[4, 1].set_title('Q5', pad=0)

    return axs


def apply_formatting(ax, legend=True, ylabel=False):
    if legend:
        ax.legend(fontsize=LEGEND_FONTSIZE, markerscale=LEGEND_SCALE, title_fontsize=LEGEND_FONTSIZE, loc="upper left")
    ax.set_xlabel('')
    ax.tick_params(axis='both', which='major', pad=-5)
    if ylabel:
        ax.set_ylabel('')

    return ax


def abbreviate_entities(df):
    new_df = df.copy(deep=True)
    new_df['Entity'] = new_df['Entity'].replace('North America', 'NA')
    new_df['Entity'] = new_df['Entity'].replace('Africa', 'AFR')
    new_df['Entity'] = new_df['Entity'].replace('Europe', 'EU')
    new_df['Entity'] = new_df['Entity'].replace('Oceania', 'OCE')
    new_df['Entity'] = new_df['Entity'].replace('Asia', 'ASIA')
    new_df['Entity'] = new_df['Entity'].replace('South America', 'SA')

    return new_df


def sample_years(df):
    return df.loc[(df['Year'] == 1980) | (df['Year'] == 2000) | (df['Year'] == 2020) | (df['Year'] == 2040)]


def cat_color(df, axs, row, pos):
    ax = sns.scatterplot(data=df, x="Year", y="Num People (million)", hue="Entity", ax=axs[row][pos])
    apply_formatting(ax)


def cat_mark(df, axs, row, pos):
    ax = sns.scatterplot(data=df, x="Year", y="Num People (million)", style="Entity", ax=axs[row][pos])
    apply_formatting(ax)


def cat_size(df, axs, row, pos):
    ax = sns.scatterplot(data=df, x="Year", y="Num People (million)", size="Entity", ax=axs[row][pos])
    apply_formatting(ax)


def cat_texture(df, axs, row, pos):
    df = sample_years(df)

    palette = sns.color_palette(["#464646"], as_cmap=False)
    ax = sns.barplot(data=df, x="Year", y="Num People (million)", hue="Entity", ax=axs[row][pos], palette=palette)

    hatches = ['//', '..', 'o', 'xx', '/////', '\\\\\\']
    for i, bar in enumerate(ax.patches):
        bar.set_hatch(hatches[i//4])

    apply_formatting(ax)


def cat_pos(df, axs, row, pos):
    df = abbreviate_entities(df)
    ax = sns.scatterplot(data=df, x="Year", y="Entity", size="Num People (million)", ax=axs[row][pos])

    apply_formatting(ax, ylabel=True)


def quant_pos(df, axs, row, pos):
    ax = sns.lineplot(data=df, x="Year", y="Num People (million)", hue="Entity", ax=axs[row][pos])
    apply_formatting(ax)


def quant_height(df, axs, row, pos):
    df = sample_years(df)
    ax = sns.barplot(data=df, x="Year", y="Num People (million)", hue="Entity", ax=axs[row][pos])
    apply_formatting(ax)


def quant_brightness(df, axs, row, pos):
    df = abbreviate_entities(df)
    col = 'Num People (million)'
    df[col] = np.log(df[col])

    df = df.pivot('Entity', 'Year', 'Num People (million)')
    cmap = sns.color_palette('mako', as_cmap=True)

    ax = sns.heatmap(data=df, ax=axs[row][pos], cmap=cmap)
    ax = apply_formatting(ax, legend=False, ylabel=True)

    ax.set_xticklabels(["'" + label.get_text()[2:4] for label in ax.get_xticklabels()], rotation=45)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0)


def quant_angle(df, axs, row, pos):
    col = 'Num People (million)'
    df[col] = np.sqrt(df[col])

    year = 2020
    entities = df['Entity'].loc[(df['Year'] == year)]
    values = df['Num People (million)'].loc[(df['Year'] == year)]
    plt.subplot(axs[row, pos], aspect=0.6, title=str(year))
    plt.pie(values, labels=entities)


def quant_size(df, axs, row, pos):
    df = abbreviate_entities(df)

    ax = sns.scatterplot(data=df, x="Year", y="Entity", size="Num People (million)", sizes=(10, 150), ax=axs[row][pos])
    apply_formatting(ax, ylabel=True)


def main():
    df = get_data(FILENAME)

    sns.set(font_scale=0.7)
    fig, axs = plt.subplots(nrows=5, ncols=2, figsize=(8.27, 11.69))
    fig.tight_layout()
    axs = set_titles(axs)

    cat_color(df, axs, 0, 0)
    cat_mark(df, axs, 1, 0)
    cat_size(df, axs, 2, 0)
    cat_texture(df, axs, 3, 0)
    cat_pos(df, axs, 4, 0)

    quant_pos(df, axs, 0, 1)
    quant_height(df, axs, 1, 1)
    quant_brightness(df, axs, 2, 1)
    quant_angle(df, axs, 3, 1)
    quant_size(df, axs, 4, 1)

    plt.show()


if __name__ == '__main__':
    main()
