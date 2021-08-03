#!/usr/bin/env python
# coding: utf-8

# # WeatherPy
# ----
# 
# #### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[2]:


# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import time
from scipy.stats import linregress
import csv

# Import API key
from api_keys import weather_api_key

# Incorporated citipy to determine city based on latitude and longitude
from citipy import citipy

# Output File (CSV)
output_data_file = "output_data/cities.csv"

# Range of latitudes and longitudes
lat_range = (-90, 90)
lng_range = (-180, 180)


# ## Generate Cities List

# In[3]:


# List for holding lat_lngs and cities
lat_lngs = []
cities = []

# Create a set of random lat and lng combinations
lats = np.random.uniform(lat_range[0], lat_range[1], size=1500)
lngs = np.random.uniform(lng_range[0], lng_range[1], size=1500)
lat_lngs = zip(lats, lngs)

# Identify nearest city for each lat, lng combination
for lat_lng in lat_lngs:
    city = citipy.nearest_city(lat_lng[0], lat_lng[1]).city_name
    
    # If the city is unique, then add it to a our cities list
    if city not in cities:
        cities.append(city)

# Print the city count to confirm sufficient count
print(len(cities))


# ### Perform API Calls
# * Perform a weather check on each city using a series of successive API calls.
# * Include a print log of each city as it'sbeing processed (with the city number and city name).
# 

# In[4]:


# different api calls

# by city Name
# f"api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}"

# by city Name and State code
# f"api.openweathermap.org/data/2.5/weather?q={city name},{state code}&appid={API key}"

# by city Name, State code and Country code
# f"api.openweathermap.org/data/2.5/weather?q={city name},{state code},{country code}&appid={API key}"

# by city ID
# f"api.openweathermap.org/data/2.5/weather?id={city id}&appid={API key}"

# by geographic coordinates
# f"api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}"

# by zip codes
# f"api.openweathermap.org/data/2.5/weather?zip={zip code},{country code}&appid={API key}"

# api calls
# f"api.openweathermap.org/data/2.5/weather?id=2172797&appid={API key}"


# take the comments from this section out if you want to get the data again
# *******************************************************
print('Beginning Data Retrieval ')
print('-' * 30)

# store all data here

city_info = []

for index, city in enumerate(cities):
    city_url = f'http://api.openweathermap.org/data/2.5/weather?units=imperial&q={city}&appid={weather_api_key}'
    try:
        print(f'Processing record number {index} for city: {city}')
        # requests.get(city_url).json()
        data = requests.get(city_url).json()
        # check if you can get the weather for this city, then we have data, otherwise
        # we'll have an exception
        weather = data['weather']
        city_info.append(data)
    except:
        print(f"\nCould not find the city: {city}, skipping...\n")

print()
print('-' * 30)
print('Data Retrieval Complete')
print('-' * 30)


# ### Convert Raw Data to DataFrame
# * Export the city data into a .csv.
# * Display the DataFrame

# In[8]:

# *******************************************************

# this is how we have them in city_info
# coord {lon, lat}
# weather {id, main, description, icon}
# base
# main {temp, feels_like, temp_min, temp_max, pressure, humidity, sea_level, grnd_level}
# visibility
# wind {speed, deg, gust}
# rain
# clouds
# dt
# sys {type, id, country, sunrise, sunset}
# timezone
# id
# name
# cod

# this is what we want:
# City	Lat	Lng	Max Temp	Humidity	Cloudiness	Wind Speed	Country	Date

#***********************************************************************************
city_data = []

for data in city_info:
    try:
        name = data['name']
        # if we find the coord, then get the lat
        lat = data['coord'].get('lat')
        lon = data['coord'].get('lon')
        max_temp = data['main']['temp_max']
        humidity = data['main']['humidity']
        cloud = data['clouds']['all']
        wind_speed = data['wind']['speed']
        country = data['sys']['country']
        date = data['dt']
        city = {'City': name, 'Lat': lat, 'Lon': lon, 'Max Temp': max_temp,
                    'Humidity': humidity, 'Cloudiness': cloud, 'Wind Speed': wind_speed,
                    'Country': country, 'Date': date}
        city_data.append(city)
    except Exception as ex:
        print(ex, data)

