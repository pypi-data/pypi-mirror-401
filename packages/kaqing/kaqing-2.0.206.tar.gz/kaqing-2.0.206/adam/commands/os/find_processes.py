from adam.commands import extract_options, validate_args
from adam.commands.command import Command
from adam.commands.devices.devices import Devices
from adam.commands.export.utils_export import state_with_pod
from adam.repl_state import ReplState, RequiredState
from adam.utils import log2, tabulize

class FindProcesses(Command):
    COMMAND = 'find processes'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(FindProcesses, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return FindProcesses.COMMAND

    def required(self):
        return [RequiredState.CLUSTER_OR_POD, RequiredState.APP_APP, ReplState.P]

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            with extract_options(args, '-kill') as (args, kill):
                with validate_args(args, state, name='words to look for'):
                    arg = ' | '.join([f'grep {a}' for a in args])
                    awk = "awk '{ print $1, $2, $8, $NF }'"
                    rs = Devices.of(state).bash(state, state, f"ps -ef | grep -v grep | {arg} | {awk}".split(' '))

                    lines: list[list[str]] = []
                    for r in rs:
                        for l in r.stdout.split('\n'):
                            l = l.strip(' \t\r\n')
                            if not l:
                                continue

                            tokens = [r.pod] + l.split(' ')
                            lines.append(tokens)

                    pids = []
                    for l in lines:
                        pids.append(f'{l[2]}@{l[0]}')

                    tabulize(lines, lambda l: '\t'.join(l), header = 'POD\tUSER\tPID\tCMD\tLAST_ARG', separator='\t')
                    log2()
                    log2(f'PIDS with {",".join(args)}: {",".join(pids)}')

                    if kill:
                        log2()
                        for pidp in pids:
                            pid_n_pod = pidp.split('@')
                            pid = pid_n_pod[0]
                            if len(pid_n_pod) < 2:
                                continue

                            pod = pid_n_pod[1]

                            log2(f'@{pod} bash kill -9 {pid}')

                            with state_with_pod(state, pod) as state1:
                                Devices.of(state).bash(state, state1, ['kill', '-9', pid])

                    return rs

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, _: ReplState):
        return f'{FindProcesses.COMMAND} word... [-kill]\t find processes with words'