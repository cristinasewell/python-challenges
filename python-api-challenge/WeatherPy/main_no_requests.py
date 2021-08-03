
# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import time
from scipy.stats import linregress
import csv

# Output File (CSV)
output_data_file = "output_data/cities.csv"

# this is what we want:
# City	Lat	Lng	Max Temp	Humidity	Cloudiness	Wind Speed	Country	Date

#***********************************************************************************
city_data = []

with open(output_data_file, 'r') as f:
    csv_obj = csv.reader(f)

    header = next(csv_obj)

    for row in csv_obj:
        name = row[1]
        lat = float(row[2])
        lon = float(row[3])
        max_temp = float(row[4])
        humidity = float(row[5])
        cloud = float(row[6])
        wind_speed = float(row[7])
        country = row[8]
        date = int(row[9])
        city = {'City': name, 'Lat': lat, 'Lon': lon, 'Max Temp': max_temp,
                    'Humidity': humidity, 'Cloudiness': cloud, 'Wind Speed': wind_speed,
                    'Country': country, 'Date': date}
        city_data.append(city)
#print(city_data)
        # city_info.append(row)

# city_data = []

# for data in city_info:
#     try:
#         name = data['name']
#         # if we find the coord, then get the lat
#         lat = data['coord'].get('lat')
#         lon = data['coord'].get('lon')
#         max_temp = data['main']['temp_max']
#         humidity = data['main']['humidity']
#         cloud = data['clouds']['all']
#         wind_speed = data['wind']['speed']
#         country = data['sys']['country']
#         date = data['dt']
#         city = {'City': name, 'Lat': lat, 'Lon': lon, 'Max Temp': max_temp,
#                     'Humidity': humidity, 'Cloudiness': cloud, 'Wind Speed': wind_speed,
#                     'Country': country, 'Date': date}
#         city_data.append(city)
#     except Exception as ex:
#         print(ex, data)

city_data_df = pd.DataFrame(city_data)
  
# city_data_df.to_csv(output_data_file)

print(city_data_df)
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




