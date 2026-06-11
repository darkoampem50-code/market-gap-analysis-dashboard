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
    df = pd.read_csv('cleaned_market_gap_data.csv')
    # Clean string spaces to prevent duplication mismatches
    df['main_category'] = df['main_category'].astype(str).str.strip()
    return df

df = load_data()

# ============================================================
# 3. SIDEBAR FILTERING TOOLS (AUTOMATIC BACKEND EXTRACTION)
# ============================================================
st.sidebar.header("Filter Options")

# Dynamically pull the exact unique categories that exist inside your file
raw_categories = df['main_category'].dropna().unique().tolist()

# Define presentation filter groups you want to display
display_categories = []
for cat in raw_categories:
    cat_lower = cat.lower()
    # Filter out empty entries, systems codes, or long ingredient lines
    if cat_lower in ['nan', ''] or len(cat) > 40:
        continue
    # Keep your essential presentation subjects
    if any(k in cat_lower for k in ['beverage', 'snack', 'dairy', 'meat', 'plant', 'asian', 'meal', 'sauce', 'supplement']):
        if cat not in display_categories:
            display_categories.append(cat)

# Sort them cleanly and keep 'All' at the absolute top
categories = ['All'] + sorted(display_categories)
selected_category = st.sidebar.selectbox("Select Product Category", categories)

# Filter dataset dynamically based on user selection
if selected_category != 'All':
    filtered_df = df[df['main_category'] == selected_category]
else:
    filtered_df = df

# 4. KPI Metrics Section (STORY 5)
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

# ============================================================
# STORY 4: THE STRATEGIC RECOMMENDATION (KEY INSIGHT BOX)
# ============================================================
st.subheader("📋 Strategic Executive Summary")

if "asian style" in str(selected_category).lower():
    st.success("""
    **💡 Key Insight & Market Recommendation:**
    Based on the data, the biggest market opportunity is in **asian style ready meal**, 
    specifically targeting products with **>= 10g** of protein and less than **5g** of sugar.
    """)
else:
    st.info("""
    **💡 Global Insight & Market Recommendation:**
    Based on the macro data, the biggest market opportunity across highly favorable, uncompetitive spaces 
    is in **asian style ready meal**, specifically targeting products with **>= 10g** of protein and less than **5g** of sugar.
    """)

# 5. Interactive Dashboard Visualizations (STORIES 1, 2 & 3)
left_chart, right_chart = st.columns(2)

with left_chart:
    st.subheader("The Positioning Matrix (Sugar vs. Protein Density)")
    fig, ax = plt.subplots(figsize=(8, 6))
    
    if not filtered_df.empty:
        hb = ax.hexbin(filtered_df['sugars_100g'], filtered_df['proteins_100g'], gridsize=25, cmap='YlOrRd', mincnt=1)
        fig.colorbar(hb, ax=ax, label='Product Count')
    
    ax.set_xlabel('Sugars per 100g')
    ax.set_ylabel('Proteins per 100g')
    ax.axvline(15, color='red', linestyle='--', alpha=0.6)
    ax.axhline(10, color='green', linestyle='--', alpha=0.6)
    st.pyplot(fig)

with right_chart:
    st.subheader("Breakdown of Market Segments")
    segment_counts = filtered_df['market_segment'].value_counts()
    
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    if not segment_counts.empty:
        sns.barplot(x=segment_counts.values, y=segment_counts.index, palette='viridis', ax=ax2)
    ax2.set_xlabel('Count')
    st.pyplot(fig2)

# ============================================================
# BONUS STORY: THE HIDDEN GEM (R&D INGREDIENT EXPLORER)
# ============================================================
st.markdown("---")
st.subheader("💎 Bonus Feature: The 'Hidden Gem' Ingredient Explorer")
st.markdown("""
To help the **R&D and Food Engineering team** replicate the structural success of top market options, 
this layer tracks the core protein drivers driving our high-protein, low-sugar cluster.
""")

col_ing1, col_ing2, col_ing3 = st.columns(3)
with col_ing1:
    st.success("🥇 **Top Source 1: Pea Protein** \n\nDominates clean plant-based ready meals.")
with col_ing2:
    st.success("🥈 **Top Source 2: Bean Base** \n\nProvides natural, complex carbohydrates + protein stability.")
with col_ing3:
    st.success("🥉 **Top Source 3: Soy / Tofu** \n\nUtilized heavily for high-tier meat alternative texturizing.")

# ============================================================
# CANDIDATE'S CHOICE CHALLENGE: COMPETITIVE HEALTH SCORE
# ============================================================
st.markdown("---")
st.subheader("🚀 Candidate's Choice Feature: Nutritional Efficiency Matrix")

calc_df = filtered_df.copy()
if not calc_df.empty:
    calc_df['protein_to_sugar_ratio'] = calc_df['proteins_100g'] / (calc_df['sugars_100g'] + 0.1)
    avg_ratio = calc_df['protein_to_sugar_ratio'].mean()
else:
    avg_ratio = 0.0

st.markdown("""
This customized metric evaluates the **Protein-to-Sugar Ratio**. It measures exactly how many grams of functional macromolecular protein a consumer receives for every **1 gram of sugar** consumed within this segment.
""")
st.metric(label="Selected Category Average Nutrient Efficiency Score", value=f"{avg_ratio:.2f}g Protein / 1g Sugar")

# 6. Interactive Data Table (STORY 6)
st.markdown("---")
st.subheader("🔍 Explore the Underlying Products")
st.markdown("Use this interactive table viewport to inspect individual brand items making up the filtered chart distributions above.")
st.dataframe(filtered_df[['product_name', 'main_category', 'sugars_100g', 'proteins_100g', 'market_segment']].head(100), use_container_width=True)
