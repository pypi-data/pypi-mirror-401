"""Loadability check for Synapse custom components."""
import importlib
import json
import sys
from pathlib import Path
from traceback import TracebackException

import click


@click.command()
@click.argument('modulename', required=True, type=str)
@click.argument('path', default=Path(), type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path))
def main(path: Path, modulename: str) -> None:
    """Check loadability of specified module."""
    # Importパスの追加
    current_dir = Path(__file__).parent
    sys.path.append(str(current_dir / 'synapse_fw'))
    sys.path.append(str(path.absolute()))

    result = {}
    # ユーザーカスタムコンポーネントのimport.
    try:
        mod = importlib.import_module(modulename)

        # 正常系のレスポンス
        result['name'] = mod.HiveComponent._hive_name # noqa: SLF001
        result['uuid'] = mod.HiveComponent._hive_uuid # noqa: SLF001
        result['tag'] = mod.HiveComponent._hive_tag # noqa: SLF001
        result['inports'] = mod.HiveComponent._hive_inports # noqa: SLF001
        result['outports'] = mod.HiveComponent._hive_outports # noqa: SLF001
    except Exception as exc: # noqa: BLE001
        # ロード失敗時のレスポンス
        formatted = TracebackException.from_exception(exc).format()
        result['exception'] = ''.join(formatted)

    sys.stdout.write(json.dumps(result, indent=2, ensure_ascii=False))
    sys.stdout.write('\n')


if __name__ == '__main__':
    main()
