# 🌊 HydroAI — Groundwater Intelligence (Streamlit)

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-ff4b4b.svg)](https://streamlit.io)
[![Plotly](https://img.shields.io/badge/Plotly-Graphs-3f4f75.svg)](https://plotly.com/python/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Made with ❤️](https://img.shields.io/badge/Made%20with-❤️-ff69b4.svg)](#)

A modern, Streamlit application that provides interactive groundwater intelligence for Gujarat. Explore real‑time metrics, visualize correlations, and chat with an AI assistant to surface insights and recommendations.


## ✨ Features
- **Dark Mode UI** with glassmorphism and subtle animations
- **Real‑time visualizations**: Scatter plots, gauge indicators, and more
- **Flexible filtering** by district and analysis mode
- **AI Assistant** powered via Google Generative AI for contextual insights
- **Data summary & key metrics** cards


## 📦 Tech Stack
- `Python`, `Streamlit`
- `Pandas`, `NumPy`
- `Plotly`
- `python-dotenv`
- `google-generativeai`


## 🗂 Project Structure
```
.
├── app/
│   └── utils/
│       └── helpers.py
├── data/
│   └── gujarat_groundwater_merged_final.csv
├── main.py
├── single_app.py
├── clean_data.py
├── requirements.txt
├── README.md
└── .gitignore
```


## 🚀 Getting Started

### 1) Clone the repository
```bash
git clone https://github.com/dhruv-thakar/Hydro-ai.git
cd Hydro-ai
```

### 2) Create and activate a virtual environment (Windows PowerShell)
```powershell
python -m venv venv
./venv/Scripts/Activate.ps1
```

### 3) Install dependencies
```bash
pip install -r requirements.txt
```

### 4) Environment variables
Create a `.env` file at the project root with the following key:
```
GOOGLE_API_KEY=your_api_key_here
```
- Get an API key from Google AI Studio.
- The `.env` file is already ignored by `.gitignore` to keep your key safe.


### 5) Run the app
```bash
streamlit run main.py
```
Then open the local URL shown in your terminal (default: http://localhost:8501).


## 🖼 Screenshots
Create a folder `assets/` and drop screenshots there, then update the paths below.

- Real‑time Visualization
  
  ![Real-time Visualization](assets/screenshot-realtime.png)

- AI Insights
  
  ![AI Insights](assets/screenshot-insights.png)


## 🧭 Data
- Primary dataset: `data/gujarat_groundwater_merged_final.csv`
- The app uses relative paths (e.g., `data/...`) so it runs consistently across machines.

If the dataset is very large (>100 MB), we recommend using **Git LFS** (already configured in this repo):
```bash
git lfs install
git lfs track "data/gujarat_groundwater_merged_final.csv"
```


## 🧪 Troubleshooting
- **google.auth.exceptions.DefaultCredentialsError / API issues**
  - Ensure `.env` contains a valid `GOOGLE_API_KEY`
  - Restart the app after setting the key
- **FileNotFoundError for CSV**
  - Verify the CSV exists under `data/gujarat_groundwater_merged_final.csv`
  - The app expects the relative path `data/...`, not an absolute path
- **Windows line endings warnings (CRLF/LF)**
  - These are harmless. Optionally set: `git config --global core.autocrlf true`


## 🤝 Contributing
Pull requests are welcome! For major changes, please open an issue to discuss what you’d like to change.


## 📝 License
This project is licensed under the **MIT License**. See `LICENSE` for details.
