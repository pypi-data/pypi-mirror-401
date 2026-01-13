# TMD 他妈的 [![Version][version-badge]][version-link] [![Build Status][workflow-badge]][workflow-link] [![Coverage][coverage-badge]][coverage-link] [![MIT License][license-badge]](LICENSE.md)

*TMD* 是一个牛逼的应用，灵感来自 [@liamosaur](https://twitter.com/liamosaur/)
的[推文](https://twitter.com/liamosaur/status/506975850596536320)，
它可以修正你之前控制台命令中的错误。

> **注意**：本项目复刻自 [thefuck](https://github.com/nvbn/thefuck)，已全面中文化并修改为 `tmd`（他妈的）版本。


*TMD* 太慢了？[试试实验性的即时模式！](#experimental-instant-mode)

![gif with examples](tmdVideo.gif)

更多示例：

```bash
➜ apt-get install vim
E: Could not open lock file /var/lib/dpkg/lock - open (13: Permission denied)
E: Unable to lock the administration directory (/var/lib/dpkg/), are you root?

➜ tmd
sudo apt-get install vim [enter/↑/↓/ctrl+c]
[sudo] password for nvbn:
Reading package lists... Done
...
```

```bash
➜ git push
fatal: The current branch master has no upstream branch.
To push the current branch and set the remote as upstream, use

    git push --set-upstream origin master


➜ tmd
git push --set-upstream origin master [enter/↑/↓/ctrl+c]
Counting objects: 9, done.
...
```

```bash
➜ puthon
No command 'puthon' found, did you mean:
 Command 'python' from package 'python-minimal' (main)
 Command 'python' from package 'python3' (main)
zsh: command not found: puthon

➜ tmd
python [enter/↑/↓/ctrl+c]
Python 3.4.2 (default, Oct  8 2014, 13:08:17)
...
```

```bash
➜ git brnch
git: 'brnch' is not a git command. See 'git --help'.

Did you mean this?
    branch

➜ tmd
git branch [enter/↑/↓/ctrl+c]
* master
```

```bash
➜ lein rpl
'rpl' is not a task. See 'lein help'.

Did you mean this?
         repl

➜ tmd
lein repl [enter/↑/↓/ctrl+c]
nREPL server started on port 54848 on host 127.0.0.1 - nrepl://127.0.0.1:54848
REPL-y 0.3.1
...
```

如果你不害怕盲目运行修正后的命令，可以禁用
`require_confirmation` [设置](#settings) 选项：

```bash
➜ apt-get install vim
E: Could not open lock file /var/lib/dpkg/lock - open (13: Permission denied)
E: Unable to lock the administration directory (/var/lib/dpkg/), are you root?

➜ tmd
sudo apt-get install vim
[sudo] password for nvbn:
Reading package lists... Done
...
```

## 目录

1. [要求](#requirements)
2. [安装](#installation)
3. [更新](#updating)
4. [工作原理](#how-it-works)
5. [创建自己的规则](#creating-your-own-rules)
6. [设置](#settings)
7. [包含规则的第三方包](#third-party-packages-with-rules)
8. [实验性即时模式](#experimental-instant-mode)
9. [开发](#developing)
10. [许可证](#license-mit)

## 要求

- python (3.5+)
- pip
- python-dev

##### [返回目录](#contents)

## 安装

### Linux 安装步骤

在 Ubuntu / Debian / Mint 等 Linux 系统上，使用以下命令安装 *TMD*：

```bash
# 更新包列表
sudo apt update

# 安装必要的依赖
sudo apt install python3-dev python3-pip python3-setuptools

# 安装 TMD
pip3 install tmdsb --user
```

确保 `~/.local/bin` 在 PATH 中：

```bash
export PATH=$HOME/.local/bin:$PATH
```

或者永久添加到 `~/.bashrc`：

```bash
echo 'export PATH=$HOME/.local/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

### 其他 Linux 发行版

在其他 Linux 发行版上，使用 `pip` 安装：

```bash
pip install tmdsb
# 或
pip3 install tmdsb --user
```

<a href='#manual-installation' name='manual-installation'>#</a>
**TMD 可以直接使用，无需配置别名！**

安装后，直接使用 `tmd` 命令即可。TMD 会自动从 shell 历史文件中读取上一个命令。

**可选：配置别名以获得更好的体验**

如果你想使用别名（可选，不是必需的），可以将以下命令放在你的 `.bash_profile`、
`.bashrc`、`.zshrc` 或其他启动脚本中：

```bash
eval $(tmd --alias)
# 你可以使用任何你想要的别名，比如：
eval $(tmd --alias TMD)
```

[或在你的 shell 配置文件中（Bash, Zsh, Fish, Powershell, tcsh）。](https://github.com/nvbn/tmd/wiki/Shell-aliases)

如果配置了别名，更改只在新 shell 会话中可用。要立即使更改生效，
运行 `source ~/.bashrc`（或你的 shell 配置文件，如 `.zshrc`）。

要在不确认的情况下运行修正后的命令，使用 `--yeah` 选项（或简写 `-y`，或者如果你特别烦躁，使用 `--hard`）：

```bash
tmd --yeah
```

要递归修正命令直到成功，使用 `-r` 选项：

```bash
tmd -r
```

##### [返回目录](#contents)

## 更新

```bash
pip3 install tmdsb --upgrade
```

**注意：别名功能在 *TMD* v1.34 中已更改**

## 卸载

要移除 *TMD*，反向执行安装过程：
- 从你的 Bash, Zsh, Fish, Powershell, tcsh, ... shell 配置中删除或注释 *tmd* 别名行
- 使用你的包管理器（brew, pip3, pkg, crew, pip）卸载二进制文件

## 工作原理

*TMD* 尝试将之前的命令与规则匹配。如果找到匹配项，
则使用匹配的规则创建新命令并执行。以下规则默认启用：

* `adb_unknown_command` &ndash; fixes misspelled commands like `adb logcta`;
* `ag_literal` &ndash; adds `-Q` to `ag` when suggested;
* `aws_cli` &ndash; fixes misspelled commands like `aws dynamdb scan`;
* `az_cli` &ndash; fixes misspelled commands like `az providers`;
* `cargo` &ndash; runs `cargo build` instead of `cargo`;
* `cargo_no_command` &ndash; fixes wrong commands like `cargo buid`;
* `cat_dir` &ndash; replaces `cat` with `ls` when you try to `cat` a directory;
* `cd_correction` &ndash; spellchecks and corrects failed cd commands;
* `cd_cs` &ndash; changes `cs` to `cd`;
* `cd_mkdir` &ndash; creates directories before cd'ing into them;
* `cd_parent` &ndash; changes `cd..` to `cd ..`;
* `chmod_x` &ndash; adds execution bit;
* `choco_install` &ndash; appends common suffixes for chocolatey packages;
* `composer_not_command` &ndash; fixes composer command name;
* `conda_mistype` &ndash; fixes conda commands;
* `cp_create_destination` &ndash; creates a new directory when you attempt to `cp` or `mv` to a non-existent one
* `cp_omitting_directory` &ndash; adds `-a` when you `cp` directory;
* `cpp11` &ndash; adds missing `-std=c++11` to `g++` or `clang++`;
* `dirty_untar` &ndash; fixes `tar x` command that untarred in the current directory;
* `dirty_unzip` &ndash; fixes `unzip` command that unzipped in the current directory;
* `django_south_ghost` &ndash; adds `--delete-ghost-migrations` to failed because ghosts django south migration;
* `django_south_merge` &ndash; adds `--merge` to inconsistent django south migration;
* `docker_login` &ndash; executes a `docker login` and repeats the previous command;
* `docker_not_command` &ndash; fixes wrong docker commands like `docker tags`;
* `docker_image_being_used_by_container` &dash; removes the container that is using the image before removing the image;
* `dry` &ndash; fixes repetitions like `git git push`;
* `fab_command_not_found` &ndash; fixes misspelled fabric commands;
* `fix_alt_space` &ndash; replaces Alt+Space with Space character;
* `fix_file` &ndash; opens a file with an error in your `$EDITOR`;
* `gem_unknown_command` &ndash; fixes wrong `gem` commands;
* `git_add` &ndash; fixes *"pathspec 'foo' did not match any file(s) known to git."*;
* `git_add_force` &ndash; adds `--force` to `git add <pathspec>...` when paths are .gitignore'd;
* `git_bisect_usage` &ndash; fixes `git bisect strt`, `git bisect goood`, `git bisect rset`, etc. when bisecting;
* `git_branch_delete` &ndash; changes `git branch -d` to `git branch -D`;
* `git_branch_delete_checked_out` &ndash; changes `git branch -d` to `git checkout master && git branch -D` when trying to delete a checked out branch;
* `git_branch_exists` &ndash; offers `git branch -d foo`, `git branch -D foo` or `git checkout foo` when creating a branch that already exists;
* `git_branch_list` &ndash; catches `git branch list` in place of `git branch` and removes created branch;
* `git_branch_0flag` &ndash; fixes commands such as `git branch 0v` and `git branch 0r` removing the created branch;
* `git_checkout` &ndash; fixes branch name or creates new branch;
* `git_clone_git_clone` &ndash; replaces `git clone git clone ...` with `git clone ...`
* `git_clone_missing` &ndash; adds `git clone` to URLs that appear to link to a git repository.
* `git_commit_add` &ndash; offers `git commit -a ...` or `git commit -p ...` after previous commit if it failed because nothing was staged;
* `git_commit_amend` &ndash; offers `git commit --amend` after previous commit;
* `git_commit_reset` &ndash; offers `git reset HEAD~` after previous commit;
* `git_diff_no_index` &ndash; adds `--no-index` to previous `git diff` on untracked files;
* `git_diff_staged` &ndash; adds `--staged` to previous `git diff` with unexpected output;
* `git_fix_stash` &ndash; fixes `git stash` commands (misspelled subcommand and missing `save`);
* `git_flag_after_filename` &ndash; fixes `fatal: bad flag '...' after filename`
* `git_help_aliased` &ndash; fixes `git help <alias>` commands replacing <alias> with the aliased command;
* `git_hook_bypass` &ndash; adds `--no-verify` flag previous to `git am`, `git commit`, or `git push` command;
* `git_lfs_mistype` &ndash; fixes mistyped `git lfs <command>` commands;
* `git_main_master` &ndash; fixes incorrect branch name between `main` and `master`
* `git_merge` &ndash; adds remote to branch names;
* `git_merge_unrelated` &ndash; adds `--allow-unrelated-histories` when required
* `git_not_command` &ndash; fixes wrong git commands like `git brnch`;
* `git_pull` &ndash; sets upstream before executing previous `git pull`;
* `git_pull_clone` &ndash; clones instead of pulling when the repo does not exist;
* `git_pull_uncommitted_changes` &ndash; stashes changes before pulling and pops them afterwards;
* `git_push` &ndash; adds `--set-upstream origin $branch` to previous failed `git push`;
* `git_push_different_branch_names` &ndash; fixes pushes when local branch name does not match remote branch name;
* `git_push_pull` &ndash; runs `git pull` when `push` was rejected;
* `git_push_without_commits` &ndash; creates an initial commit if you forget and only `git add .`, when setting up a new project;
* `git_rebase_no_changes` &ndash; runs `git rebase --skip` instead of `git rebase --continue` when there are no changes;
* `git_remote_delete` &ndash; replaces `git remote delete remote_name` with `git remote remove remote_name`;
* `git_rm_local_modifications` &ndash; adds `-f` or `--cached` when you try to `rm` a locally modified file;
* `git_rm_recursive` &ndash; adds `-r` when you try to `rm` a directory;
* `git_rm_staged` &ndash;  adds `-f` or `--cached` when you try to `rm` a file with staged changes
* `git_rebase_merge_dir` &ndash; offers `git rebase (--continue | --abort | --skip)` or removing the `.git/rebase-merge` dir when a rebase is in progress;
* `git_remote_seturl_add` &ndash; runs `git remote add` when `git remote set_url` on nonexistent remote;
* `git_stash` &ndash; stashes your local modifications before rebasing or switching branch;
* `git_stash_pop` &ndash; adds your local modifications before popping stash, then resets;
* `git_tag_force` &ndash; adds `--force` to `git tag <tagname>` when the tag already exists;
* `git_two_dashes` &ndash; adds a missing dash to commands like `git commit -amend` or `git rebase -continue`;
* `go_run` &ndash; appends `.go` extension when compiling/running Go programs;
* `go_unknown_command` &ndash; fixes wrong `go` commands, for example `go bulid`;
* `gradle_no_task` &ndash; fixes not found or ambiguous `gradle` task;
* `gradle_wrapper` &ndash; replaces `gradle` with `./gradlew`;
* `grep_arguments_order` &ndash; fixes `grep` arguments order for situations like `grep -lir . test`;
* `grep_recursive` &ndash; adds `-r` when you try to `grep` directory;
* `grunt_task_not_found` &ndash; fixes misspelled `grunt` commands;
* `gulp_not_task` &ndash; fixes misspelled `gulp` tasks;
* `has_exists_script` &ndash; prepends `./` when script/binary exists;
* `heroku_multiple_apps` &ndash; adds `--app <app>` to `heroku` commands like `heroku pg`;
* `heroku_not_command` &ndash; fixes wrong `heroku` commands like `heroku log`;
* `history` &ndash; tries to replace command with the most similar command from history;
* `hostscli` &ndash; tries to fix `hostscli` usage;
* `ifconfig_device_not_found` &ndash; fixes wrong device names like `wlan0` to `wlp2s0`;
* `java` &ndash; removes `.java` extension when running Java programs;
* `javac` &ndash; appends missing `.java` when compiling Java files;
* `lein_not_task` &ndash; fixes wrong `lein` tasks like `lein rpl`;
* `long_form_help` &ndash; changes `-h` to `--help` when the short form version is not supported
* `ln_no_hard_link` &ndash; catches hard link creation on directories, suggest symbolic link;
* `ln_s_order` &ndash; fixes `ln -s` arguments order;
* `ls_all` &ndash; adds `-A` to `ls` when output is empty;
* `ls_lah` &ndash; adds `-lah` to `ls`;
* `man` &ndash; changes manual section;
* `man_no_space` &ndash; fixes man commands without spaces, for example `mandiff`;
* `mercurial` &ndash; fixes wrong `hg` commands;
* `missing_space_before_subcommand` &ndash; fixes command with missing space like `npminstall`;
* `mkdir_p` &ndash; adds `-p` when you try to create a directory without a parent;
* `mvn_no_command` &ndash; adds `clean package` to `mvn`;
* `mvn_unknown_lifecycle_phase` &ndash; fixes misspelled life cycle phases with `mvn`;
* `npm_missing_script` &ndash; fixes `npm` custom script name in `npm run-script <script>`;
* `npm_run_script` &ndash; adds missing `run-script` for custom `npm` scripts;
* `npm_wrong_command` &ndash; fixes wrong npm commands like `npm urgrade`;
* `no_command` &ndash; fixes wrong console commands, for example `vom/vim`;
* `no_such_file` &ndash; creates missing directories with `mv` and `cp` commands;
* `omnienv_no_such_command` &ndash; fixes wrong commands for `goenv`, `nodenv`, `pyenv` and `rbenv` (eg.: `pyenv isntall` or `goenv list`);
* `open` &ndash; either prepends `http://` to address passed to `open` or creates a new file or directory and passes it to `open`;
* `pip_install` &ndash; fixes permission issues with `pip install` commands by adding `--user` or prepending `sudo` if necessary;
* `pip_unknown_command` &ndash; fixes wrong `pip` commands, for example `pip instatl/pip install`;
* `php_s` &ndash; replaces `-s` by `-S` when trying to run a local php server;
* `port_already_in_use` &ndash; kills process that bound port;
* `prove_recursively` &ndash; adds `-r` when called with directory;
* `python_command` &ndash; prepends `python` when you try to run non-executable/without `./` python script;
* `python_execute` &ndash; appends missing `.py` when executing Python files;
* `python_module_error` &ndash; fixes ModuleNotFoundError by trying to `pip install` that module;
* `quotation_marks` &ndash; fixes uneven usage of `'` and `"` when containing args';
* `path_from_history` &ndash; replaces not found path with a similar absolute path from history;
* `rails_migrations_pending` &ndash; runs pending migrations;
* `react_native_command_unrecognized` &ndash; fixes unrecognized `react-native` commands;
* `remove_shell_prompt_literal` &ndash; removes leading shell prompt symbol `$`, common when copying commands from documentations;
* `remove_trailing_cedilla` &ndash; removes trailing cedillas `ç`, a common typo for European keyboard layouts;
* `rm_dir` &ndash; adds `-rf` when you try to remove a directory;
* `scm_correction` &ndash; corrects wrong scm like `hg log` to `git log`;
* `sed_unterminated_s` &ndash; adds missing '/' to `sed`'s `s` commands;
* `sl_ls` &ndash; changes `sl` to `ls`;
* `ssh_known_hosts` &ndash; removes host from `known_hosts` on warning;
* `sudo` &ndash; prepends `sudo` to the previous command if it failed because of permissions;
* `sudo_command_from_user_path` &ndash; runs commands from users `$PATH` with `sudo`;
* `switch_lang` &ndash; switches command from your local layout to en;
* `systemctl` &ndash; correctly orders parameters of confusing `systemctl`;
* `terraform_init.py` &ndash; runs `terraform init` before plan or apply;
* `terraform_no_command.py` &ndash; fixes unrecognized `terraform` commands;
* `test.py` &ndash; runs `pytest` instead of `test.py`;
* `touch` &ndash; creates missing directories before "touching";
* `tsuru_login` &ndash; runs `tsuru login` if not authenticated or session expired;
* `tsuru_not_command` &ndash; fixes wrong `tsuru` commands like `tsuru shell`;
* `tmux` &ndash; fixes `tmux` commands;
* `unknown_command` &ndash; fixes hadoop hdfs-style "unknown command", for example adds missing '-' to the command on `hdfs dfs ls`;
* `unsudo` &ndash; removes `sudo` from previous command if a process refuses to run on superuser privilege.
* `vagrant_up` &ndash; starts up the vagrant instance;
* `whois` &ndash; fixes `whois` command;
* `workon_doesnt_exists` &ndash; fixes `virtualenvwrapper` env name os suggests to create new.
* `wrong_hyphen_before_subcommand` &ndash; removes an improperly placed hyphen (`apt-install` -> `apt install`, `git-log` -> `git log`, etc.)
* `yarn_alias` &ndash; fixes aliased `yarn` commands like `yarn ls`;
* `yarn_command_not_found` &ndash; fixes misspelled `yarn` commands;
* `yarn_command_replaced` &ndash; fixes replaced `yarn` commands;
* `yarn_help` &ndash; makes it easier to open `yarn` documentation;

##### [返回目录](#contents)

以下规则仅在特定平台上默认启用：

* `apt_get` &ndash; installs app from apt if it not installed (requires `python-commandnotfound` / `python3-commandnotfound`);
* `apt_get_search` &ndash; changes trying to search using `apt-get` with searching using `apt-cache`;
* `apt_invalid_operation` &ndash; fixes invalid `apt` and `apt-get` calls, like `apt-get isntall vim`;
* `apt_list_upgradable` &ndash; helps you run `apt list --upgradable` after `apt update`;
* `apt_upgrade` &ndash; helps you run `apt upgrade` after `apt list --upgradable`;
* `brew_cask_dependency` &ndash; installs cask dependencies;
* `brew_install` &ndash; fixes formula name for `brew install`;
* `brew_reinstall` &ndash; turns `brew install <formula>` into `brew reinstall <formula>`;
* `brew_link` &ndash; adds `--overwrite --dry-run` if linking fails;
* `brew_uninstall` &ndash; adds `--force` to `brew uninstall` if multiple versions were installed;
* `brew_unknown_command` &ndash; fixes wrong brew commands, for example `brew docto/brew doctor`;
* `brew_update_formula` &ndash; turns `brew update <formula>` into `brew upgrade <formula>`;
* `dnf_no_such_command` &ndash; fixes mistyped DNF commands;
* `nixos_cmd_not_found` &ndash; installs apps on NixOS;
* `pacman` &ndash; installs app with `pacman` if it is not installed (uses `yay`, `pikaur` or `yaourt` if available);
* `pacman_invalid_option` &ndash; replaces lowercase `pacman` options with uppercase.
* `pacman_not_found` &ndash; fixes package name with `pacman`, `yay`, `pikaur` or `yaourt`.
* `yum_invalid_operation` &ndash; fixes invalid `yum` calls, like `yum isntall vim`;

以下命令与 *TMD* 捆绑在一起，但默认未启用：

* `git_push_force` &ndash; adds `--force-with-lease` to a `git push` (may conflict with `git_push_pull`);
* `rm_root` &ndash; adds `--no-preserve-root` to `rm -rf /` command.

##### [返回目录](#contents)

## 创建自己的规则

要添加你自己的规则，在 `~/.config/tmd/rules` 中创建一个名为 `your-rule-name.py` 的文件。
规则文件必须包含两个函数：

```python
match(command: Command) -> bool
get_new_command(command: Command) -> str | list[str]
```

此外，规则可以包含可选函数：

```python
side_effect(old_command: Command, fixed_command: str) -> None
```
规则还可以包含可选变量 `enabled_by_default`、`requires_output` 和 `priority`。

`Command` 有三个属性：`script`、`output` 和 `script_parts`。
你的规则不应更改 `Command`。

**规则 API 在 3.0 中已更改：** 要访问规则的设置，使用以下方式导入：
 `from tmd.conf import settings`

`settings` 是一个特殊对象，由 `~/.config/tmd/settings.py` 和
环境变量中的值组装而成（[见下文](#settings)）。

一个简单的使用 `sudo` 运行脚本的规则示例：

```python
def match(command):
    return ('permission denied' in command.output.lower()
            or 'EACCES' in command.output)


def get_new_command(command):
    return 'sudo {}'.format(command.script)

# Optional:
enabled_by_default = True

def side_effect(command, fixed_command):
    subprocess.call('chmod 777 .', shell=True)

priority = 1000  # Lower first, default is 1000

requires_output = True
```

[更多规则示例](https://github.com/nvbn/tmd/tree/master/tmd/rules)，
[规则的实用函数](https://github.com/nvbn/tmd/tree/master/tmd/utils.py)，
[应用/操作系统特定的辅助函数](https://github.com/nvbn/tmd/tree/master/tmd/specific/)。

##### [返回目录](#contents)

## 设置

几个 *TMD* 参数可以在文件 `$XDG_CONFIG_HOME/tmd/settings.py` 中更改
（`$XDG_CONFIG_HOME` 默认为 `~/.config`）：

* `rules` &ndash; 启用的规则列表，默认为 `tmd.const.DEFAULT_RULES`；
* `exclude_rules` &ndash; 禁用的规则列表，默认为 `[]`；
* `require_confirmation` &ndash; 在运行新命令前要求确认，默认为 `True`；
* `wait_command` &ndash; 获取上一个命令输出的最大时间（秒）；
* `no_colors` &ndash; 禁用彩色输出；
* `priority` &ndash; 规则优先级的字典，优先级较低的规则将首先匹配；
* `debug` &ndash; 启用调试输出，默认为 `False`；
* `history_limit` &ndash; 要扫描的历史命令数量，如 `2000`；
* `alter_history` &ndash; 将修正后的命令推送到历史记录，默认为 `True`；
* `wait_slow_command` &ndash; 如果命令在 `slow_commands` 列表中，获取上一个命令输出的最大时间（秒）；
* `slow_commands` &ndash; 慢速命令列表；
* `num_close_matches` &ndash; 建议的最大近似匹配数，默认为 `3`。
* `excluded_search_path_prefixes` &ndash; 搜索命令时要忽略的路径前缀，默认为 `[]`。

`settings.py` 示例：

```python
rules = ['sudo', 'no_command']
exclude_rules = ['git_push']
require_confirmation = True
wait_command = 10
no_colors = False
priority = {'sudo': 100, 'no_command': 9999}
debug = False
history_limit = 9999
wait_slow_command = 20
slow_commands = ['react-native', 'gradle']
num_close_matches = 5
```

或通过环境变量：

* `TMD_RULES` &ndash; 启用的规则列表，如 `DEFAULT_RULES:rm_root` 或 `sudo:no_command`；
* `TMD_EXCLUDE_RULES` &ndash; 禁用的规则列表，如 `git_pull:git_push`；
* `TMD_REQUIRE_CONFIRMATION` &ndash; 在运行新命令前要求确认，`true/false`；
* `TMD_WAIT_COMMAND` &ndash; 获取上一个命令输出的最大时间（秒）；
* `TMD_NO_COLORS` &ndash; 禁用彩色输出，`true/false`；
* `TMD_PRIORITY` &ndash; 规则的优先级，如 `no_command=9999:apt_get=100`，
优先级较低的规则将首先匹配；
* `TMD_DEBUG` &ndash; 启用调试输出，`true/false`；
* `TMD_HISTORY_LIMIT` &ndash; 要扫描的历史命令数量，如 `2000`；
* `TMD_ALTER_HISTORY` &ndash; 将修正后的命令推送到历史记录，`true/false`；
* `TMD_WAIT_SLOW_COMMAND` &ndash; 如果命令在 `slow_commands` 列表中，获取上一个命令输出的最大时间（秒）；
* `TMD_SLOW_COMMANDS` &ndash; 慢速命令列表，如 `lein:gradle`；
* `TMD_NUM_CLOSE_MATCHES` &ndash; 建议的最大近似匹配数，如 `5`。
* `TMD_EXCLUDED_SEARCH_PATH_PREFIXES` &ndash; 搜索命令时要忽略的路径前缀，默认为 `[]`。

例如：

```bash
export TMD_RULES='sudo:no_command'
export TMD_EXCLUDE_RULES='git_pull:git_push'
export TMD_REQUIRE_CONFIRMATION='true'
export TMD_WAIT_COMMAND=10
export TMD_NO_COLORS='false'
export TMD_PRIORITY='no_command=9999:apt_get=100'
export TMD_HISTORY_LIMIT='2000'
export TMD_NUM_CLOSE_MATCHES='5'
```

##### [返回目录](#contents)

## 包含规则的第三方包

如果你想创建一组特定的非公开规则，但仍想
与他人分享，创建一个名为 `tmd_contrib_*` 的包，结构如下：

```
tmd_contrib_foo
  tmd_contrib_foo
    rules
      __init__.py
      *第三方规则*
    __init__.py
    *第三方工具*
  setup.py
```

*TMD* 会在 `rules` 模块中查找规则。

##### [返回目录](#contents)

## 实验性即时模式

*TMD* 的默认行为需要时间重新运行之前的命令。
在即时模式下，*TMD* 通过使用 [script](https://en.wikipedia.org/wiki/Script_(Unix)) 记录输出
然后读取日志来节省时间。

![即时模式 gif](tmdVideo.gif)

目前，即时模式仅支持 Python 3 与 bash 或 zsh。zsh 的自动更正功能也需要禁用，以便 tmd 正常工作。

要启用即时模式，在 `.bashrc`、`.bash_profile` 或 `.zshrc` 中的别名初始化中添加 `--enable-experimental-instant-mode`。

例如：

```bash
eval $(tmd --alias --enable-experimental-instant-mode)
```

##### [返回目录](#contents)

## 开发

参见 [CONTRIBUTING.md](CONTRIBUTING.md)

## 许可证 MIT
项目许可证可在[此处](LICENSE.md)找到。


[version-badge]:   https://img.shields.io/pypi/v/tmdsb.svg?label=version
[version-link]:    https://pypi.python.org/pypi/tmdsb/
[workflow-badge]:  https://github.com/violettoolssite/tmd/workflows/Tests/badge.svg
[workflow-link]:   https://github.com/violettoolssite/tmd/actions?query=workflow%3ATests
[coverage-badge]:  https://img.shields.io/coveralls/violettoolssite/tmd.svg
[coverage-link]:   https://coveralls.io/github/violettoolssite/tmd
[license-badge]:   https://img.shields.io/badge/license-MIT-007EC7.svg
[homebrew]:        https://brew.sh/

##### [返回目录](#contents)
