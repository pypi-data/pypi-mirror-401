import os
import json
import base64
import hashlib
from kivy.app import App
from cryptography.fernet import Fernet


class EasyDB:
    def __init__(self, name, password):
        app = App.get_running_app()
        base_dir = os.path.join(app.user_data_dir, "easydb_data")
        os.makedirs(base_dir, exist_ok=True)

        self.path = os.path.join(base_dir, f"{name}.db")
        self.key = self._make_key(password)
        self.cipher = Fernet(self.key)

        if not os.path.exists(self.path):
            self.data = {}
            self._save()
        else:
            self._safe_load()

    def _make_key(self, password):
        digest = hashlib.sha256(password.encode()).digest()
        return base64.urlsafe_b64encode(digest)

    def _safe_load(self):
        try:
            with open(self.path, "rb") as f:
                encrypted = f.read()
                decrypted = self.cipher.decrypt(encrypted)
                self.data = json.loads(decrypted.decode())
        except Exception:
            self.data = {}
            self._save()

    def _save(self):
        raw = json.dumps(self.data, ensure_ascii=False).encode()
        encrypted = self.cipher.encrypt(raw)
        with open(self.path, "wb") as f:
            f.write(encrypted)

    def create(self, table):
        if table not in self.data:
            self.data[table] = []
            self._save()
        return self

    def add(self, table, record: dict):
        if table not in self.data:
            self.create(table)

        record["id"] = len(self.data[table]) + 1
        self.data[table].append(record)
        self._save()
        return record["id"]

    def all(self, table):
        return self.data.get(table, [])

    def find(self, table, **filters):
        return [
            item for item in self.data.get(table, [])
            if all(item.get(k) == v for k, v in filters.items())
        ]

    def delete(self, table, record_id):
        if table not in self.data:
            return 0

        for item in self.data[table]:
            if item.get("id") == record_id:
                self.data[table].remove(item)
                self._save()
                return 1
        return 0

    def update(self, table, record_id, **updates):
        if table not in self.data:
            return 0

        for item in self.data[table]:
            if item.get("id") == record_id:
                item.update(updates)
                self._save()
                return 1
        return 0