import streamlit as st
import os
from chatbot import SakilaLLMQueryProcessor, run_sakila_chatbot

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Set up the Streamlit app
st.title("Sakila Movie Rental Database Chatbot")
st.write("Ask questions about movies, actors, customers, rentals, and payments.")

# Input for API key
api_key = st.text_input("Enter your Gemini API Key:", type="password")

if api_key:
    # Initialize the chatbot
    chatbot = SakilaLLMQueryProcessor(api_key=api_key)

    # Input for user query
    user_query = st.text_input("What would you like to know?")

    if user_query:
        if user_query.lower() in ('exit', 'quit', 'bye'):
            st.write("Goodbye!")
        else:
            st.write("🔄 Generating SQL and querying database...")
            result = chatbot.execute_query(user_query)

            if result["success"]:
                st.write("📝 SQL Query:")
                st.code(result['sql'])

                st.write("📊 Results:")
                if not result["data"].empty:
                    st.dataframe(result["data"])
                else:
                    st.write("No results found.")
            else:
                st.error(f"❌ Error: {result['error']}")
                st.write(f"SQL attempted: {result['sql']}")
else:
    st.warning("Please enter your Gemini API Key to proceed.")
