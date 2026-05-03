# Your Life as a Playlist

Your Life as a Playlist is an interactive Streamlit web app that uses a user's favorite artists and personality quiz answers to generate a personalized music persona.

## Features

- Enter up to three favorite artists
- Take a seven-question music personality quiz
- Receive a personalized result with:
  - Persona name
  - Emoji
  - Description
  - Anthem song
  - Personality traits
- Uses an internal Excel artist database

## Files

- `app.py` — main Streamlit application
- `database_artists.xlsx` — artist dataset
- `requirements.txt` — required Python packages

## How to Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
