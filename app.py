import os
import subprocess
from pathlib import Path
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "HeadWater B2B Core Gateway: Online"

@app.route('/execute-b2b', methods=['POST'])
def trigger_b2b_pipeline():
    root_path = Path(__file__).resolve().parent
    core_path = root_path / 'Core_Modules'
    
    results = []
    for module_num in ['1', '2', '3', '4']:
        script_file = core_path / f'hw_b2b_module_0{module_num}_build.pyc'
        execution_command = ['python3', str(script_file)]
        
        if module_num == '3': 
            execution_command.append('test_payload.json')
            
        process_run = subprocess.run(execution_command, cwd=str(root_path), capture_output=True, text=True)
        status_string = 'OK' if process_run.returncode == 0 else 'FAILED'
        results.append(f'Module {module_num}: {status_string}')
        
    return jsonify({"status": "execution_complete", "pipeline_summary": results}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
