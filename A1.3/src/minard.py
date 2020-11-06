import altair as alt
from configparser import ConfigParser
from src import data

cfg = ConfigParser()
cfg.read("./config.cfg")
CFG = cfg['DEFAULT']


def chart_troops(troops, advancing=True):
    if advancing:
        domain = CFG['AdvDomain'].split(',')
    else:
        domain = CFG['RetDomain'].split(',')
    colors = CFG['AdvColors'].split(',') + CFG['RetColors'].split(',')

    return alt.Chart(troops).mark_trail(order=False).encode(
        x=alt.X(
            'LONP:Q',
            scale=alt.Scale(domain=[troops["LONP"].min(), troops["LONP"].max()]),
            axis=alt.Axis(title=None, labels=False, grid=True, gridColor=CFG['TempGridColor'])
            ),
        longitude='LONP:Q',
        latitude='LATP:Q',
        size=alt.Size(
            'SURV',
            scale=alt.Scale(range=[int(i) for i in CFG['TroopScale'].split(',')]),
            legend=None
        ),
        color=alt.Color(
            'DIV',
            scale=alt.Scale(
                domain=domain,
                range=colors
            ),
            legend=None
        ),
        tooltip=[
            alt.Tooltip('SURV', title='Troop Numbers'),
            alt.Tooltip('DIR', title='Direction'),
            alt.Tooltip('LONP', title='Longitude'),
            alt.Tooltip('LATP', title='Latitude')
        ]
    )


def chart_troop_labels(troops):
    return alt.Chart(troops).mark_text(
        font=CFG['LabelFont'],
        fontSize=int(CFG['TroopLabelSize']),
        dx=int(CFG['TroopLabelDx']),
        dy=int(CFG['TroopLabelDy']),
        angle=int(CFG['TroopLabelAngle'])
    ).encode(
        x='LONP:Q',
        longitude="LONP:Q",
        latitude="LATP:Q",
        text="SURV"
    )


def chart_cities(cities, troops):
    return alt.Chart(cities).mark_circle(
        size=int(CFG['CitySize']),
        color=CFG['CityColor']
    ).encode(
        x='LONC:Q',
        longitude="LONC:Q",
        latitude="LATC:Q"
    )


def chart_city_labels(cities, troops):
    x_encode = alt.X(
        'LONC:Q',
        scale=alt.Scale(domain=[troops["LONP"].min(), troops["LONP"].max()]),
        axis=alt.Axis(title=None, labels=True)
    )
    return alt.Chart(cities).mark_text(
        font=CFG['LabelFont'],
        fontSize=int(CFG['CityLabelSize']),
        dx=int(CFG['CityLabelDx']),
        dy=int(CFG['CityLabelDy']),
        fontStyle=CFG['CityLabelStyle']
    ).encode(
        x=x_encode,
        longitude="LONC:Q",
        latitude="LATC:Q",
        text="CITY"
    )


def chart_movement_lines(troops, temps):
    return alt.Chart(temps, troops).mark_rule(
        color='black',
        strokeWidth=1
    ).encode(
        x=alt.X('LONT'),
        y=alt.Y(troops.LONP)
    )


def get_temp_encodes(temps, troops):
    x_encode = alt.X(
        'LONT:Q',
        scale=alt.Scale(domain=[troops["LONP"].min(), troops["LONP"].max()]),
        axis=alt.Axis(title=None, labels=True, grid=True, gridColor=CFG['TempGridColor']))
    y_encode = alt.Y(
        'TEMP',
        scale=alt.Scale(domain=[temps["TEMP"].min() - 5, temps["TEMP"].max() + 5]),
        axis=alt.Axis(title=None, grid=True, gridColor=CFG['TempGridColor'], orient='right')
    )
    return x_encode, y_encode


def chart_retreat_temp(temps, troops):
    return alt.Chart(temps).mark_line(
        color=CFG['TempColor'],
        strokeWidth=int(CFG['TempStrokeWidth'])
    ).encode(
        x='LONT:Q',
        y='TEMP:Q'
    )


def chart_temp_markers(temps, troops):
    return alt.Chart(temps).mark_circle(
        size=int(CFG['TempMarkerSize']),
        color=CFG['TempColor']
    ).encode(
        x='LONT:Q',
        y='TEMP:Q',
        tooltip=[
            alt.Tooltip('LONT', title='Longitude')
        ]
    )


def chart_temp_labels(temps, troops):
    x_encode, y_encode = get_temp_encodes(temps, troops)

    return alt.Chart(temps).mark_text(
        font=CFG['LabelFont'],
        fontSize=int(CFG['TempLabelSize']),
        dx=int(CFG['TempLabelDx']),
        dy=int(CFG['TempLabelDy']),
        fontStyle=CFG['TempLabelStyle']
    ).encode(
        x=x_encode,
        y=y_encode,
        text="DATE"
    )


def chart_temp_lines(temps):
    return alt.Chart(temps).mark_rule(
        color='black',
        strokeWidth=1
    ).encode(
        x='LONT',
        y='TEMP:Q'
    )


def chart_movements(troops, cities):
    adv_troops = data.get_troop_data(None, 'A')
    ret_troops = data.get_troop_data(None, 'R')
    return\
        chart_troops(adv_troops) +\
        chart_troops(ret_troops, advancing=False) +\
        chart_troop_labels(troops) +\
        chart_cities(cities, troops) + chart_city_labels(cities, troops)\
        .properties(
            height=int(CFG['MovementChartHeight']),
            title="Figurative Map of the successive losses in men of the French Army in the Russian campaign 1812–1813."
        )


def chart_temperature(temps, troops):
    return \
        chart_retreat_temp(temps, troops) + \
        chart_temp_markers(temps, troops) + \
        chart_temp_labels(temps, troops)\
        .properties(height=int(CFG['TempChartHeight']), title='GRAPHIC TABLE of the temperature in degrees below zero of the Réaumur thermometer')


def chart_all(df):
    troops_df = data.get_troop_data(df)
    cities_df = data.get_city_data(df)
    temps_df = data.get_temp_data(df)

    complete_chart = alt.vconcat(chart_movements(troops_df, cities_df), chart_temperature(temps_df, troops_df))
    return complete_chart.configure(
        background=CFG['BackgroundColor']
    ).configure_view(
        width=int(CFG['CompleteChartWidth']),
        height=int(CFG['CompleteChartHeight']),
        strokeWidth=int(CFG['CompleteChartStroke'])
    ).configure_title(
        fontSize=int(CFG['TitleSize']),
        font=CFG['LabelFont']
    )


def main():
    df = data.get_data()
    chart = chart_all(df)
    chart.save(CFG['OutputFile'], embed_options={'actions': False})


if __name__ == "__main__":
    main()
