# Project Setup Instructions

## Prerequisites

Before using this project, ensure that you have the following Python packages installed:

- PyYAML
- Requests
- LangChain Community
- LangChain OpenAI

You can install these packages using pip:

```
bash
pip install pyyaml
pip install requests
pip install langchain_community
pip install langchain_openai
```

## Environment Variables

### Amadeus API
```
export AMADEUS_CLIENT_ID="your_amadeus_client_id"
export AMADEUS_CLIENT_SECRET="your_amadeus_client_secret"
export AMADEUS_AUTH_URL="https://test.api.amadeus.com/v1/security/oauth2/token"
```
### OpenAI API
```
export OPENAI_API_KEY="your_openai_api_key"
```
### Spotify API
```
export SPOTIPY_CLIENT_ID="your_spotify_client_id"
export SPOTIPY_CLIENT_SECRET="your_spotify_client_secret"
export SPOTIPY_REDIRECT_URI="your_spotify_redirect_uri"
```
### Weather API
```
export WEATHER_API_KEY="your_weather_api_key"
```
## Running the scripts
```
py flight_agent.py
```
