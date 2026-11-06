from abc import ABC, abstractmethod
import json
from pathlib import Path

from taskpilot.project import Project
from taskpilot.errors import TaskPilotError

class Storage(ABC):
  """The CONTRACT every storage backend must follow"""

  @abstractmethod
  def load(self) -> list[Project]:
    """return every saved project."""

  @abstractmethod
  def save(self, projects: list[Project]) -> None:
    """persist every project."""


class JSONStorage(Storage):
  FILE_VERSION = 1

  def __init__(self, path: str | Path):
    self.path = Path(path)

  def load(self) -> list[Project]:
    if not self.path.exists():
      return []  # first run: nothing saved yet
    try:
      data = json.loads(self.path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
      raise TaskPilotError(f"Couldn't read {self.path}: the file isn't valid JSON ({error}).") from None
    return [Project.from_dict(item) for item in data.get("projects", [])]

  def save(self, projects: list[Project]) -> None:
    # Create the folder (e.g. ~/.taskpilot/) if it doesn't exist yet.
    self.path.parent.mkdir(parents=True, exist_ok=True)
    data = {
      "version": self.FILE_VERSION,
      "projects": [project.to_dict() for project in projects],
    }
    self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")

  def __repr__(self) -> str:
    return f"JSONStorage(path={str(self.path)!r})"


class MemoryStorage(Storage):
  """Keeps projects in memory only. Nothing touches the disk.

  Used by the tests. This is the PAYOFF of abstraction: ProjectManager works
  with either storage class without changing a single line.
  """

  def __init__(self, projects: list[Project] | None = None):
    self._projects = list(projects) if projects else []
    self.save_count = 0  # handy for tests: "did the manager save?"

  def load(self) -> list[Project]:
    return list(self._projects)

  def save(self, projects: list[Project]) -> None:
    self._projects = list(projects)
    self.save_count += 1


  