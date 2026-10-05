# 🎬 CineMatch — Movie Recommendation System

> A full-stack movie discovery and recommendation platform built with **Streamlit**, **FastAPI**, **Scikit-learn**, and **TMDB**.

CineMatch lets users search for movies, browse popular and curated categories, open detailed movie pages, and discover similar titles through **TF-IDF-based recommendations** and **genre-based recommendations**.

The project is structured as a separate frontend and backend application so that the user interface, API layer, recommendation logic, external movie data, and deployment infrastructure remain independently manageable.

---

## 📌 Project Overview

CineMatch is designed around a simple user journey:

```text
Search / Browse
      ↓
Select a Movie
      ↓
View Movie Details
      ↓
Generate Recommendations
      ↓
Explore Similar Movies
```

The application combines:

- **TMDB** for movie metadata, posters, backdrops, search results, and catalog categories.
- **FastAPI** as the backend/API layer.
- **Streamlit** as the interactive frontend.
- **TF-IDF + similarity matching** for text-based recommendations.
- **Genre-based matching** as a second recommendation strategy.
- **Render** for backend deployment.

---

# ✨ Key Features

## 🎥 Movie Discovery

- Search movies by title or keyword.
- Search suggestions with movie titles and release years.
- Browse movies through predefined categories.
- Display posters in a configurable grid.
- Open any movie to view its details.

### Available Home Categories

| Category | Description |
|---|---|
| 🔥 Trending | Currently trending movies |
| ⭐ Popular | Popular movies |
| 🏆 Top Rated | Highly rated movies |
| 🎞️ Now Playing | Movies currently playing |
| 🗓️ Upcoming | Upcoming movie releases |

---

## 🔎 Movie Search

The frontend sends the search query to the FastAPI backend:

```text
User enters keyword
        ↓
Streamlit
        ↓
GET /tmdb/search
        ↓
TMDB search data
        ↓
Result parsing
        ↓
Suggestions + Movie Cards
```

The frontend supports multiple API response formats and converts them into a consistent internal movie-card structure.

---

## 📄 Movie Details

When a user selects a movie, CineMatch opens a dedicated details view.

The page can display:

- Movie title
- Release date
- Genres
- Movie overview
- Poster
- Backdrop
- Recommendation sections

The frontend requests movie details using:

```http
GET /movie/id/{tmdb_id}
```

---

# 🤖 Recommendation Engine

CineMatch currently uses two recommendation approaches.

## 1. TF-IDF Based Recommendation

The project uses **TF-IDF (Term Frequency-Inverse Document Frequency)** to represent movie text as numerical vectors.

The basic pipeline is:

```text
Movie Metadata
      ↓
Text Representation
      ↓
TF-IDF Vectorization
      ↓
Movie Feature Vectors
      ↓
Similarity Comparison
      ↓
Top Similar Movies
```

The project stores the trained/reusable recommendation artifacts in the `models/` directory.

### Stored Model Artifacts

```text
models/
├── indices.pkl
├── movies_df.pkl
├── tfidf_matrix.pkl
└── tfidf_vectorizer.pkl
```

These files allow the recommendation system to reuse previously prepared data and TF-IDF representations instead of rebuilding them for every user request.

---

## 2. Genre-Based Recommendation

CineMatch also provides recommendations based on movie genres.

```text
Selected Movie
      ↓
Movie Genres
      ↓
Genre Matching
      ↓
Candidate Movies
      ↓
Recommended Movies
```

This acts as a complementary recommendation strategy and can also be used as a fallback when the combined recommendation request does not return usable results.

---

# 🏗️ System Architecture

CineMatch follows a decoupled frontend/backend architecture.

```text
                         ┌─────────────────────┐
                         │       User          │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Streamlit Frontend  │
                         │       aap.py        │
                         └──────────┬──────────┘
                                    │ HTTP Requests
                                    ▼
                         ┌─────────────────────┐
                         │    FastAPI API      │
                         │       main.py       │
                         └───────┬───────┬─────┘
                                 │       │
                     ┌───────────┘       └────────────┐
                     ▼                                ▼
          ┌───────────────────┐             ┌──────────────────┐
          │ Recommendation    │             │      TMDB        │
          │ Engine            │             │       API        │
          │                   │             │                  │
          │ • TF-IDF          │             │ • Search         │
          │ • Genre Matching  │             │ • Details        │
          │                   │             │ • Categories     │
          └─────────┬─────────┘             └──────────────────┘
                    │
                    ▼
          ┌───────────────────┐
          │ Model Artifacts   │
          │                   │
          │ TF-IDF Matrix     │
          │ Vectorizer        │
          │ Movie Data        │
          │ Indices            │
          └───────────────────┘
```

---

# 🔄 Complete Application Flow

## Home Feed Flow

