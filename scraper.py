#Author: Chris Greening
#Date: 10/01/2020
#Purpose: Web scraper for getting data from Instagram

import os
import datetime
import time
import csv

import tqdm
import numpy as np
from instascrape import Hashtag

def _load_data_into_files(data, fp):
    """Load data into .csv"""
    with open(fp, 'a', newline='') as out:
        w = csv.DictWriter(out, fieldnames=['hashtag', 'posts', 'datetime'])
        if os.path.getsize(fp) == 0:
            w.writeheader()
        for indv in data:
            w.writerow(indv)

def _load_hashtags_from_txt(fpath: str) -> list :
    """Load hashtags from txt file"""
    with open(fpath, 'r') as infile:
        tags = infile.read().splitlines()
    return tags

def _load_hashtag_data(tags: list):
    """Scrape hashtag data for the given hashtags"""
    hashtag_objs = []
    with tqdm.tqdm(total=len(tags), position = 0) as progress:
        for tag in tags:
            time.sleep(abs(np.random.normal(3, 2)))
            hashtag = Hashtag.from_hashtag(tag)
            hashtag.static_load()
            hashtag_objs.append({
                "hashtag": tag,
                "posts": hashtag.amount_of_posts,
                "datetime": datetime.datetime.now()
            })
            progress.update(1)
    return hashtag_objs

def main(hashtag_fpath, hashtag_csv):
    tags = _load_hashtags_from_txt(hashtag_fpath)
    hashtag_data = _load_hashtag_data(tags)
    _load_data_into_files(hashtag_data, hashtag_csv)

if __name__ == '__main__':
    HASHTAGS_FPATH = r'hashtags.txt'
    HASHTAGS_CSV = r'hashtag-data.csv'
    main(HASHTAGS_FPATH, HASHTAGS_CSV)