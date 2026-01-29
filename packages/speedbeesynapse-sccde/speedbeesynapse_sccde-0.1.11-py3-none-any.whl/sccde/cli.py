"""SpeeDBeeSynapse custom component development environment tool."""
from __future__ import annotations

import sys
import time
from pathlib import Path
from traceback import TracebackException
from typing import TYPE_CHECKING, Any, Final

import click
from watchfiles import BaseFilter, Change, watch

from .errors import SccdeError
from .main import Sccde
from .model import CheckState

if TYPE_CHECKING:

    from collections.abc import Callable

    from .model import ComponentValidity, PackageValidity

PACKAGE_SUFFIX = '.sccpkg'
INDENT = '  '


def _handle_sccde_errors(func: Callable) -> Callable:
    """Handle SCCDE errors."""
    def new_func(*args: Any, **kwargs: Any) -> Any: # noqa: ANN401
        try:
            return func(*args, **kwargs)
        except SccdeError as exc:
            click.echo(str(exc), err=True)
            sys.exit(1)

    new_func.__name__ = func.__name__
    return new_func


@click.group()
def cli() -> None:
    """Make subcommand group."""


@cli.command()
@click.argument('target_dir', required=False, type=click.Path(file_okay=False, dir_okay=True, path_type=Path))
@_handle_sccde_errors
def init(target_dir: Path | None) -> None:
    """Initialize directory."""
    target_dir = target_dir if target_dir else Path()
    sccde = Sccde(target_dir)

    sccde.init('Custom component package example')
    click.echo(f'The directory `{target_dir.absolute()}` is configured for SCCDE.')

    sccde.add_sample('python', 'collector', 'json')
    click.echo('Sample custom component is created.')


@cli.command()
@click.option('-C', default=Path(), type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path))
@click.option('-l', '--sample-language', default='python', type=click.Choice(['c', 'python']))
@click.option('-t', '--sample-type', default='collector', type=click.Choice(['collector', 'serializer', 'emitter']))
@click.option('-u', '--ui_type', default='json', type=click.Choice(['none', 'json', 'html']))
@_handle_sccde_errors
def add(c: Path, sample_language: str, sample_type: str, ui_type: str) -> None:
    """Add sample component."""
    sccde = Sccde(c)
    sccde.add_sample(sample_language, sample_type, ui_type)
    click.echo('Sample custom component is created.')


@cli.command()
@click.option('-C', default=Path(), type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path))
@click.option('-o', '--out', type=click.Path(path_type=Path))
@_handle_sccde_errors
def make_package(c: Path, out: Path | None) -> None:
    """Make package."""
    out = out.with_suffix(PACKAGE_SUFFIX) if out else None
    sccde = Sccde(c)
    sccde.make_package(out)


@cli.command()
@click.option('-C', default=Path(), type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path))
@click.option('-h', '--host', default='127.0.0.1', type=str)
@click.option('-p', '--port', default=8000, type=click.IntRange(1, 65535))
@click.option('--reload/--no-reload', default=False)
@click.option('--verbose', is_flag=True)
@_handle_sccde_errors
def serve(*, c: Path, host: str, port: int, reload: bool, verbose: bool) -> None:
    """Start test server."""
    sccde = Sccde(c)
    server = sccde.server(host, port, verbose=verbose)

    click.echo('Preparing Synapse data directories..')
    with server.start():
        url = f'http://{host}:{port}'
        click.echo(f'Synapse server ready: {url}')
        try:
            if reload:
                click.echo(f'Watch dir {sccde.work_dir} for reloading.')
                for changes in watch(sccde.work_dir, watch_filter=WatchFilter(), step=1000):
                    for (change_type, file) in changes:
                        click.echo(f'{change_type.name}: {file}')
                    sccde.distribute()
                    click.echo('Relocate package file.')
                    click.echo('Please restart Synapse core process in Web-browser window.')
            else:
                while True:
                    time.sleep(0.5)
        except KeyboardInterrupt:
            pass


