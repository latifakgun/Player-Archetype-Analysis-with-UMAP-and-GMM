# EYEBALL-SCOUT - PLAYER ARCHETYPE ANALYSIS
## **⚽ Eyeball Scout: AI-Driven Football Role Discovery**

Eyeball Scout is a personal data science project built to explore how Unsupervised Machine Learning can redefine traditional football analysis.

As a Statistics student passionate about football analytics, I created this tool to challenge the rigid "Forward, Midfielder, Defender" labels. By analyzing thousands of players from Europe's Top 5 leagues, this project clusters players based on their actual on-pitch behavior, discovering 17 distinct tactical archetypes (like "Progressive Defender" or "Deep-Lying Playmaker").

------

## **🎯 The Motivation (Why I Built This)**

Traditional positions often fail to tell the full story. Wayne Rooney wasn't just a striker; he was everywhere. Trent Alexander-Arnold is listed as a defender but plays like a playmaker.

My goal with Eyeball Scout was to:

    Apply advanced statistical methods (UMAP, GMM) to real-world sports data.

    Build an interactive web application using Python & Streamlit.

    Create a "style-based" scouting system rather than a "position-based" one.

This project is open-source and intended for educational purposes.

------

## **⚙️ How It Works (The Methodology)**

To ensure the AI identifies playing styles correctly, I designed a specific pipeline:

    Divide & Conquer: I trained separate models for Defenders, Midfielders, and Attackers to avoid comparing a Goalkeeper to a Striker.

    Feature Weighting: I applied custom domain-knowledge weights (e.g., giving more importance to 'Aerial Duels' for Center Backs).

    L2 Normalization: I normalized the data to focus on the shape of a player's stats (style) rather than just the volume (how much they played).

    3D Clustering: Using UMAP for dimensionality reduction and Gaussian Mixture Models (GMM) for clustering, I mapped players into a 3D space where distance equals similarity.

------

## **✨ Features**

    🌍 3D Exploration: An interactive 3D playground to see how players group together.

    ⚔️ Player Comparison: Compare any two players visually to see if their playstyles overlap, regardless of their nominal position.

    🏆 AI Role Assignment: The model assigns a specific role (e.g., Target Man) and a "Confidence Score" to every player.

    🧬 Similarity Search: A "Nearest Neighbor" engine to find similar players (great for scouting replacements).

------

## **🛠️ Tech Stack**

This project was a great opportunity for me to practice the following technologies:

    Language: Python 3.10+

    Web App: Streamlit

    Machine Learning: UMAP, Scikit-learn (GMM, StandardScaler)

    Visualization: Plotly (3D & Polar Charts)

    Data Processing: Pandas, NumPy

------

## **🚀 Installation & Usage**

If you want to run my code on your local machine:

    Clone the repository:
    Bash

    git clone https://github.com/yourusername/eyeball-scout.git
    cd eyeball-scout

    Install dependencies:
    Bash

    pip install -r requirements.txt

    Run the app:
    Bash

    streamlit run app.py

------

## **🗺️ Future Improvements (To-Do)**

Since this is a hobby project, I plan to add these features as I learn more:

    [ ] Team Standings Integration: Analyzing if certain roles correlate with league titles.

    [ ] Temporal Analysis: Visualizing how a player's role changes over their career.

    [ ] Recommendation Engine: Suggesting players based on team squad needs.

*⭐ If you find this project interesting or useful for your own learning, leaving a star would mean a lot!*

------

## **⚖️ License**

This project is open-source under the MIT License. Feel free to use it for your own research or hobby projects!

*Built by Latif Akgün, Statistics Student & Football Analytics Enthusiast*
