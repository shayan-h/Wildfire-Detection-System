import pandas as pd
from pandas import json_normalize
import requests
import random
from IPython.display import display

def get_data(lat, lon):
  # convert json to dataframe
  def flatten_json(y):
      out = {}

      def flatten(x, name=''):
          if type(x) is dict:
              for a in x:
                  flatten(x[a], name + a + '_')
          elif type(x) is list:
              i = 0
              for a in x:
                  flatten(a, name + str(i) + '_')
                  i += 1
          else:
              out[name[:-1]] = x

      flatten(y)
      return out

  def json_to_dataframe(json_obj):
      flat_json = flatten_json(json_obj)
      df = pd.DataFrame([flat_json])
      return df


  # get weather data
  def get_weather_data(api_key, lat, lon):
      # Define the API endpoint
      url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"

      # Make the API request
      response = requests.get(url)

      # Check if the request was successful (HTTP Status Code 200)
      if response.status_code == 200:
          return response.json()  # Return the JSON response
      else:
          return None  # Return None if request was unsuccessful

  # Your API Key from OpenWeatherMap
  api_key = '93e22ee8a9308b65795ed30132cf9712'

  # Get the weather data
  weather_data = get_weather_data(api_key, lat, lon)

  # Flatten the JSON and convert it to a dataframe
  df = json_to_dataframe(weather_data)

  return df

firms_url = "https://firms.modaps.eosdis.nasa.gov/api/area/csv/804dce02ada27684831944ca1f40e601/LANDSAT_NRT/world/1/2023-10-07";

df2 = pd.read_csv(firms_url)

df_usa = df2[(df2['longitude'] >= -116) & (df2['latitude'] >= 32) & (df2['longitude'] <= -67) & (df2['latitude'] <= 44)].copy()
df_usa[['latitude', 'longitude']] = df_usa[['latitude', 'longitude']].round(4)
df_usa = df_usa.head(100).reset_index()
df_usa = df_usa.drop('index', axis = 1)

print(df_usa)

# Coordinates for your location
columns=['coord_lat', 'coord_lon', 'weather_0_main', 'main_temp', 'main_pressure', 'main_humidity', 'visibility', 'wind_speed', 'wind_deg', 'clouds_all', 'sys_country']

# List to store the retrieved rows
rows_list = []
for index, row in df_usa.iterrows():
    lat = row['latitude']
    lon = row['longitude']
    row = get_data(lat, lon)
    row = row[columns]  # Ensure the order and selection of columns
    rows_list.append(row)

# Concatenate all the rows in rows_list into a DataFrame
weather_df = pd.concat(rows_list, ignore_index=True)
weather_df.rename(columns={'coord_lon': 'longitude', 'coord_lat': 'latitude'}, inplace=True)

print(weather_df)

# merge FIRMS with Weather Data
merged_data = pd.concat([df_usa, weather_df], axis=1)
print(merged_data)

# synthetic user responses simulating user response
# user response here is a combination of weather data, number of user yes and no fire, number of validated image attached
# returns likelihood of detected fire being real fire
user_response = []
for i in range(merged_data.shape[0]):
  response = round(random.uniform(0,1), 2)
  user_response.append(response)

mean_response_df = pd.DataFrame({'user_response': user_response})

complete_data = pd.concat([merged_data, mean_response_df], axis = 1)
print(complete_data)

complete_data = complete_data.iloc[:, -12:]
print(complete_data)
display(complete_data)

