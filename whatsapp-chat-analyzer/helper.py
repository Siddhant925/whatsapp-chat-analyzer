from urlextract import URLExtract
from wordcloud import WordCloud
import emoji
extractor = URLExtract()

def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]

    words = []
    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))
        words.extend(message.split())

    media_shared = df['message'].str.startswith('<', na=False).sum()

    return num_messages, words, media_shared, links

def fetch_most_busy_users(df):
    x = df['user'].value_counts().head()
    return x

def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    wc = WordCloud(
        width=800,
        height=400,
        min_font_size=10,
        background_color='white'
    )

    df_wc = wc.generate(df['message'].str.cat(sep=' '))

    return df_wc

def most_common_words(selected_user, df):
    temp = df[df['user'] != 'group_notification']
    
    if selected_user != 'Overall':
        temp = temp[temp['user'] == selected_user]
        
    temp = temp[~temp['message'].str.startswith('<', na=False)]

    with open('stop_hinglish.txt', 'r', encoding='utf-8') as f:
        stop_words = set(f.read().splitlines())
    
    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    return words

def emoji_analysis(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([item['emoji'] for item in emoji.emoji_list(message)])

    return emojis
    