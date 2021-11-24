import pandas as pd

INPUT_PATH = '../preprocess_data/uselection_tweets_1jul_11nov.csv'


def load_data(path=INPUT_PATH):
    # Load dataset
    df = pd.read_csv(path, sep=';', parse_dates=True)
    # Select columns
    df = df[['Created-At', 'PartyName', 'Score']]
    # Exclude other parties
    df = df[df.PartyName != 'BothParty']
    df = df[df.PartyName != 'Neither']
    df['Created-At'] = pd.to_datetime(df['Created-At'])
    df = df.groupby([df['Created-At'].dt.date, df['PartyName']]).mean()
    return df

if __name__ == '__main__':
    load_data()
