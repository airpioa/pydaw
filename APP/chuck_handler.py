import subprocess
from PySide6.QtWidgets import QTextEdit

class ChucKManager:
    def __init__(self, console: QTextEdit = None):
        self.console = console
        self.process = None

    def log_output(self, message):
        if self.console:
            self.console.append(message)

    def run_script(self, script_path):
        try:
            if self.process:
                self.process.terminate()  # Stop any existing process
            
            self.log_output(f"Starting ChucK script: {script_path}")
            
            self.process = subprocess.Popen(
                ["chuck", script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Read output in real-time
            while True:
                output = self.process.stdout.readline()
                if not output:
                    break
                self.log_output(output.strip())

            self.log_output(f"ChucK script finished: {script_path}")

        except Exception as e:
            self.log_output(f"Error running ChucK script: {e}")
