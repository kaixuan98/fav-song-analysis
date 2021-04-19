# this is a page that help me to compose data to csv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = "4df0ee02b3f14720a50a274c022765eb"
CLIENT_SECRET = "7d3cc0c306c643b1a5bfae311c11c371" 
REDIRECT_URI ="http://127.0.0.1:8080"
SCOPE= "user-library-read"

# create the user auth (TODO: set client_id,client_secret.. as the input)
# return the object sp which can use to access all the API function
def create_user_auth():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret= CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=SCOPE))
    return sp


# function: get user saved songs with first 250 songs from "Liked Songs" Playlist 
# input : the auth object 
# output : 250 songs in "Liked Songs" with id as keys and name as values
# this is to prevent same name if name as the key
def get_user_saved_songs(sp):
    all_results=[]
    for i in range(0,250,50):
        results = sp.current_user_saved_tracks(limit=50,offset=i)
        for idx, item in enumerate(results['items']):
            track = item['track']
            # print(item['track']['id'])
            # print(idx, track['artists'][0]['name'], " – ", track['name'])
            all_results.append({track['id'] : track['name']})
    return all_results

#function : get user's playlist 
def get_user_public_playist(sp):
    all_playlists=[]
    playlists = sp.current_user_playlists(limit=50, offset=0)

    for playlist in playlists['items']:
        # print(playlist['id'])
        all_playlists.append({playlist['id'] : playlist['name']})
    return all_playlists
    

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
                                 fields='items.track.id,total',
                                 additional_types=['track'])
    
        if len(response['items']) == 0:
            break
        # print(response['items'])
        all_songs.append(response['items'])
        offset = offset + len(response['items'])
        # print(offset, "/", response['total'])
    result = {'all_songs': all_songs , 'total': response['total']}
    return result

#function : followed playlist


#function : pack the song info into a csv file 


def main():
    sp = create_user_auth()
    list_song = get_user_saved_songs(sp)
    list_playlist = get_user_public_playist(sp)
    playlist_id = list(list_playlist[2].keys())
    songs_in_playlist = get_songs_from_playlist(sp,playlist_id[0])
    print(songs_in_playlist)


if __name__ == "__main__":
    main()