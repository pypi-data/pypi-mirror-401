"""
winterm服务模块 - 异步执行Windows终端命令服务
"""

import subprocess
import threading
import uuid
import time
import os
import shutil
from datetime import datetime
from typing import Dict, Optional, Any, List


# PowerShell 可执行文件的标准路径（按优先级排序）
POWERSHELL_PATHS: List[str] = [
    r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe",
    r"C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe",
]

# PowerShell Core (pwsh) 的常见路径
PWSH_PATHS: List[str] = [
    r"C:\Program Files\PowerShell\7\pwsh.exe",
    r"C:\Program Files (x86)\PowerShell\7\pwsh.exe",
]

# 环境变量名称
ENV_POWERSHELL_PATH = "WINTERM_POWERSHELL_PATH"


def _find_powershell() -> str:
    """
    查找可用的 PowerShell 可执行文件路径

    查找顺序：
    1. 环境变量 WINTERM_POWERSHELL_PATH（用户自定义）
    2. Windows PowerShell 标准路径
    3. PowerShell Core 标准路径
    4. PATH 环境变量中的 powershell/pwsh（兼容正常环境）

    Returns:
        PowerShell 可执行文件的绝对路径

    Raises:
        FileNotFoundError: 如果找不到 PowerShell
    """
    # 1. 检查用户配置的环境变量
    custom_path = os.environ.get(ENV_POWERSHELL_PATH)
    if custom_path:
        if os.path.isfile(custom_path):
            return custom_path
        # 用户配置了但路径无效，记录警告但继续查找

    # 2. 检查 Windows PowerShell 标准路径
    for path in POWERSHELL_PATHS:
        if os.path.isfile(path):
            return path

    # 3. 检查 PowerShell Core 标准路径
    for path in PWSH_PATHS:
        if os.path.isfile(path):
            return path

    # 4. 尝试 PATH 环境变量（兼容正常环境）
    ps_path = shutil.which("powershell")
    if ps_path:
        return ps_path

    pwsh_path = shutil.which("pwsh")
    if pwsh_path:
        return pwsh_path

    # 所有方法都失败
    checked_paths = POWERSHELL_PATHS + PWSH_PATHS
    raise FileNotFoundError(
        f"PowerShell not found. "
        f"Set {ENV_POWERSHELL_PATH} environment variable or "
        f"ensure PowerShell is installed. "
        f"Checked paths: {', '.join(checked_paths)}"
    )


class RunCmdService:
    """
    异步命令执行服务类，管理所有异步命令的执行和状态
    """

    def __init__(self):
        self.commands: Dict[str, Dict[str, Any]] = {}
        self.lock = threading.Lock()
        self._powershell_path: Optional[str] = None

    def _get_powershell_path(self) -> str:
        """
        获取 PowerShell 可执行文件路径（带缓存）

        首次调用时查找并缓存路径，后续调用直接返回缓存值。

        Returns:
            PowerShell 可执行文件的绝对路径

        Raises:
            FileNotFoundError: 如果找不到 PowerShell
        """
        if self._powershell_path is None:
            self._powershell_path = _find_powershell()
        return self._powershell_path

    def run_command(
        self,
        command: str,
        shell_type: str = "powershell",
        timeout: int = 30,
        working_directory: Optional[str] = None,
    ) -> str:
        """
        异步运行命令

        Args:
            command: 要执行的命令
            shell_type: Shell 类型 (powershell 或 cmd)
            timeout: 超时时间（秒）
            working_directory: 工作目录

        Returns:
            命令执行的token
        """
        token = str(uuid.uuid4())

        cmd_info = {
            "token": token,
            "command": command,
            "shell_type": shell_type,
            "status": "pending",
            "start_time": datetime.now(),
            "timeout": timeout,
            "working_directory": working_directory,
            "stdout": "",
            "stderr": "",
            "exit_code": None,
            "execution_time": None,
            "timeout_occurred": False,
        }

        with self.lock:
            self.commands[token] = cmd_info

        thread = threading.Thread(
            target=self._execute_command,
            args=(token, command, shell_type, timeout, working_directory),
        )
        thread.daemon = True
        thread.start()

        return token

    def _execute_command(
        self,
        token: str,
        command: str,
        shell_type: str,
        timeout: int,
        working_directory: Optional[str],
    ):
        """
        在单独线程中执行命令
        """
        try:
            start_time = time.time()

            with self.lock:
                if token in self.commands:
                    self.commands[token]["status"] = "running"

            encoding = "gbk"

            if shell_type == "powershell":
                # 使用绝对路径调用 PowerShell，避免 PATH 环境变量限制
                ps_path = self._get_powershell_path()
                cmd_args = [
                    ps_path,
                    "-NoProfile",
                    "-NoLogo",
                    "-NonInteractive",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-Command",
                    command,
                ]
            else:
                cmd_args = ["cmd", "/c", command]

            result = subprocess.run(
                cmd_args,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=working_directory,
                encoding=encoding,
                stdin=subprocess.DEVNULL,  # 防止等待输入导致挂起
            )

            execution_time = time.time() - start_time

            with self.lock:
                if token in self.commands:
                    self.commands[token].update(
                        {
                            "status": "completed",
                            "stdout": result.stdout,
                            "stderr": result.stderr,
                            "exit_code": result.returncode,
                            "execution_time": execution_time,
                        }
                    )

        except FileNotFoundError as e:
            execution_time = time.time() - start_time
            with self.lock:
                if token in self.commands:
                    self.commands[token].update(
                        {
                            "status": "completed",
                            "stdout": "",
                            "stderr": f"PowerShell not found: {e}",
                            "exit_code": -2,
                            "execution_time": execution_time,
                            "timeout_occurred": False,
                        }
                    )
        except subprocess.TimeoutExpired:
            execution_time = time.time() - start_time
            with self.lock:
                if token in self.commands:
                    self.commands[token].update(
                        {
                            "status": "completed",
                            "stdout": "",
                            "stderr": (
                                f"Command timed out after {timeout} seconds"
                            ),
                            "exit_code": -1,
                            "execution_time": execution_time,
                            "timeout_occurred": True,
                        }
                    )
        except Exception as e:
            execution_time = time.time() - start_time
            with self.lock:
                if token in self.commands:
                    self.commands[token].update(
                        {
                            "status": "completed",
                            "stdout": "",
                            "stderr": str(e),
                            "exit_code": -1,
                            "execution_time": execution_time,
                            "timeout_occurred": False,
                        }
                    )

    def query_command_status(self, token: str) -> Dict[str, Any]:
        """
        查询命令执行状态

        Args:
            token: 命令的token

        Returns:
            包含命令状态的字典
        """
        with self.lock:
            if token not in self.commands:
                return {
                    "token": token,
                    "status": "not_found",
                    "message": "Token not found",
                }

            cmd_info = self.commands[token].copy()

            if cmd_info["status"] == "running":
                return {"token": cmd_info["token"], "status": "running"}
            elif cmd_info["status"] in ["completed", "pending"]:
                return {
                    "token": cmd_info["token"],
                    "status": cmd_info["status"],
                    "exit_code": cmd_info["exit_code"],
                    "stdout": cmd_info["stdout"],
                    "stderr": cmd_info["stderr"],
                    "execution_time": cmd_info["execution_time"],
                    "timeout_occurred": cmd_info["timeout_occurred"],
                }
            else:
                return cmd_info
