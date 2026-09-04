import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# ------------------------
# Load Data
# ------------------------
@st.cache_data
def load_data():
 
df = pd.read_xlsx("cleaning data netflix")
    # إضمش موجود
    if "profit" not in df.columns:
        df["profit"] = df["Revenue"] - df["Budget"]
    return df

df = load_data()

# ------------------------
# Pages as functions
# ------------------------

def show_home():
    st.title("🎬 Movies Dashboard")

    # Top Movies Posters
    movie_posters = {
        "Avatar": "https://m.media-amazon.com/images/I/41kTVLeW1CL._AC_.jpg",
        "Avengers: Endgame": "https://m.media-amazon.com/images/I/81ExhpBEbHL._AC_SY679_.jpg",
        "Titanic": "https://m.media-amazon.com/images/I/71yAzBqCk7L._AC_SY679_.jpg",
        "The Dark Knight": "https://m.media-amazon.com/images/I/51EbJjlLg9L._AC_.jpg",
        "Inception": "https://m.media-amazon.com/images/I/5101m7V0scL._AC_.jpg"
    }

    st.header("🔥 Top 5 Movies by Popularity")
    cols = st.columns(5)
    for i, (movie, url) in enumerate(movie_posters.items()):
        with cols[i]:
            try:
                st.image(url, caption=movie, use_container_width=True)
            except:
                st.error(f"Could not load image for {movie}")

    # Top Actors
    actor_images = {
        "Robert Downey Jr.": "https://upload.wikimedia.org/wikipedia/commons/5/50/Robert_Downey_Jr_2014_Comic_Con_%28cropped%29.jpg",
        "Scarlett Johansson": "https://upload.wikimedia.org/wikipedia/commons/2/20/Scarlett_Johansson_in_Kuwait_01b-tweaked.jpg",
        "Tom Hanks": "https://upload.wikimedia.org/wikipedia/commons/9/96/Tom_Hanks_2016.jpg",
        "Leonardo DiCaprio": "https://upload.wikimedia.org/wikipedia/commons/8/8f/Leonardo_DiCaprio_66ème_Festival_de_Venise_%28Mostra%29.jpg",
        "Sylvester Stallone": "https://upload.wikimedia.org/wikipedia/commons/0/0d/Sylvester_Stallone_by_Gage_Skidmore_2.jpg"
    }

    st.header("⭐ Top 5 Actors")
    cols = st.columns(5)
    for i, (actor, url) in enumerate(actor_images.items()):
        with cols[i]:
            try:
                st.image(url, caption=actor, use_container_width=True)
            except:
                st.error(f"Could not load image for {actor}")

