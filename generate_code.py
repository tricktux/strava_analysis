from stravalib.client import Client

client_id = 33892  # Replace this ID
client = Client()
url = client.authorization_url(client_id=client_id,
                               redirect_uri='http://127.0.0.1:8000/authorization',
                               scope='read_all')
print(url)
