#!/usr/bin/env -S pdm run
# /// script
# dependencies = [
#     "markdown-it-py",
#     "rich"
# ]
# ///

"""
do.py: A single-file task runner, similar in spirit to just and xc,
    that is not AI-encumbered and that is not known to be AI-vulnerable.

Tasks are represented by Markdown code blocks with additional
metadata provided after the initial ticks. The `do.py` command
will look for these arguments in a `Do.md` file in the current
working directory.

For example, to
declare a "run" task that depends on a second task called "build":

    ```task run: build
    pdm run python -m main
    ```

Tasks can take variadic arguments, typically to wrap a system command
so as to include common arguments:

    ```task pdm *args:
    pdm --verbose {{args}}
    ```

Tasks can have arguments:

    ```task run $what: build
    pdm run python -m {{what}}
    ```

Tasks can contain comments as lines starting with `#`. Tasks can run other tasks
manually using `!` notation:

    ```task pdm *args:
    pdm --verbose {{args}}
    ```

    ```task run $what: build
    # Ensure that pdm always runs in verbose mode.
    !pdm run python -m {{what}}
    ```
"""

# Note that we do not rely on argparse or click here,
# as it's simpler to just treat argv as a list of targets.

import sys
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from textwrap import dedent 
from string import Template
import subprocess

from markdown_it import MarkdownIt
from markdown_it.tree import SyntaxTreeNode

from rich.console import Console
from rich.text import Text

## GLOBALS ##

logger = logging.getLogger(__name__)
console = Console()

## DATA MODEL ##

@dataclass(frozen=True)
class Invocation:
    dofile: Path
    targets: tuple[str, ...]
    log_level: int = logging.INFO

@dataclass(frozen=True)
class Argument:
    name: str

    def __str__(self):
        return f"${self.name}"

@dataclass(frozen=True)
class VariadicArguments:
    name: str

    def __str__(self):
        return f"*{self.name}"

def parse_arg_spec(spec):
    if spec.startswith("$"):
        return Argument(spec.removeprefix("$"))

    if spec.startswith("*"):
        return VariadicArguments(spec.removeprefix("*"))

    raise ValueError(f"Argument specifier {spec[0]} not known, must be either $ or *.")

@dataclass
class Command:
    command: str

@dataclass
class TaskCall:
    name: str
    args: tuple[str, ...]

@dataclass
class Comment:
    comment: str    

def parse_command(line):
    if line.startswith("#"):
        return Comment(line.removeprefix("#").strip())

    if line.startswith("!"):
        name, args = line.removeprefix("!").split(" ", 1)
        return TaskCall(
            name=name,
            args=tuple([
                arg
                for arg in args.split(" ")
                if arg
            ])
        )

    return Command(line)


@dataclass(frozen=True)
class Task:
    name: str
    args_decl: tuple[str, ...]
    dependencies: tuple[str, ...]
    commands: tuple[Command | TaskCall | Comment, ...]
    docstring: Optional[str] = None

    @classmethod
    def from_fence(cls, fence):
        info = fence.info.strip().removeprefix("task ").strip()
        if ":" in info:
            decl, dependencies = info.split(":", 1)
            dependencies = tuple([
                dependency
                for dependency in dependencies.split(" ")
                if dependency
            ])
        else:
            decl = info.strip()
            dependencies = ()
        
        if " " in decl:
            name, args_decl = decl.split(" ")
        else:
            name = decl.strip()
            args_decl = ""

        commands = list(
            parse_command(line)
            for line in dedent(fence.content).split("\n")
            if line
        )

        # Pop commands from the beginning until we get a non-comment.
        doccomments = []
        while commands and isinstance(commands[0], Comment):
            doccomments.append(commands.pop(0))

        docstring = (
            " ".join(comment.comment for comment in doccomments)
            if doccomments
            else None
        )


        return cls(
            name=name,
            args_decl=tuple(
                parse_arg_spec(arg)
                for arg in args_decl.split(" ")
                if arg
            ),
            dependencies=dependencies,
            commands=tuple(commands),
            docstring=docstring
        )

@dataclass(frozen=True)
class Step:
    task: Task
    arguments: tuple[str, ...]

@dataclass(frozen=True)
class Plan:
    steps: tuple[Step, ...]

    def complete(self, from_tasks, assume=None):
        assume = [] if assume is None else assume
        for idx, step in enumerate(self.steps):
            deps = step.task.dependencies
            for dep in deps:
                # Have we assumed that this dependency
                # has already been completed?
                if dep in assume:
                    logger.debug(f"assuming {dep} as needed by {step} has already been completed; skipping")
                    break
                
                # Has this dependency already been added
                # to the plan?
                predecessors = self.steps[:idx]
                good = False
                for pre in predecessors:
                    if pre.task.name == dep:
                        logger.debug(f"{dep} as needed by {step} is already in plan; skipping")
                        good = True
                        break

                if not good:
                    logger.debug(f"{dep} as needed by {step} is not in plan; adding")
                    new_steps = predecessors + (Step(
                        task=from_tasks[dep],
                        arguments=()
                    ), ) + self.steps[idx:]
                    return Plan(new_steps).complete(from_tasks)

        # If we made it thus far, we didn't have to append any dependencies, and we're good to
        # go.
        return self


