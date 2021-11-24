## Installation

1. Clone this repository
2. Create a virtual environment using your preferred method.
3. Install the requirements on the requirements.txt file (for must cases this can be done) with the following command:

```shell
pip install -r requirements.txt
```

## Preprocessing Word Clouds
I haven't add the code on Dash to show the Word Clouds, but I have added the code to generate them.
For the moment the Word Clouds are generated in a grey color with black color for the highlighted words. We need to 
update the HIGHLIGHTED_KEYWORDS variable on *wordclouds_generator.py*

Also, for some reason we don't have words for August 26 and August 27 so the program skips both days.
To generate the Word Clouds we can use the following command on the root folder of the project:

```shell
python wordcloud_generator.py twitter
```

This will create a folder called wordclouds and inside of it a folder name twitter with a Word Cloud for every day
of the period. If we want to generate wordclouds for Google trending topics (which we scraped using the same script we used to get twitter's).
just change the paramenter **twitter** for **google**

## Running the application

To run the application simply run the following command:

```shell
python app.py
```

This command will open a web server at the address 127.0.0.1:8050, open your web browser and go to that address to see the current state of the application