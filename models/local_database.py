import json
import os
from .database_interface import DatabaseInterface


class LocalDatabase(DatabaseInterface):
    def __init__(self, file_path='local_DataBase.json'):
        self.file_path = file_path
        self._initialize_database()

    def _initialize_database(self):
        """Ensure the database file exists."""
        if not os.path.exists(self.file_path):
            self._write_data([])

    def enqueue_data(self, data: dict):
        """Add a new item to the database."""
        content = self._read_data()
        content.append(data)
        self._write_data(content)

    def dequeue_data(self) -> dict:
        """Remove and return the first item from the database."""
        content = self._read_data()
        if content:
            item = content.pop(0)
            self._write_data(content)
            return item
        return None

    def get_all_data(self) -> list:
        """Return all items from the database."""
        return self._read_data()

    def _read_data(self) -> list:
        """Read and return the data from the file."""
        try:
            with open(self.file_path, 'r') as db_file:
                return json.load(db_file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _write_data(self, content: list):
        """Write data to the file atomically."""
        temp_file = f"{self.file_path}.tmp"
        with open(temp_file, 'w') as db_file:
            json.dump(content, db_file, indent=4)
        os.replace(temp_file, self.file_path)
