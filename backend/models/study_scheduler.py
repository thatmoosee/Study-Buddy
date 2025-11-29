from models.base_model import BaseModel


class StudyScheduler(BaseModel):
    def __init__(self, user_id, title, start_time, end_time, id=None):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.start_time = start_time
        self.end_time = end_time

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'start_time': self.start_time,
            'end_time': self.end_time,
        }

    def validate(self):
        if self.start_time > self.end_time:
            raise ValueError('Start time must be before end time')