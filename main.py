#****************************************************************
#Name: Rag Sai Siddarth Balijepalli
#Student Number: A00233374
#
#ANA1001 Final Project
#****************************************************************
import json
import requests
import matplotlib.pyplot as plt
from plotly.graph_objs import scattergeo, Layout, Bar
from plotly import offline
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go


#Creating a list of cities
cities = ['Toronto', 'Montreal', 'Vancouver', 'Calgary', 'Edmonton', 'Ottawa', 'Winnipeg', 'Quebec City',
'Hamilton', 'Kitchener', 'London', 'Victoria', 'Halifax', 'Oshawa', 'Windsor', 'Saskatoon', 'St. Catharines', 'Regina', 'St. Johns', 'Kelowna']

#Creating the filename to store json file
filename = 'data.json'

#Creating an empty list to append all the city names
city = []

## MY API KEY : 46da83c2b9ab61b5891cf3aed23c4d5a

#Using for loop to loop for every city in Canada
for city_name in cities:
  url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name},CA&appid=46da83c2b9ab61b5891cf3aed23c4d5a'
  r = requests.get(url)
  print(city_name)
  print(f"Status code : {r.status_code}") 
  response_dict = r.json()
  print(response_dict.keys())
  city.append(response_dict)

print(city)

#Using json.dump to write inside the json file
with open(filename, 'w') as fobj:
    json.dump(city,fobj, indent = 4)




#Question 1
## A

#Reading the json data into the script
with open(filename) as  f_obj:
  data = json.load(f_obj)

#Creating empty lists and appending to them later
temperatures,lats,long = [],[],[]
#Creating a conditional loop
for a in data:
  temp = a['main']['temp']
  lon = a['coord']['lon']
  lat = a['coord']['lat']

  temperatures.append(temp)
  lats.append(lat)
  long.append(lon)

print(temperatures)

#Storing the data to create scattergeo
temp_layout = Layout(title = "Temperature of cities in Canada")
temp_data = [{
  "type": 'scattergeo', 
  "lon":long,
  "lat":lats,
  "marker": {
    "size": [0.05*mag for mag in temperatures],
    "color":temperatures,
    "colorscale":"balance",
    "reversescale":True,
    "colorbar":{"title":"Temperature in Kelvin"}
  }
  }]

#Displaying 
fig1 = {'data':temp_data, 'layout':temp_layout}
offline.plot(fig1, filename = 'Temperatures in Canadian Cities.html')

## B

#Creating empty lists and appending later
humidities,h_longs,h_lats = [],[],[]   
#For loop to read through each temperature, long and lat for location. 
for h in data:
  c_humid = h['main']['humidity']
  hlong = h['coord']['lon']
  hlat = h['coord']['lat']
  humidities.append(c_humid)
  h_longs.append(hlong)
  h_lats.append(hlat)

print(humidities)

# Create the scattergeo plot for humidity.
humidity_layout = Layout(title = "Humidity in Canadian City")
 
humidity_data = [{
  "type": 'scattergeo', 
  "lon":h_longs,
  "lat":h_lats,
  "marker": {
    "size": [0.2*mag for mag in humidities],
    "color":humidities,
    "colorscale":"balance",
    "reversescale":True,
    "colorbar":{"title":"Humidity Level(%)"}
    }
}]

#Displaying
fig2 = {'data': humidity_data, 'layout': humidity_layout}
offline.plot(fig2, filename = 'Humidity.html')

## C
#Creating a dictionary called weather to store temperatures and humidities
weather = {
  'temperatures': temperatures, 
  'humidities': humidities
  }
#Creating a dataframe
df = pd.DataFrame(weather, columns=['temperatures','humidities'])

# Create matplotlib figure
fig3 = plt.figure() 

# Create matplotlib axes
ax = fig3.add_subplot(111) 
# Create another axes that shares the same x-axis as ax.
ax2 = ax.twinx() 
width = 0.4
df.temperatures.plot(kind='bar', color='blue', ax=ax, width=width, position=1)
df.humidities.plot(kind='bar', color='orange', ax=ax2, width=width, position=0)

ax.set_ylabel('Humidity Level')
ax2.set_ylabel('Temperature in Kelvin')
plt.title('Humidity & Temperature')
plt.savefig("Humidity & Temerature Bar Chart.jpg")


#The relation between humidity and temperature is that they are inversely proportional to each other. Meaning- if temperature decreases, relative humidity increases. For example, when temperature is decreased, the air will become wet which indicates that humidity has increased.     



