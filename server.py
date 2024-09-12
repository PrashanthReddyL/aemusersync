from flask import Flask, jsonify
import subprocess
import os

app = Flask(__name__)

# Define the directory where the user_sync executable and configuration files are stored
BASE_DIR = '/home/site/wwwroot'  # Base directory in Azure App Service
EXECUTABLE_PATH = os.path.join(BASE_DIR, 'dist', 'user-sync')  # Path to the user_sync executable
CONFIG_PATH = os.path.join(BASE_DIR, 'config', 'user_sync_config.yml')  # Path to the configuration file

@app.route('/run-sync', methods=['GET'])
def run_sync():
    try:
        # Check if the executable and configuration file exist
        if not os.path.isfile(EXECUTABLE_PATH):
            return jsonify({"status": "error", "message": "Executable not found"}), 404
        if not os.path.isfile(CONFIG_PATH):
            return jsonify({"status": "error", "message": "Configuration file not found"}), 404

        # Run the executable with the configuration file
        result = subprocess.run([EXECUTABLE_PATH, '-c', CONFIG_PATH],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Return the output of the command as the HTTP response
        return jsonify({
            "status": "success",
            "stdout": result.stdout.decode('utf-8'),
            "stderr": result.stderr.decode('utf-8')
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

