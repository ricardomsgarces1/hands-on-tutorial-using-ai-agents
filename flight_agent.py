#######################################################
# Amadeus OpenAPI Agent Script
#######################################################
# This script integrates with the Amadeus API using an OpenAPI agent. It authenticates with the API using client credentials, extracts available endpoints from the OpenAPI specification, and allows querying the API using a natural language model.
# The script uses the LangChain framework to handle OpenAPI interactions and leverages OpenAI's GPT-4 model for query interpretation.

# Prerequisites:
# - Amadeus API credentials (client_id and client_secret)
# - OpenAPI YAML file for the Amadeus API (Version 3.0)
# - OpenAI API key

# How to Obtain Amadeus API Credentials:
# 1. Go to https://developers.amadeus.com/ and sign up for an account.
# 2. After logging in, navigate to the "My Applications" section and create a new application.
# 3. Once the application is created, you will receive a client_id and client_secret.
# 4. Set these credentials as environment variables:
#    - AMADEUS_CLIENT_ID
#    - AMADEUS_CLIENT_SECRET

# How to Obtain an OpenAI API Key:
# 1. Go to https://platform.openai.com/signup and create an OpenAI account.
# 2. Once logged in, navigate to the API Keys section.
# 3. Generate a new API key and copy it.
# 4. Set this API key as an environment variable:
#    - OPENAI_API_KEY

import os
import yaml
import requests
from langchain_community.agent_toolkits.openapi.spec import reduce_openapi_spec
from langchain_community.utilities.requests import RequestsWrapper
from langchain_community.agent_toolkits.openapi import planner
from langchain_openai import ChatOpenAI

# Function to load and reduce the OpenAPI spec from a YAML file.
def load_openapi_spec(file_path):
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

# Function to construct authorization headers by requesting an access token.
def construct_auth_headers(auth_url, client_id, client_secret):
    """Constructs the authorization headers by requesting an access token."""
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    response = requests.post(auth_url, headers=headers, data=data)
    response.raise_for_status()
    return {"Authorization": f"Bearer {response.json().get('access_token')}"}

# Function to initialize the RequestsWrapper with authentication headers.
def initialize_requests_wrapper(client_id, client_secret):
    """Initializes the RequestsWrapper with authentication headers."""
    auth_url = f"{os.environ.get("AMADEUS_AUTH_URL")}/security/oauth2/token" # Ideally it should have been obtained from the openAPI definition file.

    headers = construct_auth_headers(auth_url, client_id, client_secret)
    return RequestsWrapper(headers=headers)

# Function to initialize the OpenAPI agent using the provided spec and requests wrapper.
def initialize_agent(api_spec, requests_wrapper):
    """Initializes the OpenAPI agent using the provided spec and requests wrapper."""
    # You will need an openAPI key. If you don't have one, please register and create one here: https://platform.openai.com/settings/organization/api-keys
    # Beware of token limits associated to the model used: https://platform.openai.com/settings/organization/limits
    # gpt-4 will provide a better performance, however, in Tier1, it has a token limit of 10K. gpt-4o-mini is being used, since it has a token limit of 300K in Tier1.

    llm = ChatOpenAI(
        model_name="gpt-4o-mini",
        temperature=0.0,
        api_key=os.environ.get("OPENAI_API_KEY")
    )

    return planner.create_openapi_agent(
        api_spec,  # The reduced OpenAPI spec that defines the API's structure and available endpoints.
        requests_wrapper,  # The RequestsWrapper instance that handles authenticated requests to the API.
        llm,  # The language model used to interpret queries and generate responses.
        allow_dangerous_requests=True,  # A safety flag to control whether potentially harmful requests are allowed. Defaults to False for security reasons.
        handle_parsing_errors=True  # Enables the agent to gracefully handle any errors encountered during response parsing.
    )

#######################################################
# Main logic section
#######################################################

# Define the path to the OpenAPI YAML file.
swagger_file = "amadeus_openapi.yaml"
# Load and reduce the OpenAPI spec from the YAML file.
raw_api_spec, api_spec = load_openapi_spec(swagger_file)
# Extract the list of available GET and POST endpoints from the spec.
endpoints = get_endpoints(raw_api_spec)
# Print the number of endpoints found for verification.
print(f"Endpoints: {len(endpoints)}")

# Retrieve the client ID and client secret from environment variables.
client_id = os.environ.get("AMADEUS_CLIENT_ID")
client_secret = os.environ.get("AMADEUS_CLIENT_SECRET")
# Initialize the RequestsWrapper with authentication headers.
requests_wrapper = initialize_requests_wrapper(client_id, client_secret)

# Initialize the OpenAPI agent using the reduced spec and requests wrapper.
agent = initialize_agent(api_spec, requests_wrapper)

# Define a query to interact with the agent.
query = "Find a flight from Lisbon to Sydney. The departure should happen on the 5th of May of 2025. Order the list of applicable flights by price, starting with the cheapest. Include all available details about each flight."
# Invoke the agent with the query and print the response.
response = agent.invoke(query)
print(response)
