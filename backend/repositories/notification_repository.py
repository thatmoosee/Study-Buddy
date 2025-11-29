"""
Notification repository for managing user notifications

Built by: Josh Topp
"""

import json
import os

from models.notification import Notification
from models import notification
from repositories.base_repository import BaseRepository


class NotificationRepository(BaseRepository):

    def __init__(self, json_file):
        self._json_file = os.path.abspath(json_file)
        self._storage = {}
        self._id_counter = 1
        self._load_from_file()

    def _load_from_file(self):
        try:
            with open(self._json_file, 'r') as f:
                data = json.load(f)
            for n in data.values():
                notif = Notification(
                    user_id=n['user_id'],
                    message=n['message'],
                    read=n.get('read', False),
                    id=n['id'],
                    created_at=None
                )
                self._storage[notif.id] = notif
                self._id_counter += 1
        except:
            self._storage = {}

    def _save_to_file(self):
        directory = os.path.dirname(self._json_file)
        if directory:
            os.makedirs(directory, exist_ok=True)

        data = {str(notifications.id): {
            'id' : notifications.id,
            'user_id': notifications.user_id,
            'message': notifications.message,
            'read': notifications.read,
            'created_at': notifications.created_at
        } for notifications in self._storage.values()}

        with open(self._json_file, 'w') as f:
            json.dump(data, f, indent=4)

    def find_by_user_id(self, user_id):
        for user in self._storage.values():
            if user.user_id == user_id:
                return user
        return None

    def create(self, notification):
        notification.id = self._id_counter
        self._id_counter += 1
        self._storage[notification.id] = notification
        self._save_to_file()
        return notification

    def mark_as_read(self, notification_id):
        if notification_id not in self._storage:
            self._storage[notification_id].read = True
            self._save_to_file()
            return self._storage[notification_id]
        raise ValueError("Notification not found")

    def find_by_id(self, notification_id):
        pass

    def find_all(self):
        pass