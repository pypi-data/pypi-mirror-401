import datetime
import os
import re
import shutil

from enum import Enum

from croniter import croniter

from endstone import Server
from endstone.scheduler import Task
from endstone.plugin import Plugin
from endstone.command import Command, CommandSender

from .utilities import copy_backup, zip_backup
from .options import PluginOptions
from .retention import RetentionManager
from .commands import CommandBuilder, CommandResult


class QueryStatus(Enum):
    COMPLETE = 1
    RUNNING = 2
    ERROR = 3


class NiceBackup(Plugin):
    prefix = "NiceBackup"
    api_version = "0.6"
    load = "POSTWORLD"

    description = "A simple backup scheduler plugin for Endstone."
    authors = ["Kapdap <kapdap@pm.me>"]
    website = "https://github.com/kapdap/endstone-nicebackup"

    commands = {
        "nice_backup": {
            "description": "Create a backup of the current world.",
            "usages": [
                "/nice_backup",
                "/nice_backup (create|start|stop|status|reload)[action: Action]",
            ],
            "permissions": ["nice_backup.command.backup"],
        }
    }

    permissions = {
        "nice_backup.command": {
            "description": "Allow use of /nice_backup command.",
            "default": "op",
        }
    }

    def __init__(self) -> None:
        self.options = PluginOptions()
        self.next_backup: datetime.datetime | None = None
        self.file_sizes: dict[str, int] = {}
        self.tasks: dict[str, Task] = {}
        self.retention: RetentionManager = RetentionManager(self.options)
        self.is_ready: bool = False
        return super().__init__()

    def read_config(self) -> None:
        try:
            self.save_default_config()
            self.reload_config()

            self.options.load(self.config)
            self.logger.debug(f"Config loaded: {self.options.dump()}")

            self.level_name: str = self.get_level_name()
            self.world_path: str = self.options.worlds_path + "/" + self.level_name

            self.logger.info(f"World path: {self.world_path}")
            self.logger.info(f"Backup path: {self.options.output}")
            self.logger.info(f"Backup schedule: {self.options.schedule or 'disabled'}")
            self.logger.info(
                f"Compression: {'enabled' if self.options.compress else 'disabled'}"
            )

            self.is_ready: bool = True
        except Exception as e:
            self.is_ready: bool = False
            self.logger.error(f"Failed to read plugin configuration: {e}")

    def on_enable(self) -> None:
        self.read_config()

        if self.is_ready and self.options.enabled and self.options.schedule != "":
            self.start_schedule()

    def on_disable(self) -> None:
        self.is_ready = False
        self.stop_schedule()

    def on_command(
        self, sender: CommandSender, command: Command, args: list[str]
    ) -> bool:
        if not self.is_ready:
            self.logger.error("Plugin is not ready. Command cannot be executed.")
            return False

        cmd = args[0].lower() if len(args) > 0 else "create"

        if command.name == "nice_backup":
            if cmd == "create":
                return self.create_backup(sender)
            elif cmd == "start":
                try:
                    self.options.enabled = True
                    self.options.save(self.config)
                    self.save_config()
                    self.start_schedule()
                    return True
                except Exception as e:
                    self.logger.error(f"Failed to start scheduled backups: {e}")
            elif cmd == "stop":
                try:
                    self.options.enabled = False
                    self.options.save(self.config)
                    self.save_config()
                    self.stop_schedule()
                    return True
                except Exception as e:
                    self.logger.error(f"Failed to stop scheduled backups: {e}")
            elif cmd == "status":
                message = (
                    "enabled"
                    if self.options.enabled and self.options.schedule != ""
                    else "disabled"
                )
                self.logger.info(f"Scheduled backups are currently {message}.")
                return True
            elif cmd == "reload":
                try:
                    self.read_config()
                    self.logger.info("Configuration reloaded successfully.")
                    if self.options.enabled and self.options.schedule != "":
                        self.start_schedule()
                    else:
                        self.stop_schedule()
                    return True
                except Exception as e:
                    self.logger.error(f"Failed to reload configuration: {e}")

        return False

    def start_schedule(self) -> None:
        if self.options.schedule == "":
            self.logger.error("Backup schedule is disabled.")

        if "schedule" in self.tasks:
            self.logger.info("Backup schedule is already running.")
            return

        try:
            croniter(self.options.schedule, datetime.datetime.now())
        except (KeyError, ValueError) as e:
            self.logger.error(
                f"Invalid cron expression in schedule '{self.options.schedule}': {e}"
            )
            return

        self.logger.info("Backup schedule started.")
        self.update_next_backup()

        def schedule_backup_task() -> None:
            if self.next_backup and datetime.datetime.now() >= self.next_backup:
                self.create_backup(self.server.command_sender)
                self.update_next_backup()

        self.run_task("schedule", schedule_backup_task, 0, int(self.server.current_tps))

    def stop_schedule(self) -> None:
        self.cancel_task("schedule")
        self.logger.info("Backup schedule stopped.")

    def update_next_backup(self) -> None:
        if self.options.schedule != "":
            cron = croniter(self.options.schedule, datetime.datetime.now())
            self.next_backup = cron.get_next(datetime.datetime)
            self.logger.info(
                f"Next backup: {self.next_backup.strftime('%Y-%m-%d %H:%M:%S')}"
            )

    def create_backup(self, sender: CommandSender) -> bool:
        self.logger.info("Creating world backup...")

        server = sender.server

        result = self.execute_command(server.command_sender, "save hold")

        if result.has_error:
            if "commands.generic.running" in result.errors[0].text:
                self.logger.error(
                    "A backup is already in progress. Aborting new backup."
                )
            else:
                self.logger.error(f"Failed to execute command: {result.command_line}")
                result.log_errors(self.logger)
            return False

        self.clear_file_sizes()

        timeout = datetime.datetime.now() + datetime.timedelta(
            seconds=self.options.timeout
        )

        def get_status_task() -> None:
            try:
                if self.get_status() == QueryStatus.COMPLETE:
                    self.cancel_task("get_status")
                    self.write_backup()
                    self.save_resume()
                    self.retention.clean_backups(self.logger)
                elif datetime.datetime.now() > timeout:
                    raise Exception(
                        f"Failed to prepare server for backup within the timeout period ({self.options.timeout} seconds)."
                    )
            except Exception as e:
                self.logger.error(str(e))

                self.cancel_task("get_status")
                self.save_resume()

        self.run_task(
            "get_status",
            get_status_task,
            int(self.server.current_tps),
            int(self.server.current_tps),
        )

        return True

    def write_backup(self) -> None:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = self.options.filename.format(
            level_name=self.level_name, timestamp=timestamp
        )

        output_path = os.path.join(self.options.output, file_name)
        output_path_tmp = (
            os.path.join(self.options.output_tmp, file_name)
            if self.options.output_tmp
            else output_path
        )

        try:
            if self.options.compress:
                output_path += self.options.extension
                output_path_tmp += self.options.extension

                zip_backup(self.world_path, output_path_tmp, self.file_sizes)
            else:
                copy_backup(self.world_path, output_path_tmp, self.file_sizes)

            if output_path_tmp != output_path:
                shutil.move(output_path_tmp, output_path)

            self.logger.info(f"Saved backup: {output_path}")
        except Exception as e:
            if os.path.exists(output_path):
                if os.path.isdir(output_path):
                    shutil.rmtree(output_path, True)
                else:
                    os.remove(output_path)
            raise e
        finally:
            self.del_tmp_dir()

    def get_status(self) -> QueryStatus:
        result = self.execute_command(self.server.command_sender, "save query")

        if result.has_error:
            if "commands.save-on.notDone" in result.errors[0].text:
                self.logger.info("Backup is still running...")
                return QueryStatus.RUNNING
            else:
                self.logger.error(f"Failed to execute command: {result.command_line}")
            result.log_errors(self.logger)
            return QueryStatus.ERROR

        if "commands.save-all.success" in result.messages[0].text:
            self.set_file_sizes(result.messages[1].params[0].split(", "))
            return QueryStatus.COMPLETE

        return QueryStatus.RUNNING

    def save_resume(self) -> None:
        result = self.execute_command(self.server.command_sender, "save resume")

        if result.has_error:
            self.logger.error(f"Failed to execute command: {result.command_line}")
            result.log_errors(self.logger)

    def set_file_sizes(self, list: list[str]) -> None:
        for info in list:
            parts = info.split(":")
            if len(parts) == 2:
                self.file_sizes[parts[0]] = int(parts[1])

    def clear_file_sizes(self) -> None:
        self.file_sizes = {}

    def get_level_name(self) -> str:
        with open("./server.properties", "r") as file:
            buffer = file.read()

            match = re.search(r"^level-name=(.*)$", buffer, re.MULTILINE)
            if not match:
                raise Exception("Could not find level-name in server.properties")

            return match.group(1)

    def execute_command(
        self, sender: CommandSender, command_line: str
    ) -> CommandResult:
        command = CommandBuilder(
            sender,
            command_line,
        )
        self.logger.debug(f"Executing command: {command.command_line}")
        result = command.execute()
        return result

    def run_task(self, name: str, task, delay: int, period: int) -> Task:
        if name in self.tasks:
            raise Exception(f"Task with name '{name}' already exists.")

        self.tasks[name] = self.server.scheduler.run_task(self, task, delay, period)

        return self.tasks[name]

    def cancel_task(self, task_name: str) -> None:
        if task_name in self.tasks:
            self.tasks[task_name].cancel()
            del self.tasks[task_name]

    def del_tmp_dir(self) -> None:
        if self.options.output_tmp != self.options.output:
            shutil.rmtree(self.options.output_tmp, True)
