import datetime

from enum import Flag, Enum


class Status(Flag):
    UNDONE = 0
    DONE = 1


class Category(Enum):
    BACKLOG = 1
    MAINTENANCE = 2
    BIRTHDAY = 3
    READING = 4
    WATCHING = 5
    SHOPPING = 6


class Todo:
    def __init__(self,
                 task,
                 category: Category = Category.BACKLOG,
                 date_added=None,
                 date_completed=None,
                 status: Status = Status.UNDONE,
                 position=None):
        self.task = task
        self.category = category
        self.date_added = date_added or datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        self.date_completed = date_completed
        self.status = status
        self.position = position

    def __repr__(self):
        return f'{self.task}, {self.category}, {self.date_added}, {self.date_completed}, {self.status}, {self.position}'
