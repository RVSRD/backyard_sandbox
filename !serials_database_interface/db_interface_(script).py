"""
This is somewhat like the text-rpg interface to SQLite database assumed to represent personal
lists of serials user have watched by now, want to watch (wish-list) or finished to watch by some reason.

Database consists of following tables:

- Watched Movies where user can state Title of serial, number of watched seasons, Personal rating and Genre;
- Watched Animation is quite the same as previous, but about animated only serials;
- Wanted Series is personal wish list, where user can state Title and Genre;
- Wasted Series is the permanent check-list of serials user "wasted", it includes Title,
  Number of seasons and Reason why user decided to stop watching this Title.

Interface supports such functionality:

- Main Menu to select table or to Exit program;
- in Watched Movies or in Watched Animation (same logic) user can Return to Main Menu,
  Add new title to list, Change number of watched seasons in title or Move title from
  Watched to Wasted table;
- in Wanted Movies (wish-list) user can Return to Main Menu, Add new title to list, Move
  title from Wanted to one of selected Watched table (Movies or Animation) or Delete title
  from wish-list;
- and Wasted is just an informative list of serials (Movies and Animation altogether) user
  watched through or watching no more.
"""

import sqlite3

# connecting to database and creating cursor
series_database = sqlite3.connect('www_series.db')
series_database.row_factory = sqlite3.Row
cursor = series_database.cursor()

print("\nWelcome to 'Watched, Wanted, Wasted' - personal serial goldfish notebook!")

# constant variables - restrictions in context - using throughout whole this... stuff
reasons_restriction = "Closed, Ended, Fufelized"
rating_restriction = "Favorite, Exellent, Good Enough, So-So, Fufel"
genre_restriction = "Adventure, Comedy, Detective, Drama, Fantasy, Historical, \n" \
                    "Horror, Melodrama, Mystic, Postapoc, Sci-Fi, Thriller"

# inner repeating warnings, cosplaying try/excepts blocks
typing_mistake_warning = "\n! Typo or some other kind of pathetic mistake. Restarting selection...\n"
typing_mistake_warning_inner = "\n! You should be more accurate typing! Next attempt...\n"

# INITIALIZING MAIN MENU -->


# Main Menu function
def ring_of_power():
    print("\nNow our highness deign to select from:\n"
          "- list of watched series (press 1)\n"
          "- list of watched animated series (press 2)\n"
          "- list of our wasted series (press 3)\n"
          "- list of our personal wish-list (press 4)\n"
          "- EXIT program (press 5)\n")
    # choosing table or exit
    my_choice = input("What is our highness momentous choice: ")
    try:
        if my_choice in ['1', '2', '3', '4']:
            # creating titles list here for ordering purpose
            table_titles_list(my_choice)
            selector_submenu(my_choice)
        # also closing cursor on exit
        elif my_choice == '5':
            print("\nGood cluck! Have a nice sway!")
            cursor.close()
            exit()
        # here and further such message caller activates if input is not correct
        else:
            print(typing_mistake_warning)
            ring_of_power()
    except sqlite3.OperationalError:
        print("\nCorrupted structure of DataBase! Load proper DB file and restart!")

# TOOLS (MOVE/DELETE/OOOOPS/LISTER) block -->


# this block of code is needed only when DB (or one of its category) is empty i.e. once for
# each newly activated category (and/or in case user deleted all entities in wish-list)
def oooopser(my_choice):
    print("\nOooops! We should to ADD something to our empty treasury before to SELECT!")

    # local submenu function
    def selector_subselector():
        selsub_choice = input("\nWhat would we like to do?'\n"
                              "- to ADD our precious (press 1)\n"
                              "- proceed to Main Menu (press 2)\n"
                              "Choose your destiny: ")
        if selsub_choice == '1':
            series_adder_submenu(my_choice)
        elif selsub_choice == '2':
            ring_of_power()
        else:
            print(typing_mistake_warning)
            selector_subselector()
    selector_subselector()


# this functions checks if entered title exceeds 25 characters length hardcoded for displaying;
# if entered title does, script arises warning and offers simple choice: store in DB as it is,
# or input title again, more compact way
def title_length_checker(my_choice, series_title):
    while True:
        if len(series_title) > 25:
            print("\n/ Little warning: You exceeded predefined 25 characters limit of title."
                  "\n/ Title will be stored though, but it will be truncated beeing displayed."
                  "\n/ You can proceed further (press 1) or return to title input (press 2)")
            subsub = input("\nMake Your glorious choice: ")
            if subsub == '1':
                break
            elif subsub == '2':
                series_adder_submenu(my_choice)
            else:
                print(typing_mistake_warning_inner)
        else:
            break


