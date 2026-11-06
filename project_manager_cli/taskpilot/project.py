
from datetime import datetime
from taskpilot.errors import TaskNotFoundError
from taskpilot.models import Task, task_from_dict


class Project:
  def __init__(self, name, description="", tasks: list[Task] | None = None, created_at=None):
    self.name = name
    self.description = description
    self._tasks: list[Task] = tasks if tasks is not None else []
    self.created_at = created_at or datetime.now()

  @property
  def name(self):
    return self._name
  
  @name.setter
  def name(self, value):
    cleaned_value = value.strip()
    if not cleaned_value:
      raise ValueError("A project needs a name.")
    self._name = cleaned_value
  
  @property
  def tasks(self):
    """A read-only view of the tasks in the project.
    
    We return a tuple so nobody can do 'projects.tasks.append(...)' and modify the internal list of tasks directly.
    """
    return tuple(self._tasks)  # Return a tuple to prevent external modification
  

  def add_task(self, task):
    if not isinstance(task, Task):
      raise TypeError("Only Task instances can be added to a project.")
    self._tasks.append(task)
    return task # Return the added task for convenience

  def get_task(self, task_id: int) -> Task | None:
    for task in self._tasks:
      if task.id == task_id:
        return task
    return None

  def remove_task(self, task_id: int) -> Task:
    task = self.get_task(task_id)
    if task is None:
      raise TaskNotFoundError(task_id)
    self._tasks.remove(task)
    return task

  def open_tasks(self) -> list[Task]:
    return [task for task in self._tasks if not task.is_done]

  def done_tasks(self) -> list[Task]:
    return [task for task in self._tasks if task.is_done]

  def overdue_tasks(self) -> list[Task]:
    return [task for task in self._tasks if task.is_overdue()]

  def sorted_tasks(self) -> list[Task]:
    """Open tasks first, then highest priority first.
 
    LESSON: `key=` tells sorted() WHAT to sort by. Returning a tuple sorts
    by the first item, then breaks ties with the second. False sorts
    before True, so not-done tasks come first. The minus sign flips
    priority so HIGH (3) comes before LOW (1).
    """
    return sorted(self._tasks, key=lambda task: (task.is_done, -task.priority.value))

  @property
  def progress(self) -> float:
    """Fraction of tasks done, from 0.0 to 1.0."""
    if not self._tasks:
      return 0.0
    return len(self.done_tasks()) / len(self._tasks)

  def matches(self, name: str) -> bool:
    """Case-insensitive name check, so 'Website' finds 'website'."""
    return self.name.lower() == name.strip().lower()

  def __len__(self) -> int:
    return len(self._tasks)  # Return the number of tasks in the project

  def __str__(self) -> str:
    return f"{self.name} ({len(self)} tasks, {self.progress:.0%} done)"

  def __repr__(self) -> str:
    return f"Project(name={self.name!r}, tasks={len(self)})"

  def to_dict(self) -> dict:
    return {
      "name": self.name,
      "description": self.description,
      "created_at": self.created_at.isoformat(),
      # Each task knows how to turn ITSELF into a dict (polymorphism!)
      "tasks": [task.to_dict() for task in self._tasks],
    }

  @classmethod
  def from_dict(cls, data: dict) -> "Project":
    return cls(
      name=data["name"],
      description=data.get("description", ""),
      tasks=[task_from_dict(task_data) for task_data in data.get("tasks", [])],
      created_at=datetime.fromisoformat(data["created_at"]),
    )