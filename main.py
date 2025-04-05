import json
import os
import time
from dotenv import load_dotenv
from utils.jira_helper import JiraHelper
from utils.llm_helper import query_llm

load_dotenv()

# Add this function right after your imports in main.py
def fix_json_from_llm(json_text):
    """Fix common JSON formatting issues in LLM responses"""
    import re
    
    # Try direct parse first
    try:
        return json.loads(json_text)
    except json.JSONDecodeError:
        # Extract just the JSON array if there's markdown or explanations
        json_match = re.search(r'\[\s*\{[\s\S]*\}\s*\]', json_text)
        if json_match:
            json_text = json_match.group(0)
        
        # Fix mixed number/string arrays in steps field
        # This pattern looks for "steps": [...] and fixes its contents
        pattern = r'"steps"\s*:\s*\[(.*?)\]'
        
        def fix_steps_array(match):
            steps_content = match.group(1)
            # Convert to a proper string array
            steps = re.findall(r'\d+,\s*\'([^\']+)\'|"([^"]+)"', steps_content)
            cleaned_steps = []
            for s in steps:
                # Each match is a tuple with one empty element
                step_text = s[0] if s[0] else s[1]
                cleaned_steps.append(f'"{step_text}"')
            return '"steps": [' + ', '.join(cleaned_steps) + ']'
        
        json_text = re.sub(pattern, fix_steps_array, json_text, flags=re.DOTALL)
        
        # Fix other common JSON issues
        json_text = re.sub(r'(\w+):', r'"\1":', json_text)  # Quote keys
        json_text = re.sub(r',\s*}', '}', json_text)  # Remove trailing commas
        
        try:
            return json.loads(json_text)
        except json.JSONDecodeError as e:
            print(f"Still couldn't parse JSON after fixes: {str(e)}")
            return None


def main():
    print("🚀 Starting Agent2AI Implementation")
    print("-----------------------------------")
    
    # Step 1: Test Jira connection
    jira = JiraHelper()
    if not jira.test_connection():
        print("Please fix your Jira configuration and try again.")
        return
    
    # Step 2: Requirements Generation
    print("\n🤖 REQUIREMENTS AGENT")
    print("-------------------")
    
    product_request = "Generate a flight tracking application in ReactJS/Java"
    
    req_prompt = f"""
    You are a senior software requirements analyst. Given this high-level request:
    "{product_request}"
    
    Generate a comprehensive list of 5 essential requirements for this application.
    Format each requirement as JSON with these fields:
    - title: Short title of the requirement (max 10 words)
    - description: Detailed explanation (2-3 sentences)
    - acceptance_criteria: List of 3 criteria that must be met
    
    Return ONLY a valid JSON array of these requirements with no additional text.
    """
    
    print("Generating requirements...")
    requirements_json = query_llm(req_prompt, model="perplexity")
    
    # Save raw response
    with open("requirements_raw.txt", "w") as f:
        f.write(requirements_json)
    
    # Extract JSON from response
    # This handles cases where the API returns extra text
    import re
    json_match = re.search(r'\[[\s\S]*\]', requirements_json)
    if json_match:
        requirements_json = json_match.group(0)
    
    # Parse requirements
    try:
        requirements = json.loads(requirements_json)
        print(f"✅ Generated {len(requirements)} requirements")
        
        # Save formatted JSON
        with open("requirements.json", "w") as f:
            json.dump(requirements, f, indent=2)
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse requirements JSON: {str(e)}")
        print("Check requirements_raw.txt for the API response")
        return
    
    # Step 3: Create requirements in Jira
    print("\nCreating requirements in Jira...")
    requirement_issues = []
    
    for req in requirements:
        # Format description with acceptance criteria
        description = f"{req['description']}\n\nAcceptance Criteria:\n"
        for i, ac in enumerate(req['acceptance_criteria']):
            description += f"- {ac}\n"
        
        # Create Jira issue
        issue = jira.create_requirement(req['title'], description)
        if issue:
            requirement_issues.append({
                "key": issue["key"],
                "title": req['title'],
                "description": description
            })
        
        # Pause to avoid rate limits
        time.sleep(1)
    
    if not requirement_issues:
        print("❌ Failed to create any requirements in Jira")
        return
    
    # Step 4: Test Case Generation
    print("\n🤖 TESTER AGENT")
    print("-------------")
    
    for req_issue in requirement_issues:
        print(f"\nGenerating test cases for: {req_issue['title']}")
        
        test_prompt = f"""
        You are a QA testing expert. For this requirement:

        {req_issue['title']}
        {req_issue['description']}

        Generate 3 test cases that would verify this requirement.
        Each test case should have:
        - title: Short descriptive title of the test
        - steps: An array of strings for each step (NOT numbered internally)
        - expected_result: What should happen if the test passes

        Return ONLY a valid JSON array like this:
        [
        {{
            "title": "Test Title 1",
            "steps": ["Step 1: Do something", "Step 2: Do something else"],
            "expected_result": "Expected result"
        }},
        {{
            "title": "Test Title 2",
            "steps": ["Step 1: Check X", "Step 2: Verify Y"],
            "expected_result": "Another expected result"
        }},
        {{
            "title": "Test Title 3",
            "steps": ["Step 1: Attempt Z", "Step 2: Confirm outcome"],
            "expected_result": "Third expected result"
        }}
        ]

        IMPORTANT: Ensure your response is ONLY the JSON array with no additional explanation or formatting.
        """
        
        test_cases_json = query_llm(test_prompt, model="perplexity")
        
        # Save raw response
        with open(f"test_cases_raw_{req_issue['key']}.txt", "w") as f:
            f.write(test_cases_json)
        
        # Use the new function to fix and parse the JSON
        test_cases = fix_json_from_llm(test_cases_json)

        if test_cases:
            print(f"✅ Generated {len(test_cases)} test cases")
            
            # Save formatted JSON
            with open(f"test_cases_{req_issue['key']}.json", "w") as f:
                json.dump(test_cases, f, indent=2)

            # 🔽 ADD THIS BLOCK HERE
            for test in test_cases:
                # Format steps properly for description
                steps_text = ""
                if isinstance(test['steps'], list):
                    steps_text = "\n".join(test['steps'])
                else:
                    # Handle case where steps might be a string
                    steps_text = str(test['steps'])
                
                test_description = f"Steps:\n{steps_text}\n\nExpected Result:\n{test['expected_result']}"
                
                # Create test case in Jira
                jira.create_test_case(req_issue['key'], test['title'], test_description)
        else:
            print(f"❌ Failed to parse test cases JSON. See raw file for details.")
            continue  # Skip to the next requirement
    
    
    print("\n🎉 Implementation completed!")
    print("Check your Jira project to see the created issues and subtasks")

if __name__ == "__main__":
    main()
