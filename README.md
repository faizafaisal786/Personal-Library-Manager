# Personal Library Manager

A web application to manage your personal book collection. Track your reading progress, organize books by categories, and maintain a digital library.

## Features

- Add, edit, and delete books
- Categorize books
- Track reading progress
- Search and filter books
- User authentication
- Responsive design

## Tech Stack

- Backend: Python with Flask
- Frontend: Streamlit
- Database: SQLAlchemy with SQLite
- Authentication: JWT

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Installation

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/personal-library-manager.git
   cd personal-library-manager
   ```

2. Set up the Python virtual environment and install dependencies:
   ```bash
   # Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install Python dependencies
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory with the following variables:
   ```
   FLASK_APP=app.py
   FLASK_ENV=development
   SECRET_KEY=your_secret_key
   DATABASE_URL=sqlite:///library.db
   ```

4. Initialize the database:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

5. Start the application:
   ```bash
   # Start the Streamlit app
   streamlit run app/streamlit_app.py
   ```

## Deployment

### GitHub Deployment
1. Create a new repository on GitHub
2. Push your code:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/personal-library-manager.git
   git push -u origin main
   ```

### Streamlit Cloud Deployment
1. Create a Streamlit Cloud account
2. Connect your GitHub repository
3. Configure the deployment settings:
   - Main file path: `app/streamlit_app.py`
   - Python version: 3.8 or higher
   - Environment variables: Add your `.env` variables

## Project Structure

```
personal-library-manager/
├── app/                # Application code
│   ├── models/        # Database models
│   ├── routes/        # API routes
│   ├── static/        # Static files
│   ├── streamlit_app.py  # Streamlit frontend
│   └── __init__.py
├── migrations/        # Database migrations
├── venv/             # Python virtual environment
├── .gitignore        # Git ignore file
├── requirements.txt   # Python dependencies
├── config.py         # Configuration
└── README.md
``` 