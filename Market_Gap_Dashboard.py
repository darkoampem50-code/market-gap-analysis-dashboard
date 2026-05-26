import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Page Layout Configuration
st.set_page_config(page_title="The Market Gap Analysis", layout="wide")

st.title("📊 The Market Gap Analysis: Sugar Traps vs. Nutritious Opportunities")
st.markdown("""
This interactive dashboard highlights where product categories are masquerading as healthy options 
but are secretly loaded with sugar (**Sugar Traps**), and where the actual **Market Goldmines** exist.
""")

# 2. Load the Cleaned Data
@st.cache_data
def load_data():
    return pd.read_csv('cleaned_market_gap_data.csv')

df = load_data()

# 3. Sidebar Filtering Tools
st.sidebar.header("Filter Options")

# Dropdown to filter by food categories
categories = ['All'] + list(df['main_category'].dropna().unique())
selected_category = st.sidebar.selectbox("Select Product Category", categories)

# Filter dataset dynamically based on user selection
if selected_category != 'All':
    filtered_df = df[df['main_category'] == selected_category]
else:
    filtered_df = df

# 4. KPI Metrics Section
st.subheader(f"Market Snapshot: {selected_category}")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Products Analyzed", f"{filtered_df.shape[0]:,}")
with col2:
    traps_count = filtered_df[filtered_df['market_segment'] == 'Sugar Trap (High Protein, High Sugar)'].shape[0]
    st.metric("Identified Sugar Traps 🚨", f"{traps_count:,}")
with col3:
    goldmine_count = filtered_df[filtered_df['market_segment'] == 'The Market Goldmine (Low Sugar, High Protein)'].shape[0]
    st.metric("Market Goldmines ✨", f"{goldmine_count:,}")

st.markdown("---")

# 5. Interactive Dashboard Visualizations
left_chart, right_chart = st.columns(2)

with left_chart:
    st.subheader("The Positioning Matrix (Sugar vs. Protein Density)")
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Dynamic Hexbin plot based on selection
    hb = ax.hexbin(filtered_df['sugars_100g'], filtered_df['proteins_100g'], gridsize=25, cmap='YlOrRd', mincnt=1)
    ax.set_xlabel('Sugars per 100g')
    ax.set_ylabel('Proteins per 100g')
    
    # Draw thresholds
    ax.axvline(15, color='red', linestyle='--', alpha=0.6)
    ax.axhline(10, color='green', linestyle='--', alpha=0.6)
    
    fig.colorbar(hb, ax=ax, label='Product Count')
    st.pyplot(fig)

with right_chart:
    st.subheader("Breakdown of Market Segments")
    segment_counts = filtered_df['market_segment'].value_counts()
    
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    sns.barplot(x=segment_counts.values, y=segment_counts.index, palette='viridis', ax=ax2)
    ax2.set_xlabel('Count')
    st.pyplot(fig2)

# 6. Interactive Data Table
st.subheader("Explore the Underlying Products")
st.dataframe(filtered_df[['product_name', 'main_category', 'sugars_100g', 'proteins_100g', 'market_segment']].head(100), use_container_width=True)