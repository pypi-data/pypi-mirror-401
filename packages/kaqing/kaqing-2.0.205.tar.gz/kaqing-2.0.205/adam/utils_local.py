import subprocess
from adam.config import Config
from adam.utils import ExecResult, debug

def local_tmp_dir():
    return Config().get('local-tmp-dir', '/tmp/qing-db')

class LocalExecResult(ExecResult):
    def __init__(self, stdout: str, stderr: str, command: str = None, code = 0, log_file: str = None):
        self.stdout: str = stdout
        self.stderr: str = stderr
        self.command: str = command
        self.code = code
        self.pod = 'local'
        self.log_file = log_file

    def exit_code(self) -> int:
        return self.code

    def cat_log_file_cmd(self):
        if self.log_file:
            return f':sh cat {self.log_file}'

        return None

    def __str__(self):
        return f'{"OK" if self.exit_code() == 0 else self.exit_code()} {self.command}'

    def __audit_extra__(self):
        return self.log_file if self.log_file else None

def local_exec(cmd: list[str], shell=False, show_out=False):
    stdout = ''
    stderr = ''
    returncode = 0

    try:
        if show_out:
            debug(' '.join(cmd))

        r = subprocess.run(cmd, capture_output=True, text=True, shell=shell)
        stdout = r.stdout
        stderr = r.stderr
        returncode = r.returncode
    except FileNotFoundError as e:
        pass

    return LocalExecResult(stdout, stderr, ' '.join(cmd), returncode)