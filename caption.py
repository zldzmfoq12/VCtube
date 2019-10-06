import os
import re
import sys
import json
import argparse
import tqdm
import pandas as pd
from functools import partial
from collections import OrderedDict
from youtube_transcript_api import YouTubeTranscriptApi
from utils import download_with_url, makedirs, parallel_run

def download_captions(channels):
    base_dir="./datasets/"
    c = channels
    print(c)
    video_id =[]
    text = []
    start = []
    duration = []
    names=[]
    file_list = os.listdir(base_dir+c+"/audio/")
    file_list_wav = [file for file in file_list if file.endswith(".wav")]
    # print(file_list_wav)
    for f in tqdm.tqdm(file_list_wav):
        try:
            video = f.split(".wav")[0]
            subtitle = YouTubeTranscriptApi.get_transcript(video)
            # print(subtitle)
            # break
            for s in range(len(subtitle)-1):
                # print(s)
                video_id.append(video)
                name = base_dir+c+'/audio/'+video+'.'+str(s).zfill(4)+'.wav'
                names.append(name)
                # print(subtitle[s]['text'])
                subtitle[s]['text'] = ''.join([c for c in subtitle[s]['text'] if c not in ('!', '?', ',', '.', '\n', '~', '"', "'")])
                # print(subtitle[s])
                text.append(subtitle[s]['text'])
                start.append(subtitle[s]['start'])
                duration.append(subtitle[s+1]['start'] - subtitle[s]['start'])
        except:
            # print(e)
            pass

    print(len(text), len(start), len(duration), len(names))
    df = pd.DataFrame({"id":video_id, "text":text, "start":start, "duration":duration, "name":names})
    makedirs(base_dir+c+'/text')
    df.to_csv(base_dir+c+'/text/subtitle.csv', encoding='utf-8')
    file_data=OrderedDict()
    for i in range(df.shape[0]):
        file_data[df['name'][i]]=df['text'][i]
    with open (base_dir+c+'/alignment.json', 'w', encoding="utf-8") as make_file:
        json.dump(file_data, make_file, ensure_ascii=False, indent="\n")
    print(c+' channel was finished')
        
def download_caption_batch(channels):
    print(channels)
    download_captions(channels)
    # fn = partial(download_captions)
    #
    # parallel_run(fn, channels,
    #         desc="Download caption", parallel=False)
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument('--base_dir', required=True)
    parser.add_argument('--channels', required=True)
    
    config = parser.parse_args()

    download_caption_batch(
            config.channels
    )
