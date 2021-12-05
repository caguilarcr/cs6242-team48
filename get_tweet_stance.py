from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np
import csv
from tqdm import tqdm
import math
import sys
import os

if(len(sys.argv)<3):
    print("usage: python get_tweet_strings.py start_row end_row")
    exit()

start_row = int(sys.argv[1]) #(included) 
end_row = int(sys.argv[2]) #(included)

start_sheet_name = 50000*(start_row//50000)+1 #for csv_file variable
end_sheet_name = 50000*(math.ceil(end_row/50000)) #for csv_file variable

current_row = start_sheet_name

processed_data_filePath = './data/processed_data/processed_data_'+str(start_sheet_name)+'_'+str(end_sheet_name)+'.csv'
if(not os.path.exists(processed_data_filePath)):
    print("===========\n(!) '"+processed_data_filePath+"' file not found.")
    print("-----------\nPlease generate the processed data file using tweet.py first using the following command:")
    print("python tweet.py "+str(start_sheet_name)+" "+str(end_sheet_name)+" consumer_key consumer_secret access_token access_token_secret")
    print("(!) consumer_key, consumer_secret, access_token, and access_token_secret require Twitter API access")
    print("===========")
    exit()
else:
    csv_file = open(processed_data_filePath, encoding="utf-8", errors='ignore') #CSV containing tweets (generated using tweet_extractor.ipynb)

# run in case of dependency errors:
# pip install transformers
# pip install torch==1.8.0 torchvision==0.9.0 torchaudio==0.8.0

device = "cuda:0" if torch.cuda.is_available() else "cpu"
print("PyTorch likes", device, "too")

# select mode path here
# see more at https://huggingface.co/kornosk
pretrained_LM_path_biden = "kornosk/bert-election2020-twitter-stance-biden-KE-MLM"
pretrained_LM_path_trump = "kornosk/bert-election2020-twitter-stance-trump-KE-MLM"

# load model for biden
tokenizer_biden = AutoTokenizer.from_pretrained(pretrained_LM_path_biden)
model_biden = AutoModelForSequenceClassification.from_pretrained(pretrained_LM_path_biden)
model_biden=model_biden.to(device)

# Load model for trumo
tokenizer_trump = AutoTokenizer.from_pretrained(pretrained_LM_path_trump)
model_trump = AutoModelForSequenceClassification.from_pretrained(pretrained_LM_path_trump)
model_trump=model_trump.to(device)

id2label = {
    0: "AGAINST",
    1: "FAVOR",
    2: "NONE"
}

print("Processing file:"+processed_data_filePath)

csv_reader = csv.reader(csv_file, delimiter=',')

fileName = './data/processed_data_stance/processed_data_stance_'+str(start_sheet_name)+'_'+str(end_sheet_name)+'.csv'
print("Creating file:",fileName)

f = open(fileName, 'a', encoding="utf-8", errors='ignore') #CSV with stance (will be created if not existing, else rows will be appended)

writer = csv.writer(f)
# newCols = ["Simple-ID", "Created-At","From-User-Id","To-User-Id","Language",
#             "Retweet-Count","PartyName","Id","Score","Scoring String",
#             "Negativity","Positivity","Uncovered Tokens","Total Tokens",
#             "Creation-Month","Creation-Date","Creation-Year","Creation-Time","Tweet-Text",
#             "Retweet_Count_From_API","Favourite_Count_From_API","Username","Followers_Count","Location","Verified","Created_At","Author_Info",
#             "biden_against","biden_favor","biden_neutral","trump_against","trump_favor","trump_neutral"]

# if(start_row==1):
#     writer.writerow(newCols)

colRead=False
for row in tqdm(csv_reader):
    # print(len(row),row)

    # if(not colRead):
    #     colRead=True
    #     continue

    if(len(row)==0):
        #blank row
        continue

    if(row[0]==''):
        #blank row
        continue

    current_row=int(row[0])

    if(current_row < start_row):
        # print("[skipped] current_row:",current_row)
        continue

    if(len(row)<19):
        #no tweet extracted
        writer.writerow(row)
    else:
        if(row[6] == 'Democrats'):
            sentence = row[18]
            inputs = tokenizer_biden(sentence, return_tensors="pt").to(device)
            outputs = model_biden(**inputs)
            prob_cols = torch.softmax(outputs[0], dim=1)[0].tolist() + [0,0,0]
        elif(row[6] == 'Republicans'):
            sentence = row[18]
            inputs = tokenizer_trump(sentence, return_tensors="pt").to(device)
            outputs = model_trump(**inputs)
            prob_cols = [0,0,0] + torch.softmax(outputs[0], dim=1)[0].tolist()
        else:
            sentence = row[18]
            inputs_biden = tokenizer_biden(sentence, return_tensors="pt").to(device)
            outputs_biden = model_biden(**inputs_biden)
            
            inputs_trump = tokenizer_trump(sentence, return_tensors="pt").to(device)
            outputs_trump = model_trump(**inputs_trump)
            
            predicted_probability_biden = torch.softmax(outputs_biden[0], dim=1)[0].tolist()
            predicted_probability_trump = torch.softmax(outputs_trump[0], dim=1)[0].tolist()

            prob_cols = predicted_probability_trump+predicted_probability_biden
        
        newRow = row + prob_cols
        writer.writerow(newRow)

    if(current_row==end_row):
        break


f.close()