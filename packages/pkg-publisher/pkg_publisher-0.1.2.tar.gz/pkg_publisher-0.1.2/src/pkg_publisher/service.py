"""
pkg-publisher 服务模块 - Python 包构建和发布服务（异步版本）
"""

import os
import subprocess
import logging
import shutil
import threading
import uuid
import time
from datetime import datetime
from typing import Dict, Optional, List, Any
from pathlib import Path
import requests

__version__ = "0.1.2"

ENV_PYTHON_PATH = "PKG_PUBLISHER_PYTHON_PATH"

logger = logging.getLogger("pkg-publisher")


def _get_python_env() -> Optional[dict]:
    """
    获取带有 Python 路径的环境变量

    Returns:
        修改后的环境变量字典，如果未设置则返回 None
    """
    python_path = os.environ.get(ENV_PYTHON_PATH)
    if python_path and os.path.isfile(python_path):
        env = os.environ.copy()
        python_dir = os.path.dirname(python_path)
        env["PATH"] = f"{python_dir}{os.pathsep}{env.get('PATH', '')}"
        logger.info(f"PKG_PUBLISHER_PYTHON_PATH is set to: {python_path}")
        return env
    else:
        logger.info("PKG_PUBLISHER_PYTHON_PATH is not set, using default python")
        return None


def setup_logging(level: int = logging.INFO) -> None:
    """
    配置日志输出
    
    Args:
        level: 日志级别，默认 INFO
    
    日志输出位置：
    1. 控制台 (stderr)
    2. 文件: %TEMP%/pkg-publisher.log 或 /tmp/pkg-publisher.log
    
    可通过环境变量配置：
    - PKG_PUBLISHER_LOG_LEVEL: 日志级别 (DEBUG/INFO/WARNING/ERROR/CRITICAL)
    - PKG_PUBLISHER_LOG_FILE: 自定义日志文件路径
    """
    import tempfile
    
    formatter = logging.Formatter(
        "[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    log_file = os.environ.get("PKG_PUBLISHER_LOG_FILE")
    if not log_file:
        log_file = os.path.join(tempfile.gettempdir(), "pkg-publisher.log")
    
    try:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.info(f"Log file: {log_file}")
    except Exception as e:
        logger.warning(f"Failed to create log file {log_file}: {e}")
    
    logger.setLevel(level)
    
    env_level = os.environ.get("PKG_PUBLISHER_LOG_LEVEL", "").upper()
    if env_level in ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"):
        logger.setLevel(getattr(logging, env_level))


def get_version() -> str:
    """
    获取 pkg-publisher 版本号
    
    Returns:
        版本号字符串
    """
    return __version__


def get_api_token(repository: str = "pypi") -> str:
    """
    从环境变量获取 PyPI API Token

    Args:
        repository: 仓库名称 (pypi 或 testpypi)

    Returns:
        API Token 字符串

    Raises:
        ValueError: 如果未找到对应的 API Token
    """
    if repository == "testpypi":
        token = os.getenv("TEST_PYPI_API_TOKEN")
        env_var_name = "TEST_PYPI_API_TOKEN"
    else:
        token = os.getenv("PYPI_API_TOKEN")
        env_var_name = "PYPI_API_TOKEN"
    
    if not token:
        raise ValueError(
            f"{env_var_name} not found in environment variables. "
            f"Please set the {env_var_name} environment variable."
        )
    
    return token


def get_repository_url(repository: str = "pypi") -> str:
    """
    获取 PyPI 仓库 URL

    Args:
        repository: 仓库名称 (pypi 或 testpypi)

    Returns:
        仓库 URL 字符串
    """
    if repository == "testpypi":
        return "https://test.pypi.org/legacy/"
    else:
        return "https://upload.pypi.org/legacy/"


def _clean_build_artifacts(project_path: str) -> None:
    """
    清理旧的构建产物

    Args:
        project_path: 项目路径
    """
    build_dir = os.path.join(project_path, "build")
    dist_dir = os.path.join(project_path, "dist")
    egg_info_dirs = list(Path(project_path).glob("*.egg-info"))

    for directory in [build_dir, dist_dir] + egg_info_dirs:
        if os.path.exists(directory):
            try:
                if os.path.isdir(directory):
                    shutil.rmtree(directory)
                else:
                    os.remove(directory)
                logger.debug(f"Removed: {directory}")
            except Exception as e:
                logger.warning(f"Failed to remove {directory}: {e}")


def _find_dist_files(project_path: str) -> List[str]:
    """
    查找构建产物文件

    Args:
        project_path: 项目路径

    Returns:
        构建产物文件路径列表
    """
    dist_dir = os.path.join(project_path, "dist")
    dist_files = []

    if os.path.exists(dist_dir):
        for file in os.listdir(dist_dir):
            if file.endswith((".whl", ".tar.gz")):
                dist_files.append(os.path.join(dist_dir, file))

    return sorted(dist_files)


def _get_package_files(package_path: str) -> List[str]:
    """
    获取包文件列表

    Args:
        package_path: 包文件路径（支持通配符）

    Returns:
        包文件路径列表
    """
    import glob

    if "*" in package_path or "?" in package_path:
        return sorted(glob.glob(package_path))
    else:
        return [package_path] if os.path.exists(package_path) else []


def _do_build_package(
    project_path: Optional[str],
    clean: bool
) -> Dict[str, Any]:
    """
    执行包构建（内部同步方法）

    Args:
        project_path: 项目路径
        clean: 是否清理旧的构建产物

    Returns:
        包含构建结果的字典
    """
    if project_path is None:
        project_path = os.getcwd()

    project_path = os.path.abspath(project_path)
    logger.info(f"Building package in: {project_path}")

    if not os.path.isdir(project_path):
        error_msg = f"Project path does not exist: {project_path}"
        logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg,
            "output": "",
            "dist_files": [],
            "project_path": project_path,
        }

    if clean:
        _clean_build_artifacts(project_path)

    # Determine which Python executable to use
    python_executable = "python"
    env_vars = _get_python_env()
    if env_vars and ENV_PYTHON_PATH in env_vars:
        python_executable = env_vars[ENV_PYTHON_PATH]
    
    logger.info(f"Using Python executable: {python_executable} for build")
    
    try:
        result = subprocess.run(
            [python_executable, "-m", "build"],
            cwd=project_path,
            capture_output=True,
            text=True,
            check=True,
            env=env_vars,
        )

        logger.info("Build completed successfully")

        dist_files = _find_dist_files(project_path)

        return {
            "success": True,
            "output": result.stdout,
            "error": result.stderr,
            "dist_files": dist_files,
            "project_path": project_path,
        }

    except subprocess.CalledProcessError as e:
        error_msg = f"Build failed: {e}"
        logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg,
            "output": e.stdout if e.stdout else "",
            "dist_files": [],
            "project_path": project_path,
        }
    except Exception as e:
        error_msg = f"Build failed with exception: {e}"
        logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg,
            "output": "",
            "dist_files": [],
            "project_path": project_path,
        }


