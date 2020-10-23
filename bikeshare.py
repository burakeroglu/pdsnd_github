import time
import pandas as pnd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

months = ('january', 'february', 'march', 'april', 'may', 'june')

weekdays = ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday',
            'saturday')


def choice(prompt, choices=('y', 'n')):
    """It takes a valid imput from the users"""

    while True:
        choice = input(prompt).lower().strip()
        # if the input is end, finish the script
        if choice == 'end':
            raise SystemExit
        # triggers if it has only one name
        elif ',' not in choice:
            if choice in choices:
                break
        # triggers if it has more than one name
        elif ',' in choice:
            choice = [i.strip().lower() for i in choice.split(',')]
            if list(filter(lambda x: x in choices, choice)) == choice:
                break

        prompt = ("\nPlease recheck the formatting and "
                  "be sure to enter a valid option:\n>")

    return choice


def get_filters():
    """Ask user to specify which values to select included in city(ies) and
    filters, month(s) and weekday(s).
    Returns:
        (str) city - name of the city(ies) to analyze
        (str) month - name of the month(s) to filter
        (str) day - name of the day(s) of week to filter
    """

    print("\n\nLet's explore some US bikeshare data!\n")

    print("Type end at any time if you would like to exit the program.\n")

    while True:
        city = choice("\nWhich city(ies) do you want do select data, "
                      "New York City, Chicago or Washington? Please use commas "
                      "to list the names.\n>", CITY_DATA.keys())
        month = choice("\nSelect month to filter data; January, February, March"
                       "April, May, June. Please use commas to list the"
                       "names.\n>",
                       months)
        day = choice("\nWhich day do you want to filter bikeshare data?"
                     "Use commas to list the names.\n>", weekdays)

        # confirmation step
        confirmation = choice("\nPlease approve that you would like to apply "
                              "the following filter(s) to the bikeshare data "
                              "if it is true."
                              "\n\n City(ies): {}\n Month(s): {}\n Weekday(s)"
                              ": {}\n\n [y] Yes\n [n] No\n\n>"
                              .format(city, month, day))
        if confirmation == 'y':
            break
        else:
            print("\nLet's try this again!")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """Loads data for the specified city(ies), month(s) and day(s).
    Args:
        (str) city - name of the city(ies) to analyze
        (str) month - name of the month(s) to filter
        (str) day - name of the day(s) of week to filter
    Returns:
        df - Pandas DataFrame containing filtered data
    """

    print("\nI am about to get datas which you want from me.")
    start_time = time.time()

    # filter data according to selected city filters
    if isinstance(city, list):
        df = pnd.concat(map(lambda city: pnd.read_csv(CITY_DATA[city]), city),
                       sort=True)
        # reorganize DataFrame columns
        try:
            df = df.reindex(columns=['Unnamed: 0', 'Start Time', 'End Time',
                                     'Trip Duration', 'Start Station',
                                     'End Station', 'User Type', 'Gender',
                                     'Birth Year'])
        except:
            pass
    else:
        df = pnd.read_csv(CITY_DATA[city])



import datetime as dt

    # to display statistics.
    df['Start Time'] = pnd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Weekday'] = df['Start Time'].dt.weekday_name
    df['Start Hour'] = df['Start Time'].dt.hour

    # filter the data according to month and days into two new DataFrames
    if isinstance(month, list):
        df = pnd.concat(map(lambda month: df[df['Month'] ==
                           (months.index(month)+1)], month))
    else:
        df = df[df['Month'] == (months.index(month)+1)]

    if isinstance(day, list):
        df = pnd.concat(map(lambda day: df[df['Weekday'] ==
                           (day.title())], day))
    else:
        df = df[df['Weekday'] == day.title()]

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nGetting the statistics on the most frequent times of '
          'travel...\n')
    start_time = time.time()

    # shows the most common month
    most_common_month = df['Month'].mode()[0]
    print('For the selected filter, the month with the most travels is: ' +
          str(months[most_common_month-1]).title() + '.')

    # shows the most common day
    most_common_day = df['Weekday'].mode()[0]
    print('For the selected filter, the most common day of the week is: ' +
          str(most_common_day) + '.')

    # shows the most common start hour
    most_common_hour = df['Start Hour'].mode()[0]
    print('For the selected filter, the most common start hour is: ' +
          str(most_common_hour) + '.')

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # shows the most commonly used start station
    most_common_start_station = str(df['Start Station'].mode()[0])
    print("For the selected filters, the most common start station is: " +
          most_common_start_station)

    # shows the most commonly used end station
    most_common_end_station = str(df['End Station'].mode()[0])
    print("For the selected filters, the most common start end is: " +
          most_common_end_station)

    # shows the most frequent combination of start and end station
    df['Start-End Combination'] = (df['Start Station'] + ' - ' +
                                   df['End Station'])
    most_common_start_end_combination = str(df['Start-End Combination']
                                            .mode()[0])
    print("For the filters you selected, the most common start-end combination "
          "of stations is: " + most_common_start_end_combination)

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)




