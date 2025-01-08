#######################################################
# Spotify OpenAPI Agent Script
#######################################################
# This script integrates with the Spotify API using an OpenAPI agent. It authenticates with the API using OAuth 2.0 credentials, extracts available endpoints from the OpenAPI specification, and allows querying the API using a natural language model.
# The script uses the LangChain framework to handle OpenAPI interactions and leverages OpenAI's GPT-4 model for query interpretation.

# Prerequisites:
# - Spotify API credentials (OAuth 2.0 access token)
# - OpenAPI YAML file for the Spotify API (Version 3.0)
# - OpenAI API key

# How to Obtain Spotify API Credentials:
# 1. Go to https://developer.spotify.com/dashboard/ and log in or sign up for a Spotify developer account.
# 2. Create a new application in the Spotify Developer Dashboard to obtain your client ID and secret.

# How to Obtain an OpenAI API Key:
# 1. Go to https://platform.openai.com/signup and create an OpenAI account.
# 2. Once logged in, navigate to the API Keys section.
# 3. Generate a new API key and copy it.
# 4. Set this API key as an environment variable:
#    - OPENAI_API_KEY

import os
import yaml
from langchain_community.agent_toolkits.openapi.spec import reduce_openapi_spec
from langchain_community.utilities.requests import RequestsWrapper
from langchain_community.agent_toolkits.openapi import planner
from langchain_openai import ChatOpenAI
import spotipy.util as util

# Function to load and reduce the OpenAPI spec from a YAML file.
def load_and_reduce_spec(file_path):
    """Loads and reduces the OpenAPI spec from a given YAML file."""
    with open(file_path, encoding="utf8") as f:
        raw_api_spec = yaml.load(f, Loader=yaml.Loader)
    return raw_api_spec, reduce_openapi_spec(raw_api_spec)

# Function to extract all GET and POST endpoints from the OpenAPI spec.
def get_endpoints(raw_api_spec):
    """Extracts all GET and POST endpoints from the OpenAPI spec."""
    return [
        (route, operation)
        for route, operations in raw_api_spec["paths"].items()
        for operation in operations
        if operation in ["get", "post"]
    ]

# Function to construct Spotify authorization headers.
def construct_spotify_auth_headers(raw_spec):
    """Constructs the authorization headers for Spotify using the OpenAPI spec."""
    scopes = list(raw_spec["components"]["securitySchemes"]["oauth_2_0"]["flows"]["authorizationCode"]["scopes"].keys())
    access_token = util.prompt_for_user_token(scope=",".join(scopes))
    return {"Authorization": f"Bearer {access_token}"}

# Load and reduce OpenAPI spec.
raw_spotify_api_spec, spotify_api_spec = load_and_reduce_spec("spotify_openapi.yaml")

# Construct Spotify authorization headers.
headers = construct_spotify_auth_headers(raw_spotify_api_spec)
requests_wrapper = RequestsWrapper(headers=headers)

# Extract endpoints for verification.
endpoints = get_endpoints(raw_spotify_api_spec)
print(f"Endpoints: {len(endpoints)}")

# Initialize the OpenAI language model.
# Beware of token limits associated to the model used: https://platform.openai.com/settings/organization/limits
# gpt-4 will provide a better performance, however, in Tier1, it has a token limit of 10K. gpt-4o-mini is being used, since it has a token limit of 300K in Tier1.
llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0.0,
    api_key=os.environ.get("OPENAI_API_KEY")
)

# Initialize the OpenAPI agent for Spotify.
spotify_agent = planner.create_openapi_agent(
    spotify_api_spec,  # The reduced OpenAPI spec that defines the API's structure and available endpoints.
    requests_wrapper,  # The RequestsWrapper instance that handles authenticated requests to the API.
    llm,  # The language model used to interpret queries and generate responses.
    allow_dangerous_requests=True,  # A safety flag to control whether potentially harmful requests are allowed. Defaults to False for security reasons.
    handle_parsing_errors=True  # Enables the agent to gracefully handle any errors encountered during response parsing.
)

# Define and invoke a user query: Request 1
# user_query = "give me a song I'd like, make it blues-ey"
# response = spotify_agent.invoke(user_query)
# print(response)

# Define and invoke a user query: Request 2
user_query = "make me a playlist with the first song from kind of blue. call it machine blues 2."
response = spotify_agent.invoke(user_query)
print(response)