@cli.command()
@click.option('-C', default=Path(), type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path))
@click.option('-t', '--timeout', default=2.0, type=click.FloatRange(min=0, min_open=True))
@click.option('--load/--no-load', default=True)
@click.argument('target', required=False, type=str)
@_handle_sccde_errors
def check(c: Path, target: str | None, timeout: float, load: bool) -> None:
    """
    Check components consistency.

    output following messages.
        ```
        Custom component package example (deb22cd1-e189-4ae0-884d-38dd72dd7155)
        Version: 0.1.0
        Description: Your package descrition here
        4 components:
          Sample collector(a2e2ed28-404b-4fc8-aca5-20fb03ded110)
            Read: OK
            Syntax: OK
            Load: OK
          Sample emitter(b642ea44-25f4-4908-a5c8-ed7820819a8b)
            Read: OK
            Syntax: NG
              | Traceback (most recent call last):
              |   File "/home/yogi/newhive/tools/sccde/src/sccde/main.py", line 202, in _check_python_syntax
              |     compile(source, str(module_path), 'exec')
              |   File "tmpdir/source/python/sample_emitter_2.py", line 4
              |     mport time
              |           ^
              | SyntaxError: invalid syntax
        ```
    """
    sccde = Sccde(c)
    iecho = IndentEcho('  ')

    if target:
        components = sccde.check([target], load, timeout)
        if not components:
            click.echo(f'No components match "{target}"')
        for compo in components:
            _print_component_consistency(iecho, compo)

        if not all(compo.is_valid for compo in components):
            raise click.ClickException(', '.join(f'"{compo.name}"' for compo in components if not compo.is_valid))
    else:
        consistency = sccde.check_all(load, timeout)
        _print_package_consistency(iecho, consistency)

        if not consistency.is_valid:
            raise click.ClickException(', '.join(f'"{compo.name}"' for compo in consistency.components if not compo.is_valid))


def _print_package_consistency(iecho: IndentEcho, consistency: PackageValidity) -> None:

    iecho(click.style(f'{consistency.name} ', bold=True), click.style(f'({consistency.uuid})', underline=True))
    iecho(f'Version: {consistency.version}')
    iecho(f'Description: {consistency.description}')

    iecho(f'{len(consistency.components)} components:')
    iecho.push()
    for compo in consistency.components:
        _print_component_consistency(iecho, compo)
    iecho.pop()


def _print_component_consistency(iecho: IndentEcho, component: ComponentValidity) -> None:
    iecho(click.style(f'{component.name}', bold=True), (click.style(f'({component.uuid})', underline=True)))

    iecho.push()
    if component.read_check == CheckState.OK:
        iecho('Read: ', click.style('OK', fg='green'))
    elif component.read_check == CheckState.UNCHECKED:
        iecho('Read: NOT CHECKED')
    else:
        iecho('Read: ', click.style('NG', fg='red'))
        iecho.push()
        _print_error_info(iecho, component.read_error)
        iecho.pop()

    if component.syntax_check == CheckState.OK:
        iecho('Syntax: ', click.style('OK', fg='green'))
    elif component.syntax_check == CheckState.UNCHECKED:
        iecho('Syntax: NOT CHECKED')
    else:
        iecho('Syntax: ', click.style('NG', fg='red'))
        iecho.push()
        _print_error_info(iecho, component.syntax_error)
        iecho.pop()

    if component.load_check == CheckState.OK:
        iecho('Load: ', click.style('OK', fg='green'))
    elif component.load_check == CheckState.UNCHECKED:
        iecho('Load: NOT CHECKED')
    else:
        iecho('Load: ', click.style('NG', fg='red'))
        iecho.push()
        _print_error_info(iecho, component.load_error)
        iecho.pop()
    iecho.pop()


def _print_error_info(iecho: IndentEcho, error: None | str | TracebackException) -> None:
    if isinstance(error, TracebackException):
        formatted = ''.join(list(error.format())).replace('\n', f'\n{iecho.current}| ')
        iecho('| '+formatted)
    elif isinstance(error, str):
        formatted = error.replace('\n', f'\n{iecho.current}| ')
        iecho('| '+formatted)
    else:
        pass


class IndentEcho:

    """Indent managed echo."""

    def __init__(self, indent: str):
        """Init."""
        self.indent = indent
        self.lv = 0

    def push(self) -> None:
        """Increment indent level."""
        self.lv += 1

    def pop(self) -> None:
        """Decrement indent level."""
        self.lv -= 1

    def _echo(self, *args) -> None: # noqa: ANN002
        click.echo(self.current, nl=False)
        for arg in args[:-1]:
            click.echo(arg, nl=False)
        click.echo(args[-1])

    def __call__(self, *args) -> None: # noqa: ANN002
        """Echo strings to console."""
        self._echo(*args)

    @property
    def current(self) -> str:
        """Return current indent prefix."""
        return self.indent * self.lv


class WatchFilter(BaseFilter):

    """WatchFilter for watchfiles."""

    extensions: Final[list[str]]  = ['.py', '.so', '.json']

    def __call__(self, _change: Change, path: str) -> bool:
        """Return True if the path is sccde mangement file."""
        if '.synapse' in path:
            return False

        return Path(path).suffix in self.extensions


if __name__ == '__main__':
    cli()
