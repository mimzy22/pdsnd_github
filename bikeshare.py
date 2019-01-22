import time
import pandas as pd
import numpy as np
import calendar as cal

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! I\'m Perry, your interactive guide to exploring Bikeshare Statistical Data!")

    #Get user name.
    user_name = input("\nPlease type your name: ")

    #Get user input for city (chicago, new york city, washington).
    print("\nIt's great to meet you, " + user_name + "! What city would you like data about?")

    #Confirm the city the user chose, or ask them to re-enter.
    while True:
        city = str.title(input("\nPlease type Chicago, New York City, or Washington: "))
        if city in ("Chicago","New York City","Washington"):
            break
        else :
            city = print("\nI'm sorry " + user_name + ", I don't understand.")
    print("\nGreat! I will show you Bikeshare data for {}.".format(city))

    #Get user input for month.
    print("\nNow, what month would you like data about?")
    #confirm the month the user chose, or ask them to re-enter.
    while True:
        month = str.title(input("\nPlease type the full month name (i.e. January, Febuary, etc.) or 'All' to see data for that month or all months: "))
        if month in ("January","February","March","April","May","June","July","August","September","October","November","December","All"):
            break
        else:
            month = print("\nI'm sorry " + user_name + ", I don't understand.")
    print("\nGreat! I will show you Bikeshare data for {}.".format(month))

    #Get user input for day.
    while True:
        day = str.title(input("\nPlease type the day of the week (i.e. Monday, Tuesday, etc.) you would like information for, or type 'All' to see data for all days: "))
        if day in ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday","All"):
            break
        else:
            day = print("\nI'm sorry " + user_name + ", I don't understand.")
    print("\nGreat! I will show you Bikeshare data for {}.".format(day))

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
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #load data file user selected into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    #convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #extract the month and day of the week from the Start Time df to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    #filter by month if applicable
    if month != 'All':
        #use the index of the months list to get the corresponding int
        months = ["January","February","March","April","May","June","July","August","September","October","November","December"]
        month = months.index(month) + 1

        #filter by month to create the new dataframe
        df = df[df['month'] == month]

    #filter by day of week if applicable
    if day != 'All':
        #filter by month to create the new df
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    print("\nMost Popular Start Month: ", cal.month_name[popular_month])

    # display the most common day of week
    df['day of week'] = df['Start Time'].dt.weekday_name
    popular_day_of_week = df['day of week'].mode()[0]
    print("\nMost Popular Start Day of the Week: ", popular_day_of_week)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_start_hour = df['hour'].mode()[0]
    print("\nMost Popular Start Hour (in 24-hour military time): ", popular_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()
    print("\nMost Popular Start Station (if two or more stations are equally popular each will be listed): ", start_station)

    # display most commonly used end station
    end_station = df['End Station'].mode()
    print("\nMost Popular End Station (if two or more stations are equally popular each will be listed): ", end_station)

    # create a column that combines the start and end station of each trip
    df['Start to End'] = df['Start Station'] + ' - ' + df['End Station']

    # display most frequent combination of start station and end station trip
    trip_combination = df['Start to End'].mode()
    print("\nMost frequent combination of start and end station (if two or more are equally popular each will be listed): ", trip_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum(axis=0)
    print('\nTotal travel time in seconds is: ', total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('\nMean travel time per trip in seconds is: ', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats_wa(df):
    """
        Displays statistics on bikeshare users. Only used for the Washington
        data set because that data set doesn't have gender or birth date data.
        This function skips birth date and gender data so that the program doesn't
        error out because the data is missing.
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    types_of_users = df['User Type'].value_counts()
    print('\nThe number of riders for each user type follows: ', types_of_users)

    # Display counts of gender
    print('\nNo gender data is available for Washington\n')

    # Display earliest, most recent, and most common year of birth
    print('\nNo age or birth date data is available for Washington\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats_ny_ci(df):
    """
        Displays statistics on bikeshare users. Only used for Chicago and New York City
        data sets because the Washington data set is missing gender and birth date data.
        This function provides data about the gender and birth date of users.
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    types_of_users = df['User Type'].value_counts()
    print('\nThe number of riders for each user type follows: ', types_of_users)

    # Display counts of gender
    count_by_gender = df['Gender'].value_counts()
    print('\nThe number of riders by gender follows: ',count_by_gender)

    # Display earliest, most recent, and most common year of birth
    earliest_birth_year = df['Birth Year'].min()
    print('\nThe earliest birth year is: ', earliest_birth_year)

    most_recent_birth_year = df['Birth Year'].max()
    print('\nThe most recent birth year is: ', most_recent_birth_year)

    most_common_birth_year = df['Birth Year'].mode()
    print('\nThe most common birth year is: ', most_common_birth_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    """Displays raw data 5 rows at a time as prompted by user"""

    print_raw_data = input('\nWould you like to see 5 rows of raw data? Enter yes or no.\n')
    start_iloc = -5
    end_iloc = 0

    while print_raw_data.lower() in 'yes':
        start_iloc += 5
        end_iloc += 5
        print(df.iloc[start_iloc:end_iloc])
        print_raw_data = input('\nWould you like to see the next 5 rows of raw data? Enter yes or no.\n')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        """User_stats is separated into two functions because the washington
        data set is missing gender and birth date data. Separating into two functions
        allows us to show gender and birth data data for Chicago and New York City without
        getting an error if the user choses to see Washington data.
        """
        if city in 'Washington':
            user_stats_wa(df)
        else:
            user_stats_ny_ci(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