# here we create a titles list in selected table to check further if some title exists or not
def table_titles_list(my_choice):
    # globals are easiest option here, i suppose
    global selected_table, titles_values, titles_IDs
    tables_list = ['Watched_Movies', 'Watched_Animation', 'Wasted_Series', 'Wanted_Movies']
    if my_choice == '1':
        selected_table = tables_list[0]
    elif my_choice == '2':
        selected_table = tables_list[1]
    elif my_choice == '3':
        selected_table = tables_list[2]
    else:
        selected_table = tables_list[3]
    # here we create titles list for selected table
    titles_values = [title[0] for title in cursor.execute(f"SELECT TITLE FROM {selected_table}")]
    # here we create IDs list for selected table
    titles_IDs = [ids[0] for ids in cursor.execute(f"SELECT ID FROM {selected_table}")]


# deleting option created only for wish list (Wanted_Movies table),
# such decision based on the simple thought: we can change our mind to watch some movie,
# but if we watched one already, we move it to watched category as *permanent* check
def title_delete(my_choice):
    precious_to_delete = input("\nEnter ID of title You want to delete from wish list: ").title().strip()
    if precious_to_delete:
        cursor.execute(f"DELETE FROM Wanted_Movies WHERE ID = '{precious_to_delete}'")
        series_database.commit()
        # updating titles list after deleting
        table_titles_list(my_choice)
        print("\nWhoops! Disappeared! And now our wish-list looks like...")
    else:
        print(typing_mistake_warning)
        title_delete(my_choice)


# function to move input title from Wanted to Watched (Movies or Animation)
def wished_to_watched(my_choice):
    id_to_move = input("Enter ID of TITLE we want to MOVE from wish-list "
                       "to watched one: ").strip()
    # check if ID input is digit and is not empty
    if id_to_move != '' and id_to_move.isdigit():
        # check for ID in source table: if ID does not exist, warning message arises
        # and ID enter invitation restarts, other way TITLE is binded to ID
        title_to_move = cursor.execute(f"SELECT TITLE FROM {selected_table} "
                                       f"WHERE ID = {id_to_move}").fetchone()
        while title_to_move:
            title_to_move = title_to_move['TITLE']
            break
        else:
            print("\nThere's no such ID in source list, be more careful!")
            wished_to_watched(my_choice)
        # two below variables we use to define to where we move title: to Movies or to Animation
        mover_allocator = {'1': 'Watched_Movies', '2': 'Watched_Animation'}
        mover_targeter = input("\nWhere should we move - to TV-series (press 1) or to animated series (press 2): ")
        if mover_targeter in ['1', '2']:
            # check for title in previously selected table: if title NOT exist in target table, we Move;
            # other way we call corresponding message and restart selection
            check_list = [title[0] for title in cursor.execute(f"SELECT TITLE FROM {mover_allocator[mover_targeter]}")]
            if title_to_move not in check_list:
                seasons_watched = input("\nEnter number of seasons you watched (or pass for default 1): ") or '1'
                # little checker if entered number is number with autorestart
                while seasons_watched.isdigit():
                    break
                else:
                    print("\nWe need number and you've entered something wrong!")
                    wished_to_watched(my_choice)
                print(f"\nFurther You shall enter rating of title. Your options:\n{rating_restriction}")
                series_rating = input("Now enter chosen rating You consider fits most: ").title().strip()
                # here we check if title we input exists in table FROM where we Move
                # and predefined restrictions
                if title_to_move in titles_values and series_rating in rating_restriction:
                    cursor.execute(f"""INSERT INTO {mover_allocator[mover_targeter]}
                                        (ID, TITLE, SEASONS_WATCHED, PERSONAL_RATING, GENRE)
                                        SELECT NULL, TITLE, ?, ?, GENRE FROM {selected_table} WHERE TITLE = ?""",
                                   (seasons_watched, series_rating, title_to_move))
                    cursor.execute(f"""DELETE FROM {selected_table} WHERE TITLE = '{title_to_move}'""")
                    series_database.commit()
                    print("\nSuccessfully relocated! And our wish-list now looks like...")
                else:
                    print(typing_mistake_warning_inner)
                    wished_to_watched(my_choice)
            elif title_to_move in check_list:
                print("\nSuch title exists in target treasury, we do not need to relocate one!\n"
                      "DELETE it from here or do something else.")
                selector_submenu(my_choice)
            else:
                print(typing_mistake_warning_inner)
                wished_to_watched(my_choice)
        else:
            print(typing_mistake_warning_inner)
            wished_to_watched(my_choice)
    else:
        print(typing_mistake_warning_inner)
        wished_to_watched(my_choice)


