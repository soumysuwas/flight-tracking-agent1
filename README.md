# Flight Tracking Agent

## Project Overview
This project implements AI agents for automating the software development lifecycle (SDLC) for a flight tracking application. It includes:

1. **Requirements Agent**: Expands a one-line prompt into detailed requirements and creates Jira tickets
2. **Tester Agent**: Generates test cases for each requirement and creates them as subtasks in Jira

## Implementation Details
- Uses Perplexity and Gemini APIs for generating requirements and test cases
- Integrates with Jira API to create tickets and subtasks
- Implements caching to optimize API usage

## Setup
1. Install dependencies:

pip install requests python-dotenv google-generativeai


2. Configure environment variables in a `.env` file:
PERPLEXITY_API_KEY=your_key,
GEMINI_API_KEY=your_key,
JIRA_EMAIL=your_email,
JIRA_API_TOKEN=your_token,
JIRA_URL=your_jira_url,
JIRA_PROJECT_KEY=your_project_key,


3. Run the implementation:


## Results
The implementation successfully:
- Generates 5 detailed requirements for a flight tracking application
- Creates Jira tickets for each requirement
- Generates 3 test cases for each requirement
- Creates test cases as subtasks in Jira
