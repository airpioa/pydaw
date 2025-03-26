import subprocess
from PySide6.QtWidgets import QTextEdit

class ChucKManager:
    def __init__(self, console: QTextEdit = None):
        self.console = console
        self.processes = []  # Track multiple processes (for each script)

    def log_output(self, message):
        if self.console:
            self.console.append(message)

    def run_script(self, script_path):
        """Run a ChucK script and keep track of the process."""
        try:
            # Start a new process for the script
            self.log_output(f"Starting ChucK script: {script_path}")
            
            process = subprocess.Popen(
                ["chuck", script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Add the new process to the list
            self.processes.append(process)

            # Read output in real-time
            while True:
                output = process.stdout.readline()
                if not output:
                    break
                self.log_output(output.strip())

            self.log_output(f"ChucK script finished: {script_path}")

        except Exception as e:
            self.log_output(f"Error running ChucK script: {e}")

    def stop_all_instruments(self):
        """Stop all running ChucK processes."""
        for process in self.processes:
            if process.poll() is None:  # Check if the process is still running
                process.terminate()  # Terminate the process
                self.log_output(f"Terminated ChucK process.")
        # Clear the list of processes
        self.processes.clear()
