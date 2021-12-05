import numpy as np
from progress import progress_bar
from wordcloud import WordCloud
import pandas as pd
import os
import sys

OUTPUT_FOLDER = '../assets'
HASHTAGS_FILE = '../hashtags'
HIGHLIGHTED_KEYWORDS = [
    'Happy 4th of July',
    '#AllCountriesMatter',
    '#NobodyLikesTrump',
    '#TrumpStroke',
    '#ImVotingForJoe',
    'FAKE PRESIDENT',
    'Hunter Biden',
    '#TrumpCrimeFamily',
    '#TrumpIsARacist',
    '#shutupman',
    'Fauci',
    '#TrumpISCompromised',
    '#ThankYouDoc',
    '#TRUMP2020ToSaveAmerica'
]
MISSING_DAYS = ['2020-08-26', '2020-08-27']


def create_mask():
    x, y = np.ogrid[:300, :300]
    mask = (x - 150) ** 2 + (y - 150) ** 2 > 130 ** 2
    mask = 255 * mask.astype(int)
    return mask


def color_function(word, **kwargs):
    return (50, 50, 50) if word in HIGHLIGHTED_KEYWORDS else (230, 230, 230)


def create_wordcloud_words(path=HASHTAGS_FILE, output_folder=OUTPUT_FOLDER):
    df = pd.read_csv(path, header=None)
    wc = WordCloud(
        background_color="white",
        relative_scaling=0.2,
        color_func=color_function,
        height=200,
        width=1000
    )
    rows = df.shape[0]
    if not os.path.exists(output_folder):
        os.makedirs(output_folder, exist_ok=True)
    for r in range(rows):
        progress_bar(r, rows, 'Creating word clouds')
        words = [word for word in df.iloc[r]]
        date = words.pop(0)
        if date in MISSING_DAYS:
            continue
        frequencies = {}
        words_number = len(words)
        for i, word in enumerate(words):
            frequencies[word] = words_number - i

        wordcloud = wc.generate_from_frequencies(frequencies)
        wordcloud.to_file(f'{output_folder}/{date}.png')
        # plt.imshow(wordcloud, interpolation='bilinear')
        # plt.axis("off")
        # plt.savefig(f'{output_folder}/{date}.png', format='png')


if __name__ == '__main__':
    folders = {
        'twitter': {
            'output_folder': OUTPUT_FOLDER + '/twitter',
            'path': HASHTAGS_FILE + '/hashtags.csv'
        },
        'google': {
            'output_folder': OUTPUT_FOLDER + '/google',
            'path': HASHTAGS_FILE + '/hashtags_google.csv'
        }
    }
    folder = folders['twitter']
    valid_arguments = ['twitter', 'google']
    if len(sys.argv) > 1:
        argument = sys.argv[1]
        if argument in folders.keys():
            folder = folders[argument]
        else:
            print("usage: python wordcloud_generator {twitter|google}")
            exit()

    create_wordcloud_words(**folder)
