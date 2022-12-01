import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# Function to get filter
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Please, enter the city name: ').lower
    while city not in CITY_DATA.keys():
        city = input ("Please, Choose between chicago, new york city, and washington: ").lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    month = input('Please, enter the month: ').lower()
    while month not in ('all','january', 'february', 'march', 'april', 'may', 'june'):
        print("Invaild input. Try again.")
        
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Please, enter the day: ').lower()
    while day not in  ('all','sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'):
        print("Invaild input. Try again.")
            
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
    df = pd.read_csv("{}.csv".format(city.replace(" ","_")))  
    
    #convert columns Start Time and End Time into date format
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    
    # extract month from Start Time column
    df['month'] = df['Start Time'].dt.month
    
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # extract day from Start Time column
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print("The most common month is: ", df['month'].value_counts().idxmax())

    # TO DO: display the most common day of week
    print("The most common day is: ", df['day_of_week'].value_counts().idxmax())

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print("The most common hour is: ", df['hour'].value_counts().idxmax())


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print("The most common start station is: ", df['Start Station'].value_counts().idxmax())

    # TO DO: display most commonly used end station
    print("The most common end station is: ", df['End Station'].value_counts().idxmax())

    # TO DO: display most frequent combination of start station and end station trip
    most_common_start_and_end_stations = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print("The most frequent combination of start station and end station trip:"+ str(most_common_start_and_end_stations))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_duration = df['Trip Duration'].sum() / 3600
    print("The total travel time in hours is: ", total_duration)

    # TO DO: display mean travel time
    mean_duration = df['Trip Duration'].mean() / 3600
    print("The mean travel time in hours is: ", mean_duration)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """
    Display contents of the CSV file to the display as requested by
    the user.
    """

    start_loc = 0
    end_loc = 5

    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()

    if view_data == 'yes':
        while end_loc <= df.shape[0] - 1:
            print(df.iloc[start_loc:end_loc,:])
            start_loc += 5
            end_loc += 5

            view_data = input("Do you wish to continue?: ").lower()
            if view_data == 'no':
                break

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating Users Statistics...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print("The count of user types is: \n" + str(user_types))
    
    # TO DO: Display counts of gender
    try:
        user_gender = df['Gender'].value_counts()
        print("The count of gender is: \n" + str(user_gender))
    except:
        print("\nThere is no 'Gender' column in this data.")
        
    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        earliest_year_of_birth = int(df['Birth Year'].min())
        most_recent_year_of_birth = int(df['Birth Year'].max())
        most_common_year_of_birth = int(df['Birth Year'].value_counts().idxmax())
        print("The earliest year of birth is:",earliest_year_of_birth,
              "\nMost recent year of birth is:",most_recent_year_of_birth,
               "\nThe most common year of birth is: ",most_common_year_of_birth)
    except:
        print("\nThere is no 'Birth' column in this data.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
        print("\nSee you soon :)")


if __name__ == "__main__":
    main()