def _do_publish_package(
    package_path: Optional[str],
    repository: str,
    skip_existing: bool,
    project_path: Optional[str],
) -> Dict[str, Any]:
    """
    执行包发布（内部同步方法）

    Args:
        package_path: 包文件路径
        repository: 仓库名称
        skip_existing: 是否跳过已存在的版本
        project_path: 项目路径

    Returns:
        包含发布结果的字典
    """
    logger.info(f"Publishing to {repository}")

    try:
        api_token = get_api_token(repository)
        logger.debug(f"API token retrieved for {repository}")
    except ValueError as e:
        error_msg = f"Failed to get API token: {e}"
        logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg,
            "output": "",
            "repository": repository,
            "package_files": [],
        }

    if package_path is None:
        if project_path is None:
            project_path = os.getcwd()
        dist_dir = os.path.join(project_path, "dist")
        if os.path.exists(dist_dir):
            package_path = os.path.join(dist_dir, "*")
        else:
            error_msg = f"dist directory not found: {dist_dir}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg,
                "output": "",
                "repository": repository,
                "package_files": [],
            }

    # Determine which Python executable to use for twine
    python_executable = "python"
    env_vars = _get_python_env()
    if env_vars and ENV_PYTHON_PATH in env_vars:
        python_executable = env_vars[ENV_PYTHON_PATH]
    
    logger.info(f"Using Python executable: {python_executable} for publish")
    
    # 获取仓库 URL
    repository_url = get_repository_url(repository)
    
    cmd = [
        python_executable,
        "-m",
        "twine",
        "upload",
        package_path,
        "--repository-url",
        repository_url,
        "--username",
        "__token__",
        "--password",
        api_token,
        "--non-interactive",  # 禁用交互模式，避免进度条问题
    ]

    if skip_existing:
        cmd.append("--skip-existing")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            env=env_vars,
            timeout=300,  # 5分钟超时
        )

        logger.info(f"Successfully published to {repository}")

        package_files = _get_package_files(package_path)

        return {
            "success": True,
            "output": result.stdout,
            "error": result.stderr,
            "repository": repository,
            "package_files": package_files,
        }

    except subprocess.CalledProcessError as e:
        error_msg = f"Publish failed: {e}"
        logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg,
            "output": e.stdout if e.stdout else "",
            "repository": repository,
            "package_files": [],
        }
    except Exception as e:
        error_msg = f"Publish failed with exception: {e}"
        logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg,
            "output": "",
            "repository": repository,
            "package_files": [],
        }


