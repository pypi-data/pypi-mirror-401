import asyncio
import functools
import os
import shutil
import subprocess
import threading
import time
from collections.abc import Callable
from pathlib import Path

from pantoqa_bridge.config import APPIUM_BIN, APPIUM_SERVER_HOST, APPIUM_SERVER_PORT, IS_WINDOWS
from pantoqa_bridge.logger import logger
from pantoqa_bridge.utils.process import kill_process_by_port


def find_android_home() -> str | None:
  """
  Find ANDROID_HOME path by checking:
  1. adb location (SDK root is parent of platform-tools)
  2. Common SDK installation paths
  Returns the path as a string, or None if not found.
  """

  if os.environ.get("ANDROID_HOME"):
    return os.environ["ANDROID_HOME"]

  if os.environ.get("ANDROID_SDK_ROOT"):
    return os.environ["ANDROID_SDK_ROOT"]

  # Try to find SDK root from adb location
  adb_path = shutil.which("adb")
  if adb_path:
    # adb is in <SDK>/platform-tools/adb, so SDK root is grandparent
    sdk_root = Path(adb_path).resolve().parent.parent
    if sdk_root.exists():
      return str(sdk_root)

  # Try common SDK locations
  home = Path.home()
  if IS_WINDOWS:
    common_paths = [
      Path(f"{home}/AppData/Local/Android/Sdk"),
      Path("C:/Android/Sdk"),
      Path("C:/Android/android-sdk"),
    ]
  else:  # Mac/Linux
    common_paths = [
      Path(f"{home}/Library/Android/sdk"),
      Path(f"{home}/Android/Sdk"),
      Path("/usr/local/android-sdk"),
    ]

  for sdk_path in common_paths:
    if sdk_path.exists() and (sdk_path / "platform-tools").exists():
      return str(sdk_path)

  return None


def ensure_android_home() -> tuple[str | None, bool]:
  """
  Ensure ANDROID_HOME is set in environment variables.
  If not set, attempt to auto-detect and set it.

  :return: A tuple containing the ANDROID_HOME path (or None if not found)
  and a boolean indicating if it was auto-detected and set.
  :rtype: tuple[str | None, bool]
  """
  if os.environ.get("ANDROID_HOME"):
    return os.environ.get("ANDROID_HOME"), False

  if os.environ.get("ANDROID_SDK_ROOT"):
    return os.environ.get("ANDROID_SDK_ROOT"), False

  android_home = find_android_home()
  if not android_home:
    return None, False

  return android_home, True


def start_appium_process_in_bg(on_exit: Callable[[int, int], None]):

  def start():
    cmd = [
      APPIUM_BIN,
      "--session-override",
      "--port",
      str(APPIUM_SERVER_PORT),
      "--address",
      APPIUM_SERVER_HOST,
    ]
    logger.info(f"Starting Appium at http://{APPIUM_SERVER_HOST}:{APPIUM_SERVER_PORT}")

    proc = subprocess.Popen(
      cmd,
      stdout=subprocess.DEVNULL,
      stderr=subprocess.DEVNULL,
      start_new_session=True,
      shell=False,
      env=os.environ.copy(),
    )
    logger.info("Appium process started with PID: %d", proc.pid)
    return proc

  def start_in_loop():
    max_retries = 2
    proc: subprocess.Popen[bytes] | None = None
    while max_retries > 0:
      max_retries -= 1
      proc = start()
      proc.wait()
      if proc.returncode != 1:
        break
      logger.error("Appium process exited with errors. Return code: %d", proc.returncode)
      kill_process_by_port(APPIUM_SERVER_PORT, timeout=5)
      time.sleep(1)
    if proc:
      on_exit(proc.pid, proc.returncode)
    else:
      on_exit(-1, -1)

  try:
    kill_process_by_port(APPIUM_SERVER_PORT, timeout=5)
  except Exception:
    pass
  thread = threading.Thread(target=start_in_loop, daemon=True)
  thread.start()
  logger.info("Starting Appium process in background.")


def make_sync(func):

  @functools.wraps(func)
  def wrapper(*args, **kwargs):
    return asyncio.run(func(*args, **kwargs))

  return wrapper
