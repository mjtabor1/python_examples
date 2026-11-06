

import argparse
from datetime import date
from pathlib import Path
from taskpilot import __version__
from taskpilot.errors import TaskPilotError
from taskpilot.storage import JSONStorage
from taskpilot.display import Display
from taskpilot.manager import ProjectManager
from taskpilot.models import Priority, RecurringTask


DEFAULT_DATA_FILE = Path.home() / ".taskpilot" / "data.json"


class TaskPilotCLI:
  """A collection of tasks, with methods to add, remove, and list them."""

  def __init__(self, manager: ProjectManager, display: Display):
    self.manager = manager
    self.display = display

  # --- project commands ---------------------------------------------------
 
  def project_add(self, args) -> None:
    project = self.manager.create_project(args.name, args.description)
    self.display.success(f"Created project '{project.name}'")

  def project_list(self, args) -> None:
    self.display.projects_table(self.manager.projects)

  def project_show(self, args) -> None:
    self.display.project_detail(self.manager.get_project(args.name))

  def project_remove(self, args) -> None:
    project = self.manager.remove_project(args.name)
    self.display.success(f"Removed project '{project.name}' and its {len(project)} task(s)")

  # --- task commands ------------------------------------------------------
 
  def task_add(self, args) -> None:
    task = self.manager.add_task(
        args.project,
        args.title,
        priority=Priority.from_string(args.priority),
        due_date=args.due,
        frequency=args.repeat,
        tags=args.tag,
    )
    self.display.success(f"Added task #{task.id}: {task.title}")

  def task_start(self, args) -> None:
    task = self.manager.start_task(args.task_id)
    self.display.success(f"Started #{task.id}: {task.title}")

  def task_done(self, args) -> None:
    task = self.manager.complete_task(args.task_id)
    if isinstance(task, RecurringTask):
      self.display.success(f"Nice! #{task.id} done {task.times_completed}x. It'll be back {task.frequency}.")
    else:
      self.display.success(f"Completed #{task.id}: {task.title} 🎉")

  def task_remove(self, args) -> None:
    task = self.manager.remove_task(args.task_id)
    self.display.success(f"Removed #{task.id}: {task.title}")


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------
 
 
def parse_date(text: str) -> date:
    """argparse `type=` function: turns '2026-11-20' into a date object.
 
    LESSON: argparse calls this for us. Raising ArgumentTypeError makes
    argparse print a clean usage error instead of a traceback.
    """
    try:
        return date.fromisoformat(text)
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{text}' isn't a valid date. Use YYYY-MM-DD, e.g. 2026-11-20") from None
 
 
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="taskpilot",
        description="TaskPilot: manage personal projects and tasks from your terminal.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument(
        "--data",
        type=Path,
        default=DEFAULT_DATA_FILE,
        help=f"where to save your data (default: {DEFAULT_DATA_FILE})",
    )
    groups = parser.add_subparsers(dest="group", required=True, metavar="{project,task,ai}")
 
    # LESSON: set_defaults(handler=TaskPilotCLI.project_add) stores the
    # FUNCTION itself (no parentheses = not called yet). Later, main() calls
    # it as args.handler(cli, args). That's exactly what cli.project_add(args)
    # does behind the scenes: Python passes the object in as `self`.
 
    # ---- taskpilot project ... ----
    project = groups.add_parser("project", help="create, list, show and remove projects")
    project_cmds = project.add_subparsers(dest="command", required=True)
 
    p = project_cmds.add_parser("add", help="create a new project")
    p.add_argument("name")
    p.add_argument("-d", "--description", default="", help="a short description")
    p.set_defaults(handler=TaskPilotCLI.project_add)
 
    p = project_cmds.add_parser("list", help="list all projects")
    p.set_defaults(handler=TaskPilotCLI.project_list)
 
    p = project_cmds.add_parser("show", help="show a project and its tasks")
    p.add_argument("name")
    p.set_defaults(handler=TaskPilotCLI.project_show)
 
    p = project_cmds.add_parser("remove", help="delete a project and all its tasks")
    p.add_argument("name")
    p.set_defaults(handler=TaskPilotCLI.project_remove)
 
    # ---- taskpilot task ... ----
    task = groups.add_parser("task", help="add, start, complete and remove tasks")
    task_cmds = task.add_subparsers(dest="command", required=True)
 
    p = task_cmds.add_parser("add", help="add a task to a project")
    p.add_argument("project", help="project name")
    p.add_argument("title", help='task title (use quotes for spaces: "Buy domain")')
    p.add_argument("-p", "--priority", choices=["low", "medium", "high"], default="medium")
    p.add_argument("-t", "--tag", action="append", help="add a tag (repeatable: -t ui -t urgent)")
    # A task can have a due date OR repeat, but not both.
    kind = p.add_mutually_exclusive_group()
    kind.add_argument("--due", type=parse_date, help="due date, YYYY-MM-DD (makes a deadline task)")
    kind.add_argument("--repeat", choices=RecurringTask.FREQUENCIES, help="make it a recurring task")
    p.set_defaults(handler=TaskPilotCLI.task_add)
 
    for name, handler, help_text in [
        ("start", TaskPilotCLI.task_start, "mark a task as in progress"),
        ("done", TaskPilotCLI.task_done, "mark a task as done"),
        ("remove", TaskPilotCLI.task_remove, "delete a task"),
    ]:
        p = task_cmds.add_parser(name, help=help_text)
        p.add_argument("task_id", type=int, help="the task's ID number (shown in `project show`)")
        p.set_defaults(handler=handler)
 
    # ---- taskpilot ai ... (SESSION 5) ----
    # LESSON: a "parent" parser shares arguments (--model) across several
    # subcommands without repeating ourselves.
    # model_option = argparse.ArgumentParser(add_help=False)
    # model_option.add_argument("--model", default=None, help="Ollama model to use (default: llama3.2)")
 
    # ai = groups.add_parser("ai", help="get help from a local AI model (requires Ollama)")
    # ai_cmds = ai.add_subparsers(dest="command", required=True)
 
    # p = ai_cmds.add_parser("suggest", parents=[model_option], help="suggest new tasks for a project")
    # p.add_argument("project")
    # p.add_argument("-n", "--count", type=int, default=5, help="how many ideas (default: 5)")
    # p.add_argument("--add", action="store_true", help="add the suggestions to the project")
    # p.set_defaults(handler=TaskPilotCLI.ai_suggest)
 
    # p = ai_cmds.add_parser("summary", parents=[model_option], help="get a short status report")
    # p.add_argument("project")
    # p.set_defaults(handler=TaskPilotCLI.ai_summary)
 
    # p = ai_cmds.add_parser("ask", parents=[model_option], help="ask a question about a project")
    # p.add_argument("project")
    # p.add_argument("question")
    # p.set_defaults(handler=TaskPilotCLI.ai_ask)
 
    return parser


def main(argv: list[str] | None = None) -> int:
    """Entry point. Returns an exit code: 0 = success, 1 = error.
 
    `argv` lets tests call main(["project", "list"]) directly. When it's
    None, argparse reads the real command line (sys.argv).
    """
    args = build_parser().parse_args(argv)
    display = Display()
 
    try:
        manager = ProjectManager(JSONStorage(args.data))
        cli = TaskPilotCLI(manager, display)
        args.handler(cli, args)
    except TaskPilotError as error:
        # Our own, expected errors: show a friendly message, no traceback.
        display.error(str(error))
        return 1
    except ValueError as error:
        # Validation errors from our models (e.g. an empty title).
        display.error(str(error))
        return 1
    return 0