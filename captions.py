import os
import re
import sys
import argparse
import pandas as pd
from functools import partial
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
        subtitle_list =  list(zip(video_id, text, start, duration))
        dfObj = pd.DataFrame(subtitle_list)
        dfObj.to_csv(base_dir+i+'/text/subtitle.csv', index=False, header =False)
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
