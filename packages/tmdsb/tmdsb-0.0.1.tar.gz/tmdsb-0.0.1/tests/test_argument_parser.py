import pytest
from tmd.argument_parser import Parser
from tmd.const import ARGUMENT_PLACEHOLDER


def _args(**override):
    args = {'alias': None, 'command': [], 'yes': False,
            'help': False, 'version': False, 'debug': False,
            'force_command': None, 'repeat': False,
            'enable_experimental_instant_mode': False,
            'shell_logger': None}
    args.update(override)
    return args


@pytest.mark.parametrize('argv, result', [
    (['tmd'], _args()),
    (['tmd', '-a'], _args(alias='tmd')),
    (['tmd', '--alias', '--enable-experimental-instant-mode'],
     _args(alias='tmd', enable_experimental_instant_mode=True)),
    (['tmd', '-a', 'fix'], _args(alias='fix')),
    (['tmd', 'git', 'branch', ARGUMENT_PLACEHOLDER, '-y'],
     _args(command=['git', 'branch'], yes=True)),
    (['tmd', 'git', 'branch', '-a', ARGUMENT_PLACEHOLDER, '-y'],
     _args(command=['git', 'branch', '-a'], yes=True)),
    (['tmd', ARGUMENT_PLACEHOLDER, '-v'], _args(version=True)),
    (['tmd', ARGUMENT_PLACEHOLDER, '--help'], _args(help=True)),
    (['tmd', 'git', 'branch', '-a', ARGUMENT_PLACEHOLDER, '-y', '-d'],
     _args(command=['git', 'branch', '-a'], yes=True, debug=True)),
    (['tmd', 'git', 'branch', '-a', ARGUMENT_PLACEHOLDER, '-r', '-d'],
     _args(command=['git', 'branch', '-a'], repeat=True, debug=True)),
    (['tmd', '-l', '/tmp/log'], _args(shell_logger='/tmp/log')),
    (['tmd', '--shell-logger', '/tmp/log'],
     _args(shell_logger='/tmp/log'))])
def test_parse(argv, result):
    assert vars(Parser().parse(argv)) == result
