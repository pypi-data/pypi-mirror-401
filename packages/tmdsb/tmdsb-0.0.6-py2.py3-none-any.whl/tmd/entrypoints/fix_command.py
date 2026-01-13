from pprint import pformat
import os
import sys
from difflib import SequenceMatcher
from .. import logs, types, const
from ..conf import settings
from ..corrector import get_corrected_commands
from ..exceptions import EmptyCommand
from ..ui import select_command
from ..utils import get_alias, get_all_executables


def _get_raw_command(known_args):
    if known_args.force_command:
        return [known_args.force_command]
    elif known_args.command:
        return known_args.command
    elif os.environ.get('TMD_HISTORY'):
        # 如果通过别名调用，使用环境变量中的历史
        history = os.environ['TMD_HISTORY'].split('\n')[::-1]
        alias = get_alias()
        executables = get_all_executables()
        for command in history:
            diff = SequenceMatcher(a=alias, b=command).ratio()
            if diff < const.DIFF_WITH_ALIAS or command in executables:
                return [command]
    else:
        # 不使用别名：获取最近几条命令，找到第一条非 tmd 的命令
        import subprocess
        
        # 已知的 tmd 命令列表（需要排除）
        known_commands = ['tmd']
        
        # 方法1: 直接读取历史文件的最后几行（最可靠）
        try:
            histfile = os.environ.get('HISTFILE', os.path.expanduser('~/.bash_history'))
            if os.path.exists(histfile):
                with open(histfile, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    # 从后往前查找最后10条，找到第一条非 tmd 的命令
                    for line in reversed(lines[-10:]):
                        cmd = line.strip()
                        if cmd:
                            cmd_parts = cmd.split()
                            if cmd_parts and cmd_parts[0] not in known_commands:
                                return [cmd]
        except Exception as e:
            from .. import logs
            logs.debug(f'无法读取历史文件: {e}')
        
        # 方法2: 使用 fc -ln -10 获取最近10条命令（bash 内置命令）
        try:
            result = subprocess.run(
                ['bash', '-c', 'fc -ln -10'],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
                timeout=1
            )
            if result.returncode == 0 and result.stdout.strip():
                lines = result.stdout.strip().split('\n')
                # 从后往前查找，找到第一条非 tmd 的命令
                for cmd in reversed(lines):
                    cmd = cmd.strip()
                    if cmd:
                        cmd_parts = cmd.split()
                        if cmd_parts and cmd_parts[0] not in known_commands:
                            return [cmd]
        except Exception as e:
            from .. import logs
            logs.debug(f'无法使用 fc 命令读取历史: {e}')
        
        # 方法3: 如果 fc 失败，尝试使用 history | tail -10
        try:
            result = subprocess.run(
                ['bash', '-c', 'history | tail -10'],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
                timeout=1
            )
            if result.returncode == 0 and result.stdout.strip():
                lines = result.stdout.strip().split('\n')
                # 从后往前查找，找到第一条非 tmd 的命令
                for line in reversed(lines):
                    line = line.strip()
                    if line:
                        # history 输出格式通常是: "  123  command"
                        # 需要提取命令部分（去掉行号）
                        parts = line.split(None, 1)  # 按空格分割，最多分割一次
                        if len(parts) > 1:
                            cmd = parts[1].strip()  # 取第二部分（命令）
                        else:
                            cmd = line.strip()
                        
                        # 检查是否是 tmd 命令
                        if cmd:
                            cmd_parts = cmd.split()
                            if cmd_parts and cmd_parts[0] not in known_commands:
                                return [cmd]
        except Exception as e:
            from .. import logs
            logs.debug(f'无法使用 history 命令读取历史: {e}')
    return []


def fix_command(known_args):
    """Fixes previous command. Used when `tmd` called without arguments."""
    settings.init(known_args)
    with logs.debug_time('Total'):
        logs.debug(u'Run with settings: {}'.format(pformat(settings)))
        raw_command = _get_raw_command(known_args)
        
        # 调试：显示读取到的命令
        if raw_command:
            logs.debug(u'读取到的命令: {}'.format(raw_command))
        else:
            logs.debug(u'未读取到命令')

        try:
            command = types.Command.from_raw_script(raw_command)
        except EmptyCommand:
            logs.debug('Empty command, nothing to do')
            return

        corrected_commands = get_corrected_commands(command)
        selected_command = select_command(corrected_commands)

        if selected_command:
            selected_command.run(command)
        else:
            sys.exit(1)
