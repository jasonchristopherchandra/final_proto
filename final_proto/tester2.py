from pytchat import LiveChat, CompatibleProcessor
import time
import pytchat
from urllib.parse import urlparse, parse_qs

def extract_video_id(url):
    # Examples:
    # - http://youtu.be/SA2iWivDJiE
    # - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    # - http://www.youtube.com/embed/SA2iWivDJiE
    # - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    query = urlparse(url)
    if query.hostname == 'youtu.be': return query.path[1:]
    if query.hostname in {'www.youtube.com', 'youtube.com'}:
        if query.path == '/watch': return parse_qs(query.query)['v'][0]
        if query.path[:7] == '/embed/': return query.path.split('/')[2]
        if query.path[:3] == '/v/': return query.path.split('/')[2]
    # fail?
    return None

#takes id input to find specific video from url
id = extract_video_id("https://www.youtube.com/watch?v=e-EJ2DNWLL4")

chat = LiveChat(id, 
  processor = CompatibleProcessor() )

while chat.is_alive():
  try:
    data = chat.get()
    print(data)
    if data['items'] == []:
      print("error")
      chat.terminate()
    else:
    polling = data['pollingIntervalMillis']/1000
    for c in data['items']:
      if c.get('snippet'):
        print(f"[{c['authorDetails']['displayName']}]"
              f"-{c['snippet']['displayMessage']}")
        time.sleep(polling/len(data['items']))
  except KeyboardInterrupt:
    chat.terminate()