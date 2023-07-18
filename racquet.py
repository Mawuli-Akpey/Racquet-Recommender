# Import necessary libraries
import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Load the dataset
df = pd.read_csv("final.csv")

# Parse numerical data from the string columns
df['Head Size:'] = df['Head Size:'].str.extract('(\d+.\d+) cm').astype(float)
df['Length:'] = df['Length:'].str.extract('(\d+.\d+)cm').astype(float)
df['Strung Weight:'] = df['Strung Weight:'].str.extract('(\d+.\d+)g').astype(float)
df['Swingweight:'] = pd.to_numeric(df['Swingweight:'], errors='coerce')
df['Stiffness:'] = pd.to_numeric(df['Stiffness:'], errors='coerce')

# Define mappings
power_level_mapping = {
    'Low': 1.0,
    'Low-Medium': 2.0,
    'Medium': 3.0,
    'Medium-High': 4.0,
    'High': 5.0
}

racquet_type_mapping = {
    'All Around Racquets': 1.0,
    "Traditional Player's Racquets": 2.0,
    'Spin Racquets': 3.0,
    'Power Racquets': 4.0
}

stroke_style_mapping = {
    'Compact': 1.0,
    'Compact-Medium': 2.0,
    'Medium': 3.0,
    'Medium-Full': 4.0,
    'Full': 5.0
}

composition_mapping = {category: i for i, category in enumerate(df_selected['Composition:'].unique())}

# Apply mappings
df['Power Level:'] = df['Power Level:'].map(power_level_mapping)
df['Racquet Type'] = df['Racquet Type'].map(racquet_type_mapping)
df['Stroke Style:'] = df['Stroke Style:'].map(stroke_style_mapping)
df['Composition:'] = df['Composition:'].map(composition_mapping)

# Define function to recommend racquets
def recommend_racquets(user_preferences, df, N=5):
    # Create a DataFrame with user preferences
    user_df = pd.DataFrame(user_preferences, index=[0])

    # Fill missing values with mean
    df_filled = df.fillna(df.mean())
    user_df_filled = user_df.fillna(user_df.mean())

    # Compute cosine similarity between user preferences and racquets
    similarity_scores = cosine_similarity(user_df_filled, df_filled)

    # Get indices of top N racquets
    top_racquet_indices = similarity_scores[0].argsort()[-N:][::-1]

    # Return these racquets
    return top_racquet_indices

# Streamlit interface
st.title('Tennis Racquet Recommendation System')

# User input
st.sidebar.header('User Input Preferences')
head_size = st.sidebar.slider('Head Size (in sq. cm):', float(df['Head Size:'].min()), float(df['Head Size:'].max()))
length = st.sidebar.slider('Length (in cm):', float(df['Length:'].min()), float(df['Length:'].max()))
strung_weight = st.sidebar.slider('Strung Weight (in g):', float(df['Strung Weight:'].min()), float(df['Strung Weight:'].max()))
swingweight = st.sidebar.slider('Swingweight:', float(df['Swingweight:'].min()), float(df['Swingweight:'].max()))
stiffness = st.sidebar.slider('Stiffness:', float(df['Stiffness:'].min()), float(df['Stiffness:'].max()))
price = st.sidebar.slider('Price (in $):', float(df['Price'].min()), float(df['Price'].max()))
racquet_type = st.sidebar.selectbox('Racquet Type:', list(racquet_type_mapping.keys()))
composition = st.sidebar.selectbox('Composition:', list(composition_mapping.keys()))
power_level = st.sidebar.selectbox('Power Level:', list(power_level_mapping.keys()))
stroke_style = st.sidebar.selectbox('Stroke Style:', list(stroke_style_mapping.keys()))

user_preferences = {
    "Head Size:": head_size, 
    "Length:": length, 
    "Strung Weight:": strung_weight, 
    "Swingweight:": swingweight, 
    "Stiffness:": stiffness, 
    "Price": price, 
    "Racquet Type": racquet_type_mapping[racquet_type],
    "Composition:": composition_mapping[composition], 
    "Power Level:": power_level_mapping[power_level], 
    "Stroke Style:": stroke_style
