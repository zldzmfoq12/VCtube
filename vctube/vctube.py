#-*- coding: utf-8 -*- 
import os
import re
import sys
import csv
import json
import argparse
import tqdm
import youtube_dl
import pandas as pd
from glob import glob
from pydub import AudioSegment
from functools import partial
from collections import OrderedDict
from youtube_transcript_api import YouTubeTranscriptApi
from .utils import makedirs, parallel_run

class VCtube:
    def __init__(self, output_dir:str, youtube_url:str) -> None:
        self.output_dir = output_dir
        self.youtube_url = youtube_url
    
    def download_audio(self) -> None:
        base_dir="./datasets/"
        download_path = os.path.join(base_dir+self.output_dir+"/wavs", '%(id)s.%(ext)s')

        # youtube_dl options
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors':[{
                'key':'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '192'
            }],
            'postprocessors_args':[
                '-ar', '21000'
            ],
            'prefer_ffmpeg':True,
            'keepvideo':False,
            'outtmpl': download_path # 다운로드 경로 설정
        }

        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.youtube_url])
        except Exception as e:
            print('error', e)

    def download_captions(self) -> None:
        base_dir="./datasets/"
        c = self.output_dir
        video_id =[]
        text = []
        start = []
        duration = []
        names=[]
        full_names=[]
        file_list = os.listdir(base_dir+c+"/wavs/")
        file_list_wav = [file for file in file_list if file.endswith(".wav")]
        for f in tqdm.tqdm(file_list_wav):
            try:
                video = f.split(".wav")[0]
                subtitle = YouTubeTranscriptApi.get_transcript(video, languages=['ko'])
                for s in range(len(subtitle)-1):
                    video_id.append(video)
                    full_name = base_dir+c+'/wavs/'+video+'.'+str(s).zfill(4)+'.wav'
                    full_names.append(full_name)
                    name = video+'.'+str(s).zfill(4)+'.wav'
                    names.append(name)
                    subtitle[s]['text'] = ''.join([c for c in subtitle[s]['text'] if c not in ('!', '?', ',', '.', '\n', '~', '"', "'")])
                    text.append(subtitle[s]['text'])
                    start.append(subtitle[s]['start'])
                    duration.append(subtitle[s+1]['start'] - subtitle[s]['start'])
            except:
                pass

        df = pd.DataFrame({"id":video_id, "text":text, "start":start, "duration":duration, "name":full_names})
        makedirs(base_dir+c+'/text')
        df.to_csv(base_dir+c+'/text/subtitle.csv', encoding='utf-8')
        res = [i +'|'+ j for i, j in zip(names, text)] 
        df2 = pd.DataFrame({"name":res})
        df2.to_csv(base_dir+c+'/metadata.csv', encoding='utf-8', header=False, index=False)
        file_data=OrderedDict()
        for i in range(df.shape[0]):
            file_data[df['name'][i]]=df['text'][i]
        with open (base_dir+c+'/alignment.json', 'w', encoding="utf-8") as make_file:
            json.dump(file_data, make_file, ensure_ascii=False, indent="\n")
        print(c+' channel was finished')

    def audio_split(self) -> None:
        base_dir="./datasets/"+self.output_dir+'/wavs/*.wav'
        audio_paths = glob(base_dir)
        audio_paths.sort()
        fn = partial(split_with_caption)
        parallel_run(fn, audio_paths, desc="Split with caption", parallel=False)



def split_with_caption(audio_path, skip_idx=0, out_ext="wav") -> list:
    df = pd.read_csv(audio_path.split('wavs')[0]+'text/subtitle.csv')
    filename = os.path.basename(audio_path).split('.', 1)[0]

    audio = read_audio(audio_path)
    df2 = df[df['id'].apply(str)==filename]
    df2['end']=round((df2['start']+df2['duration'])*1000).astype(int)
    df2['start'] = round(df2['start']*1000).astype(int)
    edges = df2[['start', 'end']].values.tolist()
    
    audio_paths = []
    for idx, (start_idx, end_idx) in enumerate(edges[skip_idx:]):
        start_idx = max(0, start_idx)
        

        target_audio_path = "{}/{}.{:04d}.{}".format(
                os.path.dirname(audio_path), filename, idx, out_ext)

        segment=audio[start_idx:end_idx]
        
        segment.export(target_audio_path, "wav")  # for soundsegment

        audio_paths.append(target_audio_path)

    return audio_paths

def read_audio(audio_path):
    return AudioSegment.from_file(audio_path)



            