# function to move input title from Watched to Wasted
def watched_to_wasted(my_choice):
    id_to_move = input("\nEnter ID of TITLE we want to MOVE from watched "
                       "list to wasted one: ").strip()
    # check if ID input is digit and is not empty
    if id_to_move != '' and id_to_move.isdigit():
        # check for ID in source table: if ID does not exist, warning message arises
        # and ID enter invitation restarts, other way TITLE is binded to ID
        title_to_move = cursor.execute(f"SELECT TITLE FROM {selected_table} "
                                       f"WHERE ID = {id_to_move}").fetchone()
        while title_to_move:
            title_to_move = title_to_move['TITLE']
            break
        else:
            print("\nThere's no such ID in source list, be more careful!")
            watched_to_wasted(my_choice)
        # creating check list of titles for Wasted_Series table, then check
        check_titles_list = [title[0] for title in cursor.execute(f"SELECT TITLE FROM Wasted_Series")]
        if title_to_move not in check_titles_list:
            print("\nSpecify flawlessly the reason why we move this series to Wasted category")
            reason_to_waste = input(f"\nEnter one of the follows {reasons_restriction}: ").title().strip()
            if title_to_move in titles_values and reason_to_waste in reasons_restriction:
                cursor.execute(f"""INSERT INTO Wasted_Series
                                (TITLE, SEASONS_WATCHED, REASON_TO_WASTE)
                                SELECT TITLE, SEASONS_WATCHED, ? FROM {selected_table} WHERE TITLE = ?""",
                               (reason_to_waste, title_to_move))
                cursor.execute(f"""DELETE FROM {selected_table} WHERE ID = {id_to_move}""")
                series_database.commit()
                print("\nSuccessfully relocated! And our watched list now looks like...")
                # renew list of titles in table
                table_titles_list(my_choice)
            else:
                print(typing_mistake_warning_inner)
                watched_to_wasted(my_choice)
        # if title exists in both tables we call corresponding message and Delete it from source table
        elif title_to_move in check_titles_list:
            print("\nSuch title exists in target treasury, we do not need to relocate one!\n"
                  "Also we do not need two of them, so we just annihilate that one!")
            cursor.execute(f"""DELETE FROM {selected_table} WHERE TITLE = '{title_to_move}'""")
            series_database.commit()
            selector_submenu(my_choice)
        else:
            print(typing_mistake_warning_inner)
            watched_to_wasted(my_choice)
    else:
        print(typing_mistake_warning_inner)
        watched_to_wasted(my_choice)


# function to change number of watched seasons in Movies or Animation tables
def seasons_watched_changer(my_choice):
    title_number_change = input("Enter ID of TITLE where You need "
                                "to change numbers of watched seasons: ").strip()
    # check if title to update number os seasons exists
    if title_number_change.isdigit() and int(title_number_change) in titles_IDs:
        seasons_watched_update = input("Enter new number of seasons You watched: ")
        if seasons_watched_update.isdigit():
            current_number = cursor.execute(f"SELECT SEASONS_WATCHED FROM {selected_table} "
                                            f"WHERE ID = '{title_number_change}'")
            # check if new number greater than current
            check_number = [row[0] for row in current_number]
            if int(seasons_watched_update) > check_number[0]:
                cursor.execute(f"""UPDATE {selected_table}
                                   SET SEASONS_WATCHED = {seasons_watched_update}
                                   WHERE ID = '{title_number_change}'""")
                series_database.commit()
                print("\nNumber of seasons You vouchsafed to watch gloriously changed!")
                selector_submenu(my_choice)
            else:
                print(f"\nNEW number can not be less or equal of current {check_number[0]}! Try again!\n")
                seasons_watched_changer(my_choice)
        else:
            print(typing_mistake_warning_inner)
            seasons_watched_changer(my_choice)
    else:
        print(typing_mistake_warning_inner)
        seasons_watched_changer(my_choice)

# NEW SERIES ADDER BLOCK -->


