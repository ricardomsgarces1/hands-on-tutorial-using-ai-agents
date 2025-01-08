# Using AI Agents to abstract Complex APIs
Leveraging LangChain’s OpenAPI Toolkit enables us to build AI agents that can abstract the complexities of interacting with large APIs. By separating high-level planning from low-level execution, agents can navigate extensive API specifications more efficiently, minimizing token usage and improving the coherence of long interaction sequences.

In this <a href="https://nextingenai.com/hands-on-tutorial-using-ai-agents-to-abstract-complex-apis/">hands-on tutorial</a>, I’ll demonstrate how to create a hierarchical planning agent that leverages LangChain's OpenAPI Toolkit to simplify API interactions and streamline complex workflows.

In this repository, you can find several examples of AI Agents that leverage LangChain’s OpenAPI Toolkit.


## Prerequisites

Before using this project, ensure that you have the following Python packages installed:

- PyYAML
- Requests
- LangChain Community
- LangChain OpenAI
- Spotipy! (Only required for the agent that interacts with Spotify)

You can install these packages using pip:

```
bash
pip install pyyaml
pip install requests
pip install langchain_community
pip install langchain_openai
pip install spotipy
```

## Environment Variables
To authenticate and access necessary APIs, set the following environment variables. Replace the placeholder values with your actual credentials. Keep in mind that you only need to configure the variables used in the scripts that you will be executing.

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
### Spotify OpenAPI Agent Script
This script integrates with the Spotify API using an OpenAPI agent. 
To use the Amadeus OpenAPI Agent Script, execute the following command:

```
py flight_agent.py
```
To use the Spotify OpenAPI Agent Script, execute the following command:

```
py spotify_agent.py
```
To use the Weather OpenAPI Agent Script, execute the following command:
```
py weather_agent.py
```
