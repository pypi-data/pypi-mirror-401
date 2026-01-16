from abc import ABC
from concurrent.futures import Future, ThreadPoolExecutor
from contextlib import redirect_stdout
import copy
import csv
from datetime import datetime
import importlib
import io
import json
import os
from pathlib import Path
import random
import string
import threading
import traceback
from typing import Callable, Iterator, TypeVar, Union
from dateutil import parser
import subprocess
import sys
import time
import click
import yaml
from prompt_toolkit.completion import Completer

from . import __version__

T = TypeVar('T')

log_state = threading.local()

class ConfigReadable:
    def is_debug() -> bool:
        pass

    def get(self, key: str, default: T) -> T:
        pass

class ConfigHolder:
    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ConfigHolder, cls).__new__(cls)

        return cls.instance

    def __init__(self):
        if not hasattr(self, 'config'):
            # set by Config
            self.config: 'ConfigReadable' = None
            # only for testing
            self.is_display_help = True
            # set by ReplSession
            self.append_command_history = lambda entry: None

NO_SORT = 0
SORT = 1
REVERSE_SORT = -1

def tabulize(lines: list[T], fn: Callable[..., T] = None, header: str = None, dashed_line = False, separator = ' ', to: int = 1, sorted: int = NO_SORT):
    if fn:
        lines = list(map(fn, lines))

    if sorted == SORT:
        lines.sort()
    elif sorted == REVERSE_SORT:
        lines.sort(reverse=True)

    maxes = []
    nls = []

    def format_line(line: str):
        nl = []
        words = line.split(separator)
        for i, word in enumerate(words):
            nl.append(word.ljust(maxes[i], ' '))
        nls.append('  '.join(nl))

    all_lines = lines
    if header:
        all_lines = [header] + lines

    for line in all_lines:
        words = line.split(separator)
        for i, word in enumerate(words):
            lw = len(word)
            if len(maxes) <= i:
                maxes.append(lw)
            elif maxes[i] < lw:
                maxes[i] = lw

    if header:
        format_line(header)
        if dashed_line:
            nls.append(''.ljust(sum(maxes) + (len(maxes) - 1) * 2, '-'))
    for line in lines:
        format_line(line)

    table = '\n'.join(nls)

    if to == 1:
        log(table)
    elif to == 2:
        log2(table)

    return table

def convert_seconds(total_seconds_float):
    total_seconds_int = int(total_seconds_float)  # Convert float to integer seconds

    hours = total_seconds_int // 3600
    remaining_seconds_after_hours = total_seconds_int % 3600

    minutes = remaining_seconds_after_hours // 60
    seconds = remaining_seconds_after_hours % 60

    return hours, minutes, seconds

def epoch(timestamp_string: str):
    return parser.parse(timestamp_string).timestamp()

def log(s = None):
    if not loggable():
        return False

    # want to print empty line for False or empty collection
    if s == None:
        print()
    else:
        click.echo(s)

    return True

def log2(s = None, nl = True):
    if not loggable():
        return False

    if s:
        click.echo(s, err=True, nl=nl)
    else:
        print(file=sys.stderr)

    return True