city_data_df = pd.DataFrame(city_data)
  
city_data_df.to_csv(output_data_file)

city_data_df
#***********************************************************************************



# ## Inspect the data and remove the cities where the humidity > 100%.
# ----
# Skip this step if there are no cities that have humidity > 100%. 

# In[9]:


humidity = city_data_df[city_data_df['Humidity'] > 100]
humidity


# In[10]:


#  Get the indices of cities that have humidity over 100%.
indexis = []
if humidity.index.any():
    # if you find an index where the humidity is > 100
    indexis = humidity.index
    city_data_df = city_data_df.drop(index=indexis)

#for index in indexis:
#    city_data_df.drop(index=index)


# In[11]:


# Make a new DataFrame equal to the city data to drop all humidity outliers by index.
# Passing "inplace=False" will make a copy of the city_data DataFrame, which we call "clean_city_data".
clean_city_data = pd.DataFrame(city_data_df)
clean_city_data


# In[27]:


def scatter_plot(y, y_label, y_units):
    clean_city_data.plot(kind='scatter', x='Lat', y=y, edgecolor='black')
    plt.ylabel(f'{y_label} (y_units)')
    plt.xlabel("Latitude")
    date = time.localtime()
    plt.title(f'Latitude vs {y_label} Plot')
    # save it as a png
    plt.savefig(f"./pngs/LATvs{y_label}.png")
    plt.show()


# ## Plotting the Data
# * Use proper labeling of the plots using plot titles (including date of analysis) and axes labels.
# * Save the plotted figures as .pngs.

# ## Latitude vs. Temperature Plot

# In[28]:


#plt.scatter(clean_city_data['Lat'], clean_city_data['Max Temp'])
scatter_plot(y='Max Temp', y_label='Max Temperature', y_units='F')
# clean_city_data.plot(kind='scatter', x='Lat', y='Max Temp')
# plt.ylabel("Max Temperature (F)")
# plt.xlabel("Latitude")
# plt.title('Latitude vs Temperature Plot')

# # save it as a png
# plt.savefig(f"./pngs/LATvsTEMP.png")
# plt.show()


# ## Latitude vs. Humidity Plot

# In[ ]:


# clean_city_data.plot(kind='scatter', x='Lat', y='Humidity')
# plt.ylabel("Humidity (%)")
# plt.xlabel("Latitude")
# plt.title('Latitude vs Humidity Plot')
# plt.show()
scatter_plot(y='Humidity', y_label='Humidity', y_units='%')


# ## Latitude vs. Cloudiness Plot

# In[ ]:


# clean_city_data.plot(kind='scatter', x='Lat', y='Cloudiness')
# plt.ylabel("Cloudiness (%)")
# plt.xlabel("Latitude")
# plt.title('Latitude vs Cloudiness Plot')
# plt.show()
scatter_plot(y='Cloudiness', y_label='Cloudiness', y_units='%')


# ## Latitude vs. Wind Speed Plot

# In[ ]:


# clean_city_data.plot(kind='scatter', x='Lat', y='Wind Speed')
# plt.ylabel("Wind Speed (mph)")
# plt.xlabel("Latitude")
# plt.title('Latitude vs Wind Speed Plot')
# plt.show()
scatter_plot(y='Wind Speed', y_label='Wind Speed', y_units='mph')


# ## Linear Regression

# In[30]:


def linear_regression(x_values, y_values, title, x_label, y_label, anotate_xy, mark_type='b--', color='pink'):
    # calculate the linear regression with scipy.stats
    (slope, intercept, rvalue, pvalue, stderr) = linregress(x_values, y_values)
    regression = x_values * slope + intercept
    # slope line equation
    # y = mx + b where m = slope and b = y intercept
    eq_line = f'y = {round(slope,3)}x + {round(intercept,3)}'

    print('Regression')
    print('----------------')
    print(f'rValue: {rvalue}')

    # plot the regression
    plt.figure(figsize=(10, 7))
    plt.scatter(x_values, y_values, s=30, color=color, edgecolor='black')
    plt.plot(x_values, regression, mark_type)

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.annotate(s=eq_line, xy=anotate_xy, fontsize=14, color='red', verticalalignment='top')
    
    plt.savefig(f"./pngs/{title}.png")
    plt.show()


