import os
import shutil
import subprocess
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pantoqa_bridge.config import (APPIUM_BIN, APPIUM_SERVER_HOST, APPIUM_SERVER_PORT, PKG_NAME,
                                   SCRCPY_SERVER_BIN, SERVER_HOST, SERVER_PORT)
from pantoqa_bridge.logger import logger
from pantoqa_bridge.routes.action import router as action_router
from pantoqa_bridge.routes.adb import router as adb_router
from pantoqa_bridge.routes.executor import route as executor_route
from pantoqa_bridge.routes.misc import route as misc_route
from pantoqa_bridge.routes.screen_mirror import route as screen_mirror_route
from pantoqa_bridge.utils.misc import ensure_android_home, start_appium_process_in_bg
from pantoqa_bridge.utils.pkg import get_latest_package_version, get_pkg_version, upgrade_package
from pantoqa_bridge.utils.process import (kill_process_by_port, kill_self_process,
                                          wait_for_port_to_alive)


def create_app() -> FastAPI:

  def on_exit(pid: int, returncode: int) -> None:
    if returncode == 0:
      logger.info(f"Appium process exited normally PID={pid}.")
      return

    logger.info(f"Appium process exited PID={pid}. Return code: {returncode}. ")
    logger.info("Killing bridge server...")
    kill_self_process()

  start_appium_process_in_bg(on_exit=on_exit)

  @asynccontextmanager
  async def lifespan(app: FastAPI):
    await wait_for_port_to_alive(APPIUM_SERVER_PORT, APPIUM_SERVER_HOST, timeout=15)
    yield
    kill_process_by_port(APPIUM_SERVER_PORT, timeout=5)

  app = FastAPI(
    title="PantoAI QA Ext",
    lifespan=lifespan,
  )

  # Allow *.getpanto.ai, *.pantomax.co and localhost origins
  allow_origin_regex = r"(https://(([a-zA-Z0-9-]+\.)*pantomax\.co|([a-zA-Z0-9-]+\.)*getpanto\.ai)|http://localhost(:\d+)?)$"  # noqa: E501

  app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=allow_origin_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
  )
  app.include_router(misc_route)
  app.include_router(executor_route)
  app.include_router(action_router)
  app.include_router(screen_mirror_route)
  app.include_router(adb_router)
  return app


def start_bridge_server(host=SERVER_HOST, port=SERVER_PORT):
  try:
    app = create_app()
    uvicorn.run(
      app,
      host=host,
      port=port,
    )
  except DependencyNotInstalledError as e:
    logger.error(e)
  except Exception as e:
    logger.error(f"Failed to start server: {e}")


class DependencyNotInstalledError(Exception):
  pass


def precheck_required_tools():

  def _current_package_check():
    curent_pkg_version = get_pkg_version(PKG_NAME)
    latest_pkg_version = get_latest_package_version(PKG_NAME)
    if curent_pkg_version < latest_pkg_version:
      logger.info(f"[Check] A new version of {PKG_NAME} is available: {latest_pkg_version} "
                  f"(current: {curent_pkg_version}). Upgrading...")
      upgrade_package(PKG_NAME)
      logger.info(f"[Check] {PKG_NAME} upgraded successfully. Please restart.")
      exit(1)
    else:
      logger.info(f"[Check] {PKG_NAME} is up-to-date: {curent_pkg_version}")

  def _install_uiautomator2() -> None:
    subprocess.check_output(
      [APPIUM_BIN, "driver", "install", "uiautomator2"],
      stderr=subprocess.STDOUT,
      text=True,
    )

  def _install_appium() -> None:
    subprocess.check_output(
      ["npm", "install", "-g", "appium"],
      stderr=subprocess.STDOUT,
      text=True,
    )

  _current_package_check()

  required_tools = [
    ("node", "node --version", "Node.js", None),
    ("npm", "npm --version", "npm", None),
    (APPIUM_BIN, f"{APPIUM_BIN} --version", "Appium", _install_appium),
  ]
  for cmd, version_cmd, name, install_func in required_tools:
    if shutil.which(cmd) is None:
      if not install_func:
        raise DependencyNotInstalledError(f"{name} is not installed or not found in PATH.")
      logger.info(f"[Check] {name} is not installed. Installing...")
      try:
        install_func()
        logger.info(f"[Check] {name} installed successfully.")
      except subprocess.CalledProcessError as e:
        raise DependencyNotInstalledError(f"Failed to install {name}: {e.output}") from e
    else:
      version_output = subprocess.check_output(version_cmd, shell=True, text=True).strip()
      logger.info(f"[Check] {name} found: {version_output}")

  # Check if uiautomator2 server is installed
  uiautomator2_check = subprocess.check_output(
    f"{APPIUM_BIN} driver list --installed --json",
    shell=True,
    text=True,
  )
  if "uiautomator2" in uiautomator2_check:
    logger.info("[Check] Appium uiautomator2 driver is installed.")
  else:
    logger.info("[Check] Appium uiautomator2 driver is not installed. Installing...")
    try:
      _install_uiautomator2()
      logger.info("[Check] Appium uiautomator2 driver installed successfully.")
    except subprocess.CalledProcessError as e:
      raise DependencyNotInstalledError(
        f"Failed to install Appium uiautomator2 driver: {e.output}") from e

  android_home, auto_detected = ensure_android_home()
  if auto_detected and android_home:
    os.environ["ANDROID_HOME"] = android_home
  if android_home:
    logger.info(
      f"[Check] ANDROID_HOME: {android_home} {'(auto-detected)' if auto_detected else ''}")
  else:
    logger.warning("[Check] Android SDK not found. Please install Android SDK and set ANDROID_HOME"
                   "environment variable.")

  adb_android_home = os.path.join(android_home, "platform-tools", "adb") if android_home else None
  if shutil.which("adb"):
    logger.info(f"[Check] adb found in PATH: {shutil.which('adb')}")
  elif adb_android_home and os.path.exists(adb_android_home):
    logger.info(f"[Check] adb found at ANDROID_HOME: {adb_android_home}")
    os.environ["PATH"] += os.pathsep + os.path.dirname(adb_android_home)
  else:
    raise DependencyNotInstalledError("Android SDK not found. "
                                      "Please install Android SDK "
                                      "and set ANDROID_HOME or ANDROID_SDK_ROOT "
                                      "environment variable.")

  if SCRCPY_SERVER_BIN and os.path.exists(SCRCPY_SERVER_BIN):
    logger.info(f"[Check] scrcpy server binary found at: {SCRCPY_SERVER_BIN}")
  else:
    logger.warning(
      "[Check] scrcpy server binary not found. Screen mirroring may not work properly.")


if __name__ == '__main__':
  start_bridge_server()