```text
User opens CineMatch
        ↓
Streamlit loads sidebar
        ↓
User selects category
        ↓
GET /home
        ↓
FastAPI processes request
        ↓
Movie data is returned
        ↓
Streamlit creates poster grid
        ↓
User selects a movie
```

---

## Search Flow

```text
User enters movie keyword
        ↓
Streamlit sends:
GET /tmdb/search?query=<keyword>
        ↓
FastAPI / TMDB search
        ↓
Search response
        ↓
Frontend normalizes response
        ↓
Suggestions displayed
        ↓
User selects movie
        ↓
Movie details page
```

---

## Recommendation Flow

```text
Movie Details
      ↓
Movie Title
      ↓
GET /movie/search
      ↓
┌───────────────────────────────┐
│ Recommendation Bundle         │
│                               │
│ TF-IDF Recommendations        │
│ Genre Recommendations         │
└───────────────┬───────────────┘
                ↓
       Two recommendation tabs
                ↓
      Similar Movies / More Like This
```

---

# 🔌 Backend API

The Streamlit frontend communicates with the FastAPI backend through HTTP requests.

## API Base URL

The deployed frontend is configured to communicate with the deployed backend:

```text
https://movie-recommendation-1-aey1.onrender.com
```

For local development, the backend can be run on:

```text
http://127.0.0.1:8000
```

---

## API Endpoints Used by the Frontend

### 1. Home Feed

```http
GET /home
```

Parameters:

```text
category
limit
```

Example:

```text
/home?category=popular&limit=24
```

Supported categories:

```text
trending
popular
top_rated
now_playing
upcoming
```

---

### 2. TMDB Search

```http
GET /tmdb/search
```

Parameter:

```text
query
```

Example:

```text
/tmdb/search?query=batman
```

Used by the frontend to obtain movie search results and suggestions.

---

### 3. Movie Details

```http
GET /movie/id/{tmdb_id}
```

Example:

```text
/movie/id/550
```

Returns the movie information required by the details page.

---

### 4. Combined Movie Recommendations

```http
GET /movie/search
```

Parameters used by the frontend:

```text
query
tfidf_top_n
genre_limit
```

Example:

```text
/movie/search?query=Inception&tfidf_top_n=12&genre_limit=12
```

The frontend expects recommendation groups including:

```text
tfidf_recommendations
genre_recommendations
```

---

### 5. Genre Recommendation

```http
GET /recommend/genre
```

Parameters:

```text
tmdb_id
limit
```

Example:

```text
/recommend/genre?tmdb_id=550&limit=18
```

This endpoint is used as a fallback recommendation source.

---

# 🖥️ Frontend Architecture

The Streamlit application is implemented primarily in:

```text
aap.py
```

The frontend contains several logical layers.

```text
aap.py
│
├── Configuration
│
├── Streamlit Page Configuration
│
├── Global UI / CSS Theme
│
├── Session State & Routing
│
├── UI Helper Functions
│
├── API Helper Functions
│
├── Movie Search Parsing
│
├── Poster Grid
│
├── Sidebar
│
├── Home View
│
└── Details View
```

---

## Session-Based Routing

CineMatch uses Streamlit session state to maintain the current view.

```text
view
├── home
└── details
```

The selected TMDB movie ID is maintained through:

```text
selected_tmdb_id
```

The application also uses query parameters for movie detail navigation.

Example:

```text
?view=details&id=<tmdb_id>
```

This allows a selected movie to be represented directly in the URL.

---

# 🎨 UI / UX

CineMatch uses a custom dark cinematic theme.

### Design Characteristics

- Dark background
- Pink and purple accent colors
- Rounded cards
- Movie poster hover effects
- Cinematic hero sections
- Responsive poster grid
- Dark selectboxes
- Interactive buttons
- Movie genre chips
- Backdrop-based movie headers

### Main UI Sections

```text
┌─────────────────────────────────────────────┐
│                 CineMatch                   │
│         Movie Discovery Platform            │
├─────────────────────────────────────────────┤
│ Search                                      │
│ [ Search by movie title... ]                │
├─────────────────────────────────────────────┤
│ Category / Feed                             │
│                                             │
│ Poster  Poster  Poster  Poster  Poster      │
│ Poster  Poster  Poster  Poster  Poster      │
├─────────────────────────────────────────────┤
│ Recommendations                            │
└─────────────────────────────────────────────┘
```

---

# 📁 Project Structure