# ####  Northern Hemisphere - Max Temp vs. Latitude Linear Regression

# In[31]:


north_hemisphere = clean_city_data[clean_city_data['Lat'] >= 0]
north_hemisphere

north_temp = north_hemisphere['Max Temp']
north_lat = north_hemisphere['Lat']

linear_regression(x_values=north_lat, y_values=north_temp,
                  title='Northern Hemisphere - Max Temp vs. Latitude Linear Regression',
                 x_label='Latitude', y_label='Max Temperature (F)', anotate_xy=(10, 50))


# ####  Southern Hemisphere - Max Temp vs. Latitude Linear Regression

# In[32]:


south_hemisphere = clean_city_data[clean_city_data['Lat'] < 0]
south_hemisphere

south_temp = south_hemisphere['Max Temp']
south_lat = south_hemisphere['Lat']

linear_regression(x_values=south_lat, y_values=south_temp,
                  title='Southern Hemisphere - Max Temp vs. Latitude Linear Regression',
                 x_label='Latitude', y_label='Max Temperature (F)', anotate_xy=(-50, 80))


# ####  Northern Hemisphere - Humidity (%) vs. Latitude Linear Regression

# In[33]:


north_humidity = north_hemisphere['Humidity']
linear_regression(x_values=north_lat, y_values=north_humidity,
                  title='Northern Hemisphere - Humidity vs. Latitude Linear Regression',
                 x_label='Latitude', y_label='Humidity (%)', anotate_xy=(5, 20))


# ####  Southern Hemisphere - Humidity (%) vs. Latitude Linear Regression

# In[34]:


south_humidity = south_hemisphere['Humidity']
linear_regression(x_values=south_lat, y_values=south_humidity,
                  title='Southern Hemisphere - Humidity vs. Latitude Linear Regression',
                 x_label='Latitude', y_label='Humidity (%)', anotate_xy=(-50, 40))


# ####  Northern Hemisphere - Cloudiness (%) vs. Latitude Linear Regression

# In[37]:


north_cloudiness = north_hemisphere['Cloudiness']
linear_regression(x_values=north_lat, y_values=north_cloudiness,
                  title='Northern Hemisphere - Cloudiness vs. Latitude Linear Regression',
                 x_label='Latitude', y_label='Cloudiness (%)', anotate_xy=(0, 40))


# ####  Southern Hemisphere - Cloudiness (%) vs. Latitude Linear Regression

# In[38]:


south_cloudiness = south_hemisphere['Cloudiness']
linear_regression(x_values=south_lat, y_values=south_cloudiness,
                  title='Southern Hemisphere - Cloudiness vs. Latitude Linear Regression',
                 x_label='Latitude', y_label='Cloudiness (%)', anotate_xy=(-50, 40))


# ####  Northern Hemisphere - Wind Speed (mph) vs. Latitude Linear Regression

# In[39]:


north_wind = north_hemisphere['Wind Speed']
linear_regression(x_values=north_lat, y_values=north_wind,
                  title='Northern Hemisphere - Wind Speed vs. Latitude Linear Regression',
                 x_label='Latitude', y_label='Wind Speed (%)', anotate_xy=(0, 40))


# ####  Southern Hemisphere - Wind Speed (mph) vs. Latitude Linear Regression

# In[40]:


south_wind = south_hemisphere['Wind Speed']
linear_regression(x_values=south_lat, y_values=south_wind,
                  title='Southern Hemisphere - Wind Speed vs. Latitude Linear Regression',
                 x_label='Latitude', y_label='Wind Speed (%)', anotate_xy=(-50, 40))


# In[ ]:




