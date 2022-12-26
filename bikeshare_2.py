import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS_NAME = ["january", "february", "march", "april", "may", "june", "all"]
DAYS_NAME = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

# functions of filter
def getCountryName():
    while True:
        print("would you like to see data for chicago, new york city or washington")
        country = input("enter country name: ")
        if country.lower() not in CITY_DATA:
            print("please enter valid country name")
        else:
            return country.lower()

def getBoth():
    """"function to get both month and day from the user"""
    month = getMonth()
    day = getDay()
    return month, day

def getDay():
    """"function to get right Day from the user"""
    try:
        print("please enter name of the day you want (e.g. 1 = sunday, wednesday = 4, Monday = 2)")
        day = int(input())
        if day > 7 or day < 1:
            print("please enter valid name days")
            getDay()
        else:
            return day
    except:
        print("please enter numeric value")

def getMonth():
    """"function to get right month from the user"""
    print("which month you want from january, february, march, april, may, june, if you want all months type \"all\"")
    month = input()
    if month.lower() not in MONTHS_NAME:
        print("please enter valid value")
        getMonth()
    else:
        return month.lower()
######################

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')
    month = ""
    day = ""

    city = getCountryName()
    print("would you like to filter by month, day, both, or not at all? Type \"none\" for no time filter.")
    response = input()

    if response.lower() == "both":
        month, day = getBoth()
    elif response.lower() == "month":
        month = getMonth()
        day = ""
    elif response.lower() == "day":
        day = getDay()
        month = ""


    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    # if day or month not concluded with us, make check that the string is empty for this
    if month != "":
        df['month'] = df['Start Time'].dt.month
    if day != "":
        df['day_of_week'] = df['Start Time'].dt.dayofweek


    # filter by month if applicable
    if month != 'all' and month:
        # use the index of the months list to get the corresponding int
        month = MONTHS_NAME.index(month) + 1
        df = df[df["month"] == month]

    # filter by day of week if applicable
    if day != 'all' and day:
        # filter by day of week to create the new dataframe
        df = df[df["day_of_week"] == day]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()


    # display the most common month
    if "month" in df:
        print("the most common month :", df["month"].mode()[0])

    # display the most common day of week
    if "day_of_week" in df:
        print("the most common day of week :", df["day_of_week"].mode()[0])

    #########
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most popular hour
    popular_hour = df['hour'].mode()[0]

    #############

    print("the most common start hour :", popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print(df["Start Time"].mode()[0])

    # display most commonly used end station
    print(df["End Station"].mode()[0])

    # display most frequent combination of start station and end station trip
    combination = df['Start Station'].astype(str) + " -> " + df['End Station'].astype(str)
    most_combination = combination.mode()[0]
    print("most frequent start station:", most_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("total travel time :", df["Trip Duration"].sum())

    # display mean travel time
    print("mean travel time :", df["Trip Duration"].mean())


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("counts of user types :", df["User Type"].value_counts())

    try:
        # Display counts of gender
        print("counts of gender :", df["Gender"].value_counts())

        # Display earliest, most recent, and most common year of birth
        # print("earliest, most recent, and most common year of birth :", df["Birth Year"].mean())
        print("earliest year of birth :", df["Birth Year"].min())
        print("most recent year of birth :", df["Birth Year"].max())
        print("most common year of birth :", df["Birth Year"].mode()[0])

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    except:
        print("no data on user like gender or birth day for this file")

def individualTrip(df):
    number = 0
    while True:
        print("would you like to view individual trip date?/ type -> yes, no")
        response = input("enter your response : ")
        if response.lower() == "yes":
            print(df.iloc[number:number + 5,:])
            number += 5
        elif response.lower() == "no":
            break
        else:
            print("please enter valid value")

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        individualTrip(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()