def _do_validate_package(package_path: str) -> Dict[str, Any]:
    """
    执行包验证（内部同步方法）

    Args:
        package_path: 包文件路径

    Returns:
        包含验证结果的字典
    """
    logger.info(f"Validating package: {package_path}")

    if not os.path.exists(package_path):
        error_msg = f"Package file not found: {package_path}"
        logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg,
            "output": "",
            "package_path": package_path,
        }

    # Determine which Python executable to use for twine check
    python_executable = "python"
    env_vars = _get_python_env()
    if env_vars and ENV_PYTHON_PATH in env_vars:
        python_executable = env_vars[ENV_PYTHON_PATH]
    
    logger.info(f"Using Python executable: {python_executable} for validation")
    
    try:
        result = subprocess.run(
            [python_executable, "-m", "twine", "check", package_path],
            capture_output=True,
            text=True,
            check=True,
            env=env_vars,
        )

        logger.info("Package validation passed")

        return {
            "success": True,
            "output": result.stdout,
            "error": result.stderr,
            "package_path": package_path,
        }

    except subprocess.CalledProcessError as e:
        error_msg = f"Validation failed: {e}"
        logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg,
            "output": e.stdout if e.stdout else "",
            "package_path": package_path,
        }
    except Exception as e:
        error_msg = f"Validation failed with exception: {e}"
        logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg,
            "output": "",
            "package_path": package_path,
        }


def _do_get_package_info(
    package_name: str,
    version: Optional[str],
    repository: str,
) -> Dict[str, Any]:
    """
    获取包信息（内部同步方法）

    Args:
        package_name: 包名
        version: 版本号
        repository: 仓库名称

    Returns:
        包含包信息的字典
    """
    logger.info(f"Getting package info: {package_name}")

    if repository == "testpypi":
        base_url = "https://test.pypi.org/pypi"
    else:
        base_url = "https://pypi.org/pypi"

    if version:
        url = f"{base_url}/{package_name}/{version}/json"
    else:
        url = f"{base_url}/{package_name}/json"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        logger.info(f"Successfully retrieved info for {package_name}")

        return {
            "success": True,
            "package_name": package_name,
            "version": version,
            "info": data,
            "error": None,
        }

    except requests.exceptions.RequestException as e:
        error_msg = f"Failed to get package info: {e}"
        logger.error(error_msg)
        return {
            "success": False,
            "package_name": package_name,
            "version": version,
            "info": {},
            "error": error_msg,
        }
    except Exception as e:
        error_msg = f"Failed to get package info with exception: {e}"
        logger.error(error_msg)
        return {
            "success": False,
            "package_name": package_name,
            "version": version,
            "info": {},
            "error": error_msg,
        }


