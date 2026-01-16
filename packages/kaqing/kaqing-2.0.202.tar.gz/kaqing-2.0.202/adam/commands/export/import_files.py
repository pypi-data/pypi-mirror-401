from adam.commands import validate_args
from adam.commands.command import Command
from adam.commands.export.export_sessions import ExportSessions
from adam.commands.export.exporter import export
from adam.commands.export.utils_export import state_with_pod
from adam.repl_state import ReplState, RequiredState

class ImportCSVFiles(Command):
    COMMAND = 'import files'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ImportCSVFiles, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return ImportCSVFiles.COMMAND

    def required(self):
        return RequiredState.CLUSTER_OR_POD

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            with validate_args(args, state, name='file') as spec:
                with state_with_pod(state) as state:
                    with export(state) as exporter:
                        return exporter.import_files(spec)

    def completion(self, state: ReplState):
        # warm up cache
        # ExportSessions.export_session_names(state.sts, state.pod, state.namespace)
        # ExportSessions.export_session_names(state.sts, state.pod, state.namespace, export_state='pending_import')

        return {}

    def help(self, _: ReplState):
        return f'{ImportCSVFiles.COMMAND} <file-names,...>\t import files in session to Athena or SQLite'