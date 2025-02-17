import sqlite3
import re
from typing import Tuple, List, Dict
import pandas as pd

class ChinookQueryProcessor:
    def __init__(self, db_path: str = 'chinook.db'):
        self.db_path = db_path
        # Define query patterns and their corresponding SQL templates
        self.query_patterns = [
            {
                'pattern': r'(?i)tracks?\s+by\s+(.+?)(?:\s+|$)',
                'sql': """
                    SELECT DISTINCT t.Name as Track, ar.Name as Artist, al.Title as Album, g.Name as Genre
                    FROM Track t
                    JOIN Album al ON t.AlbumId = al.AlbumId
                    JOIN Artist ar ON al.ArtistId = ar.ArtistId
                    LEFT JOIN Genre g ON t.GenreId = g.GenreId
                    WHERE ar.Name LIKE ?
                    ORDER BY t.Name
                """,
                'param_processor': lambda m: (f"%{m.group(1)}%",)
            },
            {
                'pattern': r'(?i)albums?\s+by\s+(.+?)(?:\s+|$)',
                'sql': """
                    SELECT al.Title as Album, ar.Name as Artist, 
                           COUNT(t.TrackId) as Tracks,
                           SUM(t.Milliseconds)/60000.0 as Duration_Minutes
                    FROM Album al
                    JOIN Artist ar ON al.ArtistId = ar.ArtistId
                    LEFT JOIN Track t ON al.AlbumId = t.AlbumId
                    WHERE ar.Name LIKE ?
                    GROUP BY al.AlbumId
                    ORDER BY al.Title
                """,
                'param_processor': lambda m: (f"%{m.group(1)}%",)
            },
            {
                'pattern': r'(?i)songs?\s+in\s+genre\s+(.+?)(?:\s+|$)',
                'sql': """
                    SELECT t.Name as Track, ar.Name as Artist, al.Title as Album
                    FROM Track t
                    JOIN Album al ON t.AlbumId = al.AlbumId
                    JOIN Artist ar ON al.ArtistId = ar.ArtistId
                    JOIN Genre g ON t.GenreId = g.GenreId
                    WHERE g.Name LIKE ?
                    ORDER BY ar.Name, t.Name
                """,
                'param_processor': lambda m: (f"%{m.group(1)}%",)
            },
            {
                'pattern': r'(?i)customers?\s+from\s+(.+?)(?:\s+|$)',
                'sql': """
                    SELECT FirstName, LastName, City, Country, Email
                    FROM Customer
                    WHERE Country LIKE ? OR City LIKE ?
                    ORDER BY Country, City, LastName
                """,
                'param_processor': lambda m: (f"%{m.group(1)}%", f"%{m.group(1)}%")
            },
            {
                'pattern': r'(?i)top\s+(\d+)\s+tracks?(?:\s+by\s+sales)?',
                'sql': """
                    SELECT t.Name as Track, ar.Name as Artist, 
                           COUNT(il.InvoiceLineId) as Times_Sold,
                           SUM(il.UnitPrice * il.Quantity) as Total_Revenue
                    FROM Track t
                    JOIN Album al ON t.AlbumId = al.AlbumId
                    JOIN Artist ar ON al.ArtistId = ar.ArtistId
                    JOIN InvoiceLine il ON t.TrackId = il.TrackId
                    GROUP BY t.TrackId
                    ORDER BY Times_Sold DESC
                    LIMIT ?
                """,
                'param_processor': lambda m: (int(m.group(1)),)
            }
        ]

    def connect_db(self):
        """Create database connection"""
        return sqlite3.connect(self.db_path)

    def process_query(self, user_query: str) -> Tuple[str, tuple]:
        """Process natural language query and convert to SQL"""
        for pattern in self.query_patterns:
            match = re.search(pattern['pattern'], user_query)
            if match:
                return pattern['sql'], pattern['param_processor'](match)

        # Default query if no patterns match
        return """
            SELECT t.Name as Track, ar.Name as Artist, al.Title as Album
            FROM Track t
            JOIN Album al ON t.AlbumId = al.AlbumId
            JOIN Artist ar ON al.ArtistId = ar.ArtistId
            LIMIT 10
        """, ()

    def execute_query(self, user_query: str) -> pd.DataFrame:
        """Execute the query and return results as a pandas DataFrame"""
        sql, params = self.process_query(user_query)
        
        conn = self.connect_db()
        try:
            df = pd.read_sql_query(sql, conn, params=params)
            return df
        finally:
            conn.close()

    def get_query_examples(self) -> List[str]:
        """Return example queries that the processor can handle"""
        return [
            "Show tracks by Queen",
            "Show top 5 songs by AC/DC",
            "Find albums by Queen",
            "List songs in Rock genre",
            "Show customers from Brazil"
        ]
    
