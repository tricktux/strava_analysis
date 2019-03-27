from stravalib.client import Client

client_id = 33892  # Replace this ID
client = Client()
url = client.authorization_url(client_id=client_id,
                               redirect_uri='http://127.0.0.1:8000/authorization',
                               scope='read_all')
print(url)
#  client = Client()
#  code = ''
#  client_id = 12345
#  client_secret = ''

#  year = 2018
#  resolution = 'high'
#  types = ['time', 'altitude', 'heartrate', 'temp', 'distance', 'watts']

#  access_token = client.exchange_code_for_token(
#  client_id=client_id, client_secret=client_secret, code=code)

#  client = Client(access_token=access_token)
#  df_overview = pd.DataFrame()
#  activities = dict()

#  for activity in client.get_activities(
#  after='{}-01-01T00:00:00Z'.format(str(year)),
#  before='{}-01-01T00:00:00Z'.format(str(year + 1))):
#  streams = client.get_activity_streams(
#  activity.id, types=types, series_type='time', resolution=resolution)
#  for key, value in streams.items():
#  streams[key] = value.data

#  df_overview = df_overview.append(
#  pd.DataFrame(
#  [{
#  'Name': activity.name,
#  'Date': activity.start_date,
#  'Moving Time [min]': int(activity.moving_time.seconds / 60),
#  'Distance [km]': round(activity.distance.num / 1000, 1),
#  'Measurements': list(streams.keys())
#  }],
#  index=[activity.id]))

#  activities[activity.id] = pd.DataFrame(streams)

#  writer = pd.ExcelWriter(
#  'strava_export_{}.xlsx'.format(str(year)), engine='openpyxl')
#  df_overview.to_excel(writer, "Overview")

#  for activity_id, df in activities.items():
#  df.to_excel(
#  writer, ' '.join([
#  str(df_overview.loc[activity_id]['Date'].date()),
#  df_overview.loc[activity_id]['Name']
#  ])[:30])

#  writer.save()