def elapsed_time(start_time: float):
    end_time = time.time()
    elapsed_time = end_time - start_time
    hours = int(elapsed_time // 3600)
    minutes = int((elapsed_time % 3600) // 60)
    seconds = int(elapsed_time % 60)

    return f"{hours:02}:{minutes:02}:{seconds:02}"

def duration(start_time: float, end_time: float = None):
    if not end_time:
        end_time = time.time()
    d = convert_seconds(end_time - start_time)
    t = []
    if d:
        t.append(f'{d[0]}h')
    if t or d[1]:
        t.append(f'{d[1]}m')
    t.append(f'{d[2]}s')

    return ' '.join(t)

def strip(lines):
    return '\n'.join([line.strip(' ') for line in lines.split('\n')]).strip('\n')

def deep_merge_dicts(dict1, dict2):
    """
    Recursively merges dict2 into dict1.
    If a key exists in both dictionaries and its value is a dictionary,
    the function recursively merges those nested dictionaries.
    Otherwise, values from dict2 overwrite values in dict1.
    """
    merged_dict = dict1.copy()  # Create a copy to avoid modifying original dict1

    for key, value in dict2.items():
        if key in merged_dict and isinstance(merged_dict[key], dict) and isinstance(value, dict):
            # If both values are dictionaries, recursively merge them
            merged_dict[key] = deep_merge_dicts(merged_dict[key], value)
        elif key not in merged_dict or value:
            # Otherwise, overwrite or add the value from dict2
            if key in merged_dict and isinstance(merged_dict[key], Completer):
                pass
                # print('SEAN completer found, ignoring', key, value)
            else:
                merged_dict[key] = value
    return merged_dict

def deep_sort_dict(d):
    """
    Recursively sorts a dictionary by its keys, and any nested lists by their elements.
    """
    if not isinstance(d, (dict, list)):
        return d

    if isinstance(d, dict):
        return {k: deep_sort_dict(d[k]) for k in sorted(d)}

    if isinstance(d, list):
        return sorted([deep_sort_dict(item) for item in d])

def get_deep_keys(d, current_path=""):
    """
    Recursively collects all combined keys (paths) from a deep dictionary.

    Args:
        d (dict): The dictionary to traverse.
        current_path (str): The current path of keys, used for recursion.

    Returns:
        list: A list of strings, where each string represents a combined key path
            (e.g., "key1.subkey1.nestedkey").
    """
    keys = []
    for k, v in d.items():
        new_path = f"{current_path}.{k}" if current_path else str(k)
        if isinstance(v, dict):
            keys.extend(get_deep_keys(v, new_path))
        else:
            keys.append(new_path)
    return keys

def display_help(replace_arg = False):
    if not ConfigHolder().is_display_help:
        return

    args = copy.copy(sys.argv)
    if replace_arg:
        args[len(args) - 1] = '--help'
    else:
        args.extend(['--help'])
    subprocess.run(args)

def random_alphanumeric(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))

    return random_string.lower()

def json_to_csv(json_data: list[dict[any, any]], delimiter: str = ','):
    def flatten_json(y):
        out = {}
        def flatten(x, name=''):
            if type(x) is dict:
                for a in x:
                    flatten(x[a], name + a + '_')
            elif type(x) is list:
                i = 0
                for a in x:
                    flatten(a, name + str(i) + '_')
                    i += 1
            else:
                out[name[:-1]] = x
        flatten(y)
        return out

    if isinstance(json_data, dict):
        json_data = [json_data]

    flattened_data = [flatten_json(record) for record in json_data]
    if flattened_data:
        keys = flattened_data[0].keys()
        header = io.StringIO()
        with redirect_stdout(header) as f:
            dict_writer = csv.DictWriter(f, keys, delimiter=delimiter)
            dict_writer.writeheader()
        body = io.StringIO()
        with redirect_stdout(body) as f:
            dict_writer = csv.DictWriter(f, keys, delimiter=delimiter)
            dict_writer.writerows(flattened_data)

        return header.getvalue().strip('\r\n'), [l.strip('\r') for l in body.getvalue().split('\n')]
    else:
        return None

def log_to_file(config: dict[any, any]):
    with log_exc():
        base = f"/kaqing/logs"
        os.makedirs(base, exist_ok=True)

        now = datetime.now()
        timestamp_str = now.strftime("%Y%m%d-%H%M%S")
        filename = f"{base}/login.{timestamp_str}.txt"
        with open(filename, 'w') as f:
            if isinstance(config, dict):
                try:
                    json.dump(config, f, indent=4)
                except:
                    f.write(config)
            else:
                    f.write(config)

def copy_config_file(rel_path: str, module: str, suffix: str = '.yaml', show_out = True):
    dir = f'{Path.home()}/.kaqing'
    path = f'{dir}/{rel_path}'
    if not os.path.exists(path):
        os.makedirs(dir, exist_ok=True)
        module = importlib.import_module(module)
        with open(path, 'w') as f:
            yaml.dump(module.config(), f, default_flow_style=False)
        if show_out and not idp_token_from_env():
            log2(f'Default {os.path.basename(path).split(suffix)[0] + suffix} has been written to {path}.')

    return path

def idp_token_from_env():
    return os.getenv('IDP_TOKEN')

def is_lambda(func):
    return callable(func) and hasattr(func, '__name__') and func.__name__ == '<lambda>'

def debug(s = None):
    if ConfigHolder().config.is_debug():
        log2(f'DEBUG {s}')

def debug_complete(s = None):
    CommandLog.log(f'DEBUG {s}', config=ConfigHolder().config.get('debugs.complete', 'off'))

def debug_trace():
    if ConfigHolder().config.is_debug():
    # if LogConfig.is_debug():
        log2(traceback.format_exc())

def in_docker() -> bool:
    if os.path.exists('/.dockerenv'):
        return True

    try:
        with open('/proc/1/cgroup', 'rt') as f:
            for line in f:
                if 'docker' in line or 'lxc' in line:
                    return True
    except FileNotFoundError:
        pass

    return False

class Ing:
    def __init__(self, msg: str, suppress_log=False):
        self.msg = msg
        self.suppress_log = suppress_log

    def __enter__(self):
        if not hasattr(log_state, 'ing_cnt'):
            log_state.ing_cnt = 0

        try:
            if not log_state.ing_cnt:
                if not self.suppress_log and not ConfigHolder().config.is_debug():
                    log2(f'{self.msg}...', nl=False)

            return None
        finally:
            log_state.ing_cnt += 1

    def __exit__(self, exc_type, exc_val, exc_tb):
        log_state.ing_cnt -= 1
        if not log_state.ing_cnt:
            if not self.suppress_log and not ConfigHolder().config.is_debug():
                log2(' OK')

        return False

def ing(msg: str, body: Callable[[], None]=None, suppress_log=False):
    if not body:
        return Ing(msg, suppress_log=suppress_log)

    r = None

    t = Ing(msg, suppress_log=suppress_log)
    t.__enter__()
    try:
        r = body()
    finally:
        t.__exit__(None, None, None)

    return r

def loggable():
    return ConfigHolder().config and ConfigHolder().config.is_debug() or not hasattr(log_state, 'ing_cnt') or not log_state.ing_cnt

class TimingNode:
    def __init__(self, depth: int, s0: time.time = time.time(), line: str = None):
        self.depth = depth
        self.s0 = s0
        self.line = line
        self.children = []

    def __str__(self):
        return f'[{self.depth}: {self.line}, children={len(self.children)}]'

    def tree(self):
        lines = []
        if self.line:
            lines.append(self.line)

        for child in self.children:
            if child.line:
                lines.append(child.tree())
        return '\n'.join(lines)

class LogTiming:
    def __init__(self, msg: str, s0: time.time = None):
        self.msg = msg
        self.s0 = s0

    def __enter__(self):
        if (config := ConfigHolder().config.get('debugs.timings', 'off')) not in ['on', 'file']:
            return

        if not hasattr(log_state, 'timings'):
            log_state.timings = TimingNode(0)

        self.me = log_state.timings
        log_state.timings = TimingNode(self.me.depth+1)
        if not self.s0:
            self.s0 = time.time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if (config := ConfigHolder().config.get('debugs.timings', 'off')) not in ['on', 'file']:
            return False

        child = log_state.timings
        log_state.timings.line = timing_log_line(self.me.depth, self.msg, self.s0)

        if child and child.line:
            self.me.children.append(child)
        log_state.timings = self.me

        if not self.me.depth:
            # log timings finally
            CommandLog.log(self.me.tree(), config)

            log_state.timings = TimingNode(0)

        return False

def log_timing(msg: str, body: Callable[[], None]=None, s0: time.time = None):
    if not s0 and not body:
        return LogTiming(msg, s0=s0)

    if not ConfigHolder().config.get('debugs.timings', False):
        if body:
            return body()

        return

    r = None

    t = LogTiming(msg, s0=s0)
    t.__enter__()
    try:
        if body:
            r = body()
    finally:
        t.__exit__(None, None, None)

    return r

def timing_log_line(depth: int, msg: str, s0: time.time):
    elapsed = time.time() - s0
    offloaded = '-' if threading.current_thread().name.startswith('offload') or threading.current_thread().name.startswith('async') else '+'
    prefix = f'[{offloaded} timings] '

    if depth:
        if elapsed > 0.01:
            prefix = ('  ' * (depth-1)) + '* '
        else:
            prefix = '  ' * depth

    return f'{prefix}{msg}: {elapsed:.2f} sec'

class WaitLog:
    wait_log_flag = False

def wait_log(msg: str):
    if not WaitLog.wait_log_flag:
        log2(msg)
        WaitLog.wait_log_flag = True

def clear_wait_log_flag():
    WaitLog.wait_log_flag = False

def bytes_generator_from_file(file_path, chunk_size=4096):
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk

class GeneratorStream(io.RawIOBase):
    def __init__(self, generator):
        self._generator = generator
        self._buffer = b''  # Buffer to store leftover bytes from generator yields

    def readable(self):
        return True

    def _read_from_generator(self):
        try:
            chunk = next(self._generator)
            if isinstance(chunk, str):
                chunk = chunk.encode('utf-8')  # Encode if generator yields strings
            self._buffer += chunk
        except StopIteration:
            pass  # Generator exhausted

    def readinto(self, b):
        # Fill the buffer if necessary
        while len(self._buffer) < len(b):
            old_buffer_len = len(self._buffer)
            self._read_from_generator()
            if len(self._buffer) == old_buffer_len:  # Generator exhausted and buffer empty
                break

        bytes_to_read = min(len(b), len(self._buffer))
        b[:bytes_to_read] = self._buffer[:bytes_to_read]
        self._buffer = self._buffer[bytes_to_read:]
        return bytes_to_read

    def read(self, size=-1):
        if size == -1:  # Read all remaining data
            while True:
                old_buffer_len = len(self._buffer)
                self._read_from_generator()
                if len(self._buffer) == old_buffer_len:
                    break
            data = self._buffer
            self._buffer = b''
            return data
        else:
            # Ensure enough data in buffer
            while len(self._buffer) < size:
                old_buffer_len = len(self._buffer)
                self._read_from_generator()
                if len(self._buffer) == old_buffer_len:
                    break

            data = self._buffer[:size]
            self._buffer = self._buffer[size:]
            return data

class LogTrace:
    def __init__(self, err_msg: Union[str, callable, bool] = None):
        self.err_msg = err_msg

    def __enter__(self):
        return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            if self.err_msg is True:
                log2(str(exc_val))
            elif callable(self.err_msg):
                log2(self.err_msg(exc_val))
            elif self.err_msg is not False and self.err_msg:
                log2(self.err_msg)

            if self.err_msg is not False and ConfigHolder().config.is_debug():
                traceback.print_exception(exc_type, exc_val, exc_tb, file=sys.stderr)

        # swallow exception
        return True

def log_exc(err_msg: Union[str, callable, bool] = None):
    return LogTrace(err_msg=err_msg)

class ParallelService:
    def __init__(self, handler: 'ParallelMapHandler'):
        self.handler = handler

    def map(self, fn: Callable[..., T]) -> Iterator[T]:
        executor = self.handler.executor
        collection = self.handler.collection
        collect = self.handler.collect
        samples_cnt = self.handler.samples

        iterator = None
        if executor:
            iterator = executor.map(fn, collection)
        elif samples_cnt < sys.maxsize:
            samples = []

            for elem in collection:
                if not samples_cnt:
                    break

                samples.append(fn(elem))
                samples_cnt -= 1

            iterator = iter(samples)
        else:
            iterator = map(fn, collection)

        if collect:
            return list(iterator)
        else:
            return iterator

thread_pools: dict[str, ThreadPoolExecutor] = {}
thread_pool_lock = threading.Lock()

class ParallelMapHandler:
    def __init__(self, collection: list, workers: int, samples: int = sys.maxsize, msg: str = None, collect = True, name = None):
        self.collection = collection
        self.workers = workers
        self.executor = None
        self.samples = samples
        self.msg = msg
        if msg and msg.startswith('d`'):
            if ConfigHolder().config.is_debug():
                self.msg = msg.replace('d`', '', 1)
            else:
                self.msg = None
        self.collect = collect
        self.name = name

        self.begin = []
        self.end = []
        self.start_time = None

    def __enter__(self):
        self.start_time = None

        self.calc_msgs()

        if self.workers > 1 and (not self.size() or self.size()) and self.samples == sys.maxsize:
            self.start_time = time.time()

            self.executor = self.pool()
            # self.executor = ThreadPoolExecutor(max_workers=self.workers)
            self.executor.__enter__()

        return ParallelService(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.name and self.executor:
            self.executor.__exit__(exc_type, exc_val, exc_tb)

        if self.end:
            log2(f'{" ".join(self.end)} in {elapsed_time(self.start_time)}.')

        return False

    def pool(self, thread_name_prefix: str = None):
        if not self.name:
            return ThreadPoolExecutor(max_workers=self.workers)

        if self.name not in thread_pools:
            thread_pools[self.name] = ThreadPoolExecutor(max_workers=self.workers, thread_name_prefix=thread_name_prefix)

        return thread_pools[self.name]

    def size(self):
        if not self.collection:
            return 0

        return len(self.collection)

    def calc_msgs(self):
        if not self.msg:
            return

        self.begin = []
        self.end = []
        size = self.size()
        offloaded = False
        serially = False
        sampling = False
        if size == 0:
            offloaded = True
            msg = self.msg.replace('{size}', '1')
        elif self.workers > 1 and size > 1 and self.samples == sys.maxsize:
            msg = self.msg.replace('{size}', f'{size}')
        elif self.samples < sys.maxsize:
            sampling = True
            samples = self.samples
            if self.samples > size:
                samples = size
            msg = self.msg.replace('{size}', f'{samples}/{size} sample')
        else:
            serially = True
            msg = self.msg.replace('{size}', f'{size}')

        for token in msg.split(' '):
            if '|' in token:
                self.begin.append(token.split('|')[0])
                if not sampling and not serially and not offloaded:
                    self.end.append(token.split('|')[1])
            else:
                self.begin.append(token)
                if not sampling and not serially and not offloaded:
                    self.end.append(token)

        if offloaded:
            log2(f'{" ".join(self.begin)} offloaded...')
        elif sampling or serially:
            log2(f'{" ".join(self.begin)} serially...')
        else:
            log2(f'{" ".join(self.begin)} with {self.workers} workers...')

# parallelizers: dict[str, ParallelMapHandler] = {}
# parallelizer_lock = threading.Lock()

def parallelize(collection: list, workers: int = 0, samples = sys.maxsize, msg: str = None, collect = True, name = None):
    return ParallelMapHandler(collection, workers, samples = samples, msg = msg, collect = collect, name = name)
    # if not name:
    #     return ParallelMapHandler(collection, workers, samples = samples, msg = msg, collect = collect)

    # with parallelizer_lock:
    #     if name not in parallelizers:
    #         parallelizers[name] = ParallelMapHandler(collection, workers, samples = samples, msg = msg, collect = collect, name = name)

    # return parallelizers[name]

class OffloadService:
    def __init__(self, handler: 'OffloadHandler'):
        self.handler = handler

    def submit(self, fn: Callable[..., T], /, *args, **kwargs) -> Future[T]:
        executor = self.handler.executor

        if executor:
            return executor.submit(fn, *args, **kwargs)
        else:
            future = Future()

            future.set_result(fn(*args, **kwargs))

            return future

class OffloadHandler(ParallelMapHandler):
    def __init__(self, max_workers: int, msg: str = None, name: str = None):
        super().__init__(None, max_workers, msg=msg, collect=False, name=f'offload-{name}')

    def __enter__(self):
        self.start_time = None
        self.calc_msgs()

        if self.workers > 1:
            self.start_time = time.time()

            self.executor = self.pool(thread_name_prefix='offload')
            # self.executor = ThreadPoolExecutor(max_workers=self.workers, thread_name_prefix='offload')
            self.executor.__enter__()

        return OffloadService(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.name and self.executor:
            self.executor.__exit__(exc_type, exc_val, exc_tb)

        if self.end:
            log2(f'{" ".join(self.end)} in {elapsed_time(self.start_time)}.')

        return False

    def calc_msgs(self):
        if not self.msg:
            return

        self.begin = []
        self.end = []
        size = self.size()

        offloaded = False
        serially = False
        sampling = False
        if size == 0:
            offloaded = True
            msg = self.msg.replace('{size}', '1')
        elif self.workers > 1 and size > 1 and self.samples == sys.maxsize:
            msg = self.msg.replace('{size}', f'{size}')
        elif self.samples < sys.maxsize:
            sampling = True
            samples = self.samples
            if samples > size:
                samples = size
            msg = self.msg.replace('{size}', f'{samples}/{size} sample')
        else:
            serially = True
            msg = self.msg.replace('{size}', f'{size}')

        for token in msg.split(' '):
            if '|' in token:
                self.begin.append(token.split('|')[0])
                if not sampling and not serially and not offloaded:
                    self.end.append(token.split('|')[1])
            else:
                self.begin.append(token)
                if not sampling and not serially and not offloaded:
                    self.end.append(token)

        if offloaded:
            log2(f'{" ".join(self.begin)} offloaded...')
        elif sampling or serially:
            log2(f'{" ".join(self.begin)} serially...')
        else:
            log2(f'{" ".join(self.begin)} with {self.workers} workers...')

# offloaders: dict[str, OffloadHandler] = {}
# offloaders_lock = threading.Lock()

def offload(max_workers: int = 3, msg: str = None, name: str = None):
    return OffloadHandler(max_workers, msg = msg, name = name)
    # if not name:
    #     return OffloadHandler(max_workers, msg = msg)

    # with offloaders_lock:
    #     if name not in offloaders:
    #         offloaders[name] = OffloadHandler(max_workers, msg = msg, name = name)

    # return offloaders[name]

def kaqing_log_file_name(suffix = 'log'):
    return f"{ConfigHolder().config.get('log-prefix', '/tmp/qing')}-{datetime.now().strftime('%d%H%M%S')}.{suffix}"

class LogFileHandler:
    def __init__(self, suffix = 'log'):
        self.suffix = suffix

    def __enter__(self):
        self.f = open(kaqing_log_file_name(), 'w')
        self.f.__enter__()

        return self.f

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.f.__exit__(exc_type, exc_val, exc_tb)

        if ConfigHolder().append_command_history:
            ConfigHolder().append_command_history(f':sh cat {self.f.name}')

        return False

def kaqing_log_file(suffix = 'log'):
    return LogFileHandler(suffix = suffix)

class CommandLog:
    log_file = None

    def log(line: str, config: str = 'off'):
        if config == 'file':
            if not CommandLog.log_file:
                try:
                    CommandLog.log_file = open(kaqing_log_file_name(suffix='cmd.log'), 'w')
                except:
                    pass

            try:
                CommandLog.log_file.write(line + '\n')
            except:
                pass
        elif config == 'on':
            log2(line)

    def close_log_file():
        if CommandLog.log_file:
            try:
                CommandLog.log_file.close()
            except:
                pass

            if ConfigHolder().append_command_history:
                ConfigHolder().append_command_history(f':sh cat {CommandLog.log_file.name}')

            CommandLog.log_file = None

class ExecResult(ABC):
    def exit_code(self) -> int:
        pass
