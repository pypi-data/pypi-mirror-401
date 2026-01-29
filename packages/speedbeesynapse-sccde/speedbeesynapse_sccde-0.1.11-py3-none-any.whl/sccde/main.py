"""SpeeDBeeSynapse custom component development environment tool."""
from __future__ import annotations

import copy
import importlib
import importlib.resources
import json
import subprocess
import sys
import uuid
import warnings
import zipfile
from traceback import TracebackException
from typing import TYPE_CHECKING

from . import pack, utils
from . import resources as sccde_resources
from .errors import AlreadyInitializedError, NotInitializedError, SccInfoNotWritableError
from .model import CheckState, ComponentValidity, PackageValidity
from .server import TestServer

if TYPE_CHECKING:
    from collections.abc import Generator
    from pathlib import Path

INFO_FILE_NAME = 'scc-info.json'
SCC_INFO = {
    'package-name': '',
    'package-version': '0.1.0',
    'package-uuid': '',
    'package-description': 'Your package description here',
    'python-components-source-dir': 'source/python',
    'author': '',
    'license': '',
    'license-file': '',
    'components': {},
}
SERVE_DATA_DIR = '.synapse'


def get_components(info_path: Path) -> list[str]:
    """Return module list for syntax-check."""
    # 環境情報ファイルを読み込み
    with info_path.open(mode='rt', encoding='utf-8') as fo:
        info = json.load(fo)

    # module
    return [ c['modulename'] for c in info['components'].values() ]


