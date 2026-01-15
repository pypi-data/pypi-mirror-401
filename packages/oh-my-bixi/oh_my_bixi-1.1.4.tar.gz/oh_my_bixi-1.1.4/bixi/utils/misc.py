import collections
import concurrent.futures
import hashlib
import random
import re
import os
from copy import deepcopy
from typing import Sequence, Callable, Optional
import unicodedata

from bixi.utils.reflect import dynamic_import


def slugify(value: str, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')


def seed_all(seed: int, is_deterministic: bool = False):
    """Seed everything

    Args:
        seed: seed value
        is_deterministic: whether to ensure deterministic CUDA behavior in the cost of computing efficiency
    """

    def _import_or_none(package: str):
        try:
            return dynamic_import(package)
        except Exception:
            return None

    random.seed(seed)
    numpy = _import_or_none('numpy')
    if numpy is not None:
        numpy.random.seed(seed)
    torch = _import_or_none('torch')
    if torch is not None:
        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        if is_deterministic and torch is not None:
            torch.backends.cudnn.deterministic = True


class RegexMatchingSet(object):
    """A set-like object that matches strings against a list of regular expressions."""

    def __init__(self, expressions: Sequence[str]):
        """Initializes REMatchingSet with a list of regular expressions.

        Args:
            expressions (Sequence[str]): A sequence of regular expression strings.
        """
        pattern_composed = '|'.join([f"({expr})" for expr in expressions])
        self.re_pattern = re.compile(pattern_composed)
        self._raw_expressions = expressions

    def __contains__(self, identifier: str) -> bool:
        mo = self.re_pattern.fullmatch(identifier)
        return mo is not None

    def __repr__(self) -> str:
        return f"REMatchingSet{{{self.re_pattern.pattern}}}"


class LRU(collections.OrderedDict):
    """Limit size, evicting the least recently looked-up key when full.

    This class extends `collections.OrderedDict` to implement a Least Recently Used (LRU) cache.
    """

    def __init__(self, max_size=128, *args, **kwargs):
        """Initializes the LRU cache with a specified maximum size.

        Args:
            max_size (int): The maximum size of the cache. Defaults to 128.
        """
        self.max_size = max_size
        super().__init__(*args, **kwargs)

    def __getitem__(self, key):
        value = super().__getitem__(key)
        self.move_to_end(key)
        return value

    def __setitem__(self, key, value):
        if key in self:
            self.move_to_end(key)
        super().__setitem__(key, value)
        if len(self) > self.max_size:
            oldest = next(iter(self))
            del self[oldest]


class CachedRandomAccess(collections.UserDict):
    """A dictionary interface for any random access mapping with caching.

    This class provides a dictionary-like interface for accessing elements
    using a provided function, with optional caching (LRU) to improve performance
    for repeated accesses.
    """

    def __init__(self, fn_access: Callable, max_size: int = -1):
        """Initializes the CachedRandomAccess with a function and optional cache size.

        Args:
            fn_access (Callable): A function that takes an index and returns the corresponding element.
            max_size (int): The maximum size of the cache. If -1, caching is disabled. Defaults to -1.
        """
        super().__init__()
        if max_size > 0:
            self.data = LRU(max_size=max_size)
        self.fn_access = fn_access

    def __getitem__(self, key):
        if key in self.data:
            return self.data[key]
        else:
            elem = self.fn_access(key)
            self.data[key] = elem
            return elem


def salted_seed(seed: int, salt: str, num_digits: Optional[int] = None) -> int:
    """Generate a salted seed using a hash function.
    Args:
        seed (int): The seed value.
        salt (str): The salt string.
        num_digits (Optional[int], optional): The number of digits to return. Defaults to all digits.
    """
    # Convert the seed to a string and concatenate with the salt
    seed_str = str(seed) + salt

    # Create a SHA-256 hash of the concatenated string
    hash_obj = hashlib.sha256(seed_str.encode())

    # Convert the hash to an integer and return it
    seed = int(hash_obj.hexdigest(), 16)

    if num_digits is not None:
        seed = seed % (10 ** num_digits)

    return seed


class AsyncExecutor:
    def __init__(self, max_workers=None):
        self._max_workers = max_workers
        self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
        self._futures = set()  # Track all submitted tasks

    def submit(self, fn: Callable, *args, _is_deepcopy_args: bool = True, **kwargs):
        """Submit a function to the executor.
        Args:
            fn (Callable): The function to execute
            _is_deepcopy_args: Whether to capture the values (deepcopy) of the arguments. Default to True to keep
                consistency between normal blocking execution and asynchronous execution. Turn off to avoid copying
                overhead when you are sure that the arguments are not mutable.
        Returns:
            concurrent.futures.Future: The future object representing the execution of the function
        """
        if _is_deepcopy_args:
            args = deepcopy(args)
            kwargs = deepcopy(kwargs)
        future = self._executor.submit(fn, *args, **kwargs)
        self._futures.add(future)
        future.add_done_callback(lambda f: self._futures.discard(f))  # Auto-remove completed futures
        return future

    def wait_all(self, timeout=None):
        """Wait for all pending tasks to complete.

        Args:
            timeout (float, optional): The maximum number of seconds to wait. If None, wait indefinitely.

        Returns:
            tuple: A tuple containing two sets: (done_futures, not_done_futures)
        """
        futures_to_wait = set(self._futures)  # Create a copy of the set
        if not futures_to_wait:
            return set(), set()

        return concurrent.futures.wait(futures_to_wait, timeout=timeout)

    def shutdown(self, wait=True):
        self._executor.shutdown(wait=wait)
        self._futures.clear()

    def __del__(self):
        self.shutdown(wait=True)


def wandb_resumable_init(iteration_index: Optional[int] = None,
                         wandb_id: str = None,
                         wandb_project: str = None,
                         wandb_name: str = None,
                         wandb_group: str = None,
                         wandb_config: dict = None
                         ):
    """Initialize wandb with resumability support.
    Note: wandb is tricky to initialize in the DDP + restorability setting. The correct strategy is to initialize
        it in the main process. and then restore the run from the wandb run id.

    Args:
        iteration_index: The (training) iteration number to resume from.
            It is the key to determine whether to resume a run or not.
            If None, it means we are evaluating a run.
            If <=0, it means we are creating a new run.
            If >0, it means we are resuming a run from a previous run.

        wandb_id: The wandb run id.
        wandb_project: The wandb project name.
        wandb_name: The wandb run name.
        wandb_group: The wandb group name.
        wandb_config: The wandb config dictionary.        

    Raises:
        ValueError: If the rank is not the main process.
    """
    try:
        import wandb
        
    except ImportError:
        raise ImportError("wandb is not installed. Please install wandb to use this function.")

    if iteration_index is None:
        """Used in evaluation, resume from a run with workspace project & id"""
        resume = 'must'
        resume_from = None

    elif iteration_index <= 0:
        """Create a new run, so no need to resume"""
        resume = None
        resume_from = None

    elif iteration_index > 0:
        """Training resuming from a previous run. Use resume_from instead of resume to allow
        resuming from an offline run that did not synced.
        """
        resume = None
        resume_from = f"{wandb_id}?_step={iteration_index}"

    else:
        raise ValueError(f"Invalid iteration_index: {iteration_index}")

    # detecting rank 0 process to initialize wandb
    rank = int(os.getenv('RANK') or 0)
    if rank != 0:
        raise ValueError(f"Wandb should be initialized in the main process. Rank {rank} is not the main process.")

    wandb.init(
        id=wandb_id,
        project=wandb_project,
        name=wandb_name,
        group=wandb_group,
        config=wandb_config,
        resume=resume,
        resume_from=resume_from
    )


# =========================================================
# Global thread pool
# =========================================================
_global_executor = None
_DEFAULT_POOLSIZE = 8


def get_global_executor(max_workers=None) -> AsyncExecutor:
    global _global_executor, _DEFAULT_POOLSIZE
    if max_workers is None:
        max_workers = _DEFAULT_POOLSIZE
    if _global_executor is None:
        _global_executor = AsyncExecutor(max_workers=max_workers)
    return _global_executor
