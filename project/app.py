import requests, sys, time, os, argparse
import getopt, pprint
import json
import time
from flask import Flask
from flask import render_template
from pymongo import MongoClient
from bson import json_util
import pandas as pd


app = Flask(__name__)


client = MongoClient('mongodb+srv://kaveesha:BDATGeorgian@cluster0-xs3bw.mongodb.net/test?retryWrites=true&w=majority')
DBS_NAME = client.get_database('youtube')
COLLECTION_NAME = DBS_NAME.videos

"""""
x = 0
while True:
    x = x+1
    #r = requests.get("https://www.googleapis.com/youtube/v3/videos?part=id,statistics,snippet&chart=mostPopular&regionCode=CA&maxResults=10&key=AIzaSyDRMOciWMbsexg5fw6VVGwd7gB5yEpxCfM&format=json")
    r = requests.get("https://api.donorschoose.org/common/json_feed.html?subject1=-1&APIKey=DONORSCHOOSE")
    if r.status_code == 200:
        data = r.json()
        #print(data)
        DBS_NAME.projects.insert_one(data)
        ##Sleep for 24 hours (86400 sec)
        #time.sleep(86400)
    else:
        exit()
    if x==1:
        break
"""""

# List of simple to collect features
snippet_features = ["title",
                    "publishedAt",
                    "channelId",
                    "channelTitle",
                    "categoryId"]

# Any characters to exclude, generally these are things that become problematic in CSV files
unsafe_characters = ['\n', '"']

# Used to identify columns, currently hardcoded order
header = ["video_id"] + snippet_features + ["trending_date", "tags", "view_count", "likes", "dislikes",
                                            "comment_count", "thumbnail_link", "comments_disabled",
                                            "ratings_disabled", "description"]
#"""""
def setup(api_path, code_path):
    with open(api_path, 'r') as file:
        api_key = file.readline()
        #api_key = file.readline().strip()

    with open(code_path) as file:
        country_codes = [x.rstrip() for x in file]

    return api_key, country_codes


def prepare_feature(feature):
    # Removes any character from the unsafe characters list and surrounds the whole item in quotes
    for ch in unsafe_characters:
        feature = str(feature).replace(ch, "")
    return f'"{feature}"'


def api_request(page_token, country_code):
    # Builds the URL and requests the JSON from it
    request_url = f"https://www.googleapis.com/youtube/v3/videos?part=id,statistics,snippet{page_token}chart=mostPopular&regionCode={country_code}&maxResults=50&key={api_key}"
    #request_url = f'https://www.googleapis.com/youtube/v3/videos?part=id,statistics,snippetchart=mostPopular&regionCode=CA&maxResults=50&key=AIzaSyDRMOciWMbsexg5fw6VVGwd7gB5yEpxCfM'
    print (request_url)
    request = requests.get(request_url)
    if request.status_code == 429:
        print("Temp-Banned due to excess requests, please wait and continue later")
        sys.exit()
    return request.json()


def get_tags(tags_list):
    # Takes a list of tags, prepares each tag and joins them into a string by the pipe character
    return prepare_feature("|".join(tags_list))


def get_videos(items):
    lines = []
    for video in items:
        comments_disabled = False
        ratings_disabled = False

        # We can assume something is wrong with the video if it has no statistics, often this means it has been deleted
        # so we can just skip it
        if "statistics" not in video:
            continue

        # A full explanation of all of these features can be found on the GitHub page for this project
        video_id = prepare_feature(video['id'])

        # Snippet and statistics are sub-dicts of video, containing the most useful info
        snippet = video['snippet']
        statistics = video['statistics']

        # This list contains all of the features in snippet that are 1 deep and require no special processing
        features = [prepare_feature(snippet.get(feature, "")) for feature in snippet_features]

        # The following are special case features which require unique processing, or are not within the snippet dict
        description = snippet.get("description", "")
        thumbnail_link = snippet.get("thumbnails", dict()).get("default", dict()).get("url", "")
        trending_date = time.strftime("%y.%d.%m")
        tags = get_tags(snippet.get("tags", ["[none]"]))
        view_count = statistics.get("viewCount", 0)

        # This may be unclear, essentially the way the API works is that if a video has comments or ratings disabled
        # then it has no feature for it, thus if they don't exist in the statistics dict we know they are disabled
        if 'likeCount' in statistics and 'dislikeCount' in statistics:
            likes = statistics['likeCount']
            dislikes = statistics['dislikeCount']
        else:
            ratings_disabled = True
            likes = 0
            dislikes = 0

        if 'commentCount' in statistics:
            comment_count = statistics['commentCount']
        else:
            comments_disabled = True
            comment_count = 0

        # Compiles all of the various bits of info into one consistently formatted line
        line = [video_id] + features + [prepare_feature(x) for x in [trending_date, tags, view_count, likes, dislikes,
                                                                       comment_count, thumbnail_link, comments_disabled,
                                                                       ratings_disabled, description]]
        lines.append(",".join(line))
    return lines


