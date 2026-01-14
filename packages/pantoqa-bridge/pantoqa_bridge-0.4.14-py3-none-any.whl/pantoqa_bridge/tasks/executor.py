import abc
import asyncio
import importlib
import importlib.util
import sys
import uuid
from pathlib import Path

from appium import webdriver
from appium.options.android import UiAutomator2Options

from pantoqa_bridge.config import APPIUM_SERVER_URL, MAESTRO_BIN
from pantoqa_bridge.logger import logger


class QAExecutable(abc.ABC):

  def __init__(self, files: list[str]):
    self.files = files

  @abc.abstractmethod
  async def execute(self):
    ...


class MaestroExecutable(QAExecutable):

  def __init__(self,
               files: list[str],
               maestro_bin: str | None = None,
               device_serial: str | None = None):
    super().__init__(files)
    self.maestro_bin = maestro_bin or MAESTRO_BIN
    self.device_serial = device_serial

  async def execute(self):
    yml_files = [f for f in self.files if (f.endswith('.yml') or f.endswith('.yaml'))]
    if not yml_files:
      logger.error("No Maestro test files found.")
      return
    cmd = [self.maestro_bin, "test"]
    if self.device_serial:
      cmd.extend(["--device", self.device_serial])
    cmd.extend(yml_files)
    logger.debug(f"Maestro command: {' '.join(cmd)}")

    logger.info(f"Running Maestro: {' '.join(cmd)}")
    result = await asyncio.create_subprocess_exec(
      *cmd,
      stdout=asyncio.subprocess.PIPE,
      stderr=asyncio.subprocess.STDOUT,
    )

    if not result.stdout:
      logger.error("No output from Maestro process.")
      return
    async for line in result.stdout:
      logger.info(f"> {line.decode().strip()}")
    await result.wait()
    logger.info(f"Maestro finished with return code: {result.returncode}")
    return result.returncode


class AppiumExecutable(QAExecutable):

  def __init__(self,
               files: list[str],
               appium_url: str | None = None,
               device_serial: str | None = None):
    super().__init__(files)
    options = UiAutomator2Options()
    options.set_capability("platformName", "Android")
    options.set_capability("automationName", "UiAutomator2")
    options.set_capability("deviceName", "Android Device")
    if device_serial:
      options.set_capability("udid", device_serial)
    options.set_capability("noReset", True)
    options.set_capability("fullReset", False)
    options.set_capability("ignoreHiddenApiPolicyError", True)
    self.default_wait_in_sec = 20
    self.options = options
    self.appium_url = appium_url or APPIUM_SERVER_URL

  async def execute(self):
    file = self.files[0]
    filepath = Path(file).resolve()
    module_name = f"_dynamic_{uuid.uuid4().hex}"
    spec = importlib.util.spec_from_file_location(module_name, filepath)
    assert spec, "Spec should not be None"
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore

    try:
      with webdriver.Remote(self.appium_url, options=self.options) as driver:
        driver.implicitly_wait(self.default_wait_in_sec)
        output = module.main(driver)
        return output
    finally:
      if module_name in sys.modules:
        del sys.modules[module_name]
      del module