```text
Movie_Recommender/
│
├── aap.py
│   └── Streamlit frontend
│
├── main.py
│   └── FastAPI backend
│
├── requirement.txt
│   └── Python dependencies
│
├── pyproject.toml
│   └── Project metadata / Python configuration
│
├── .python-version
│   └── Python runtime version
│
├── .env
│   └── Local environment variables
│
├── .gitignore
│   └── Git exclusions
│
├── README.md
│   └── Project documentation
│
├── data/
│   └── movies_metadata.csv
│       └── Movie dataset
│
├── models/
│   ├── indices.pkl
│   ├── movies_df.pkl
│   ├── tfidf_matrix.pkl
│   └── tfidf_vectorizer.pkl
│
└── .streamlit/
    └── config.toml
        └── Streamlit theme configuration
```

---

# 🧰 Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| Frontend | Streamlit | Interactive web interface |
| Backend | FastAPI | REST API |
| Server | Uvicorn | ASGI server |
| ML | Scikit-learn | TF-IDF / similarity processing |
| Data | Pandas | Movie data processing |
| Numerical Computing | NumPy | Numerical operations |
| Scientific Computing | SciPy | Supporting scientific operations |
| HTTP | Requests / HTTPX | API communication |
| Movie Data | TMDB | Movie metadata and images |
| Styling | HTML / CSS | Cinematic UI |
| Deployment | Render | Backend hosting |

---

# 🧪 Local Development

## Prerequisites

Make sure the following are installed:

- Python 3.13
- Git
- VS Code or another Python IDE
- TMDB API credentials

---

## 1. Clone the Repository

```bash
git clone https://github.com/NEERAJ-C-cy/Movie_Recommender.git
cd Movie_Recommender
```

---

## 2. Create Virtual Environment

Windows:

```powershell
python -m venv .venv
```

Activate:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate again:

```powershell
.\.venv\Scripts\Activate.ps1
```

---

## 3. Install Dependencies

```bash
pip install -r requirement.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file:

```env
TMDB_API_KEY=your_tmdb_api_key
```

Do not commit `.env` to GitHub.

---

# ▶️ Run the Application

## Start FastAPI Backend

```bash
uvicorn main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Start Streamlit Frontend

Open a second terminal.

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Run:

```bash
streamlit run aap.py
```

The Streamlit application will then be available through the local URL shown in the terminal.

---

# ☁️ Deployment

CineMatch separates deployment into frontend and backend responsibilities.

## Backend — Render

The FastAPI backend can be deployed on Render.

### Build Command

```bash
pip install -r requirement.txt
```

### Start Command

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

The deployed backend currently used by the frontend is:

```text
https://movie-recommendation-1-aey1.onrender.com
```

---

## Python Runtime

The project uses Python 3.13 for deployment compatibility.

The repository includes:

```text
.python-version
```

with the selected Python runtime.

This is important because scientific Python packages such as NumPy, SciPy, and Scikit-learn need compatible pre-built wheels for the deployment runtime.

---

# 🔐 Environment & Security

Sensitive credentials should never be committed to Git.

### Recommended `.gitignore`

```gitignore
.venv/
__pycache__/
*.pyc
.env
.streamlit/secrets.toml
```

### Never commit

```text
TMDB_API_KEY
.env
API credentials
private deployment credentials
```

Use environment variables for secrets.

---

# ⚡ Performance Considerations

The frontend uses Streamlit caching for short-lived API responses.

The API helper uses:

```python
@st.cache_data(ttl=30)
```

This reduces repeated API requests during short interactions such as movie searching.

The recommendation artifacts are also stored as reusable files:

```text
tfidf_matrix.pkl
tfidf_vectorizer.pkl
movies_df.pkl
indices.pkl
```

This avoids unnecessarily rebuilding the recommendation representation for every request.

---

# 🛡️ Error Handling

The frontend API helper handles:

- HTTP errors
- Request failures
- Invalid responses
- Missing recommendation data
- Missing movie posters
- Missing movie details
- Empty search results

The application displays user-friendly messages such as:

```text
Search failed
Home feed failed
Could not load details
No recommendations available
```

Instead of exposing raw application failures directly to the user.

---

# 🔁 Recommendation Fallback

CineMatch does not depend on only one recommendation strategy.

The recommendation flow is:

```text
Request Recommendations
        ↓
Combined Recommendation Endpoint
        ↓
TF-IDF + Genre Results
        ↓
        ├── TF-IDF available
        │       ↓
        │   Show similar movies
        │
        └── Request unavailable / failed
                ↓
          Genre Recommendation
                ↓
          Show fallback results
```

This makes the recommendation experience more resilient.

---

# 📊 Data & Model Artifacts

The project contains reusable recommendation artifacts.

| File | Role |
|---|---|
| `movies_df.pkl` | Stored movie dataframe |
| `tfidf_vectorizer.pkl` | TF-IDF vectorizer |
| `tfidf_matrix.pkl` | TF-IDF feature matrix |
| `indices.pkl` | Movie/index mapping |

The original movie dataset is stored under:

```text
data/movies_metadata.csv
```

---

# 🧩 Design Decisions