def get_pages(country_code, next_page_token="&"):
    country_data = []

    # Because the API uses page tokens (which are literally just the same function of numbers everywhere) it is much
    # more inconvenient to iterate over pages, but that is what is done here.
    while next_page_token is not None:
        # A page of data i.e. a list of videos and all needed data
        video_data_page = api_request(next_page_token, country_code)

        # Get the next page token and build a string which can be injected into the request with it, unless it's None,
        # then let the whole thing be None so that the loop ends after this cycle
        next_page_token = video_data_page.get("nextPageToken", None)
        next_page_token = f"&pageToken={next_page_token}&" if next_page_token is not None else next_page_token

        # Get all of the items as a list and let get_videos return the needed features
        items = video_data_page.get('items', [])
        country_data += get_videos(items)

    return country_data


def write_to_file(country_code, country_data):

    print(f"Writing {country_code} data to file...")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(f"{output_dir}/{country_code}_videos.csv", "w+", encoding='utf-8') as file:
        for row in country_data:
            file.write(f"{row}\n")


def get_data():
    x= 0
    #while True:
      #  x = x+1
    for country_code in country_codes:
        country_data = [",".join(header)] + get_pages(country_code)
        write_to_file(country_code, country_data)
        #Sleep for 24 hours (86400 secs)
        #time.sleep(2) # for demo purpose this is reduced to 24 seconds
       # if x == 1:
         #   break


def import_content(filepath):
    cdir = os.path.dirname(__file__)
    file_res = os.path.join(cdir, filepath)
    data = pd.read_csv(file_res)
    data_json = json.loads(data.to_json(orient='records'))
    print(COLLECTION_NAME.find())
    i = 0
    for data in data_json:
        i = i+1
        COLLECTION_NAME.insert_one(data)
#"""
#Define which attributes to query
#FIELDS = {'__id': 0}
#FIELDS = {'state': True, 'resource': True, 'poverty_Type': True, 'expirationDate': True, 'numDonors': True, '_id': False}
#FIELDS = {'_id': 0, 'proposals': [{'state': 1,'resource': 1, 'povertyType' : {'label': 1}, 'numDonors': 1, 'expirationDate': 1}]}
FIELDS = {'_id': False, 'title': True,'channelTitle': True, 'trending_date': True, 'view_count': True, 'likes': True, 'dislikes': True, 'comment_count': True, 'channelTitle' : True}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/YouTubeCA/TrendingVideos")
def youtube_videos():
    connection = MongoClient('mongodb+srv://kaveesha:BDATGeorgian@cluster0-xs3bw.mongodb.net/test?retryWrites=true&w=majority')
    DBS_NAME = client.get_database('youtube')
    collection = DBS_NAME.videos

    # Retrieve all the records along the 5 attributes that we are interested in
    videos = collection.find({}, projection=FIELDS, limit=10).sort([("trending_date", -1)])
    json_videos = []
    for video in videos:
        json_videos.append(video)
    json_videos = json.dumps(json_videos, default=json_util.default)
    connection.close()
    return json_videos


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--key_path', help='Path to the file containing the api key, by default will use api_key.txt in the same directory', default='api_key.txt')
    parser.add_argument('--country_code_path', help='Path to the file containing the list of country codes to scrape, by default will use country_codes.txt in the same directory', default='country_codes.txt')
    parser.add_argument('--output_dir', help='Path to save the outputted files in', default='output/')

    args = parser.parse_args()

    output_dir = args.output_dir
    api_key, country_codes = setup(args.key_path, args.country_code_path)

    filepath = args.output_dir + "/CA_videos.csv"
    get_data()
    #filepath = '/Users/kaveeshasavindi/PycharmProjects/project/output/CA_videos.csv'
    import_content(filepath)
    app.run(host='0.0.0.0', port=5000, debug=True)

