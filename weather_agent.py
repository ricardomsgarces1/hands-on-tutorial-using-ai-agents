#######################################################
# Weather OpenAPI Agent Script
#######################################################
# This script integrates with Visual Crossing Weather API using an OpenAPI agent. It authenticates with the API using an access key, extracts available endpoints from the OpenAPI specification, and allows querying the API using a natural language model.
# The script uses the LangChain framework to handle OpenAPI interactions and leverages OpenAI's GPT-4 model for query interpretation.

# Prerequisites:
# - OpenAPI YAML file for the Visual Crossing Weather API (Version 3.0)
# - OpenAI API key
# - Visual Crossing Weather API key

# How to Obtain a Visual Crossing Weather API Key:
# 1. Visit https://www.visualcrossing.com/weather-api and sign up for an account if you don't have one.
# 2. Once logged in, navigate to the API section in your dashboard.
# 3. Create or access your API key and copy it.
# 4. Set this key as an environment variable:
#    - WEATHER_API_KEY

# How to Obtain an OpenAI API Key:
# 1. Go to https://platform.openai.com/signup and create an OpenAI account.
# 2. Once logged in, navigate to the API Keys section.
# 3. Generate a new API key and copy it.
# 4. Set this API key as an environment variable:
#    - OPENAI_API_KEY

import os
import yaml
from langchain_community.agent_toolkits.openapi.spec import reduce_openapi_spec
from langchain_community.agent_toolkits.openapi import planner
from langchain_openai import ChatOpenAI
from langchain_community.utilities.requests import RequestsWrapper

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

# Load and reduce the OpenAPI spec for the weather API.
raw_weather_api_spec, weather_api_spec = load_and_reduce_spec("weather_openapi.yaml")

# Extract and print the list of available endpoints.
endpoints = get_endpoints(raw_weather_api_spec)
print(f"Endpoints: {len(endpoints)}")

# Initialize the OpenAI language model.
llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0.3,
    api_key=os.environ.get("OPENAI_API_KEY")
)

# Initialize the RequestsWrapper with a placeholder authorization header.
headers = {"Authorization": "None"}
requests_wrapper = RequestsWrapper(headers=headers)

# Initialize the OpenAPI agent for the weather API.
agent = planner.create_openapi_agent(
    weather_api_spec,  # The reduced OpenAPI spec that defines the API's structure and available endpoints.
    requests_wrapper,  # The RequestsWrapper instance that handles authenticated requests to the API.
    llm,  # The language model used to interpret queries and generate responses.
    allow_dangerous_requests=True,  # A safety flag to control whether potentially harmful requests are allowed. Defaults to False for security reasons.
    handle_parsing_errors=True  # Enables the agent to gracefully handle any errors encountered during response parsing.
)

# Define and invoke a user query.
user_query = f"How are the weather conditions in Lisbon today? The Weather API key is {os.environ.get('WEATHER_API_KEY')}." # The API key should be part of the payload.
response = agent.invoke(user_query)
print(response)