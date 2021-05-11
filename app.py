import os

import googleapiclient.discovery
from textblob import TextBlob
import pandas as pd


from flask import Flask, request, render_template


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    # return 'Hello, World!'
    if request.method == 'POST':
        try:
            url =request.form['url']
            if "youtube.com/watch?v=" not in url:
                return render_template('index.html', error="Url invalid")
            videoId = url[url.find('=')+1:]
            os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

            api_service_name = "youtube"
            api_version = "v3"
            DEVELOPER_KEY = "YOUR_API_KEY"

            youtube = googleapiclient.discovery.build(
                api_service_name, api_version, developerKey = 'AIzaSyB9M8at9waqOd3CjpdHvKKIBoMRfg0U2Ws')
            req = youtube.commentThreads().list(
                part="snippet",
                maxResults=5,
                textFormat="plainText",
                videoId=videoId
            )

            response = req.execute()

            #filter data yang didapat dari api
            data = []
            for i in response['items']:
                originText = i['snippet']["topLevelComment"]["snippet"]["textOriginal"]
                data.append(originText)

            #membersihkan komentar dari tanda baca
            df = pd.DataFrame({'clean' : data})
            df['clean'] = df['clean'].apply(lambda x: " ".join(word.lower() for word in x.split()))
            df['clean'] = df['clean'].str.replace('[^\w\s]', '')
            print(data)

            #mengolah komentar menggunakan TextBlob
            finalResult = []
            iteration = 0
            for i in df.values.tolist():
                tb = TextBlob(i[0])
                result = tb.sentiment
                if result.polarity < 0:
                    react = 'negative'
                elif result.polarity == 0:
                    react = 'neutral'
                elif result.polarity > 0:
                    react = 'positive'

                #hasil akhir
                finalResult.append({
                    'comment' : data[iteration],
                    'clearComment' : i[0],
                    'polarity' :  result.polarity,
                    'subjectivity' :  result.subjectivity,
                    'react' : react

                })
                iteration+=1

            return render_template('index.html', url=finalResult)
        except:
            return render_template('index.html', error="Something error")
    else:
        return render_template('index.html')
        
