# this is a page that help me to compose data to csv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import credentials
import csv

# create the user auth (TODO: set client_id,client_secret.. as the input)
# return the object sp which can use to access all the API function
def create_user_auth():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=credentials.CLIENT_ID,
                                               client_secret= credentials.CLIENT_SECRET,
                                               redirect_uri=credentials.REDIRECT_URI,
                                               scope=credentials.SCOPE))
    return sp


# function: get user saved songs with first 250 songs from "Liked Songs" Playlist 
# input : the auth object 
# output : 250 songs in "Liked Songs" with id as keys and name as values
# this is to prevent same name if name as the key
def get_user_saved_songs(sp):
    all_results=[]
    for i in range(0,500,50):
        results = sp.current_user_saved_tracks(limit=50,offset=i)
        for idx, item in enumerate(results['items']):
            track = item['track']
            added_at = item['added_at']
            released_date = track['album']['release_date']
            # print(item['track']['id'])
            # print(idx, track['artists'][0]['name'], " – ", track['name'])
            all_results.append({'track_name' : track['name'] , 'track_id' : track['id'],
            'artist_name': track['artists'][0]['name'], 'artist_id': track['artists'][0]['id'],
            'popularity':track['popularity'], 'added_at' : added_at  , 'released_date' : released_date})
    return all_results

#function : get user's playlist 
def get_user_public_playist(sp):
    all_playlists=[]
    playlists = sp.current_user_playlists(limit=50, offset=0)

    for playlist in playlists['items']:
        # print(playlist['id'])
        all_playlists.append({playlist['id'] : playlist['name']})
    return all_playlists

# search a playlist 
def search_playlist(sp, query):
    results = []
    response = sp.search(q=query, type='playlist')

    for res in response['playlists']['items']:
        results.append({"playlist_id": res['id'] , "playlist_name" : res['name'] })
    return results  


#function : get the songs from that playlist 
# pass in the sp and playlist_id 
# return a dict 
#    max 100 song from the playlist under the key "all_songs" 
#    total song in the playlist 
def get_songs_from_playlist(sp,playlist_id):
    all_songs = []
    total_songs = 0
    pl_id = 'spotify:playlist:'+ playlist_id
    offset =0 
    while True:
        response = sp.playlist_items(pl_id,
                                 offset=offset,
                                 fields='items.track.id,total,items.track.name,items.track.artists.name ,items.track.artists.id,items.track.popularity',
                                 additional_types=['track'])
    
        if len(response['items']) == 0:
            break
        all_songs.append(response['items'])
        offset = offset + len(response['items'])
        # print(offset, "/", response['total'])
    result = {'all_songs': all_songs , 'total': response['total']}
    return result


 

#packing all the song in "Liked Song" into a csv file that has the song name, id ( artist can be added when doing analysis)
def main():
    sp = create_user_auth()
    list_song = get_user_saved_songs(sp)
    list_playlist = get_user_public_playist(sp)
    playlist_id = list(list_playlist[2].keys())
    songs_in_playlist = get_songs_from_playlist(sp,playlist_id[0])

    with open('fav_song_list.csv', mode='w') as csv_file:
        fieldnames = ['song_name', 'song_id', 'artist_name' , 'artist_id', 'popularity' , 'added_at' , 'released_date']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for song in list_song:
            writer.writerow({'song_name': song['track_name'], 'song_id': song['track_id'],
            'artist_name':song['artist_name'],'artist_id':song['artist_id'],'popularity': song['popularity'],
            'added_at' : song['added_at'] , 'released_date' : song['released_date']})

    # get mandarin song 
    result = search_playlist(sp, "mandopop hits")
    mandopop_playlits_id = result[0]['playlist_id']
    songs_in_playlist = get_songs_from_playlist(sp,mandopop_playlits_id)


    with open('mandopop.csv', mode='w') as csv_file:
        fieldnames = ['song_id' , 'song_name', 'artists' , 'artists_id', 'popularity']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for song in songs_in_playlist['all_songs'][0]:
            artist_names = []
            for artist in song['track']['artists']: 
                artist_names.append({ "artist_name": artist["name"] , "artist_id": artist["id"]})
            writer.writerow({'song_id': song['track']['id'] , 'song_name': song['track']['name'], 
            'artists': artist_names,  'popularity' : song['track']['popularity']})

    # get billboard song 
    result = search_playlist(sp, "billboard hot 100")
    billboard_playlist_id = result[0]['playlist_id']
    songs_in_playlist = get_songs_from_playlist(sp,billboard_playlist_id)


    with open('billboard.csv', mode='w') as csv_file:
        fieldnames = ['song_id' , 'song_name', 'artists' , 'artists_id' , 'popularity']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for song in songs_in_playlist['all_songs'][0]:
            artist_names = []
            for artist in song['track']['artists']: 
                artist_names.append({ "artist_name": artist["name"] , "artist_id": artist["id"]})
            writer.writerow({'song_id': song['track']['id'] , 'song_name': song['track']['name'], 
            'artists': artist_names , 'popularity' : song['track']['popularity']})


if __name__ == "__main__":
    main()