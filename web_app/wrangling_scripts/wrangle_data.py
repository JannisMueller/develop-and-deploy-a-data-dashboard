import pandas as pd
import plotly.graph_objs as go
import requests
from collections import defaultdict, OrderedDict


# default list of all countries of interest: five most important emgerging countries
country_default = OrderedDict([('Brazil', 'BRA'), ('India', 'IND'), ('Mexico', 'MEX'),
                               ('South Africa', 'ZAF'), ('China', 'CHN')])


def return_figures(countries=country_default):
    """Creates four plotly visualizations using the World Bank API
    
    # Example of the World Bank API endpoint:
    # arable land for the United States and Brazil from 1990 to 2015
    # http://api.worldbank.org/v2/countries/usa;bra/indicators/AG.LND.ARBL.HA?date=1990:2015&per_page=1000&format=json

    Args:
        country_default (dict): list of countries for filtering the data

    Returns:
        list (dict): list containing the four plotly visualizations

    """
    # when the countries variable is empty, use the country_default dictionary
    if not bool(countries):
        countries = country_default

    # prepare filter data for World Bank API
    # the API uses ISO-3 country codes separated by ;
    country_filter = list(countries.values())
    country_filter = [x.lower() for x in country_filter]
    country_filter = ';'.join(country_filter)

    # setting the paramets and indicators for the World Bank API 
    params = {'format': 'json', 'per_page': '500', 'date':'2000:2014'}

    # World Bank indicators of interest for pulling data:
    # Forest area (% of land area), Forest area (sq. km), Agricultural land (% of land area), Agricultural land (sq. km)
    indicators = ['AG.LND.FRST.ZS', 'AG.LND.FRST.K2', 'AG.LND.AGRI.ZS', 'AG.LND.AGRI.K2']
    
    data_frames = [] # stores the data frames with the indicator data of interest
    urls = [] # url endpoints for the World Bank API

    for indicator in indicators:
        url = 'http://api.worldbank.org/v2/countries/'+ country_filter+'/indicators/' + indicator
        urls.append(url)
        try:           
            r = requests.get(url, params=params)
            data = r.json()[1]
        
        except:
            print('Data can not be loaded', indicator)
            
        for i, value in enumerate(data):
            value['indicator'] = value['indicator']['value']
            value['country'] = value['country']['value']
    
        data_frames.append(data)

    # first chart plots Forest area (% of land area) from 2000 to 2014 in top 5 emerging markets
    # as a line chart
    
    graph_one = []
    
    #creating first Data frame for Forest area 
    df_one = pd.DataFrame(data_frames[0])
    
    # filter and sort values for the visualization
    # filtering plots the countries in decreasing order by year
    
    df_one.sort_values('date', ascending=True, inplace=True)
    # countrylist for making sure that the countries appear in the same order in all charts
    countrylist = df_one.country.unique().tolist()
    
    # getting the x and y variables for the plottinh
    for country in countrylist:
        x_val = df_one[df_one['country'] == country].date.tolist()
        y_val = df_one[df_one['country'] == country].value.tolist()
    
        graph_one.append(
        go.Scatter(
        x = x_val,
        y = y_val,
        mode = 'lines',
        name = country
        )
        )

    layout_one = dict(title = 'Forest area (% of land area) from 2000 to 2014',
                xaxis = dict(title = 'Year',
                autotick=False, tick0=2002, dtick=4),
                yaxis = dict(title = '% of land area'),
                )

# second chart plots Forest area (sq. km) from 2000 to 2014 in top 5 emerging markets
    graph_two = []
    #creating second Data frame for Forest area (sq. km) 
    df_two = pd.DataFrame(data_frames[1])
    
    # filter and sort values for the visualization
    # filtering plots the countries in decreasing order by year
    
    df_two = df_two[df_two['date'] == '2014']
   
    graph_two.append(
        go.Bar(
        x = df_two.country.tolist(),
        y = df_two.value.tolist()
            )
        )

    layout_two = dict(title = 'Forest area (sq. km) in 2014',
                        xaxis = dict(title = 'Country',),
                        yaxis = dict(title = 'sq.km'),
                    )


# third chart plots Agricultural area (% of land area) from 2000 to 2014 in top 5 emerging markets
    graph_three = []
    #creating third Data frame for Agricultural area (% of land area)
    df_three = pd.DataFrame(data_frames[2])
    df_three.sort_values('date', ascending=True, inplace=True)
    
    for country in countrylist:
        x_val = df_three[df_three['country'] == country].date.tolist()
        y_val = df_three[df_three['country'] == country].value.tolist()
    # filter and sort values for the visualization
    # filtering plots the countries in decreasing order by year
        df_three.sort_values('date', ascending=True, inplace=True)
    
        graph_three.append(
         go.Scatter(
            x = x_val,
            y = y_val,
            mode = 'lines',
            name = country
            )
           )

    layout_three = dict(title = 'Agricultural area (% of land area) from 2000 to 2014',
                xaxis = dict(title = 'Year',
                autotick=False, tick0=2002, dtick=4),
                yaxis = dict(title = '% of land area')
                       )
    
# fourth chart shows Agricultural area (sq. km) from 2000 to 2014 in top 5 emerging markets
    graph_four = []
    
    #creating fourth Data frame for Agricultural area (sq. km)
    df_four = pd.DataFrame(data_frames[3])
    # filter and sort values for the visualization
    df_four = df_four[df_four['date']== '2014']
    
    graph_four.append(
      go.Bar(
      x = df_four.country.tolist(),
      y = df_four.value.tolist(),
      name = country

      )
    )

    layout_four = dict(title = 'Agricultural area (sq. km) in 2014',
                xaxis = dict(title = 'Country'),
                yaxis = dict(title = 'sq.km'),
                )
    
    # append all charts to the figures list
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))
    figures.append(dict(data=graph_four, layout=layout_four))

    return figures