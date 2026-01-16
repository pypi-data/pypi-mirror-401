from adam.commands import extract_options
from adam.commands.command import Command
from adam.commands.export.exporter import export
from adam.repl_state import ReplState, RequiredState

class ExportTables(Command):
    COMMAND = 'export'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ExportTables, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return ExportTables.COMMAND

    def required(self):
        return RequiredState.CLUSTER_OR_POD

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            with extract_options(args, '--export-only') as (args, export_only):
                with export(state) as exporter:
                    return exporter.export(args, export_only=export_only)

    def completion(self, state: ReplState):
        return {}

    def help(self, _: ReplState):
        return f'{ExportTables.COMMAND} [* [in KEYSPACE]] | [TABLE] [as target-name] [with consistency <level>]\t export tables to Sqlite, Athena or CSV file'