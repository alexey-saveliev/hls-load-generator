from locust import HttpUser, task, between
import requests
import random
session = requests.Session()
#Put your stream master file address here
stream_url =  "https://<hls-proxy>/video/3/index.m3u8"
session_url = stream_url.rsplit('/', 1)[0]

class HLSUser(HttpUser):
    wait_time = between(1, 2)
    session = requests.Session()
    @task
    def get_variant_playlist(self):
        try:
            playlist_url = stream_url
            playlist_response = self.session.get(playlist_url)
            playlist = playlist_response.text
            ts = [x for x in playlist.split('\n') if x.endswith('.ts')]            
            ts_url = session_url + '/' + ts[-1]
            self.client.get(ts_url)
        except Exception as e:
            print(f"Error occurred: {e}")