class Sccde:

    """Sccde directory management class."""

    def __init__(self, work_dir: Path) -> None:
        """Initialize."""
        self.work_dir = work_dir

    def init(self, package_name: str) -> None:
        """Initialize resource repogitory."""
        self.work_dir.mkdir(parents=True, exist_ok=True)
        if self.__info_path.is_file():
            raise AlreadyInitializedError(self.work_dir)

        info = copy.deepcopy(SCC_INFO)
        info['package-name'] = package_name
        info['package-uuid'] = str(uuid.uuid4())
        self.__save_scc_info(info)

    def add_sample(self, sample_lang: str, sample_type: str, ui_type: str) -> None:
        """Add sample into the current environment."""
        if sample_lang == 'none':
            return

        info = self.__load_scc_info()

        # 追加するサンプルのUUIDの生成、ファイル名サフィックスの決定
        suffix_num = len(info['components']) + 1
        new_uuid = str(uuid.uuid4())

        if sample_lang == 'python':
            # Python用のディレクトリの準備
            python_dir = self.__info_path.parent / info['python-components-source-dir']
            python_dir.mkdir(parents=True, exist_ok=True)

            # Pythonカスタムコンポーネントサンプルのコピー
            with (python_dir / f'sample_{sample_type}_{suffix_num}.py').open(mode='w', encoding='utf-8') as fo:
                with warnings.catch_warnings():
                    warnings.simplefilter('ignore')
                    content = importlib.resources.read_text(sccde_resources, f'sample_{sample_type}.py')
                    content = content.replace('{{REPLACED-UUID}}', new_uuid)
                fo.write(content)

            # カスタムUIファイルのコピー
            parameter_ui_path = self._add_sample_ui(sample_type, ui_type, suffix_num)

            # 環境情報ファイルの更新
            new_info = {
                'name': f'Sample {sample_type}',
                'description': '',
                'component-type': 'python',
                'modulename': f'sample_{sample_type}_{suffix_num}',
            }

            if parameter_ui_path is None:
                new_info['parameter-ui-type'] = 'none'
            else:
                new_info['parameter-ui-type'] = ui_type
                new_info['parameter-ui'] = parameter_ui_path.relative_to(self.work_dir).as_posix()
                if ui_type == 'html':
                    new_info['parameter-ui-size'] = 'middle'

            info['components'][new_uuid] = new_info

        elif sample_lang == 'c':
            utils.print_error('c component sample is not supported now')

        self.__save_scc_info(info)

    def _add_sample_ui(self, sample_type: str, ui_type: str, suffix_num: int) -> Path | None:
        """Add custom-ui sample."""
        if ui_type == 'json':
            resname = f'sample_{sample_type}_ui.json'
            if not importlib.resources.is_resource(sccde_resources, resname):
                return None

            parameter_ui_path = self.__info_path.parent / f'parameter_ui/sample_{sample_type}_{suffix_num}/custom_ui.json'
            parameter_ui_path.parent.mkdir(parents=True, exist_ok=True)
            with parameter_ui_path.open(mode='w', encoding='utf-8') as fo:
                with warnings.catch_warnings():
                    warnings.simplefilter('ignore')
                    content = importlib.resources.read_text(sccde_resources, resname)
                fo.write(content)
            return parameter_ui_path

        if ui_type == 'html':
            resname = f'sample_{sample_type}_html.zip'
            if not importlib.resources.is_resource(sccde_resources, resname):
                return None

            parameter_ui_path = self.__info_path.parent / f'parameter_ui/sample_{sample_type}_{suffix_num}'
            with importlib.resources.path(sccde_resources, resname) as tmp_path, \
                 zipfile.ZipFile(tmp_path, 'r') as zo:
                    zo.extractall(path=parameter_ui_path)
            return parameter_ui_path

        return None


    def make_package(self, out: Path | None) -> None:
        """Initialize resource repogitory."""
        info = self.__load_scc_info()
        pack.make_package(self.__info_path, info, out)

    def server(self, host: str, port: int, *, verbose: bool = False) -> TestServer:
        """Start synapse test process."""
        self.distribute()

        datadir = self.work_dir / SERVE_DATA_DIR / 'var-speedbeesynapse'
        server = TestServer(datadir, host, port)
        server.verbose = verbose
        return server

    def distribute(self) -> None:
        """Distribute package files into the specified directory."""
        info = self.__load_scc_info()
        base_dir = self.work_dir / SERVE_DATA_DIR / 'scc_packages' / info['package-uuid']
        if (base_dir / 'contents').exists():
            (base_dir / 'contents/DELETED').touch()

        target_dir = base_dir / 'contents.new'
        target_dir.mkdir(parents=True, exist_ok=True)

        pack.distribute(self.__info_path, info, target_dir)

        (target_dir.parent / 'packagefile.sccpkg').touch()

    def check_all(self, load: bool = True, timeout: float = 2.0) -> PackageValidity:
        """Check consistency for all components in the package."""
        info = self.__load_scc_info()

        python_dir = self.work_dir / info['python-components-source-dir']
        components = [ self.check_component(python_dir, compo_id, compo, load, timeout) \
                for (compo_id, compo) in info['components'].items() ]

        return PackageValidity(name=info['package-name'],
                                  uuid=uuid.UUID(info['package-uuid']),
                                  version=info['package-version'],
                                  description=info['package-description'],
                                  components=components)

    def check(self, targets: list[str], load: bool = True, timeout: float = 2.0) -> list[ComponentValidity]:
        """Check consistency for the specified component."""
        info = self.__load_scc_info()

        compo_ids = self._filter_component(info, targets)

        python_dir = self.work_dir / info['python-components-source-dir']
        return [ self.check_component(python_dir, compo_id, info['components'][compo_id], load, timeout) \
                for compo_id in compo_ids ]

    def _filter_component(self, info: dict, targets: list[str]) -> Generator[uuid.UUID]:
        targets = [ t.lower() for t in targets ]

        # コンポーネント名、モジュール名、UUIDのいずれかが`target`と前方一致する
        # コンポーネントIDをyieldする
        for (compo_id, compo) in info['components'].items():
            for target in targets:
                if compo['name'].lower().startswith(target):
                    yield compo_id
                    break
                if compo['modulename'].split('.')[-1].lower().startswith(target):
                    yield compo_id
                    break
                if compo_id.lower().startswith(target):
                    yield compo_id
                    break


    def check_component(self, python_dir: Path,
                        compo_id: uuid.UUID,
                        compo: dict,
                        load: bool,
                        timeout: float) -> ComponentValidity:
        """Check component consistency."""
        component =  ComponentValidity(name=compo['name'],
                                       uuid=compo_id)

        # 存在チェック
        try:
            module_path = python_dir / (compo['modulename'].replace('.', '/') + '.py')
            with module_path.open('r') as fo:
                source = fo.read()
            component.read_check = CheckState.OK
        except Exception as exc: # noqa: BLE001
            component.read_check = CheckState.ERROR
            component.read_error = TracebackException.from_exception(exc)
            return component

        # 構文チェック
        syntax_error = self._check_python_syntax(module_path, source)
        if syntax_error is None:
            component.syntax_check = CheckState.OK
        else:
            component.syntax_check = CheckState.ERROR
            component.syntax_error = syntax_error
            return component

        if not load:
            return component

        # 読み込みチェック
        load_error = self._check_python_loadability(python_dir, compo['modulename'], timeout)
        if load_error is None:
            component.load_check = CheckState.OK
        else:
            component.load_check = CheckState.ERROR
            component.load_error = load_error
            return component

        return component

    def _check_python_syntax(self, module_path: Path, source: str) -> None | TracebackException:
        """
        Check python component syntax.

        Return TracebackException of SyntaxException or ValueException if the source file cannot be parsed,
        or None otherwise.
        """
        try:
            compile(source, str(module_path), 'exec')
        except (SyntaxError, ValueError) as exc:
            return TracebackException.from_exception(exc)

        return None

    def _check_python_loadability(self, python_dir: Path, modulename: str, timeout: float) -> None | str | TracebackException:
        """
        Check python component loadability.

        Return exception if the source file cannot be parsed.
        """
        try:
            cp = subprocess.run([sys.executable, # noqa: S603
                                 '-m', 'sccde.check',
                                 modulename, str(python_dir.absolute())],
                                capture_output=True,
                                check=True,
                                timeout=timeout)
            info = json.loads(cp.stdout)
            return info.get('exception', None)
        except subprocess.TimeoutExpired as exc:
            return TracebackException.from_exception(exc)

    def __load_scc_info(self) -> dict:
        """Load and parse scc-info.json."""
        try:
            with self.__info_path.open(mode='rt', encoding='utf-8') as fo:
                return json.load(fo)
        except Exception as err:
            raise NotInitializedError(self.work_dir) from err

    def __save_scc_info(self, info: dict) -> None:
        """Save info into scc-info.json."""
        try:
            with self.__info_path.open(mode='wt', encoding='utf-8') as fo:
                json.dump(info, fo, ensure_ascii=False, indent=2)
                fo.write('\n')
        except Exception as err:
            raise SccInfoNotWritableError(self.__info_path) from err

    @property
    def __info_path(self) -> Path:
        return self.work_dir / INFO_FILE_NAME

