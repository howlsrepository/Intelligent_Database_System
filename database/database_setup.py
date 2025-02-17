import urllib.request
import os
import sqlite3

def setup_chinook_database():
    """Download and setup the Chinook database"""
    # Download the database if it doesn't exist
    if not os.path.exists('chinook.db'):
        print("Downloading Chinook database...")
        url = "https://raw.githubusercontent.com/lerocha/chinook-database/master/ChinookDatabase/DataSources/Chinook_Sqlite.sqlite"
        urllib.request.urlretrieve(url, 'chinook.db')
        print("Download complete!")
    else:
        print("Chinook database already exists!")

    # Test the connection and print some basic stats
    try:
        conn = sqlite3.connect('chinook.db')
        cursor = conn.cursor()
        
        # Get table counts
        tables = [
            'Album', 'Artist', 'Customer', 'Employee', 'Genre',
            'Invoice', 'InvoiceLine', 'MediaType', 'Playlist',
            'PlaylistTrack', 'Track'
        ]
        
        print("\nDatabase Statistics:")
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"{table}: {count} records")
            
        conn.close()
        print("\nDatabase setup complete and working correctly!")
        
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    setup_chinook_database()