#################
#Question 2.

#Part 1
#Creating empty list and adding to that list later
weather_description = []

#Using for loop
for d in data:
  
  description = d['weather'][0]['description']
  weather_description.append(description)

#Part 2 Removing duplicates using pandas
unique_dict = {'describe' : weather_description}

unique_df = pd.DataFrame(unique_dict, columns = ['describe'])
unique_df.drop_duplicates(subset = 'describe')
unique_df["describe"].value_counts(sort= True)

#Removing the duplicates
duplicates = unique_df.pivot_table(columns = ['describe'], aggfunc = 'size')


#Creating a bar graph and labelling it.
fig4 = plt.figure()

ax = fig4.add_subplot(111)
width = 0.5
duplicates.plot(kind = 'bar', color = 'blue', ax= ax, width = width, position = 0)

ax.set_ylabel('Weather description')
ax.set_xlabel('Count')
plt.title('Weather description of Cities in Canada.')

plt.savefig("Question_2_DescriptionCount.jpg")


#Question no.3

#Get highest and lowest wind speed from the json file

#Creating empty lists and adding to that list later
print("\n")
winds =[]
cityNames = []

#Using for loop for wind speed
for w in data:
	wind = str(w['wind']['speed'])
	winds.append(wind)
#Using for loop for city name
for c in data:
  cityname = c['name']
  cityNames.append(cityname)


winds_dict = { 'speed' : winds, 'name':cityNames}
#Creating a data frame 
wind_df = pd.DataFrame(winds_dict, columns = ['speed','name'])
print(wind_df)
column = wind_df["speed"]
name_column = wind_df['name']

max_value = column.max()
min_value = column.min()


#Displaying the result
print("\n")
print(f"{wind_df['name'][6]} has the highest wind speed of {max_value}")
print(f"{wind_df['name'][5]} has the lowest wind speed of {min_value}")

##Question 4
print("\n")

#Reading the data from data.json file
with open(filename) as fobject :
	data = json.load(fobject)

#Creating empty list and appending to the list
sunrise, sunset, c_sunduration, sunduration = [], [], [], []

#Defining

def avgtime(timestringlist):
	minutecounts = []
	for val in timestringlist:
		h = val[:2]
		m = val[3:5]
		total_minutes = (int(h)*60) + int(m)
		minutecounts.append(total_minutes)	
	avgtimemins = sum(minutecounts)/len(minutecounts)
	hours = int(avgtimemins/60)
	minutes = avgtimemins % 60
	return f"{hours} hours and {minutes} minutes"


#Using for loop
for i in range(len(data)):
  sunrise.append({'city': data[i]['name'], 'sunrise' : data[i]['sys']['sunrise']})
  sunset.append({'city': data[i]['name'], 'sunset' : data[i]['sys']['sunset']})
  c_sunduration.append({'city': data[i]['name'], 'duration' : datetime.utcfromtimestamp(data[i]['sys']['sunset'] - data[i]['sys']['sunrise']).strftime("%H:%M")})
  sunduration.append(datetime.utcfromtimestamp(data[i]['sys']['sunset'] - data[i]['sys']['sunrise']).strftime("%H:%M"))
  print(f"The duration of light today, in {data[i]['name']}, was {avgtime(sunduration[i].split())}")

print(f"\nThe average length of the day for all the cities : {avgtime(sunduration)}")





#Question 5

#Reading data from data.json 

with open(filename) as file_object:
  data = json.load(file_object)

#Creating a for loop and printing
for i in range(len(data)):
  print(f"The difference between the actual temperature and feels like temperature for {data[i]['name']} is {data[i]['main']['temp'] - data[i]['main']['feels_like']} degrees.")

## I think there is a significant difference between actual temperature and feels like temperature because feels like temperature is measure for a human in which the relative humidity is factored in.



#Question 6

#Creating an empty list and adding to it later.
windspeed_city = []

#Using for loop
# for i in range(len(data)):
#   windspeed_city.append({'city': data[i]['name'], 'wind_speed' : data[i]['wind']['speed']})



#Displaying 
fig6 = go.Figure(go.Indicator(
  mode  = 'gauge+number',
  value = windspeed_city[0]['wind_speed'],
  domain = {'x' :[0,1],'y':[0,1]},
  title = {'text': 'Wind Speed in Toronto'}))

#Saving the plot offline. To view the plot, download the data.
#offline.plot(fig6, filename = "windspeed.html")



