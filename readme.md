# Database Chatbot 

## Overview 
This chatbot is an interactive application that allows users to query the database using natural language. We have taken the Sakila Movie Rental Database as a sample database to showcase the working of this chatbot. The chatbot utilizes a Large Language Model (LLM) to generate SQL queries based on user input and execute them on the SQLite database containing Sakila data. 

## Features
1) Streamlit Web Interface: Provides an easy-to-use frontend for querying the database.
2) Natural Language Query Processing: Converts user queries into SQL using Google Gemini AI.
3) Command-Line Interface (CLI): Users can interact with the chatbot via the terminal.

## Project Structure
├── database_setup.py       # Initializes and  explores the Sakila SQLite database
├── chatbot.py              # Core chatbot logic for converting natural language to SQL
├── streamlit_app.py        # Streamlit web application for the chatbot
├── .env.example            # Example environment file containing sample API key
├── .gitignore              # Excludes .env from version control
└── requirements.txt        # Dependencies required for the project

## Installation
### Clone the Repository
git clone https://github.com/howlsrepository/Intelligent_Database_System
cd <repository_folder>
### Set Up a Virtual Environment (Recommended)
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
### Install Dependencies 
pip install -r requirements.txt
### Configure API Key
1) Make a new file in yoru working directory and name it `.env`
2) Copy contents of `.env.exmaple` to `.env`
3) Edit `.env` and add your Google Gemini API key

## Usage
### Command-Line Chatbot
Run the chatbot in the terminal: 
python chatbot.py

### Streamlit Web App
Start the web-based chatbot: 
streamlit run streamlit_app.py
