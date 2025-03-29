import subprocess
from PySide6.QtWidgets import QTextEdit


class ChucKManager:
    def __init__(self, console: QTextEdit = None):
        self.console = console
        self.processes = {}  # Dictionary to track processes by script path

    def log_output(self, message):
        """Log a message to the console."""
        if self.console:
            self.console.append(message)
        print(message)  # Also print to the terminal for debugging

    def run_script(self, script_path):
        """Run a ChucK script and keep track of the process."""
        try:
            self.log_output(f"Starting ChucK script: {script_path}")
            process = subprocess.Popen(
                ["chuck", script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            self.processes[script_path] = process
            self.log_output(f"ChucK script started: {script_path}")
        except Exception as e:
            self.log_output(f"Error running ChucK script: {e}")

    def stop_script(self, script_path):
        """Stop a specific ChucK script."""
        process = self.processes.get(script_path)
        if process and process.poll() is None:  # Check if the process is running
            process.terminate()  # Terminate the process
            process.wait()  # Wait for the process to terminate
            self.log_output(f"Stopped ChucK script: {script_path}")
            del self.processes[script_path]  # Remove the process from the dictionary
        else:
            self.log_output(f"No running process found for script: {script_path}")

    def stop_all_scripts(self):
        """Stop all running ChucK scripts."""
        for script_path, process in list(self.processes.items()):
            if process.poll() is None:  # Check if the process is running
                process.terminate()  # Terminate the process
                process.wait()  # Wait for the process to terminate
                self.log_output(f"Stopped ChucK script: {script_path}")
        self.processes.clear()  # Clear the dictionary
        self.log_output("All ChucK scripts have been stopped.")