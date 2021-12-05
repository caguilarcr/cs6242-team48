# CS6242 - Group 48

## Members
- Carlos Aguilar
- Harshal Gajjar
- Akshay Jadiya
- Arushi Agrawal
- Ramin Dabirian

## Usage

### 1. Install dependencies
1. *[Recommended]* Create a new virtual environment
2. Install all packages listed in `requirements.txt` using the command `python -m pip install -r requirements.txt` 

### 2. Processing Tweet stances
Don't want to run this step? Feel free to skip and use the output files we have already generated and skip to step 4.

#### 2.1. Download the partial dataset
1. Download the csv containing 20M tweet IDs (and some more information) of 2020 related election tweets from:
	- [No expiry; account required] [IEEE Website](https://ieee-dataport.org/open-access/usa-nov2020-election-20-mil-tweets-sentiment-and-party-name-labels-dataset#files)
	- [Expires Feb 3, 2020; no account required] [OneDrive](https://gtvault-my.sharepoint.com/:x:/g/personal/hgajjar3_gatech_edu/EeIuX6pMTNlGnXrEmKUlD14B2r86btLYU8BX8mqdicwLHw?e=Ys5P4I&download=1)
2. Place the downloaded csv file named `uselection_tweets_1jul_11nov.csv` in the same folder as `get_tweet_strings.py`

#### 2.2. Fetch tweet strings using Twitter API
Don't want to run? Look at the sample output of this step: `./data/processed_data/sample_processed_data_1_50000.csv` or the complete output on OneDrive [here](https://gtvault-my.sharepoint.com/:f:/g/personal/hgajjar3_gatech_edu/Eipvk4-oYiRHmfEkMMM95-YB5nerkGsd_g1_8xStn7jMNQ?e=XOEjU8).

1. Run the following command to process the first 50k tweet IDs in `uselection_tweets_1jul_11nov.csv` and generate a new csv `./data/processed_data/processed_data_1_50000.csv` containing tweet strings (and some more information dump).
```
python get_tweet_strings.py 1 50000 "<consumer_key>" "<consumer_secret>" "<access_token>" "<access_token_secret>"
```
2. Repeat the above process to get all the tweet strings, next command in the sequence:
```
python get_tweet_strings.py 50001 100000 "<consumer_key>" "<consumer_secret>" "<access_token>" "<access_token_secret>"
```

> **Note:** All our generated data sheets are batched in size of `50k`. And hence all the start/end indices are of the form: `i*50000+1`,  `(i+1)*50000` where `i` belongs to the set `{0,1,2,...,399}`

####  2.3. Compute tweet string stance
Don't want to run? Look at the sample output of this step: `./data/processed_data_stance/sample_processed_data_stance_1_50000.csv` or the complete output on OneDrive [here](https://gtvault-my.sharepoint.com/:f:/g/personal/hgajjar3_gatech_edu/EvEbD-DZgbxCs9_5h3ZH1xYBXVBQ5LdkWLxDhbyN7T6ZpA?e=xSVYTA).

1. Once a csv file containing tweet strings has been placed in `./data/processed_data/`, the following command can be executed to compute stance. It will process appropriate csv from `./data/processed_data` to generate a similarly named new csv with stance in the folder `./data/processed_data_stance/`
```
python get_tweet_stance.py 1 50000
# reads: ./data/processed_data/processed_data_1_50000.csv
# generates: ./data/processed_data_stance/processed_data_stance_1_50000.csv
```
2. Repeat the above step to compute stance for each of the 20 million tweets.

#### 2.4. Aggregate the tweet stance data
Don't want to run? Look at the sample output of this step: `./data/processed_data_stance_aggregated/sample_stance_democrat_50000_1.csv` or the complete output on OneDrive [here](https://gtvault-my.sharepoint.com/:f:/g/personal/hgajjar3_gatech_edu/Ei0mb8yP_PlJof-b4HDwQYoB5hU610VEU88sTJlkPE_waA?e=kWbVRU).

1. Once csv files are populated in `./data/processed_data_stance/`, following command can be executed to get new csv in `./data/processed_data_stance_aggregated/` with day-wise aggregated stance values (total stance, total count) for each day.
```
python aggregate_stance_values.py
```

**Note:** `aggregate_stance_values.py` processes all sheets present in `./data/processed_data_stance` in a single go. Hence, looping is not required in this step.

#### 2.5. Cleaning of aggregate data
1. All the csv files generated in `./data/processed_data_stance_aggregated` need to be unified in a single sheet. 
2. Later, days with multiple rows (i.e. spread across multiple 50k tweet sheets) need to be grouped together.
3. *[Optional]* Data needs to be normalised. We subtracted the standard deviation and divided by the mean per day.
4. Upon doing this, save the final result as `./data/final_chart_data.csv/`. 
**Note** that our processed output already exists at the same location.


### 3. Processing Trending Hashtags
Requires Google Chrome, and access to [this](https://us.trend-calendar.com/trend) website containing historical trends. 
Don't want to run this step? Feel free to skip and use the output files we have already generated and skip to step 4.

1. Download `ChromeDriver` for your installed version of chrome from [here](https://chromedriver.chromium.org/downloads). Upon downloading change the line 8 in `./hashtags/scrapper.py` to point to the download driver's location. Also, line 20 can be changed from `twitter` to `google` to get trends from Google instead of Twitter.
2. Run the following command to get trending hashtags on the dataset's range of dates. This will create a new file `./data/hashtags.csv` with top trends for each row/date. 
**Note** that our output already exists at the same location.
```
cd ./hashtags
python scrapper.py
cd ..
```
3. Run the following command to generate word cloud for each of the days. This will populate the folder `./assets/google` with png files. Note that our output already exists at the same locations.
```
cd ./hashtags
python wordcloud_generator.py
cd..
```

### 4. Run Visualisation Server
Upon generation of stance data (from step 2) and trending topics/hashtags (from step 3), run the following command to launch an interactive webpage that uses port 8080.
```
python launch_visualisation_server.py
```
