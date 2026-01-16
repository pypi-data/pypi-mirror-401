from adam.commands import validate_args
from adam.commands.command import Command
from adam.commands.export.export_sessions import ExportSessions, export_session
from adam.repl_state import ReplState, RequiredState

class DownloadExportSession(Command):
    COMMAND = 'download export session'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(DownloadExportSession, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return DownloadExportSession.COMMAND

    def required(self):
        return RequiredState.CLUSTER_OR_POD

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            with validate_args(args, state, name='export session') as session:
                with export_session(state) as sessions:
                    sessions.download_session(session)

            return state

    def completion(self, state: ReplState):
        return {}
        # return super().completion(state, {session: None for session in ExportSessions.export_session_names(state.sts, state.pod, state.namespace, export_state='pending_import')})

    def help(self, _: ReplState):
        return f'{DownloadExportSession.COMMAND} <export-session-name>\t download csv files in export session'