import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from prettytable import PrettyTable

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
VALID_DAYS = ['monday', 'tuesday','wednesday','thursday','friday','saturday','sunday']
VALID_MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    while True:
        # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
        city = input('Which city you want to exlpore data for? (Chicago, New York City, Washington)\n')
        if city.lower() in ['chicago', 'new york city', 'washington']:
            break
        else:
            print('Please enter valid city name.')
    while True:
        # get user input for month (all, january, february, ... , june)
        month = input('\nFilter by which month? (January, February, ... , June) or (Press Enter to skip)?\n')
        if month == '' or month.lower() in VALID_MONTHS:
            break
        else:
            print('Please enter valid month.')
    while True:
        # get user input for day of week (all, monday, tuesday, ... sunday)
        day = input('\nFilter by which week day? (Monday, Tuesday, ... Sunday) or (Press Enter to skip)?\n')
        if day == '' or day.lower() in VALID_DAYS:
            break
        else:
            print('Please enter a valid day')
    print('#'*60)
    return city.lower(), month.lower(), day.lower()

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
    df = pd.read_csv(CITY_DATA.get(city))
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    df['hour'] = df['Start Time'].dt.hour
    # filter by month if applicable
    if month.strip() != '':
        # use the index of the months list to get the corresponding int
        month = VALID_MONTHS.index(month)
        # filter by month to create the new dataframe
        df = df.loc[df['month'] == month]
    # filter by day of week if applicable
    if day.strip() != '':
        # filter by day of week to create the new dataframe
        day = VALID_DAYS.index(day)
        df = df.loc[df['day_of_week'] == day]
    return df

def time_stats(df,city, month, day):
    """ Displays statistics on the most frequent times of travel. """
    print('\nCalculating The Most Frequent Times of Travel For City({})...'.format(city))
    start_time = time.time()
    # display the most common month
    if month == '':
        print('Most common month: ', VALID_MONTHS[df['month'].value_counts().idxmax()-1], ', Count: ', df['month'].value_counts().max())
    # display the most common day of week
    if day == '':
        print('Most common day of week: ', VALID_DAYS[df['day_of_week'].mode()[0]], ', Count: ', df['day_of_week'].value_counts().max())
    # display the most common start hour
    print('Most common hour: ', df['hour'].mode()[0],', Count: ', df['hour'].value_counts().max())
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('#'*60)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('Calculating The Most Popular Stations and Trip...')
    start_time = time.time()
    # display most commonly used start station
    print('Top start station: ', df['Start Station'].mode()[0])
    # display most commonly used end station
    print('Top end station: ', df['End Station'].mode()[0])
    # display most frequent combination of start station and end station trip
    groupby_stations = df.groupby(['Start Station','End Station'])
    start_end_stations = groupby_stations.size().idxmax()
    print('\nMost famous Origin and Destination')
    print('Origin: ',start_end_stations[0])
    print('Destination: ',start_end_stations[1])
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('#'*60)

def trip_duration_stats(df):
    """ Displays statistics on the total and average trip duration. """
    print('Calculating Trip Duration...')
    start_time = time.time()
    # display total travel time
    travel_time = df['Trip Duration']
    print('Total Travel Time: ',travel_time.sum())
    # display mean travel time
    print('Mean Travel Time: ', travel_time.mean())
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('#'*60)

def user_stats(df,city):
    """ Displays statistics on bikeshare users. """
    print('Calculating User Stats...')
    start_time = time.time()
    # Display counts of user types
    print('User types and counts')
    for key,val in df['User Type'].value_counts().items():
        print(key,':',val)
    # Display counts of gender
    try:
        gender_items = df['Gender'].value_counts().items()
        print('Gender types and counts')
        for key,val in gender_items:
            print(key,':',val)
    except:
        print('OOPs Gender data not available for this city')
    # Display earliest, most recent, and most common year of birth
    try:
        earliest = int(df['Birth Year'].min())
        most_recent = int(df['Birth Year'].max())
        most_common = int(df['Birth Year'].value_counts().idxmax())
        most_common_count = int(df['Birth Year'].value_counts().max())
        print('Following are the earliest, most recent, and most common year of birth')
        print('Earliest Birth Year:', earliest)
        print('Most Recent Birth Year:', most_recent)
        print('Most Common Birth Year:', most_common, 'Count: ', most_common_count)
    except KeyError:
        print('OOPs Birth Year data not available for this city')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('#'*60)

def print_user_interests(city,month,day):
    """ Display the Filters choosen by the user """
    print('It looks you are interested in following data.')
    print('Filter by City -> ',city)
    if month != '':
        print('Filter by Month->',month)
    if day != '':
        print('Filter by Day->', day)
    print('Below data will be based on selected options....')
    print('#'*60)

def plot_riders_data(df):
    """ Plots the rider growth per month """
    print('Printing Riders growth per month')
    months = []
    riders = []
    for key,val in df['month'].sort_index().value_counts(sort = False).items():
        months.append(VALID_MONTHS[key-1])
        riders.append(val)
    plt.plot(months,riders)
    plt.xlabel('Months')
    plt.ylabel('Riders Count')
    plt.show()

def display_raw_data(df):
    """ Display raw data from the dataframeself in Tabular Format using Pretty Table library.
        Initially prints the 5 rows and asks from user if they want to proceed further
    """
    print('#'*60)
    print('Displaying raw data from for the bikeshare.\n')
    no_of_rows = df.shape[0]
    for i in range(0, no_of_rows,5):
        t = PrettyTable()
        t.field_names = df.columns[1:7].insert(0,'Index')
        tempdf = df.iloc[i:i+5,1:7]
        for row in tempdf.itertuples():
            t.add_row(row)
        print(t)
        print_more = input('\nWould you like to see more data? Please enter yes or no.\n')
        if print_more.lower() != 'yes':
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        if df.empty:
            print('No data found using selected options.')
            print('#'*60)
        else:
            print_user_interests(city,month,day)
            time_stats(df,city,month,day)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df,city)
            if month == '':
                is_plot = input('\nWould you like to plot riders data per month? Enter yes or no.\n')
                if is_plot.lower() == 'yes':
                    plot_riders_data(df)
            display_raw_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
