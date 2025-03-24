import sqlite3
import os
import pandas as pd
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# Absolute database path
db_path = "sakila_master.db"

class SakilaLLMQueryProcessor:
    def __init__(self, api_key: str):
        self.db_path = db_path
        self.api_key = api_key
        self.llm = None
        self.schema_info = None

        print(f"Using database at: {self.db_path}")

        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"❌ ERROR: Database file not found at {self.db_path}")

        if not api_key:
            raise ValueError("❌ ERROR: API key is required for this chatbot")
        
        self.configure_api(api_key)
        self.fetch_schema_info()

    def configure_api(self, api_key: str):
        genai.configure(api_key=api_key)
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", google_api_key=api_key)

    def connect_db(self):
        try:
            conn = sqlite3.connect(self.db_path)
            print("✅ Connected to Sakila Database.")
            return conn
        except sqlite3.Error as e:
            raise ConnectionError(f"❌ ERROR: Failed to connect to database - {e}")

    def fetch_schema_info(self):
        self.schema_info = """
        📌 Sakila Database Schema:

        📂 Table: actor
           ➡ Columns: actor_id, first_name, last_name, last_update

        📂 Table: country
           ➡ Columns: country_id, country, last_update

        📂 Table: city
           ➡ Columns: city_id, city, country_id, last_update

        📂 Table: address
           ➡ Columns: address_id, address, address2, district, city_id, postal_code, phone, last_update

        📂 Table: language
           ➡ Columns: language_id, name, last_update

        📂 Table: category
           ➡ Columns: category_id, name, last_update

        📂 Table: customer
           ➡ Columns: customer_id, store_id, first_name, last_name, email, address_id, active, create_date, last_update

        📂 Table: film
           ➡ Columns: film_id, title, description, release_year, language_id, original_language_id, rental_duration, rental_rate, length, replacement_cost, rating, special_features, last_update

        📂 Table: film_actor
           ➡ Columns: actor_id, film_id, last_update

        📂 Table: film_category
           ➡ Columns: film_id, category_id, last_update

        📂 Table: film_text
           ➡ Columns: film_id, title, description

        📂 Table: inventory
           ➡ Columns: inventory_id, film_id, store_id, last_update

        📂 Table: staff
           ➡ Columns: staff_id, first_name, last_name, address_id, picture, email, store_id, active, username, password, last_update

        📂 Table: store
           ➡ Columns: store_id, manager_staff_id, address_id, last_update

        📂 Table: payment
           ➡ Columns: payment_id, customer_id, staff_id, rental_id, amount, payment_date, last_update

        📂 Table: rental
           ➡ Columns: rental_id, rental_date, inventory_id, customer_id, return_date, staff_id, last_update
        """

    def generate_sql_with_llm(self, natural_language_query: str) -> str:
        if not self.llm:
            return "Error: API key not configured"
        
        prompt = f"""
        You are a SQL expert. Convert the following natural language query into a valid SQL query 
        for the Sakila SQLite database. Use the schema information provided below:
        
        {self.schema_info}
        
        Query: {natural_language_query}
        
        Return only the SQL query without any explanations or markdown formatting.
        """
        
        print(f"\n🔎 Sending query to LLM: '{natural_language_query}'")
        response = self.llm.invoke(prompt)
        sql_query = response.content.strip()
        
        return sql_query

    def execute_query(self, user_query: str):
        sql = self.generate_sql_with_llm(user_query)
        try:
            conn = self.connect_db()
            df = pd.read_sql_query(sql, conn)
            conn.close()
            return {"success": True, "data": df, "sql": sql}
        except sqlite3.Error as e:
            return {"success": False, "error": str(e), "sql": sql}


def run_sakila_chatbot():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ ERROR: GEMINI_API_KEY environment variable not found.")
        return
    
    chatbot = SakilaLLMQueryProcessor(api_key=api_key)
    print("\n✨ Sakila Movie Rental Database Chatbot ✨")
    
    while True:
        user_query = input("\n> What would you like to know? ")
        if user_query.lower() in ('exit', 'quit', 'bye'):
            print("Goodbye!")
            break
        
        print("\n🔄 Generating SQL and querying database...")
        result = chatbot.execute_query(user_query)
        
        if result["success"]:
            print("\n📝 SQL Query:")
            print(f"{result['sql']}\n")
            print("📊 Results:")
            print(result["data"].to_string(index=False) if not result["data"].empty else "No results found.")
        else:
            print(f"\n❌ Error: {result['error']}")
            print(f"SQL attempted: {result['sql']}")


if __name__ == "__main__":
    run_sakila_chatbot()
