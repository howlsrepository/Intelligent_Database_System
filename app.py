import streamlit as st
import pandas as pd
from chinook_query_processor import ChinookQueryProcessor

def main():
    st.title("🎵 Chinook Music Store Query System")
    
    # Initialize query processor
    processor = ChinookQueryProcessor()
    
    # Add description and examples
    st.write("""
    This system can answer questions about the Chinook music store database.
    Try asking questions like:
    """)
    
    # Show example queries
    examples = processor.get_query_examples()
    for example in examples:
        st.write(f"- {example}")
    
    # Create query input
    user_query = st.text_input("Enter your question:", "Show tracks by Queen")
    
    if user_query:
        try:
            # Get results
            df = processor.execute_query(user_query)
            
            # Show the query results
            if not df.empty:
                st.subheader("📊 Query Results")
                
                # Display the dataframe
                st.dataframe(
                    df,
                    hide_index=True,
                )
                
                # Show some statistics
                st.subheader("📈 Quick Statistics")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Number of Results", len(df))
                
                with col2:
                    if 'Total_Revenue' in df.columns:
                        total_revenue = df['Total_Revenue'].sum()
                        st.metric("Total Revenue", f"${total_revenue:.2f}")
                    elif 'Duration_Minutes' in df.columns:
                        total_duration = df['Duration_Minutes'].sum()
                        st.metric("Total Duration", f"{total_duration:.1f} minutes")
            else:
                st.warning("No results found for your query.")
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    main()