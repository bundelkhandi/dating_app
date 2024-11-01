
# Dating App 

This project is a dating app feature built using **FastAPI** and **Streamlit** that allows fetching, displaying, and mapping user data based on geographical distance and compatibility scores. The app visualizes matches on a map, showing distance and compatibility between the users.

## Features

- **Fetch Users**: Scrape a specific number of users.
- **Random User**: Display a random user's details.
- **Nearest Users**: Fetch and display the nearest users to a selected random user.
- **Map Visualization**: Visualize nearest users on a map with distance and compatibility score.

## Tech Stack

- **Backend**: FastAPI
- **Frontend**: Streamlit
- **Geographical Calculations**: Haversine formula for distance calculation
- **Mapping**: Folium for map visualization

## Prerequisites

- Python 3.7+
- Virtual environment setup (optional but recommended)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/bundelkhandi/dating_app
   cd dating_app
    ``` 
2. Create and activate a virtual environment:

    ```bash
    python -m venv env
    source env/bin/activate   # On Windows, use `env\Scripts\activate`
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```
 4. Running the Servers
    ```bash
    uvicorn main:app --reload
    ```
     This will start the FastAPI server at http://localhost:8000.

5. Run Streamlit App:

    ```bash
    streamlit run app.py
    ```
    This will start the Streamlit app in the browser, typically at http://localhost:8501.