# function to add title to our DB to definite table (or do not, if title already exists)
def series_adder_submenu(my_choice):
    if my_choice == '1' or my_choice == '2':
        series_title = input("\nEnter new series title: ").title().strip()
        # check if input >25 and displays storage warning if it's so,
        # then offers to continue or to go back and retype
        title_length_checker(my_choice, series_title)
        # check it title we add NOT in target table (Movies or Animation in this case):
        # if so - we add, other way we call corresponding message and restart selection
        if series_title not in titles_values:
            watched_seasons_num = input("Enter number of seasons you watched (or skip for default 1): ") or '1'
            # checking if entered value is number
            while watched_seasons_num.isdigit():
                break
            else:
                print("\nWe need number and you've entered something wrong!")
                series_adder_submenu(my_choice)
            print(f"\nFurther You shall enter rating of title. Your options:\n{rating_restriction}")
            series_rating = input("\nNow enter chosen rating You consider fits most: ").title().strip()
            print(f"\nAnd finally enter genre of watched series. Your options:\n{genre_restriction}")
            genre_of_series = input("\nChoose genre from upper list, please: ").title().strip()
            # checking restrictions
            if genre_of_series in genre_restriction and series_rating in rating_restriction:
                cursor.execute(f"""INSERT INTO {selected_table}
                                     (ID, TITLE, SEASONS_WATCHED, PERSONAL_RATING, GENRE)
                                     VALUES
                                     (NULL, ?, ?, ?, ?)""",
                               (series_title, watched_seasons_num, series_rating, genre_of_series))
                series_database.commit()
                # updating titles' list after adding
                table_titles_list(my_choice)
            else:
                print(typing_mistake_warning_inner)
                series_adder_submenu(my_choice)
        else:
            print("\nSuch title exists! And therefore...")
            selector_submenu(my_choice)
    elif my_choice == '3':
        series_title = input("\nEnter wasted series title: ").title().strip()
        # check if input >25 and displays storage warning if it's so,
        # then offers to continue or to go back and retype
        title_length_checker(my_choice, series_title)
        # check it title we add NOT in wasted table: if so - we add,
        # other way we call corresponding message and restart selection
        if series_title not in titles_values:
            watched_seasons_num = input("Enter number of seasons you watched (or skip for default 1): ") or '1'
            # check if entered value is number
            while watched_seasons_num.isdigit():
                break
            else:
                print("\nWe need number and you've entered something wrong!")
                series_adder_submenu(my_choice)
            print(f"Possible reasons why series are wasted: {reasons_restriction}")
            reason_to_waste = input("Enter corresponding reason why wasted: ").title().strip()
            # checking restriction
            if reason_to_waste in reasons_restriction:
                cursor.execute(f"""INSERT INTO {selected_table}
                                             (TITLE, SEASONS_WATCHED, REASON_TO_WASTE)
                                             VALUES
                                             (?, ?, ?)""",
                               (series_title, watched_seasons_num, reason_to_waste))
                series_database.commit()
            else:
                print(typing_mistake_warning_inner)
                series_adder_submenu(my_choice)
        else:
            print("\nSuch title exists! And therefore...")
            selector_submenu(my_choice)
    elif my_choice == '4':
        series_title = input("\nEnter new series title: ").title().strip()
        # check if input >25 and displays storage warning if it's so,
        # then offers to continue or to go back and retype
        title_length_checker(my_choice, series_title)
        # check it title we add NOT in wanted table: if so we add,
        # other way we call corresponding message and restart selection
        if series_title not in titles_values:
            print(f"\nGenre of series You wish to watch:\n{genre_restriction}")
            genre_of_series = input("\nEnter genre you've chosen: ").title().strip()
            # checking restriction
            if genre_of_series in genre_restriction:
                cursor.execute(f"""INSERT INTO {selected_table}
                                            (TITLE, GENRE)
                                            VALUES
                                            (?, ?)""", (series_title, genre_of_series))
                series_database.commit()
                # updating titles' list after adding
                table_titles_list(my_choice)
            else:
                print(typing_mistake_warning_inner)
                series_adder_submenu(my_choice)
        else:
            print("\nSuch title exists! And therefore...")
            selector_submenu(my_choice)
    print("\nRoyal quest finished! And now our list looks like...")
    # restarting selection submenu
    selector_submenu(my_choice)

# SELECTOR BASIC LOGIC -->


