# Flight Tracking Agent

##  Project Overview
This project implements AI agents to automate the Software Development Lifecycle (SDLC) for a flight tracking application using Large Language Models and Jira integration.

##  Features
- ✅ **Requirements Agent**: Expands a one-line prompt into detailed requirements
  - Takes a simple product request: "Generate a flight tracking application in ReactJS/Java"
  - Generates comprehensive requirements with acceptance criteria
  - Automatically creates Jira tickets for each requirement
  
-  **Tester Agent**: Creates test cases for all requirements
  - Analyzes each requirement to understand testing needs
  - Generates detailed test cases with steps and expected results
  - Creates subtasks in Jira linked to parent requirements

##  Technologies Used
- **Perplexity API**: Primary LLM for generating requirements and test cases
- **Gemini API**: Alternative LLM for content generation
- **Jira REST API**: For ticket and subtask creation
- **Python**: Core implementation language
- **Request Caching**: To optimize API usage and conserve credits

##  Project Structure
```


flight-tracking-agent/
├── main.py              \# Entry point and orchestration
├── utils/
│   ├── jira_helper.py   \# Jira API integration
│   └── llm_helper.py    \# LLM API handling and caching
├── requirements.txt     \# Dependencies
└── .env                 \# Environment variables (excluded from Git)

```

##  How to Run

### 1. Clone the Repository
```

git clone https://github.com/soumysuwas/flight-tracking-agent1.git
cd flight-tracking-agent1

```

### 2. Install Dependencies
```

pip install -r requirements.txt

```

### 3. Configure Environment Variables
Create a `.env` file in the root folder:
```

PERPLEXITY_API_KEY=your_key
GEMINI_API_KEY=your_key
JIRA_EMAIL=your_email
JIRA_API_TOKEN=your_token
JIRA_URL=your_jira_url
JIRA_PROJECT_KEY=your_project_key

```

### 4. Run the Application
```

python main.py

```
#### Using an IDE (e.g., Visual Studio Code)
1. Open the project folder in VS Code
2. Open main.py in the editor
3. Click the "Run" button (▶️) in the top-right corner
   or press F5 (Windows/Linux) / Cmd+F5 (macOS)
4. Alternatively, use the integrated terminal in VS Code 
   and execute: python main.py

#### Using Terminal/Command Line

#### Navigate to the project root directory
cd path/to/flight-tracking-agent1

#### Execute the main Python script
```
python main.py  # On Windows
```
#### OR
```
python3 main.py  # On macOS/Linux if python command isn't aliased
```
Note: Ensure your Python environment has all required dependencies installed and the .env file is properly configured before running the application.

## 🎥 Demo
Check out the video demonstration here: https://www.youtube.com/watch?v=bW7p9Ts85dw

##  Results
The implementation successfully:
- Generates 5 detailed requirements for the flight tracking application
- Creates Jira tickets for each requirement with acceptance criteria
- Generates 3 test cases for each requirement
- Creates test cases as subtasks in Jira

##  Future Scope
This project represents the first steps in automating the SDLC. Future enhancements could include:
- Design Agent: To create UI/UX specifications and wireframes
- Code Agent: To generate actual implementation code
- CI/CD Agent: To automate testing and deployment
- End-to-end orchestration platform for all agents

## 👨‍💻 Author
Made by Soumy Suwas
```
