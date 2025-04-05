import os
import base64
import requests
import json
from dotenv import load_dotenv

load_dotenv()

class JiraHelper:
    def __init__(self):
        self.base_url = os.getenv("JIRA_URL")
        self.email = os.getenv("JIRA_EMAIL")
        self.token = os.getenv("JIRA_API_TOKEN")
        self.project_key = os.getenv("JIRA_PROJECT_KEY")
        
        # Create auth header
        auth_str = f"{self.email}:{self.token}"
        self.headers = {
            "Authorization": f"Basic {base64.b64encode(auth_str.encode()).decode()}",
            "Content-Type": "application/json"
        }
    
    def test_connection(self):
        """Test if Jira connection works"""
        url = f"{self.base_url}/rest/api/3/myself"
        
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                print("✅ Connected to Jira successfully!")
                return True
            else:
                print(f"❌ Jira connection failed: {response.status_code}")
                print(response.text)
                return False
        except Exception as e:
            print(f"❌ Error connecting to Jira: {str(e)}")
            return False
    
    def create_requirement(self, title, description):
        """Create a requirement ticket in Jira"""
        url = f"{self.base_url}/rest/api/3/issue"
        
        # Format description for Jira's Atlassian Document Format
        data = {
            "fields": {
                "project": {
                    "key": self.project_key
                },
                "summary": title,
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "type": "text",
                                    "text": description
                                }
                            ]
                        }
                    ]
                },
                "issuetype": {
                    "id": "10005"  # Task ID from your Jira project
                }
            }
        }
        # Add this debug line to see what's being sent
        print(f"Request body: {json.dumps(data, indent=2)}")
        
        try:
            response = requests.post(url, headers=self.headers, json=data)
            
            if response.status_code in [200, 201]:
                print(f"✅ Created requirement: {title}")
                return response.json()
            else:
                print(f"❌ Failed to create requirement: {response.status_code}")
                print(response.text)
                return None
        except Exception as e:
            print(f"❌ Error creating requirement: {str(e)}")
            return None
    
    def create_test_case(self, parent_key, title, description):
        """Create a test case as a subtask in Jira"""
        url = f"{self.base_url}/rest/api/3/issue"

        # Normalize steps format if they're in array format with numbers or brackets
        if isinstance(description, str) and 'Steps:' in description:
            import re
            steps_match = re.search(r'Steps:\n(.*?)\n\nExpected Result', description, re.DOTALL)
            if steps_match:
                steps_content = steps_match.group(1)
                # Clean up the steps content to remove JSON artifacts, numbers, etc.
                cleaned_steps = re.sub(r'[\[\]\'"]', '', steps_content)       # Remove brackets and quotes
                cleaned_steps = re.sub(r'\d+,\s*', '', cleaned_steps)         # Remove numbered prefixes
                cleaned_steps = re.sub(r'\n+', '\n', cleaned_steps).strip()   # Remove extra newlines
                # Replace in description
                description = description.replace(steps_match.group(1), cleaned_steps)

        data = {
            "fields": {
                "project": {
                    "key": self.project_key
                },
                "parent": {
                    "key": parent_key
                },
                "summary": f"Test: {title}",
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "type": "text",
                                    "text": description
                                }
                            ]
                        }
                    ]
                },
                "issuetype": {
                    "id": "10007"  # Subtask ID from your Jira project
                }
            }
        }

        print(f"Test case request body: {json.dumps(data, indent=2)}")

        try:
            response = requests.post(url, headers=self.headers, json=data)

            if response.status_code in [200, 201]:
                print(f"  ✅ Created test case: {title}")
                return response.json()
            else:
                print(f"  ❌ Failed to create test case: {response.status_code}")
                print(response.text)
                return None
        except Exception as e:
            print(f"  ❌ Error creating test case: {str(e)}")
            return None