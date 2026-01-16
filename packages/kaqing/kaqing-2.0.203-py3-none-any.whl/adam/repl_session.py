from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

from adam.config import Config
from adam.utils import ConfigHolder

class ReplSession:
    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ReplSession, cls).__new__(cls)

        return cls.instance

    def __init__(self):
        if not hasattr(self, 'prompt_session'):
            self.prompt_session = PromptSession(auto_suggest=AutoSuggestFromHistory())
            ConfigHolder().append_command_history = self.append_history

    def append_history(self, entry: str):
        if entry and  self.prompt_session and Config().get('repl.history.push-cat-remote-log-file', True):
            self.prompt_session.history.append_string(entry)