def show_general_analysis():
    st.title("📊 General Analysis")

    # Tabs for 18 Visualizations
    tabs = st.tabs([
        "Movies per Year", "Top Actors", "Top Genres", "Budget vs Revenue",
        "Profit by Genre", "Top 10 Movies by Profit", "Runtime Distribution",
        "Popularity vs Rating_Count", "Movies by Country", "Movies by Language",
        "Revenue by Company", "Revenue by Country", "Rating Distribution",
        "Top Directors", "Budget Trend", "Revenue Trend",
        "Genre Popularity Over Time", "WordCloud Genres"
    ])

    # 1. Movies per Year
    with tabs[0]:
        df["Release_Year"] = pd.to_datetime(df["Release_Date"], errors="coerce").dt.year
        yearly = df.groupby("Release_Year").size().reset_index(name="Count")
        fig = px.line(yearly, x="Release_Year", y="Count", title="Number of Movies per Year")
        st.plotly_chart(fig, use_container_width=True)

    # 2. Top Actors
    with tabs[1]:
        top_actors = df["Main_actor"].value_counts().head(10)
        fig = px.bar(top_actors, x=top_actors.index, y=top_actors.values, title="Top 10 Actors by Movies Count")
        st.plotly_chart(fig, use_container_width=True)

    # 3. Top Genres
    with tabs[2]:
        top_genres = df["Genres"].value_counts().head(10)
        fig = px.bar(top_genres, x=top_genres.index, y=top_genres.values, title="Top 10 Genres")
        st.plotly_chart(fig, use_container_width=True)

    # 4. Budget vs Revenue
    with tabs[3]:
        fig = px.scatter(df, x="Budget", y="Revenue", size="Popularity", color="Genres",
                         hover_data=["Title"], title="Budget vs Revenue")
        st.plotly_chart(fig, use_container_width=True)

    # 5. Profit by Genre
    with tabs[4]:
        fig = px.bar(df.groupby("Genres")["profit"].mean().reset_index(),
                     x="Genres", y="profit", title="Average Profit by Genre")
        st.plotly_chart(fig, use_container_width=True)

    # 6. Top 10 Movies by Profit
    with tabs[5]:
        fig = px.bar(df.sort_values("profit", ascending=False).head(10),
                     x="Title", y="profit", title="Top 10 Movies by Profit")
        st.plotly_chart(fig, use_container_width=True)

    # 7. Runtime Distribution
    with tabs[6]:
        fig = px.histogram(df, x="Runtime", nbins=30, title="Runtime Distribution")
        st.plotly_chart(fig, use_container_width=True)

    # 8. Popularity vs Rating_Count
    with tabs[7]:
        fig = px.scatter(df, x="Popularity", y="Rating_Count", color="Genres", hover_data=["Title"],
                         title="Popularity vs Rating Count")
        st.plotly_chart(fig, use_container_width=True)

    # 9. Movies by Country
    with tabs[8]:
        country_count = df["Country_of_Origin"].value_counts().reset_index()
        country_count.columns = ["Country", "Count"]
        fig = px.choropleth(country_count, locations="Country", locationmode="country names",
                            color="Count", projection="natural earth",
                            title="Movies by Country of Origin")
        st.plotly_chart(fig, use_container_width=True)

    # 10. Movies by Language
    with tabs[9]:
        lang_count = df["Original_Language"].value_counts().head(10)
        fig = px.pie(values=lang_count.values, names=lang_count.index, title="Movies by Language")
        st.plotly_chart(fig, use_container_width=True)

    # 11. Revenue by Company
    with tabs[10]:
        top_companies = df.groupby("Production_Companies")["Revenue"].sum().sort_values(ascending=False).head(10)
        fig = px.bar(top_companies, x=top_companies.index, y=top_companies.values, title="Top Companies by Revenue")
        st.plotly_chart(fig, use_container_width=True)

    # 12. Revenue by Country
    with tabs[11]:
        top_countries = df.groupby("Country_of_Origin")["Revenue"].sum().sort_values(ascending=False).head(10)
        fig = px.bar(top_countries, x=top_countries.index, y=top_countries.values, title="Top Countries by Revenue")
        st.plotly_chart(fig, use_container_width=True)

    # 13. Rating Distribution
    with tabs[12]:
        fig = px.histogram(df, x="Rating_Count", nbins=30, title="Rating Count Distribution")
        st.plotly_chart(fig, use_container_width=True)

    # 14. Top Directors
    with tabs[13]:
        if "Director" in df.columns:
            top_directors = df["Director"].value_counts().head(10)
            fig = px.bar(top_directors, x=top_directors.index, y=top_directors.values, title="Top Directors")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No 'Director' column in data")

    # 15. Budget Trend
    with tabs[14]:
        yearly_budget = df.groupby("Release_Year")["Budget"].mean().reset_index()
        fig = px.line(yearly_budget, x="Release_Year", y="Budget", title="Average Budget over Years")
        st.plotly_chart(fig, use_container_width=True)

    # 16. Revenue Trend
    with tabs[15]:
        yearly_revenue = df.groupby("Release_Year")["Revenue"].mean().reset_index()
        fig = px.line(yearly_revenue, x="Release_Year", y="Revenue", title="Average Revenue over Years")
        st.plotly_chart(fig, use_container_width=True)

    # 17. Genre Popularity Over Time
    with tabs[16]:
        genre_year = df.groupby(["Release_Year", "Genres"]).size().reset_index(name="Count")
        fig = px.line(genre_year, x="Release_Year", y="Count", color="Genres", title="Genre Popularity Over Time")
        st.plotly_chart(fig, use_container_width=True)

    # 18. WordCloud Genres
    with tabs[17]:
        text = " ".join(df["Genres"].dropna().astype(str))
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)

        fig, ax = plt.subplots(figsize=(10,5))
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)

def show_interactive_analysis():
    st.title("🎛️ Interactive Analysis")

    # Filters
    actors = st.multiselect("Select Actor(s)", options=df["Main_actor"].dropna().unique())
    genres = st.multiselect("Select Genre(s)", options=df["Genres"].dropna().unique())
    languages = st.multiselect("Select Language(s)", options=df["Original_Language"].dropna().unique())
    companies = st.multiselect("Select Company(s)", options=df["Production_Companies"].dropna().unique())

    filtered_df = df.copy()
    if actors:
        filtered_df = filtered_df[filtered_df["Main_actor"].isin(actors)]
    if genres:
        filtered_df = filtered_df[filtered_df["Genres"].isin(genres)]
    if languages:
        filtered_df = filtered_df[filtered_df["Original_Language"].isin(languages)]
    if companies:
        filtered_df = filtered_df[filtered_df["Production_Companies"].isin(companies)]

    st.write(f"📊 Showing {len(filtered_df)} movies after filtering")

    if not filtered_df.empty:
        fig = px.scatter(filtered_df, x="Budget", y="Revenue", size="Popularity", color="Genres",
                         hover_data=["Title"], title="Budget vs Revenue (Filtered)")
        st.plotly_chart(fig, use_container_width=True)

        fig = px.bar(filtered_df.sort_values("profit", ascending=False).head(10),
                     x="Title", y="profit", title="Top 10 Movies by Profit (Filtered)")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No movies found for selected filters.")

# ------------------------
# Sidebar for Navigation
# ------------------------
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Go to", ["Home", "General Analysis", "Interactive Analysis"])

if page == "Home":
    show_home()
elif page == "General Analysis":
    show_general_analysis()
elif page == "Interactive Analysis":
    show_interactive_analysis()
