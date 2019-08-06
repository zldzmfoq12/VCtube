import os
import re
import sys
import json
import librosa
import argparse
import numpy as np
from tqdm import tqdm
from glob import glob
from pydub import silence
from pydub import AudioSegment
from functools import partial
import pandas as pd

from hparams import hparams
from utils import parallel_run, add_postfix
from audio import load_audio, save_audio, get_duration, get_silence

def abs_mean(x):
    return abs(x).mean()

def remove_breath(audio):
    edges = librosa.effects.split(
            audio, top_db=40, frame_length=128, hop_length=32)

    for idx in range(len(edges)):
        start_idx, end_idx = edges[idx][0], edges[idx][1]
        if start_idx < len(audio):
            if abs_mean(audio[start_idx:end_idx]) < abs_mean(audio) - 0.05:
                audio[start_idx:end_idx] = 0

    return audio


def read_audio(audio_path):
    return AudioSegment.from_file(audio_path)

def split_on_silence_with_pydub(
        audio_path, skip_idx=0, out_ext="wav",
        silence_thresh=-40, min_silence_len=400,
        silence_chunk_len=100, keep_silence=100):

    df = pd.read_csv(audio_path.split('audio')[0]+'text/subtitle.csv')
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
        
        segment.export(target_audio_path, out_ext)  # for soundsegment

        audio_paths.append(target_audio_path)

    return audio_paths

def split_on_silence_batch(audio_paths, method, **kargv):
    audio_paths.sort()
    method = method.lower()
    
    if method == "pydub":
        fn = partial(split_on_silence_with_pydub, **kargv)

    parallel_run(fn, audio_paths,
            desc="Split on silence", parallel=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--audio_pattern', required=True)
    parser.add_argument('--out_ext', default='wav')
    parser.add_argument('--method', default='pydub')
    config = parser.parse_args()

    audio_paths = glob(config.audio_pattern)

    split_on_silence_batch(
            audio_paths, config.method,
            out_ext=config.out_ext,
    )