## Why FastAPI?

FastAPI provides a lightweight API layer between the UI and recommendation/data services.

Benefits:

- Clear API boundaries
- Easy local development
- Automatic API documentation
- Good integration with Python ML code
- Independent frontend/backend deployment

---

## Why Streamlit?

Streamlit allows the recommendation system to be exposed through an interactive UI without requiring a separate JavaScript frontend.

It is used for:

- Search
- Category navigation
- Movie cards
- Details pages
- Recommendation tabs
- Interactive controls

---

## Why TF-IDF?

TF-IDF provides a simple and explainable way to represent movie text and compare titles based on their textual characteristics.

It is computationally practical for a portfolio-scale recommendation system and provides a useful baseline for content-based recommendations.

---

## Why a Hybrid Recommendation Experience?

Using both TF-IDF and genre-based recommendations gives the application more than one way to find related movies.

```text
Text Similarity
       +
Genre Similarity
       ↓
Better Movie Discovery
```

---

# 🚧 Current Limitations

CineMatch is currently a portfolio/project-scale recommendation platform.

Current limitations include:

- Recommendations are content-oriented rather than user-personalized.
- There is no user login/profile system.
- There is no persistent user rating history.
- There is no collaborative filtering system.
- Recommendation quality depends on the available movie metadata.
- TMDB availability and API limits can affect external movie data.
- The recommendation artifacts are currently file-based rather than stored in a dedicated model/database service.

---

# 🔮 Future Roadmap

Planned/improvable areas include:

### Recommendation Engine

- [ ] Hybrid content + collaborative filtering
- [ ] Personalized recommendations
- [ ] User rating history
- [ ] User preference profiles
- [ ] Recommendation scoring/ranking
- [ ] Improved text preprocessing
- [ ] Semantic embeddings
- [ ] Vector database integration

### Product Features

- [ ] User authentication
- [ ] Favorites / watchlist
- [ ] Movie ratings
- [ ] Watch history
- [ ] Advanced movie filters
- [ ] Actor/director discovery
- [ ] Similarity explanations
- [ ] Personalized home feed

### Engineering

- [ ] Automated tests
- [ ] API monitoring
- [ ] Structured logging
- [ ] CI/CD pipeline
- [ ] Docker support
- [ ] Production database
- [ ] API rate limiting
- [ ] Better observability

---

# 🧪 Testing Recommendations

For production hardening, the following areas should be tested:

```text
API
├── /home
├── /tmdb/search
├── /movie/id/{tmdb_id}
├── /movie/search
└── /recommend/genre

Recommendation Engine
├── TF-IDF loading
├── Similarity calculation
├── Genre matching
└── Missing data handling

Frontend
├── Search
├── Category selection
├── Movie navigation
├── Details page
└── Recommendation fallback
```

---

# 📸 Screenshots

Add your actual application screenshots to the repository:

```text
screenshots/
├── home.png
├── search.png
├── movie-details.png
└── recommendations.png
```

Then reference them in this README:

```markdown
![CineMatch Home](screenshots/home.png)
```

Recommended screenshots:

1. Home feed
2. Search suggestions
3. Movie details
4. TF-IDF recommendations
5. Genre recommendations

---

# 🌐 Project Links

### Backend

```text
https://movie-recommendation-1-aey1.onrender.com
```

### GitHub

```text
https://github.com/NEERAJ-C-cy/Movie_Recommender
```

---

# 👨‍💻 Author

## Neeraj Yadav

B.Tech Computer Science Engineering  
AI/ML Engineer Aspirant

Interested in:

- Artificial Intelligence
- Machine Learning
- Recommendation Systems
- Python
- Backend Development
- Applied AI

GitHub:

https://github.com/NEERAJ-C-cy

---

# ⭐ Why This Project?

CineMatch was built to demonstrate how a machine-learning recommendation system can be transformed into a complete usable application.

Instead of keeping the ML model as an isolated notebook, the project connects:

```text
Machine Learning
      +
Data Processing
      +
REST API
      +
Interactive UI
      +
External API Integration
      +
Cloud Deployment
```

into a single end-to-end application.

---

# 📜 License

This project is intended for educational, learning, and portfolio purposes.

Movie metadata and images are provided through TMDB services and remain subject to their respective terms and policies.

---

# 🙌 Acknowledgements

- **TMDB** — movie metadata, search, posters, and movie imagery.
- **FastAPI** — backend API framework.
- **Streamlit** — interactive application framework.
- **Scikit-learn** — machine-learning utilities and TF-IDF processing.
- **Pandas / NumPy / SciPy** — data and numerical processing.

---

## ⭐ If You Like the Project

If CineMatch helped you understand recommendation systems, FastAPI, Streamlit, or full-stack ML deployment, consider giving the repository a ⭐.
