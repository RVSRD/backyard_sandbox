"""
Script displays band list in "database", shelve in this case.
User chooses band and script displays songs of the chosen one.
User chooses song and script displays lyrics of the chosen one.
In this shelve version user is able to add bands, songs and lyrics.
If band user adds already exists, script offers choice: proceed to Main Menu
or add new song for existing band.
If song user adds exists too, script offers choice again: proceed to Main Menu
or add another one for existing band.
After successful lyrics addition, script offers to proceed to Main Menu
or add one more song for the band.
"""

# Importing shelve module
import shelve

# initializing two shelve objects:
# - first with bands as keys and its songs titles as values
# - second with songs titles as keys and its lyrics as values
artist_and_songs = shelve.open('artists', writeback=True)
songs_and_lyrics = shelve.open('songs', writeback=True)


# MAIN MENU BLOCK -->

def main_menu():
    menu_choice = input("What would you like to do? You can SELECT, ADD or EXIT: ").upper().strip()
    if menu_choice == 'SELECT':
        # band/song selection function caller
        artist_selector()
    elif menu_choice == 'ADD':
        # band/song addition function caller
        artist_adder()
    elif menu_choice == 'EXIT':
        print("That's all folks!")
        # closing shelve on exit
        artist_and_songs.close()
        songs_and_lyrics.close()
        exit()
    else:
        # instead of adult try/except, simpler 'else' version
        # supposed, user types correctly
        print("Something went wrong, try again!")
        main_menu()


# SELECTOR SUBMENU BLOCK -->

# submenu function of band choice
def artist_selector():
    print("We've got next artists in our database:")
    # displaying list of bands in "database"
    for artist in artist_and_songs:
        print(artist)
    artist_choice = input("Choose one to see its lyrics list: ").title().strip()
    print(f"You've chosen {artist_choice} and this artist has such songs in our database:")
    # transferring to function of song selection
    lyric_selector(artist_choice)


# function of song selection of preselected band
def lyric_selector(artist_choice):
    # displaying songs list (curlicue, but working)
    songs = [song for song in artist_and_songs[artist_choice]]
    for song in songs:
        print(song)
    # choosing the song from the displayed list
    song_choice = input("Choose one to see its lyrics list: ").title().strip()
    print(f"You've chosen {song_choice} and this song has such lyrics in our database:")
    print(songs_and_lyrics[song_choice])
    # function to recall song selection submenu
    selector_repeater()


# function-repeater:
#  - offers to select again and restart selection if user agreed;
# - other way it offers to proceed to Main Menu or to Exit at all.
def selector_repeater():
    one_more = input("Would you like to choose again? YES or NO: ").upper().strip()
    if one_more == "YES":
        artist_selector()
    elif one_more == "NO":
        one_more_sub = input("Would you like to return to MENU or to EXIT: ").upper().strip()
        if one_more_sub == "MENU":
            main_menu()
        else:
            print("That's all folks!")
            # closing shelve on exit
            artist_and_songs.close()
            songs_and_lyrics.close()
            exit()
    else:
        # instead of adult try/except, simpler 'else' version
        print("Typo! Try again!")
        selector_repeater()


# ADDER SUBMENU BLOCK -->

# function to add new band to 'database', bands adding as a key of dictionary
def artist_adder():
    artist_to_add = input("Enter Artist to add to our database: ").title().strip()
    # checking if band's added already exists in 'database'
    if artist_to_add in artist_and_songs.keys():
        print("We already have this artist, what would you like to do?")
        # if band exists, user has such options:
        # - transfer to Main Menu
        # - add another band
        # - add new song to existing band
        adder_sub_selector = input("1 for MENU, 2 for new artist or 3 for new title: ").strip()
        if adder_sub_selector == '1':
            main_menu()
        elif adder_sub_selector == '2':
            artist_adder()
        elif adder_sub_selector == '3':
            # calling next function - song_adder()
            song_adder(artist_to_add)
        else:
            # instead of adult try/except, simpler 'else' version
            print("Typo! Try again!")
            artist_adder()
    else:
        # here we add band to shelve key
        artist_and_songs[artist_to_add] = artist_and_songs
        # initializing empty song list (values) for new band (key)
        artist_and_songs[artist_to_add] = []
        # calling function to add song to selected band
        song_adder(artist_to_add)


# function to add song to preselected band
def song_adder(artist_to_add):
    song_to_add = input("Enter song title: ").title().strip()
    # check if song exists in 'database'
    # if it exists, script informs user and offers to:
    # - proceed to Main Menu
    # - add another song to selected band
    if song_to_add in songs_and_lyrics.keys():
        print("Such title exist, no need to add!")
        song_adder_submenu = input("1 for MENU or 2 to add another title: ").strip()
        if song_adder_submenu == '1':
            main_menu()
        elif song_adder_submenu == '2':
            song_adder(artist_to_add)
        else:
            print("Typo! Try again!")
            song_adder(artist_to_add)
    else:
        # adding song to song list of selected band
        artist_and_songs[artist_to_add].append(song_to_add)
        lyrics_adder(artist_to_add, song_to_add)


# adding lyrics line by line, to finish  and to record lines to song
# user has to enter empty line
def lyrics_adder(artist_to_add, song_to_add):
    # initializing list of lines
    lines_of_text = []

    # loop restarts until user enter empty line, after that script records lines to list
    while True:
        line_of_text = input("Enter lyrics of the song's title line by line and empty line to finish: ")
        if line_of_text:
            lines_of_text.append(line_of_text)
        else:
            break
    # separating entered list to single raws
    lyrics_to_add = '\n'.join(lines_of_text)
    # connecting entered lyrics to song
    songs_and_lyrics[song_to_add] = lyrics_to_add
    # after lyrics successfully added, script informs user of completion and
    # offers to:
    # - proceed to Main Menu
    # - add one more song
    print("New title and its lyrics added to our database!")

    # function-submenut to choose between returning to Main Menu
    # and adding one more title to preselected band
    def lyrics_adder_submenu():
        lyrics_adder_submenu_choice = input("1 for MENU, 2 to add one more title: ")
        if lyrics_adder_submenu_choice == '1':
            main_menu()
        elif lyrics_adder_submenu_choice == '2':
            # restarting functions to add one more song
            song_adder(artist_to_add)
            lyrics_adder(artist_to_add, song_to_add)
        else:
            # instead of adult try/except, simpler 'else' version
            print("Typo! Try again!")
            lyrics_adder_submenu()
    lyrics_adder_submenu()


# STARTER -->

main_menu()
