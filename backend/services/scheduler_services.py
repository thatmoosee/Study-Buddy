"""
Scheduler service for study session management

Built by:
"""
from repositories.study_scheduler_repository import StudySchedulerRepository
from models.study_scheduler import StudyScheduler
from datetime import datetime

class SchedulerService:
    def __init__(self, study_session_repository):
        self.study_session_repository = study_session_repository

    def create_study_scheduler(self, user_id, title, start_time, end_time, group_id=None):
        try:
            start_time = datetime.strptime(start_time, '%Y-%m-%dT%H:%M')
            end_time = datetime.strptime(end_time, '%Y-%m-%dT%H:%M')
            new_start_time = start_time.strftime('%m/%d/%Y %I:%M%p')
            new_end_time = end_time.strftime('%m/%d/%Y %I:%M%p')
        except ValueError:
            raise Exception('Invalid format of start time or end time')
        session = StudyScheduler(
            user_id=user_id,
            title=title,
            start_time= new_start_time,
            end_time= new_end_time,

        )
        return self.study_session_repository.create(session)
    def get_sessions(self):
        return self.study_session_repository.find_all()

    def get_user_sessions(self, user_id):
        return self.study_session_repository.get_sessions_by_user(user_id)

    def delete_session(self, session_id):
        return self.study_session_repository.delete(session_id)

