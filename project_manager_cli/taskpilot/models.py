from datetime import date, datetime
from enum import Enum


class Priority(Enum):
  LOW = 1
  MEDIUM = 2
  HIGH = 3


class Status(Enum):
  TODO = "todo"
  IN_PROGRESS = "in_progress"
  DONE = "done"


class Task:

  kind = "task"  # Class attribute: shared by all instances of the class

  def __init__(self, title, task_id=None, priority=Priority.MEDIUM, status=Status.TODO, created_at=None, tags=None):
    self.title = title # Instance attribute: unique to each instance of the class
    self.id = task_id
    self.priority = priority
    self.status = status

    self.tags = tags if tags is not None else []
    self.created_at = created_at or datetime.now()
  
  @property
  def title(self):
    return self._title
  
  @title.setter
  def title(self, value):
    cleaned_value = value.strip()
    if not cleaned_value:
      raise ValueError("A task needs a title.")
    self._title = cleaned_value
  
  @property
  def is_done(self):
    return self.status is Status.DONE
  
  def start(self):
    if self.is_done:
      raise ValueError("Cannot start a task that is already done.")
    self.status = Status.IN_PROGRESS
  
  def complete(self):
    self.status = Status.DONE

  def is_overdue(self) -> bool:
    """A plain Task has no due date, so it's never overdue.

    LESSON: Subclasses OVERRIDE this method with their own version.
    """
    return False

  def details(self) -> str:
    """Extra info to show next to the title. Subclasses override this."""
    return ""
  
  def to_dict(self):
    return {
      "kind": self.kind,
      "id": self.id,
      "title": self.title,
      "priority": self.priority.name,
      "status": self.status.value,
      "tags": self.tags,
      "created_at": self.created_at.isoformat()
    }
  
  @classmethod
  def from_dict(cls, data):
    return cls(**cls._init_args_from_dict(data))
  
  @classmethod
  def _init_args_from_dict(cls, data):
    """Helper method to initialize a Task instance from a dictionary."""
    return {
      "title": data["title"],
      "task_id": data["id"],
      "priority": Priority[data["priority"]],
      "status": Status(data["status"]),
      "created_at": datetime.fromisoformat(data["created_at"]),
      "tags": data.get("tags", [])
    }

  # --- Dunder ("double underscore") methods -----------------------------
    # LESSON: __str__ is the friendly text for users (print, f-strings).
    #         __repr__ is the unambiguous text for developers (REPL, debugger).
 
  def __str__(self) -> str:
    check = "x" if self.is_done else " "
    return f"[{check}] #{self.id} {self.title} ({self.priority})"

  def __repr__(self) -> str:
    # type(self).__name__ shows the REAL class, e.g. "DeadlineTask"
    return f"{type(self).__name__}(id={self.id!r}, title={self.title!r}, status={self.status})"


class DeadlineTask(Task):

  kind = "deadline"  # Class attribute: shared by all instances of the class

  # LESSON: **kwargs collects any extra keyword arguments into a dictionary 
  # and we pass them straight up to Task. That way we don't have to repeat all the Task init code here.
  def __init__(self, title: str, due_date: date, **kwargs):
    super().__init__(title, **kwargs) # Call the parent class's __init__ method to handle the common attributes
    self.due_date = due_date

  @property
  def days_left(self) -> int:
    return (self.due_date - date.today()).days

  # LESSON: OVERRIDING. Same method name as the parent, new behavior.
  def is_overdue(self) -> bool:
    return not self.is_done and self.days_left < 0

  def details(self) -> str:
    if self.is_done:
      return f"was due {self.due_date:%b %d}"
    if self.days_left < 0:
      return f"OVERDUE by {-self.days_left} day(s)"
    if self.days_left == 0:
      return "due today"
    return f"due in {self.days_left} day(s)"

  def to_dict(self) -> dict:
    data = super().to_dict()
    data["due_date"] = self.due_date.isoformat()

    return data

  @classmethod
  def _init_args_from_dict(cls, data: dict) -> dict:
    args = super()._init_args_from_dict(data)
    args["due_date"] = datetime.fromisoformat(data["due_date"])

    return args


class RecurringTask(Task):
  """A habit-style task (e.g. "water plants") that resets after each completion."""
  kind = "recurring"
  FREQUENCIES = ("daily", "weekly", "monthly")

  def __init__(
    self,
    title: str,
    frequency: str = "weekly",
    times_completed: int = 0,
    last_completed: date | None = None,
    **kwargs,
  ):
    super().__init__(title, **kwargs)
    if frequency not in self.FREQUENCIES:
      raise ValueError(f"Frequency must be one of: {', '.join(self.FREQUENCIES)}")
    self.frequency = frequency
    self.times_completed = times_completed
    self.last_completed = last_completed

  def complete(self) -> None:
    """OVERRIDE: a recurring task is never permanently "done".

    Completing it records the streak and resets it back to TODO,
    ready for next time. Same method name as Task.complete(), very
    different behavior — that's polymorphism in action.
    """
    self.times_completed += 1
    self.last_completed = date.today()
    self.status = Status.TODO

  def details(self) -> str:
    text = f"repeats {self.frequency}, done {self.times_completed}x"
    if self.last_completed:
      text += f" (last {self.last_completed:%b %d})"
    return text

  def to_dict(self) -> dict:
    data = super().to_dict()
    data["frequency"] = self.frequency
    data["times_completed"] = self.times_completed
    data["last_completed"] = self.last_completed.isoformat() if self.last_completed else None
    return data

  @classmethod
  def _init_args_from_dict(cls, data: dict) -> dict:
    args = super()._init_args_from_dict(data)
    args["frequency"] = data["frequency"]
    args["times_completed"] = data.get("times_completed", 0)
    last = data.get("last_completed")
    args["last_completed"] = date.fromisoformat(last) if last else None
    return args



# ---------------------------------------------------------------------------
# Loading the right class back from JSON  (SESSION 3)
# ---------------------------------------------------------------------------
# LESSON: A REGISTRY maps a saved "kind" string to the class that knows how
# to rebuild it. Adding a new task type later = write the class + add one line.

TASK_TYPES = {
  Task.kind: Task,
  DeadlineTask.kind: DeadlineTask,
  RecurringTask.kind: RecurringTask,
}


def task_from_dict(data: dict) -> Task:
  task_class = TASK_TYPES.get(data.get("kind", "task"), Task)
  return task_class.from_dict(data)
