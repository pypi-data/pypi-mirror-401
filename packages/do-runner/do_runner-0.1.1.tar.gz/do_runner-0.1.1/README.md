# do: Simple just- and xc-like task runner

Do is a simple task runner that does not include any AI antifeatures,
and that is not known to be AI-vulnerable.

Like [`just`](https://just.systems), Do makes it easy to define simple
recipes that can take arguments and depend on each other.

Like [`xc`](https://xcfile.dev/), Do pulls tasks from a specially formatted
Markdown file, using code fences to define tasks.

Do is intended to run either as a standalone script, using PEP 723 metadata,
or to be installable as a wheel. Thus, Do consists of a single file, `do.py`,
that can be vendored into projects as necessary, or that can be depended on
as a wheel.

## License and AI Policy

This project is licensed under the MIT license. This license does
not preclude you from using Do with AI-encumbered or AI-vulnerable projects,
but you do not have the author's consent to do so. This may seem like a
contradiction, but copyright is a blunt tool that does not in general
have the humanistic nuance to describe something like
"you can legally do this thing, but if you do, you're an asshole."

Any AI-generated contributions will result in an immediate block.
Don't be that guy.

## Running Do

There are several ways of running `do` itself, depending on your needs.

To run `do` as a Python package, ensure that `do-runner` is installed in your environment (typically by making it a development dependency in your pyproject.toml):

```
python -m do ...
```

To run `do` as a [uv](https://docs.astral.sh/uv/) tool:

```
uvx do-runner
```

To run `do` from a copy vendored into a repo that uses Do:

```
./do.py ...
```

Finally, if Do is installed globally, you can run `do` directly as a command. For shell environments where `do` is a reserved keyword, the aliases `do_` and `go-do` are also defined, such that the following invocations are all identical:

```
do --help
do_ --help
go-do --help
```

In the rest of this README, we'll use `do` to refer to whatever method you use to run `do`.

## Using Do

By default, `do` pulls its list of tasks from a file called `Do.md`.
This can be overriden by passing the `--dofile` argument to `do`:

```
do --dofile=other-do.md
```

When run without arguments, `do` prints a list of valid tasks from
the given dofile.

The main `do` command can be run with either the name of a single task,
possibly followed by arguments to that task, or as a list of
tasks.

For example, if `test` and `build` are distinct tasks in `Do.md`, then
the following will run the `test` and `build` tasks in that order:

```
do test build
```

If `run` is a task that accepts arguments, then the following will run
the `run` task with `python -m do` as its arguments:

```
do run python -m do
```

## Defining Tasks

Tasks are represented by Markdown code blocks with additional
metadata provided after the initial ticks. 

For example, to
declare a "run" task that depends on a second task called "build":

````
```task run: build
pdm run python -m main
```
````

Tasks can take variadic arguments, typically to wrap a system command
so as to include common arguments:

````
```task pdm *args:
pdm --verbose {{args}}
```
````

Tasks can have arguments:

````
```task run $what: build
pdm run python -m {{what}}
```
````

Tasks can contain comments as lines starting with `#`. Tasks can run other tasks
manually using `!` notation:

````
```task pdm *args:
pdm --verbose {{args}}
```
````

````
```task run $what: build
# Ensure that pdm always runs in verbose mode.
!pdm run python -m {{what}}
```
````

