import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
import math

st.title("Dating App User Fetcher")

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (math.sin(d_lat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         (math.sin(d_lon / 2) ** 2))
    c = 2 * math.asin(math.sqrt(a))
    return R * c

num_users = st.number_input("Enter number of users to scrape", min_value=1)

if st.button("Submit"):
    response = requests.post(f"http://localhost:8000/users/?num_users={num_users}")
    if response.ok:
        st.success(f"Fetched {num_users} users!")
    else:
        st.error("Failed to fetch users.")

if 'random_user' not in st.session_state:
    st.session_state.random_user = None
if 'user_map' not in st.session_state:
    st.session_state.user_map = None

if st.button("Get Random User"):
    response = requests.get("http://localhost:8000/users/random/")
    if response.ok:
        st.session_state.random_user = response.json()
        st.write("Random User Details:")
        st.write(f"UID: {st.session_state.random_user['uid']}")
        st.write(f"Email: {st.session_state.random_user['email']}")
        st.write(f"First Name: {st.session_state.random_user['first_name']}")
        st.write(f"Last Name: {st.session_state.random_user['last_name']}")
        st.write(f"Gender: {st.session_state.random_user['gender']}")
        st.write(f"Latitude: {st.session_state.random_user['latitude']}")
        st.write(f"Longitude: {st.session_state.random_user['longitude']}")
        st.write(f"Run ID: {st.session_state.random_user['run_id']}")
        st.write(f"DateTime: {st.session_state.random_user['datetime']}")
    else:
        st.error("Failed to get random user.")

uid = st.session_state.random_user['uid'] if st.session_state.random_user else ""
count = st.number_input("Number of nearest users to fetch", min_value=1)

if st.button("Get Nearest Users"):
    if st.session_state.random_user is not None:  
        response = requests.get(f"http://localhost:8000/users/nearest/{uid}/{count}")
        if response.ok:
            nearest_users = response.json()
            st.write("Nearest Users:")
            user_locations = []

            random_user_lat = st.session_state.random_user['latitude']
            random_user_lon = st.session_state.random_user['longitude']
            user_locations.append({"name": "Random User", "latitude": random_user_lat, "longitude": random_user_lon, "color": "red"})

            for user in nearest_users:
                distance = calculate_distance(random_user_lat, random_user_lon, user['latitude'], user['longitude'])
                compatibility_score = user['compatibility_score']  
                st.write(f"UID: {user['uid']}, First Name: {user['first_name']}, Distance: {distance:.2f} km, Compatibility Score: {compatibility_score}")
                user_locations.append({"name": f"{user['first_name']} {user['last_name']} - Score: {compatibility_score}", "latitude": user['latitude'], "longitude": user['longitude'], "color": "blue"})

            user_map = folium.Map(location=[random_user_lat, random_user_lon], zoom_start=5)
            for user in user_locations:
                folium.Marker(location=[user["latitude"], user["longitude"]], 
                              popup=user["name"], 
                              icon=folium.Icon(color=user["color"])).add_to(user_map)

            st.session_state.user_map = user_map

if st.session_state.user_map is not None:
    st_folium(st.session_state.user_map, width=700, height=500)
