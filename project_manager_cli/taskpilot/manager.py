from datetime import date

from taskpilot.project import Project
from taskpilot.storage import Storage
from taskpilot.errors import ProjectExistsError, ProjectNotFoundError, TaskNotFoundError
from taskpilot.models import DeadlineTask, Priority, RecurringTask, Task

class ProjectManager:

  def __init__(self, storage: Storage):
    self.storage = storage
    self.projects: list[Project] = storage.load()

  def save(self) -> None:
    # Simple rule: every method that CHANGES data calls save() at the end.
    self.storage.save(self.projects)

   # --- Projects ----------------------------------------------------------
 
  def create_project(self, name: str, description: str = "") -> Project:
      if self._find_project(name) is not None:
          raise ProjectExistsError(name)
      project = Project(name, description)
      self.projects.append(project)
      self.save()
      return project

  def get_project(self, name: str) -> Project:
      project = self._find_project(name)
      if project is None:
          raise ProjectNotFoundError(name)
      return project

  def remove_project(self, name: str) -> Project:
      project = self.get_project(name)
      self.projects.remove(project)
      self.save()
      return project

  def _find_project(self, name: str) -> Project | None:
      # LESSON: A leading underscore marks a "private" helper method.
      # It's for use inside this class, not by the CLI.
      for project in self.projects:
          if project.matches(name):
              return project
      return None


  # --- Tasks -------------------------------------------------------------
 
  def add_task(
      self,
      project_name: str,
      title: str,
      priority: Priority = Priority.MEDIUM,
      due_date: date | None = None,
      frequency: str | None = None,
      tags: list[str] | None = None,
  ) -> Task:
      project = self.get_project(project_name)
      task = self._build_task(title, priority, due_date, frequency, tags)
      project.add_task(task)
      self.save()
      return task

  def _build_task(self, title, priority, due_date, frequency, tags) -> Task:
      """Decide WHICH kind of Task to create.

      LESSON: This is a tiny FACTORY: one place that knows which class to
      build. Callers just describe what they want; they never write
      `DeadlineTask(...)` themselves.
      """
      common = {"task_id": self._next_task_id(), "priority": priority, "tags": tags or []}
      if due_date is not None:
          return DeadlineTask(title, due_date, **common)
      if frequency is not None:
          return RecurringTask(title, frequency, **common)
      return Task(title, **common)

  def _next_task_id(self) -> int:
      """Task IDs are unique across ALL projects, so `task done 7` is never ambiguous."""
      highest = 0
      for project in self.projects:
          for task in project:  # works because Project defines __iter__
              highest = max(highest, task.id or 0)
      return highest + 1

  def find_task(self, task_id: int) -> tuple[Project, Task]:
      for project in self.projects:
          task = project.get_task(task_id)
          if task is not None:
              return project, task
      raise TaskNotFoundError(task_id)

  def start_task(self, task_id: int) -> Task:
      _, task = self.find_task(task_id)  # `_` = "I don't need this value"
      task.start()
      self.save()
      return task

  def complete_task(self, task_id: int) -> Task:
      _, task = self.find_task(task_id)
      task.complete()  # polymorphism: RecurringTask resets, others become DONE
      self.save()
      return task

  def remove_task(self, task_id: int) -> Task:
      project, task = self.find_task(task_id)
      project.remove_task(task_id)
      self.save()
      return task