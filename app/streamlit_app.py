import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the page
st.set_page_config(
    page_title="Personal Library Manager",
    page_icon="📚",
    layout="wide"
)

# API configuration
def get_api_url():
    if os.getenv('STREAMLIT_CLOUD'):
        # Production URL - replace with your actual deployed API URL
        return "https://your-api-url.herokuapp.com/api"
    else:
        # Local development URL
        return "http://localhost:5000/api"

API_URL = get_api_url()

def main():
    st.title("📚 Personal Library Manager")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Dashboard", "Add Book", "Manage Books", "Statistics"])
    
    if page == "Dashboard":
        show_dashboard()
    elif page == "Add Book":
        show_add_book()
    elif page == "Manage Books":
        show_manage_books()
    elif page == "Statistics":
        show_statistics()

def show_dashboard():
    st.header("📊 Dashboard")
    
    # Fetch books from API
    try:
        response = requests.get(f"{API_URL}/books")
        books = response.json()
        
        if books:
            df = pd.DataFrame(books)
            
            # Display recent books
            st.subheader("Recent Books")
            st.dataframe(df[['title', 'author', 'status', 'added_date']].head(5))
            
            # Reading progress
            st.subheader("Reading Progress")
            status_counts = df['status'].value_counts()
            fig = px.pie(values=status_counts.values, names=status_counts.index, title="Books by Status")
            st.plotly_chart(fig)
            
        else:
            st.info("No books in your library yet. Add some books to get started!")
    except Exception as e:
        st.error(f"Error fetching books: {str(e)}")

def show_add_book():
    st.header("➕ Add New Book")
    
    with st.form("add_book_form"):
        title = st.text_input("Title")
        author = st.text_input("Author")
        isbn = st.text_input("ISBN (optional)")
        category = st.text_input("Category")
        status = st.selectbox("Status", ["To Read", "Reading", "Completed", "On Hold"])
        
        submitted = st.form_submit_button("Add Book")
        
        if submitted:
            try:
                book_data = {
                    "title": title,
                    "author": author,
                    "isbn": isbn,
                    "category": category,
                    "status": status,
                    "added_date": datetime.now().isoformat()
                }
                
                response = requests.post(f"{API_URL}/books", json=book_data)
                
                if response.status_code == 201:
                    st.success("Book added successfully!")
                else:
                    st.error(f"Error adding book: {response.text}")
            except Exception as e:
                st.error(f"Error: {str(e)}")

def show_manage_books():
    st.header("📖 Manage Books")
    
    try:
        response = requests.get(f"{API_URL}/books")
        books = response.json()
        
        if books:
            df = pd.DataFrame(books)
            
            # Search and filter
            search_term = st.text_input("Search books")
            if search_term:
                df = df[df['title'].str.contains(search_term, case=False) | 
                       df['author'].str.contains(search_term, case=False)]
            
            # Display books with edit options
            for _, book in df.iterrows():
                with st.expander(f"{book['title']} by {book['author']}"):
                    st.write(f"Status: {book['status']}")
                    st.write(f"Category: {book['category']}")
                    
                    if st.button("Edit", key=f"edit_{book['id']}"):
                        edit_book(book)
                    
                    if st.button("Delete", key=f"delete_{book['id']}"):
                        delete_book(book['id'])
        else:
            st.info("No books in your library yet.")
    except Exception as e:
        st.error(f"Error: {str(e)}")

def edit_book(book):
    with st.form(f"edit_form_{book['id']}"):
        title = st.text_input("Title", value=book['title'])
        author = st.text_input("Author", value=book['author'])
        status = st.selectbox("Status", ["To Read", "Reading", "Completed", "On Hold"], 
                            index=["To Read", "Reading", "Completed", "On Hold"].index(book['status']))
        
        if st.form_submit_button("Save Changes"):
            try:
                update_data = {
                    "title": title,
                    "author": author,
                    "status": status
                }
                
                response = requests.put(f"{API_URL}/books/{book['id']}", json=update_data)
                
                if response.status_code == 200:
                    st.success("Book updated successfully!")
                else:
                    st.error(f"Error updating book: {response.text}")
            except Exception as e:
                st.error(f"Error: {str(e)}")

def delete_book(book_id):
    try:
        response = requests.delete(f"{API_URL}/books/{book_id}")
        
        if response.status_code == 200:
            st.success("Book deleted successfully!")
        else:
            st.error(f"Error deleting book: {response.text}")
    except Exception as e:
        st.error(f"Error: {str(e)}")

def show_statistics():
    st.header("📈 Statistics")
    
    try:
        response = requests.get(f"{API_URL}/books")
        books = response.json()
        
        if books:
            df = pd.DataFrame(books)
            
            # Books by category
            st.subheader("Books by Category")
            category_counts = df['category'].value_counts()
            fig1 = px.bar(x=category_counts.index, y=category_counts.values, 
                         title="Number of Books by Category")
            st.plotly_chart(fig1)
            
            # Reading progress over time
            st.subheader("Reading Progress Over Time")
            df['added_date'] = pd.to_datetime(df['added_date'])
            monthly_counts = df.groupby(df['added_date'].dt.to_period('M')).size()
            fig2 = px.line(x=monthly_counts.index.astype(str), y=monthly_counts.values,
                          title="Books Added Over Time")
            st.plotly_chart(fig2)
            
        else:
            st.info("No books in your library yet.")
    except Exception as e:
        st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 