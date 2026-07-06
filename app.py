import streamlit as st
import pandas as pd 
st.set_page_config(
    page_title="Student Compass",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="auto"
)
st.title(':blue[_Student Compass_]', text_alignment = 'center')
st.subheader("Find courses, competitions, volunteering and research opportunities", divider="gray", text_alignment = 'center')
sheet_id = "158o1hH__S18hUX1qHfGiTkJiRxOWZQd84ALYvGzLghM"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
df = pd.read_csv(url)
search = st.text_input('Search')

def create_filter(text, column, variants):
    selected = st.sidebar.multiselect(
        text,
        variants
    )
    if selected == []:
        mask_selected = column == column
    else:
        mask_selected = column.isin(selected)
    return mask_selected

mask_difficulty = create_filter(
    "What is your level?",
    df["difficulty"],
    ["beginner", "intermediate", "advanced"]
)
mask_cost = create_filter(
    "What is the cost?",
    df["cost"],
    ["free", "paid", "mixed"]
)
mask_category = create_filter(
    "What is the category?",
    df["category"],
    ["competition", "course", "summer_program", "extracurricular", "research", "volunteering", "tutoring"]
)

mask_title = df['title'].str.contains(search, case=False, regex = False)
mask_description = df['description'].str.contains(search, case=False, regex = False)
mask_tags = df['tags'].str.contains(search, case=False, regex = False)
mask_search = mask_title | mask_description | mask_tags
final_mask = mask_difficulty & mask_search & mask_cost & mask_category
results = df[final_mask]



for _, row in results.iterrows():
     core_info = f"🏷 {row['category']} • 📚 {row['field']} • 🟢 {row['difficulty']}"
     access_info = f"💰 {row['cost']} • 🌍 {row['country']}"
     with st.container(border = True):
        st.subheader(row["title"])
        st.write(row["description"])
        st.write(core_info)
        st.write(access_info)
        st.link_button("🌐 Visit resource", row["url"])