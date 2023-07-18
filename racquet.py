import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

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

# Define function to recommend racquets
def recommend_racquets(user_preferences, df, N=5):
    # Create a DataFrame with user preferences
    user_df = pd.DataFrame(user_preferences, index=[0])

    # Fill missing values with mean
    df_filled = df.copy()
    for col in df_filled.select_dtypes(include=np.number).columns:
        df_filled[col] = df_filled[col].fillna(df_filled[col].mean())
        
    user_df_filled = user_df.fillna(user_df.mean())

    # Compute cosine similarity between user preferences and racquets
    similarity_scores = cosine_similarity(user_df_filled, df_filled.select_dtypes(include=np.number))

    # Get indices of top N racquets
    top_racquet_indices = similarity_scores[0].argsort()[-N:][::-1]

    # Return these racquets
    return top_racquet_indices

# Load data
df = pd.read_csv('final.csv')

# Get unique values for mappings
composition_mapping = {category: i for i, category in enumerate(df['Composition:'].unique())}

# Apply mappings
df['Power Level:'] = df['Power Level:'].map(power_level_mapping)
df['Racquet Type'] = df['Racquet Type'].map(racquet_type_mapping)
df['Stroke Style:'] = df['Stroke Style:'].map(stroke_style_mapping)
df['Composition:'] = df['Composition:'].map(composition_mapping)

# Display title
st.title('Tennis Racquet Recommendation System')

# Get user input
head_size = st.slider("Head Size:", float(df["Head Size:"].min()), float(df["Head Size:"].max()))
length = st.slider("Length:", float(df["Length:"].min()), float(df["Length:"].max()))
strung_weight = st.slider("Strung Weight:", float(df["Strung Weight:"].min()), float(df["Strung Weight:"].max()))
swingweight = st.slider("Swingweight:", float(df["Swingweight:"].min()), float(df["Swingweight:"].max()))
stiffness = st.slider("Stiffness:", float(df["Stiffness:"].min()), float(df["Stiffness:"].max()))
price = st.slider("Price:", float(df["Price"].min()), float(df["Price"].max()))
racquet_type = st.selectbox('Racquet Type', list(racquet_type_mapping.keys()))
composition = st.selectbox('Composition:', list(df['Composition:'].unique()))
power_level = st.selectbox('Power Level:', list(power_level_mapping.keys()))
stroke_style = st.selectbox('Stroke Style:', list(stroke_style_mapping.keys()))

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
    "Stroke Style:": stroke_style_mapping[stroke_style]
}

# Get recommendations
recommendation_indices = recommend_racquets(user_preferences, df)
recommended_racquets = df.iloc[recommendation_indices][["Racquet Name", "URL"]]

# Display recommendations
st.header('Recommended Racquets:')
st.table(recommended_racquets)