def trip_duration_stats(df):
    """Display statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_travel_time = (str(int(total_travel_time//86400)) +
                         'd ' +
                         str(int((total_travel_time % 86400)//3600)) +
                         'h ' +
                         str(int(((total_travel_time % 86400) % 3600)//60)) +
                         'm ' +
                         str(int(((total_travel_time % 86400) % 3600) % 60)) +
                         's')
    print('For the selected filters, the total travel time is : ' +
          total_travel_time + '.')

    # shows the mean time for travelling
    mean_travel_time = df['Trip Duration'].mean()
    mean_travel_time = (str(int(mean_travel_time//60)) + 'm ' +
                        str(int(mean_travel_time % 60)) + 's')
    print("For the selected filters, the mean travel time is : " +
          mean_travel_time + ".")

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)


def user_stats(df, city):
    """Display statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Shows the total count of user types
    user_types = df['User Type'].value_counts().to_string()
    print("Distribution for user types:")
    print(user_types)

    # Shows the total count of gender
    try:
        gender_distribution = df['Gender'].value_counts().to_string()
        print("\nDistribution for each gender:")
        print(gender_distribution)
    except KeyError:
        print("I'm sorry! There is no information about user genders for {}."
              .format(city.title()))

    # Shows the earliest, most recent, and most common year of birth
    try:
        earliest_birth_year = str(int(df['Birth Year'].min()))
        print("\nFor the filter you selected, the oldest person to ride one "
              "bike was born in: " + earliest_birth_year)
        most_recent_birth_year = str(int(df['Birth Year'].max()))
        print("For the filter you selected, the youngest person to ride one "
              "bike was born in: " + most_recent_birth_year)
        most_common_birth_year = str(int(df['Birth Year'].mode()[0]))
        print("For the filter you selected, the most common birth year amongst "
              "riders is: " + most_common_birth_year)
    except:
        print("I'm sorry! There is no data of birth year for {}."
              .format(city.title()))

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)


def raw_data(df, mark_place):
    """Display 5 line of sorted raw data each time."""

    print("\nYou selected to view raw data.")

    # this variable holds where the user last stopped
    if mark_place > 0:
        last_place = choice("\nWould you like to continue from where you "
                            "stopped last time? \n [y] Yes\n [n] No\n\n>")
        if last_place == 'n':
            mark_place = 0

    # sort data by column
    if mark_place == 0:
        sort_df = choice("\nHow would you like to sort the way the data is "
                         "displayed in the dataframe? Press Enter to view "
                         "unsorted.\n \n [st] Start Time\n [et] End Time\n "
                         "[td] Trip Duration\n [ss] Start Station\n "
                         "[es] End Station\n\n>",
                         ('st', 'et', 'td', 'ss', 'es', ''))

        asc_or_desc = choice("\nWould you like it to be sorted ascending or "
                             "descending? \n [a] Ascending\n [d] Descending"
                             "\n\n>",
                             ('a', 'd'))

        if asc_or_desc == 'a':
            asc_or_desc = True
        elif asc_or_desc == 'd':
            asc_or_desc = False

        if sort_df == 'st':
            df = df.sort_values(['Start Time'], ascending=asc_or_desc)
        elif sort_df == 'et':
            df = df.sort_values(['End Time'], ascending=asc_or_desc)
        elif sort_df == 'td':
            df = df.sort_values(['Trip Duration'], ascending=asc_or_desc)
        elif sort_df == 'ss':
            df = df.sort_values(['Start Station'], ascending=asc_or_desc)
        elif sort_df == 'es':
            df = df.sort_values(['End Station'], ascending=asc_or_desc)
        elif sort_df == '':
            pass

    # each loop shows 5 lines of raw data
    while True:
        for i in range(mark_place, len(df.index)):
            print("\n")
            print(df.iloc[mark_place:mark_place+5].to_string())
            print("\n")
            mark_place += 5

            if choice("Do you want to continue printing raw data?"
                      "\n\n[y]Yes\n[n]No\n\n>") == 'y':
                continue
            else:
                break
        break

    return mark_place

import click
def main():
    while True:
        click.clear()
        city, month, day = get_filters()
        df = load_data(city, month, day)

        mark_place = 0
        while True:
            select_data = choice("\nPlease select the information you would "
                                 "like to obtain.\n\n [ts] Time Stats\n [ss] "
                                 "Station Stats\n [tds] Trip Duration Stats\n "
                                 "[us] User Stats\n [rd] Display Raw Data\n "
                                 "[r] Restart\n\n>",
                                 ('ts', 'ss', 'tds', 'us', 'rd', 'r'))
            click.clear()
            if select_data == 'ts':
                time_stats(df)
            elif select_data == 'ss':
                station_stats(df)
            elif select_data == 'tds':
                trip_duration_stats(df)
            elif select_data == 'us':
                user_stats(df, city)
            elif select_data == 'rd':
                mark_place = raw_data(df, mark_place)
            elif select_data == 'r':
                break

        restart = choice("\nWould you like to restart?\n\n[y]Yes\n[n]No\n\n>")
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
    main()
#thankyou.
