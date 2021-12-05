import tweepy
import csv
from tqdm import tqdm
import math
import sys
import os
# import urllib.request

if(len(sys.argv)<7):
    print("usage: python get_tweet_strings.py start_row end_row consumer_key consumer_secret access_token access_token_secret")
    print("(!) consumer_key, consumer_secret, access_token, and access_token_secret require Twitter API access")
    exit()

APIkey = 0
start_row = int(sys.argv[1]) #(included) 
end_row = int(sys.argv[2]) #(included)

consumer_key0 = sys.argv[3]
consumer_secret0 = sys.argv[4]
access_token0 = sys.argv[5]
access_token_secret0 = sys.argv[6]

auth0 = tweepy.OAuthHandler(consumer_key0, consumer_secret0)
auth0.set_access_token(access_token0, access_token_secret0)

# if the process/code stops because of an error, please make sure to update the following manually after checking the last row of csv:
# 1. start_row variable
# 2. fileName variable (if incorrect, to attend to correct file)

start_sheet_name = 50000*(start_row//50000)+1 #for csv_file variable
end_sheet_name = 50000*(math.ceil(end_row/50000)) #for csv_file variable
fileName = './data/processed_data/processed_data_'+str(start_sheet_name)+'_'+str(end_sheet_name)+'.csv' #CSV with the tweet string (will be created if not existing, else rows will be appended)

ieee_dataset_file = "./uselection_tweets_1jul_11nov.csv"

if(os.path.exists(ieee_dataset_file)):
    csv_file = open(ieee_dataset_file, encoding="utf-8") #CSV containing data from IEEE dataset
else:
    print("===========\n(!) IEEE Dataset doesn't exist on local drive.\n\nPlease download the file using the following command/link and place in the same folder as this python file and then re-run.")
    print("-----------\nIEEE Website: https://ieee-dataport.org/open-access/usa-nov2020-election-20-mil-tweets-sentiment-and-party-name-labels-dataset#files")
    print('-----------\nOneDrive download URL (expires Feb 3, 2020): \nhttps://gtvault-my.sharepoint.com/:x:/g/personal/hgajjar3_gatech_edu/EeIuX6pMTNlGnXrEmKUlD14B2r86btLYU8BX8mqdicwLHw?e=Ys5P4I&download=1')
    print('-----------\nBash command to download from above link (expires Feb 3, 2020): \nwget -O uselection_tweets_1jul_11nov.csv "https://gtvault-my.sharepoint.com/:x:/g/personal/hgajjar3_gatech_edu/EeIuX6pMTNlGnXrEmKUlD14B2r86btLYU8BX8mqdicwLHw?e=Ys5P4I&download=1"')
    #Link expires Feb 3, 2020
    #if expired download the csv file from here: https://ieee-dataport.org/open-access/usa-nov2020-election-20-mil-tweets-sentiment-and-party-name-labels-dataset#files
    # url = 'https://gtvault-my.sharepoint.com/:x:/g/personal/hgajjar3_gatech_edu/EeIuX6pMTNlGnXrEmKUlD14B2r86btLYU8BX8mqdicwLHw?e=Ys5P4I&download=1'
    # urllib.request.urlretrieve(url, filename="uselection_tweets_1jul_11nov.csv")
    # os.system('wget -O uselection_tweets_1jul_11nov.csv "https://gtvault-my.sharepoint.com/:x:/g/personal/hgajjar3_gatech_edu/EeIuX6pMTNlGnXrEmKUlD14B2r86btLYU8BX8mqdicwLHw?e=Ys5P4I&download=1"')
    # print()
    inp = input("-----------\nDo you want to run the above bash command using os.system and continue with execution(y/[n]):")
    if(inp=="y"):
        os.system('wget -O uselection_tweets_1jul_11nov.csv "https://gtvault-my.sharepoint.com/:x:/g/personal/hgajjar3_gatech_edu/EeIuX6pMTNlGnXrEmKUlD14B2r86btLYU8BX8mqdicwLHw?e=Ys5P4I&download=1"')
        print('-----------\nDownload complete')
        csv_file = open(ieee_dataset_file, encoding="utf-8") #CSV containing data from IEEE dataset
    else:
        print("-----------\nOkay, no problem. \nPlease place the manually downloaded file in the same directory as this python file")
        print("===========")
        exit()

#which key to use?
api0 = tweepy.API(auth0)
api = eval("api"+str(APIkey))

current_row = 0
current_data_count = 0
current_data = []
current_ids = []

csv_reader = csv.reader(csv_file, delimiter=';')
f = open(fileName, 'a', encoding="utf-8")
print("Creating file:",fileName)

writer = csv.writer(f)
newCols = ["Simple-ID", "Created-At","From-User-Id","To-User-Id","Language",
            "Retweet-Count","PartyName","Id","Score","Scoring String",
            "Negativity","Positivity","Uncovered Tokens","Total Tokens",
            "Creation-Month","Creation-Date","Creation-Year","Creation-Time","Tweet-Text",
            "Retweet_Count_From_API","Favourite_Count_From_API","Username","Followers_Count","Location","Verified","Created_At","Author_Info"]

if(start_row==1):
    writer.writerow(newCols)

colRead=False

with tqdm(initial=start_row) as progress_bar:
    # progress_bar.update(start_row)

    for row in csv_reader:
        if(not colRead):
            colRead=True
            continue

        current_row+=1

        if(current_row < start_row):
            # print("[skipped] current_row:",current_row)
            continue

        newRow = [current_row] + row + row[0].split(" ")[0].split("/") + [" ".join(row[0].split(" ")[1:])]
        
        current_data.append(newRow)
        current_data_count+=1

        if(current_data_count==100 or current_row==end_row):
            current_ids = list(map(lambda x: x[7], current_data))
            # print(current_row, "reached")
            
            progress_bar.update(100)

            tweets = api.lookup_statuses(current_ids[0:]) # id_list is the list of tweet ids

            for tweet in tweets:
                current_data[current_ids.index(tweet.id_str)] = current_data[current_ids.index(tweet.id_str)]+[tweet.text,
                                                                                                    tweet.retweet_count, 
                                                                                                    tweet.favorite_count, 
                                                                                                    tweet.author._json['screen_name'], 
                                                                                                    tweet.author._json['followers_count'], 
                                                                                                    tweet.author._json['location'],
                                                                                                    tweet.author._json['verified'],
                                                                                                    tweet.author._json['created_at'],
                                                                                                    tweet.author]

            for newRow in current_data:
                writer.writerow(newRow)

            current_data=[]
            current_data_count=0

        if(current_row==end_row+1):
            break


f.close()