def selector_submenu(my_choice):
    # submenu function, plain enough
    def selector_submenu_selector():
        if my_choice == '1' or my_choice == '2':
            print("\nSomething magical happened previously and now we deign to:\n"
                  "- BACK to Main Menu (press 1)\n"
                  "- ADD new precious to our treasury (press 2)\n"
                  "- CHANGE number of watched seasons of Title (press 3)\n"
                  "- MOVE from Watched to Wasted list (press 4)\n")
            our_main_or_add = input("What is our choice here: ")
            if our_main_or_add == '1':
                ring_of_power()
            elif our_main_or_add == '2':
                series_adder_submenu(my_choice)
            elif our_main_or_add == '3':
                seasons_watched_changer(my_choice)
            elif our_main_or_add == '4':
                watched_to_wasted(my_choice)
                selector_submenu(my_choice)
            else:
                print(typing_mistake_warning)
                selector_submenu_selector()
        elif my_choice == '3':
            print("\nSomething magical happened previously and now we deign to:\n"
                  "- BACK to Main Menu (press 1)\n"
                  "- ADD new precious to our treasury (press 2)\n")
            our_main_or_add = input("What is our choice here: ")
            if our_main_or_add == '1':
                ring_of_power()
            elif our_main_or_add == '2':
                series_adder_submenu(my_choice)
            else:
                print(typing_mistake_warning)
                selector_submenu_selector()
        elif my_choice == '4':
            print("\nSomething magical happened previously and now we deign to:\n"
                  "- BACK to Main Menu (press 1)\n"
                  "- ADD new precious to our treasury (press 2)\n"
                  "- MOVE precious to WATCHED treasury (press 3)\n"
                  "- DELETE soured precious from treasury (press 4)")
            our_main_or_add = input("\nWhat is our choice here: ")
            if our_main_or_add == '1':
                ring_of_power()
            elif our_main_or_add == '2':
                series_adder_submenu(my_choice)
            elif our_main_or_add == '3':
                wished_to_watched(my_choice)
                selector_submenu(my_choice)
            elif our_main_or_add == '4':
                title_delete(my_choice)
                selector_submenu(my_choice)
            else:
                print(typing_mistake_warning)
                selector_submenu_selector()

    # subfunction to display titles in Movies or Animation tables
    def movies_displayer():
        # check if it's not empty
        if watched_movies_list:
            print("\nCasting magic...\n")
            # fetching rows and its data from table to print with some little aligning
            # and wit limit of 25 characters are displayed
            for row in watched_movies_list:
                print(f"ID: {row['ID']: ^3} || "
                      f"Title: {row['TITLE'][:25]: ^25} || "
                      f"Seasons watched: {row['SEASONS_WATCHED']: >2} || "
                      f"Personal rating: {row['PERSONAL_RATING']: ^12} || "
                      f"Genre: {row['GENRE']: ^10}")
            selector_submenu_selector()
        # this function calls only if table is empty
        else:
            oooopser(my_choice)

    # subfunction to display titles in Wasted table
    def wasted_movies_displayer():
        # check if it's not empty
        if wasted_movies_list:
            print("\nCasting magic...\n")
            # fetching rows and its data from table to print with some little aligning
            # and wit limit of 25 characters are displayed
            for row in wasted_movies_list:
                print(f"Title: {row['TITLE'][:25]: ^25} || "
                      f"Seasons watched: {row['SEASONS_WATCHED']: >2} || "
                      f"Reason to waste: {row['REASON_TO_WASTE']: ^15}")
            selector_submenu_selector()
        # this function calls only if table is empty
        else:
            oooopser(my_choice)

    # subfunction to display titles in Wanted table
    def wanted_movies_displayer():
        if wanted_movies_list:
            print("\nCasting magic...\n")
            # fetching rows and its data from table to print with some little aligning
            # and wit limit of 25 characters are displayed
            for row in wanted_movies_list:
                print(f"ID: {row['ID']: ^3} || Title: {row['TITLE'][:25]: ^25} || Genre: {row['GENRE']: ^10}")
            selector_submenu_selector()
        # this function calls only if table is empty
        else:
            oooopser(my_choice)

    # define tables and its data to fetch
    if my_choice in ['1', '2']:
        watched_select_query = f"SELECT ID, TITLE, SEASONS_WATCHED, PERSONAL_RATING, GENRE FROM " \
                          f"{selected_table} ORDER BY TITLE"
        cursor.execute(watched_select_query)
        watched_movies_list = cursor.fetchall()
        movies_displayer()
    elif my_choice == '3':
        wasted_select_query = f"SELECT TITLE, SEASONS_WATCHED, REASON_TO_WASTE FROM " \
                              f"{selected_table} ORDER BY TITLE"
        cursor.execute(wasted_select_query)
        wasted_movies_list = cursor.fetchall()
        wasted_movies_displayer()
    elif my_choice == '4':
        wishlist_select_query = f"SELECT ID, TITLE, GENRE FROM {selected_table} ORDER BY ID"
        cursor.execute(wishlist_select_query)
        wanted_movies_list = cursor.fetchall()
        wanted_movies_displayer()
    else:
        print(typing_mistake_warning)
        selector_submenu(my_choice)


# general ignition
ring_of_power()