## PARSERS ##

def parse_argv():
    argv = sys.argv[1:]
    dofile = Path.cwd() / "Do.md"
    targets = []
    kwargs = {}
    
    # This is the worst way to write a for loop in Python,
    # but makes it somewhat easy to "eat" arguments to flags.
    idx = 0
    while idx < len(argv):
        if argv[idx] == "--":
            idx += 1
            targets = argv[idx:]
            break

        if not argv[idx].startswith("--"):
            targets = argv[idx:]
            break

        if argv[idx].strip() == "--dofile":
            idx += 1
            dofile = Path(argv[idx])

        if argv[idx].strip() == "--debug":
            kwargs["log_level"] = logging.DEBUG

        if argv[idx].strip() == "--help":
            # Bail and print help.
            print_help()
            sys.exit(0)

        idx += 1

    return Invocation(
        dofile=dofile,
        targets=tuple(targets),
        **kwargs
    )

def extract_fences(node):
    if node.type == "fence":
        info = node.info.strip()
        if info.startswith("task"):
            yield node

    for child in node.children:
        yield from extract_fences(child)

def parse_dofile(dofile):
    md = MarkdownIt("commonmark")
    with open(dofile, "r") as f:
        tokens = md.parse(f.read())
    
    node = SyntaxTreeNode(tokens)
    tasks = {
        task.name: task 
        for task in map(Task.from_fence, extract_fences(node))
    }

    return tasks

## EXECUTORS ##

def build_args_mapping(task, args):
    mapping = {}
    for idx, arg_spec in enumerate(task.args_decl):
        match arg_spec:
            case Argument(name):
                mapping[name] = args[idx]

            case VariadicArguments(name):
                mapping[name] = " ".join(args[idx:])
                break

    return mapping

def execute_task(task, args, workdir, tasks, completed, level):
    args_map = build_args_mapping(task, args)
    def expand(s) -> str:
        return Template(s).safe_substitute(args_map)

    logger.debug(f"would execute {task} with {args}:")
    if level == 0:
        text = Text(task.name)
        text.stylize("purple bold")
        console.print(text)
    for command in task.commands:
        match command:
            case Comment(comment):
                text = Text(f"# {comment}")
                text.stylize("bold green")
                console.print(text)

            case Command(command):
                expanded = expand(command)
                text = Text(f"$ {expanded}")
                text.stylize("bold")
                console.print(text)
                proc = subprocess.Popen(expanded, shell=True, cwd=workdir)
                proc.wait()

            case TaskCall(subtask, subargs):
                subargs = tuple(map(expand, subargs))
                text = Text(f"$ do {subtask} {' '.join(subargs)}")
                text.stylize("bold blue")
                console.print(text)
                subplan = Plan(steps=(
                    Step(
                        task=tasks[subtask],
                        arguments=subargs
                    ),
                )).complete(tasks, assume=completed)
                logger.debug(f"subtask plan: {subplan}")
                execute_plan(subplan, tasks, workdir, completed, level=level + 1)

            case _ as unknown:
                raise RuntimeError(unknown)

    if level == 0 and task.commands:
        print()

def execute_plan(plan, tasks, workdir, completed=None, level=0):
    completed = [] if completed is None else completed
    for step in plan.steps:
        execute_task(step.task, step.arguments, workdir, tasks, completed, level)
        completed.append(step.task.name)
        logger.debug(f"completed = {completed}")

## MAIN COMMAND ##

def print_help():
    print(dedent("""
    Usage: pdm run [OPTIONS] do.py TARGETS

    Options:

    --dofile PATH: Path to the Markdown file containing tasks
                   (default = "./Do.md").
    --debug: Activates additional logging.
    """))

def print_targets(inv, tasks):
    print(dedent(f"""
    Usage: pdm run [OPTIONS] do.py TARGETS

    Targets loaded from {inv.dofile}:
    """))
    for name, task in sorted(tasks.items(), key=(lambda i: i[0])):
        spec = f"{name}"
        if task.args_decl:
            spec += f" {' '.join(str(arg) for arg in task.args_decl)}"
        if task.docstring:
            print(f"{spec}: {task.docstring}")

        else:
            print(spec)

def main():
    inv = parse_argv()
    tasks = parse_dofile(inv.dofile)
    workdir = inv.dofile.parent

    logging.basicConfig(level=inv.log_level)

    # If there's no targets given, print a list of valid tasks.
    if not inv.targets:
        print_targets(inv, tasks)
        return

    # Either inv.targets is a single task followed by one or more
    # arguments, or a list of targets. To tell which, we look at
    # the first task in targets and see if it has any arguments.
    first_task = tasks[inv.targets[0]]
    if first_task.args_decl:
        plan = Plan(steps=(Step(
            task=first_task,
            arguments=tuple(inv.targets[1:])
        ),))
    else:
        plan = Plan(steps=tuple(
            Step(task=tasks[target], arguments=())
            for target in inv.targets
        ))

    plan = plan.complete(tasks)

    execute_plan(plan, tasks, workdir)
    

if __name__ == "__main__":
    main()
