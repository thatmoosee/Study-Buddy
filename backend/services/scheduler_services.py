from repositories.study_scheduler_repository import StudySchedulerRepository
from models.study_scheduler import StudyScheduler

class SchedulerService:
    def __init__(self, study_session_repository):
        self.study_session_repository = study_session_repository

    def create_study_scheduler(self, user_id, title, start_time, end_time):
        session = StudyScheduler(
            user_id=user_id,
            title=title,
            start_time=start_time,
            end_time=end_time,

        )
        return self.study_session_repository.create(session)

    def get_sessions(self, user_id):
        return self.study_session_repository.find_by_user_id(user_id)