"""
Notification service for user alert management

Built by:
"""

from models.notification import Notification

class NotificationService:
    def __init__(self, repo):
        self.repo = repo

    def send_notification(self, user_id, message):
        notif = Notification(
            user_id=user_id,
            message=message,
        )
        return self.repo.create(notif)

    def send_notification(self, user_id, message):
        notification = Notification(user_id, message)
        return self.repo.create(notification)

    def get_notifications(self, user_id):
        return self.repo.find_by_user_id(user_id)

    def mark_notifications_as_read(self, notif_id):
        return self.repo.mark_notifications_as_read(notif_id)
