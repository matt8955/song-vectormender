import csv
import asyncio
import pandas as pd
import aiohttp 
import asynclyrics
from tqdm.asyncio import tqdm

def open_csv(path,size=20000):
    return pd.read_csv(path,chunksize=size)

async def write_result(id_, artist, writer,session,writer2):
    async with asyncio.Lock():
        if isinstance(artist,str):   
            lyrics = await session.get_artist_lyrics(artist)
            await asyncio.sleep(2)
            if lyrics:
                for track, lyric in lyrics.items():
                    if track:
                        [writer.writerow([id_,artist,track,num,line]) for 
                            num,line in enumerate(lyric.split(" \n "))]
            else:
                writer2.writerow([id_, artist])
async def bound_fetch(id_,artist, writer, sem,session,writer2):
    # Getter function with semaphore.
    #since fxn has to pass in here we are blocking by 4 max semifore
    
    async with sem:
        await write_result(id_, artist, writer,session,writer2)

async def main(ids,names,i):
    # create instance of Semaphore
    
    
    
    with open(f'lyrics_scrape_{i}.csv', 'a') as success, open('fails.csv', 'a') as fail:
        writer = csv.writer(success, delimiter='|')
        failwriter = csv.writer(fail, delimiter='|')
        sem = asyncio.Semaphore(20) 
        pylyrics = asynclyrics.AsyncLyrics()
        tasks = [bound_fetch(id_,artist,writer,sem,pylyrics,failwriter) for id_,artist in zip(ids,names)]
        [await f for f in tqdm(asyncio.as_completed(tasks), total=len(tasks))]
        await pylyrics.close_connection()

if __name__ == "__main__":
    path = 'unique_artists.csv'
    artists_chunks = open_csv(path,5000)
    loop_up_to = 120
    for i, artists in enumerate(artists_chunks):
        if i > loop_up_to:
            ids = artists.artist_id.to_list()
            names = artists.name.to_list()
            asyncio.run(main(ids,names,i))
            print(f'finished chunk_{i}')