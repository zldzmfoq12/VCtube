import os
import re
import sys
import json
import argparse
import pandas as pd
from functools import partial
from collections import OrderedDict
from youtube_transcript_api import YouTubeTranscriptApi

def download_captions():
    for i in channels:
        video_id =[]
        text = []
        start = []
        duration = []
        file_list = os.listdir(base_dir)
        file_list_wav = [file for file in file_list if file.endswith(".wav")]
        for f in file_list_wav:
            try:
                video = f.split(".wav")[0]
                subtitle = YouTubeTranscriptApi.get_transcript(video)
                for s in range(len(subtitle)-1):
                    video_id.append(video)
                    name = basedir+i+'/audio/'+c+'.'+str(i).zfill(4)+'.wav'
                    names.append(name)
                    subtitle[s]['text'] = ''.join([c for c in s['text'] if c not in ('!', '?', ',', '.', '\n', '~', '"', "'")])
                    text.append(subtitle[s]['text'])
                    start.append(int(subtitle[s]['start']))
                    duration.append(subtitle[s+1]['start']-subtitle[s]['start'])
            except:
                pass
        df = pd.DataFrame({"id":id, "text":text, "start":start, "duration":duration, "name":names})
        df.to_csv(base_dir+i+'/text/subtitle.csv', encoding='utf-8')
        file_data=OrderedDict()
        for i in range(df.shape[0]):
            file_data[df['name'][i]]=df['text'][i]
        with open (base_dir+i+'/alignment.json', 'w', encoding="utf-8") as make_file:
            json.dump(file_data, make_file, ensure_ascii=False, indent="\n")
        print(i+' channel was finished')
        
def download_caption_batch(base_dirs, channels):

    fn = partial(download_captions, **kargv)

    parallel_run(fn, channels,
            desc="Download caption", parallel=False)
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--base_dir', required=True)
    parser.add_argument('--channels', required=True)
    
    config = parser.parse_args()
    config.channels = config.channels.split(",")

    download_caption_batch(
            config.base_dir, config.config.channels,
    )
