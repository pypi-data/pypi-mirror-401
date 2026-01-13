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
        # 不使用别名：优先从当前 shell 会话获取历史（最可靠，包含最新命令）
        from ..shells import shell
        import subprocess
        
        # 已知的 tmd 命令列表（需要排除）
        known_commands = ['tmd']
        
        # 方法1: 优先使用 fc 命令从当前 shell 会话获取历史（最可靠，包含最新命令）
        # 这比读取历史文件更可靠，因为 bash 历史是异步写入的
        try:
            shell_name = shell.friendly_name
            if shell_name == 'Bash':
                # 使用 fc -ln 获取最近10条历史（从当前会话）
                result = subprocess.run(
                    ['bash', '-c', 'fc -ln -10'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                    text=True,
                    timeout=1
                )
                if result.returncode == 0 and result.stdout.strip():
                    lines = result.stdout.strip().split('\n')
                    executables = get_all_executables()
                    # 从后往前查找，找到第一条非 tmd 命令
                    for cmd in reversed(lines):
                        cmd = cmd.strip()
                        if cmd:
                            cmd_parts = cmd.split()
                            if cmd_parts and cmd_parts[0] not in known_commands:
                                # 优先返回包含空格的命令
                                if ' ' in cmd:
                                    return [cmd]
                    
                    # 如果没有包含空格的命令，返回任何非 tmd 命令
                    for cmd in reversed(lines):
                        cmd = cmd.strip()
                        if cmd:
                            cmd_parts = cmd.split()
                            if cmd_parts and cmd_parts[0] not in known_commands:
                                return [cmd]
            elif shell_name == 'ZSH':
                # 使用 fc -ln 获取最近10条历史（从当前会话）
                result = subprocess.run(
                    ['zsh', '-c', 'fc -ln -10'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                    text=True,
                    timeout=1
                )
                if result.returncode == 0 and result.stdout.strip():
                    lines = result.stdout.strip().split('\n')
                    # 从后往前查找，找到第一条非 tmd 命令
                    for cmd in reversed(lines):
                        cmd = cmd.strip()
                        if cmd:
                            cmd_parts = cmd.split()
                            if cmd_parts and cmd_parts[0] not in known_commands:
                                # 优先返回包含空格的命令
                                if ' ' in cmd:
                                    return [cmd]
                    
                    # 如果没有包含空格的命令，返回任何非 tmd 命令
                    for cmd in reversed(lines):
                        cmd = cmd.strip()
                        if cmd:
                            cmd_parts = cmd.split()
                            if cmd_parts and cmd_parts[0] not in known_commands:
                                return [cmd]
        except Exception as e:
            from .. import logs
            logs.debug(f'无法使用 fc 命令读取历史: {e}')
        
        # 方法2: 如果 fc 失败，尝试使用 shell.get_history()（从历史文件读取）
        try:
            history = shell.get_history()
            if history:
                executables = get_all_executables()
                # 从后往前查找，找到第一条非 tmd 命令
                # 只检查最近5条，确保是最近的命令
                for command in reversed(history[-5:]):
                    if command and command.strip():
                        cmd_parts = command.strip().split()
                        if cmd_parts:
                            first_word = cmd_parts[0]
                            # 排除所有已知的 tmd 命令
                            if first_word not in known_commands:
                                # 优先返回包含空格的命令
                                if ' ' in command.strip():
                                    return [command.strip()]
                
                # 如果包含空格的命令没找到，再查找可执行文件命令
                for command in reversed(history[-5:]):
                    if command and command.strip():
                        cmd_parts = command.strip().split()
                        if cmd_parts:
                            first_word = cmd_parts[0]
                            if first_word not in known_commands:
                                if first_word in executables or any(first_word == exe for exe in executables):
                                    return [command.strip()]
                
                # 最后，返回最后一个非空且不是已知命令的命令
                for command in reversed(history[-5:]):
                    if command and command.strip():
                        cmd_parts = command.strip().split()
                        if cmd_parts and cmd_parts[0] not in known_commands:
                            return [command.strip()]
        except Exception as e:
            from .. import logs
            logs.debug(f'无法使用 shell.get_history() 读取历史: {e}')
        
        # 方法2: 对于 Bash，直接读取历史文件（作为备选，确保读取最新命令）
        try:
            shell_name = shell.friendly_name
            if shell_name == 'Bash':
                histfile = os.environ.get('HISTFILE', os.path.expanduser('~/.bash_history'))
                if os.path.exists(histfile):
                    try:
                        with open(histfile, 'r', encoding='utf-8', errors='ignore') as f:
                            lines = f.readlines()
                            # 从后往前查找，只检查最近5条，确保是最近的命令
                            # 优先返回包含空格的命令
                            for line in reversed(lines[-5:]):
                                cmd = line.strip()
                                if cmd:
                                    cmd_parts = cmd.split()
                                    # 跳过所有已知的 tmd 命令
                                    if cmd_parts and cmd_parts[0] not in known_commands:
                                        # 优先返回包含空格的命令
                                        if ' ' in cmd:
                                            return [cmd]
                            
                            # 如果没有包含空格的命令，返回任何非 tmd 命令
                            for line in reversed(lines[-5:]):
                                cmd = line.strip()
                                if cmd:
                                    cmd_parts = cmd.split()
                                    if cmd_parts and cmd_parts[0] not in known_commands:
                                        return [cmd]
                    except Exception as e:
                        from .. import logs
                        logs.debug(f'无法读取历史文件 {histfile}: {e}')
            elif shell_name == 'ZSH':
                # 对于 ZSH，直接读取历史文件
                histfile = os.environ.get('HISTFILE', os.path.expanduser('~/.zsh_history'))
                if os.path.exists(histfile):
                    try:
                        with open(histfile, 'r', encoding='utf-8', errors='ignore') as f:
                            lines = f.readlines()
                            # zsh 历史格式: : timestamp:0;command
                            # 只检查最近5条，优先返回包含空格的命令
                            for line in reversed(lines[-5:]):
                                if ';' in line:
                                    cmd = line.split(';', 1)[1].strip()
                                    if cmd:
                                        cmd_parts = cmd.split()
                                        if cmd_parts and cmd_parts[0] not in known_commands:
                                            if ' ' in cmd:
                                                return [cmd]
                            
                            # 如果没有包含空格的命令，返回任何非 tmd 命令
                            for line in reversed(lines[-5:]):
                                if ';' in line:
                                    cmd = line.split(';', 1)[1].strip()
                                    if cmd:
                                        cmd_parts = cmd.split()
                                        if cmd_parts and cmd_parts[0] not in known_commands:
                                            return [cmd]
                    except Exception as e:
                        from .. import logs
                        logs.debug(f'无法读取历史文件 {histfile}: {e}')
        except Exception as e:
            from .. import logs
            logs.debug(f'无法从历史文件读取: {e}')
    return []


def fix_command(known_args):
    """Fixes previous command. Used when `tmd` called without arguments."""
    settings.init(known_args)
    with logs.debug_time('Total'):
        logs.debug(u'Run with settings: {}'.format(pformat(settings)))
        raw_command = _get_raw_command(known_args)

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