class PkgPublisherService:
    """
    异步包构建和发布服务类，管理所有异步任务的执行和状态
    """

    def __init__(self):
        self.tasks: Dict[str, Dict[str, Any]] = {}
        self.lock = threading.Lock()

    def build_package(
        self,
        project_path: Optional[str] = None,
        clean: bool = True,
    ) -> str:
        """
        异步构建 Python 包

        Args:
            project_path: 项目路径，默认为当前目录
            clean: 是否清理旧的构建产物

        Returns:
            任务执行的token
        """
        token = str(uuid.uuid4())

        task_info = {
            "token": token,
            "task_type": "build_package",
            "project_path": project_path or os.getcwd(),
            "clean": clean,
            "status": "pending",
            "start_time": datetime.now(),
            "stdout": "",
            "stderr": "",
            "exit_code": None,
            "execution_time": None,
        }

        with self.lock:
            self.tasks[token] = task_info

        thread = threading.Thread(
            target=self._execute_build_package,
            args=(token, project_path, clean),
        )
        thread.daemon = True
        thread.start()

        return token

    def publish_package(
        self,
        package_path: Optional[str] = None,
        repository: str = "pypi",
        skip_existing: bool = False,
        project_path: Optional[str] = None,
    ) -> str:
        """
        异步发布 Python 包

        Args:
            package_path: 包文件路径，默认为 dist/*
            repository: 仓库名称 (pypi 或 testpypi)
            skip_existing: 是否跳过已存在的版本
            project_path: 项目路径，用于查找 dist 目录

        Returns:
            任务执行的token
        """
        token = str(uuid.uuid4())

        task_info = {
            "token": token,
            "task_type": "publish_package",
            "package_path": package_path,
            "repository": repository,
            "skip_existing": skip_existing,
            "project_path": project_path,
            "status": "pending",
            "start_time": datetime.now(),
            "stdout": "",
            "stderr": "",
            "exit_code": None,
            "execution_time": None,
        }

        with self.lock:
            self.tasks[token] = task_info

        thread = threading.Thread(
            target=self._execute_publish_package,
            args=(token, package_path, repository, skip_existing, project_path),
        )
        thread.daemon = True
        thread.start()

        return token

    def validate_package(self, package_path: str) -> str:
        """
        异步验证 Python 包

        Args:
            package_path: 包文件路径

        Returns:
            任务执行的token
        """
        token = str(uuid.uuid4())

        task_info = {
            "token": token,
            "task_type": "validate_package",
            "package_path": package_path,
            "status": "pending",
            "start_time": datetime.now(),
            "stdout": "",
            "stderr": "",
            "exit_code": None,
            "execution_time": None,
        }

        with self.lock:
            self.tasks[token] = task_info

        thread = threading.Thread(
            target=self._execute_validate_package,
            args=(token, package_path),
        )
        thread.daemon = True
        thread.start()

        return token

    def get_package_info(
        self,
        package_name: str,
        version: Optional[str] = None,
        repository: str = "pypi",
    ) -> str:
        """
        异步获取 Python 包信息

        Args:
            package_name: 包名
            version: 版本号（可选）
            repository: 仓库名称 (pypi 或 testpypi)

        Returns:
            任务执行的token
        """
        token = str(uuid.uuid4())

        task_info = {
            "token": token,
            "task_type": "get_package_info",
            "package_name": package_name,
            "version": version,
            "repository": repository,
            "status": "pending",
            "start_time": datetime.now(),
            "stdout": "",
            "stderr": "",
            "exit_code": None,
            "execution_time": None,
        }

        with self.lock:
            self.tasks[token] = task_info

        thread = threading.Thread(
            target=self._execute_get_package_info,
            args=(token, package_name, version, repository),
        )
        thread.daemon = True
        thread.start()

        return token

    def _execute_build_package(
        self, token: str, project_path: Optional[str], clean: bool
    ):
        """
        在单独线程中执行包构建
        """
        start_time = time.time()

        try:
            with self.lock:
                if token in self.tasks:
                    self.tasks[token]["status"] = "running"

            result = _do_build_package(project_path, clean)

            execution_time = time.time() - start_time

            with self.lock:
                if token in self.tasks:
                    self.tasks[token].update(
                        {
                            "status": "completed",
                            "stdout": result.get("output", ""),
                            "stderr": result.get("error", ""),
                            "exit_code": 0 if result.get("success") else -1,
                            "execution_time": execution_time,
                            "result_data": result,
                        }
                    )

        except Exception as e:
            execution_time = time.time() - start_time
            with self.lock:
                if token in self.tasks:
                    self.tasks[token].update(
                        {
                            "status": "completed",
                            "stdout": "",
                            "stderr": str(e),
                            "exit_code": -1,
                            "execution_time": execution_time,
                            "result_data": {"success": False, "error": str(e), "dist_files": []},
                        }
                    )

    def _execute_publish_package(
        self,
        token: str,
        package_path: Optional[str],
        repository: str,
        skip_existing: bool,
        project_path: Optional[str],
    ):
        """
        在单独线程中执行包发布
        """
        start_time = time.time()

        try:
            with self.lock:
                if token in self.tasks:
                    self.tasks[token]["status"] = "running"

            result = _do_publish_package(
                package_path, repository, skip_existing, project_path
            )

            execution_time = time.time() - start_time

            with self.lock:
                if token in self.tasks:
                    self.tasks[token].update(
                        {
                            "status": "completed",
                            "stdout": result.get("output", ""),
                            "stderr": result.get("error", ""),
                            "exit_code": 0 if result.get("success") else -1,
                            "execution_time": execution_time,
                            "result_data": result,
                        }
                    )

        except Exception as e:
            execution_time = time.time() - start_time
            with self.lock:
                if token in self.tasks:
                    self.tasks[token].update(
                        {
                            "status": "completed",
                            "stdout": "",
                            "stderr": str(e),
                            "exit_code": -1,
                            "execution_time": execution_time,
                            "result_data": {"success": False, "error": str(e), "package_files": []},
                        }
                    )

    def _execute_validate_package(self, token: str, package_path: str):
        """
        在单独线程中执行包验证
        """
        start_time = time.time()

        try:
            with self.lock:
                if token in self.tasks:
                    self.tasks[token]["status"] = "running"

            result = _do_validate_package(package_path)

            execution_time = time.time() - start_time

            with self.lock:
                if token in self.tasks:
                    self.tasks[token].update(
                        {
                            "status": "completed",
                            "stdout": result.get("output", ""),
                            "stderr": result.get("error", ""),
                            "exit_code": 0 if result.get("success") else -1,
                            "execution_time": execution_time,
                            "result_data": result,
                        }
                    )

        except Exception as e:
            execution_time = time.time() - start_time
            with self.lock:
                if token in self.tasks:
                    self.tasks[token].update(
                        {
                            "status": "completed",
                            "stdout": "",
                            "stderr": str(e),
                            "exit_code": -1,
                            "execution_time": execution_time,
                            "result_data": {"success": False, "error": str(e), "package_path": package_path},
                        }
                    )

    def _execute_get_package_info(
        self,
        token: str,
        package_name: str,
        version: Optional[str],
        repository: str,
    ):
        """
        在单独线程中获取包信息
        """
        start_time = time.time()

        try:
            with self.lock:
                if token in self.tasks:
                    self.tasks[token]["status"] = "running"

            result = _do_get_package_info(package_name, version, repository)

            execution_time = time.time() - start_time

            with self.lock:
                if token in self.tasks:
                    self.tasks[token].update(
                        {
                            "status": "completed",
                            "stdout": result.get("output", ""),
                            "stderr": result.get("error", ""),
                            "exit_code": 0 if result.get("success") else -1,
                            "execution_time": execution_time,
                            "result_data": result,
                        }
                    )

        except Exception as e:
            execution_time = time.time() - start_time
            with self.lock:
                if token in self.tasks:
                    self.tasks[token].update(
                        {
                            "status": "completed",
                            "stdout": "",
                            "stderr": str(e),
                            "exit_code": -1,
                            "execution_time": execution_time,
                            "result_data": {"success": False, "error": str(e), "package_name": package_name},
                        }
                    )

    def query_task_status(self, token: str) -> Dict[str, Any]:
        """
        查询任务执行状态

        Args:
            token: 任务的token

        Returns:
            包含任务状态的字典
        """
        with self.lock:
            if token not in self.tasks:
                return {
                    "token": token,
                    "status": "not_found",
                    "message": "Token not found",
                }

            task_info = self.tasks[token].copy()

            if task_info["status"] == "running":
                return {
                    "token": task_info["token"],
                    "status": "running",
                    "task_type": task_info["task_type"],
                }
            elif task_info["status"] in ["completed", "pending"]:
                return {
                    "token": task_info["token"],
                    "status": task_info["status"],
                    "task_type": task_info["task_type"],
                    "exit_code": task_info["exit_code"],
                    "stdout": task_info["stdout"],
                    "stderr": task_info["stderr"],
                    "execution_time": task_info["execution_time"],
                    "result_data": task_info.get("result_data"),
                }
            else:
                return task_info
