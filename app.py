def clear_logs():
    try:
        reply = QMessageBox.question(
            None,
            "Confirm Clear Logs",
            "Are you sure you want to permanently delete all session logs?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            json_file = log_dir / "session_log.json"
            csv_file = log_dir / "session_log.csv"
            if json_file.exists():
                json_file.unlink()
            if csv_file.exists():
                csv_file.unlink()
            print("Logs cleared.")
            QMessageBox.information(None, "Logs Cleared", "All session logs have been deleted.")
    except Exception as e:
        print(f"Error clearing logs: {e}")
# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QPushButton, QVBoxLayout # type: ignore
import sys
import json
import csv
import datetime

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

block_cipher = None

log_dir = Path("/Users/kevon/Python/GhostBrowseAI/logs")
log_dir.mkdir(parents=True, exist_ok=True)

def open_log_folder():
    try:
        subprocess.run(["open", str(log_dir)])
    except Exception as e:
        print(f"Failed to open log folder: {e}")

# Function to log a browsing session to the logs directory in dist/logs
def log_session(topic, url):
    log_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "topic": topic,
        "url": url
    }
    log_file_path = log_dir / "session_log.json"
    with open(log_file_path, "a") as log_file:
        json.dump(log_data, log_file)
        log_file.write("\n")

# Simulate a session for demonstration
import random
def simulate_session():
    topics = [
        "History of jazz music",
        "Basics of investing",
        "How solar panels work",
        "Dog training techniques",
        "Famous black inventors",
        "How the stock market works",
        "Benefits of meditation",
        "Ancient Egyptian culture",
        "How to start a small business",
        "Principles of credit scores"
    ]
    topic = random.choice(topics)
    url_topic = topic.replace(" ", "_")
    url = f"https://en.wikipedia.org/wiki/{url_topic}"
    log_session(topic, url)
    print(f"Simulated session: {topic} -> {url}")

def export_logs_to_csv():
    print("\nExporting logs to session_log.csv...")
    json_file_path = log_dir / "session_log.json"
    csv_file_path = log_dir / "session_log.csv"

    if not json_file_path.exists():
        print("No session log found to export.")
        return

    try:
        with open(json_file_path, "r") as json_file, open(csv_file_path, "w", newline='') as csv_file:
            fieldnames = ["timestamp", "topic", "url"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

            for line in json_file:
                entry = json.loads(line)
                writer.writerow(entry)

        print("Export complete: session_log.csv")
    except Exception as e:
        print(f"Error exporting logs: {e}")

def show_export_prompt():
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("GhostBrowseAI")

    def ask_user():
        reply = QMessageBox.question(
            window,
            "Export Logs",
            "Do you want to export session logs to CSV?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            export_logs_to_csv()
            QMessageBox.information(window, "Export Complete", "Logs have been exported successfully.")
            open_log_folder()

    def open_logs():
        open_log_folder()

    def start_session():
        simulate_session()
        QMessageBox.information(window, "Session Started", "A simulated session has been logged.")

    layout = QVBoxLayout()
    export_button = QPushButton("Export Session Logs")
    export_button.clicked.connect(ask_user)
    open_button = QPushButton("Open Log Folder")
    open_button.clicked.connect(open_logs)
    start_button = QPushButton("Start Simulated Session")
    start_button.clicked.connect(start_session)
    clear_button = QPushButton("Clear Logs")
    clear_button.clicked.connect(clear_logs)

    layout.addWidget(export_button)
    layout.addWidget(open_button)
    layout.addWidget(start_button)
    layout.addWidget(clear_button)

    window.setLayout(layout)
    window.show()
    sys.exit(app.exec_())



if __name__ == "__main__":
    show_export_prompt()
