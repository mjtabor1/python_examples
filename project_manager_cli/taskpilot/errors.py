

class TaskPilotError(Exception):
  """Base class for every error TaskPilot raises on purpose."""


class ProjectNotFoundError(TaskPilotError):
  """Raised when we look up a project name that doesn't exist."""

  def __init__(self, name: str):
    # LESSON: super().__init__(...) runs the PARENT class's __init__.
    # Exception's __init__ stores the message, so str(error) shows it.
    super().__init__(f"No project named '{name}'. Try: taskpilot project list")
    self.name = name


class ProjectExistsError(TaskPilotError):
  """Raised when creating a project whose name is already taken."""

  def __init__(self, name: str):
    super().__init__(f"A project named '{name}' already exists.")
    self.name = name


class TaskNotFoundError(TaskPilotError):
  """Raised when we look up a task ID that doesn't exist."""

  def __init__(self, task_id: int):
    super().__init__(f"No task with ID #{task_id}.")
    self.task_id = task_id


class AIUnavailableError(TaskPilotError):
  """Raised when the local AI model (Ollama) can't be reached or used."""