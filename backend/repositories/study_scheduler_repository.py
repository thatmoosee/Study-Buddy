import json
import os
from sched import scheduler

from models.study_scheduler import StudyScheduler

from backend.repositories.base_repository import BaseRepository


class StudySchedulerRepository(BaseRepository):
    def __init__(self, json_file):
        self._json_file = os.path.abspath(json_file)
        self._storage = {}
        self._id_counter = 1
        self._load_from_file()

    def _load_from_file(self):
        try:
            with open(self._json_file, 'r') as f:
                data = json.load(f)
            for s in data.values():
                scheduler = StudyScheduler(
                    user_id=s['user_id'],
                    title=s['title'],
                    start_time=s['start_time'],
                    end_time=s['end_time'],
                    id=s['id']
                )
                self._storage[scheduler.id] = scheduler
                if scheduler.id >= self._id_counter:
                    self._id_counter = scheduler.id + 1
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"No existing schedule data or error loading: {e}")
            self._storage = {}
            self._id_counter = 1

    def _save_to_file(self):
        directory = os.path.dirname(self._json_file)
        if directory:
            os.makedirs(directory, exist_ok=True)

        data = {str(schedule.id): {
            'id': schedule.id,
            'user_id': schedule.user_id,
            'title': schedule.title,
            'start_time': schedule.start_time,
            'end_time': schedule.end_time
        } for schedule in self._storage.values()}

        with open(self._json_file, 'w') as f:
            json.dump(data, f, indent=4)


    def create(self, schedule):
        schedule.id = self._id_counter
        self._id_counter += 1
        self._storage[schedule.id] = schedule
        self._save_to_file()
        return schedule


    def find_by_user_id(self, user_id):
        for schedule in self._storage.values():
            if schedule.user_id == user_id:
                return schedule
        return None


    def find_all(self):
        return list(self._storage.values())

    def find_by_id(self, id):
        return self._storage.get(id)