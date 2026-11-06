
from rich.console import Console
from rich.markup import escape
from rich.table import Table
from rich.panel import Panel

from taskpilot.project import Project
from taskpilot.models import Priority, Status, Task


class Display:
  # LESSON: Dictionaries as lookup tables. Much tidier than if/elif chains.
  PRIORITY_STYLES = {
      Priority.HIGH: "bold red",
      Priority.MEDIUM: "yellow",
      Priority.LOW: "green",
  }
  STATUS_ICONS = {
      Status.TODO: "[dim]○[/dim]",
      Status.IN_PROGRESS: "[cyan]◐[/cyan]",
      Status.DONE: "[green]✔[/green]",
  }

  def __init__(self, console: Console | None = None):
    self.console = console or Console()

  # --- Simple messages ---------------------------------------------------
 
  # These messages often contain user text (titles, names), so we escape
  # the whole message. Only the icon in front is styled.
  def success(self, message: str) -> None:
      self.console.print(f"[green]✔[/green] {escape(message)}")

  def info(self, message: str) -> None:
      self.console.print(f"[cyan]ℹ[/cyan] {escape(message)}")

  def error(self, message: str) -> None:
      self.console.print(f"[bold red]Error:[/bold red] {escape(message)}")

  def thinking(self, message: str = "Thinking..."):
      """A spinner to show while we wait on something slow (like the AI).

      Use it with `with display.thinking(): ...`. The spinner stops
      automatically when the `with` block ends.
      """
      return self.console.status(message, spinner="dots")

  # --- Projects ----------------------------------------------------------
 
  def projects_table(self, projects: list[Project]) -> None:
      if not projects:
          self.info('No projects yet. Create one with: taskpilot project add "My Project"')
          return

      table = Table(title="Your Projects", header_style="bold magenta")
      table.add_column("Project", style="bold")
      table.add_column("Description")
      table.add_column("Tasks", justify="right")
      table.add_column("Progress")

      for project in projects:
          overdue = len(project.overdue_tasks())
          task_count = str(len(project))
          if overdue:
              task_count += f" [red]({overdue} overdue)[/red]"
          table.add_row(
              escape(project.name),
              escape(project.description) or "[dim]—[/dim]",
              task_count,
              self._progress_bar(project.progress),
          )
      self.console.print(table)

  def project_detail(self, project: Project) -> None:
      header = f"[bold]{escape(project.name)}[/bold]"
      if project.description:
          header += f"\n[dim]{escape(project.description)}[/dim]"
      header += f"\n{self._progress_bar(project.progress)}"
      self.console.print(Panel(header, expand=False))
      self.tasks_table(project.sorted_tasks())

  # --- Tasks -------------------------------------------------------------
 
  def tasks_table(self, tasks: list[Task]) -> None:
      if not tasks:
          self.info("No tasks here yet. Add one with: taskpilot task add <project> \"Title\"")
          return

      table = Table(header_style="bold magenta")
      table.add_column("ID", justify="right", style="dim")
      table.add_column("", justify="center")  # status icon
      table.add_column("Task")
      table.add_column("Priority")
      table.add_column("Details")

      for task in tasks:
          # LESSON: POLYMORPHISM in action. We call task.details() and
          # task.is_overdue() on every task. A plain Task, a DeadlineTask
          # and a RecurringTask each answer differently, and this code
          # never needs an `if isinstance(...)` check.
          parts = []
          if task.details():
              style = "bold red" if task.is_overdue() else "default"
              parts.append(f"[{style}]{escape(task.details())}[/{style}]")
          for tag in task.tags:
              parts.append(f"[blue]#{escape(tag)}[/blue]")
          details = " ".join(parts)

          title = escape(task.title)
          if task.is_done:
              title = f"[strike dim]{title}[/strike dim]"

          style = self.PRIORITY_STYLES[task.priority]
          table.add_row(
              str(task.id),
              self.STATUS_ICONS[task.status],
              title,
              f"[{style}]{task.priority}[/{style}]",
              details,
          )
      self.console.print(table)