"""
Script displays the list of bands in "database", user chooses one.
Script displays the list of songs of the chosen band, user chooses one.
Script displays the lyrics of chosen song.
After that script offers to continue or to quit.
(Supposed, user inputs are correct, without typos; strip() and title() here are FGT)
"""

# Importing "database", separate module in this case
import lyrics_selector_data


def lyrics_selector():
    # Displaying the list of bands
    artists = [key for key in lyrics_selector_data.artists_song.keys()]
    print("\nWe've got next artists in our database:\n")
    for artist in artists:
        print(artist)
    # Choosing band
    artist_choice = input("\nChoose one to see its lyrics list: ").strip().title()
    print(f"\nYou've chosen -->{artist_choice}<-- and this artist has such songs in our database:\n")
    # Displaying the list of the songs for the chosen band
    songs = [song for song in lyrics_selector_data.artists_song[artist_choice]]
    for song in songs:
        print(song)
    # Choosing song
    song_choice = input("\nChoose one to see its lyrics list: ").strip().title()
    print(f"\nYou've chosen -->{song_choice}<-- and this song has such lyrics in our database:\n")
    # Displaying the lyrics of the chosen song
    print(lyrics_selector_data.songs_lyrics[song_choice])
    # continue-or-not after selection is over
    cont_or_not = input("\nWould you like to choose again? Type Yes or No: ").strip().title()
    if cont_or_not == 'Yes':
        lyrics_selector()
    else:
        exit()


lyrics_selector()
