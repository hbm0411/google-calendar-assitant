import requests
import json
import re

# Replace with your actual API key
API_KEY = 'AIzaSyB4Xi6TUJD2Xt3tjOiwNDHnp7zCelp0Exc'

# Replace with your desired channel ID
CHANNEL_ID = 'UCzkA5UTtr_vNYqMSB3DisVA'

# List of search queries
search_queries = [
    # "Peppa Pig Season 1 Episode"
    # "Muddy Puddles",
    # "Mr Dinosaur is Lost",
    # "Best Friend",
    # "Polly Parrot",
    # "Hide and Seek",
    # "The Playgroup",
    # "Mummy Pig at Work",
    # "Piggy in the Middle",
    # "Daddy Loses His Glasses",
    # "Gardening",
    "Hiccups",
    "Bicycles",
    "Secrets",
    "Flying a Kite",
    "Picnic",
    "Musical Instruments",
    "Frogs and Worms and Butterflies",
    "Dressing Up",
    "New Shoes",
    "The School Fete",
    "Mummy Pig's Birthday",
    # "The Tooth Fairy",
    # "The New Car",
    # "Treasure Hunt",
    # "Not Very Well",
    # "Snow",
    # "Windy Castle",
    # "My Cousin Chloé",
    # "Pancakes",
    # "Babysitting",
    # "Ballet Lesson",
    # "Thunderstorm",
    # "Cleaning the Car",
    # "Lunch",
    # "Camping",
    # "The Sleepy Princess",
    # "The Tree House",
    # "Fancy Dress Party",
    # "The Museum",
    # "Very Hot Day",
    # "Chloé's Puppet Show",
    # "Daddy Gets Fit",
    # "Tidying Up",
    # "The Playground",
    # "Daddy Puts Up a Picture",
    # "At the Beach",
    # "Mister Skinnylegs",
    # "Grandpa Pig's Boat",
    # "Shopping",
    # "My Birthday Party",
    # "Daddy's Movie Camera",
    # "School Play"
]

# Base URLs for YouTube Data API
search_url = 'https://www.googleapis.com/youtube/v3/search'
videos_url = 'https://www.googleapis.com/youtube/v3/videos'

# List to store results
results = []

def format_duration(iso_duration):
    # Regular expression to parse ISO 8601 duration
    pattern = re.compile(
        r'PT'                          # Starts with 'PT'
        r'(?:(\d+)H)?'                 # Optional hours
        r'(?:(\d+)M)?'                 # Optional minutes
        r'(?:(\d+)S)?'                 # Optional seconds
    )
    match = pattern.fullmatch(iso_duration)
    if not match:
        return iso_duration  # Return original if pattern doesn't match

    hours, minutes, seconds = match.groups()

    # Build the formatted duration string
    parts = []
    if hours:
        parts.append(f"{int(hours)}H")
    if minutes:
        parts.append(f"{int(minutes)}M")
    if seconds:
        parts.append(f"{int(seconds)}S")

    return ' '.join(parts)

for query in search_queries:
    
    # Step 1: Perform search.list API call
    search_params = {
        'part': 'snippet',
        'channelId': CHANNEL_ID,
        'q': query,
        'type': 'video',
        'maxResults': 3,
        'order': 'relevance',
        'key': API_KEY
    }
    search_response = requests.get(search_url, params=search_params)
    search_data = search_response.json()
    
    # Check if any items are returned
    if 'items' in search_data and len(search_data['items']) > 0:
        video_ids = [item['id']['videoId'] for item in search_data['items']]
        titles = [item['snippet']['title'] for item in search_data['items']]
        
        # Step 2: Perform videos.list API call to get video durations
        videos_params = {
            'part': 'contentDetails',
            'id': ','.join(video_ids),
            'key': API_KEY
        }
        videos_response = requests.get(videos_url, params=videos_params)
        videos_data = videos_response.json()
        
        # Check if any items are returned
        if 'items' in videos_data and len(videos_data['items']) > 0:
            video_result_list = []
            for i, video in enumerate(videos_data['items']):
                duration = video['contentDetails']['duration']
                formatted_duration = format_duration(duration)
                result = {
                    'title': titles[i],
                    'data': {
                        'videoId': video_ids[i],
                        'duration': formatted_duration
                    }
                }
                video_result_list.append(result)
            results.append({
                'title': query,
                'data': video_result_list
            })

# Output the results in JSON format
print(json.dumps(results, indent=2))
with open('results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
