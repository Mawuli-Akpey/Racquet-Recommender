import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Define function to recommend racquets
def recommend_racquets(user_preferences, df, N=5):
    # Create a DataFrame with user preferences
    user_df = pd.DataFrame(user_preferences, index=[0])

    # Fill missing values with mean
    df_filled = df.fillna(df.mean())
    user_df_filled = user_df.fillna(df.mean())

    # Compute cosine similarity between user preferences and racquets
    similarity_scores = cosine_similarity(user_df_filled, df_filled)

    # Get indices of top N racquets
    top_racquet_indices = similarity_scores[0].argsort()[-N:][::-1]

    # Return these racquets
    return df.iloc[top_racquet_indices][["Racquet Name", "URL"]]

# Define mappings
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

power_level_mapping = {
    'Low': 1.0,
    'Low-Medium': 2.0,
    'Medium': 3.0,
    'Medium-High': 4.0,
    'High': 5.0
}

# Read data
df = pd.read_csv('final.csv')

# Define composition_mapping
composition_mapping = {category: i for i, category in enumerate(df['Composition:'].unique())}

# Get user input
numeric_columns = ["Head Size:", "Length:", "Strung Weight:", "Swingweight:", "Stiffness:", "Price"]
for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Replace the Streamlit user inputs with direct inputs
head_size = 100  # replace with your desired head size
length = 27  # replace with your desired length
strung_weight = 300  # replace with your desired strung weight
swingweight = 320  # replace with your desired swingweight
stiffness = 65  # replace with your desired stiffness
price = 200  # replace with your desired price
racquet_type = 'All Around Racquets'  # replace with your desired racquet type
composition = 'Graphite'  # replace with your desired composition
power_level = 'Medium'  # replace with your desired power level
stroke_style = 'Full'  # replace with your desired stroke style

user_preferences = {
    "Head Size:": head_size, 
    "Length:": length, 
    "Strung Weight:": strung_weight, 
    "Swingweight:": swingweight, 
    "Stiffness:": stiffness, 
    "Price": price, 
    "Racquet Type": racquet_type_mapping[racquet_type],
    "Composition:": composition_mapping.get(composition, np.nan), 
    "Power Level:": power_level_mapping[power_level], 
    "Stroke Style:": stroke_style_mapping[stroke_style]
}

# Get recommendations
recommended_racquets = recommend_racquets(user_preferences, df)

print(recommended_racquets)
