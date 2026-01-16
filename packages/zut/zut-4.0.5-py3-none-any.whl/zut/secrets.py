"""
Definition and resolution of delayable secrets (specified with `file:`, `pass:` or `env:` prefixes) and other secret/password helpers.
"""
from __future__ import annotations

import logging
import os
import secrets
import subprocess
from pathlib import Path
from shutil import which
from typing import TYPE_CHECKING, overload

from zut.gpg import PASS_ROOT, get_pass, get_pass_path, is_pass_available

if TYPE_CHECKING:
    from typing import Literal

_logger = logging.getLogger(__name__)


#region Pass

__shortcuts__ = (PASS_ROOT, get_pass, get_pass_path, is_pass_available,)

#endregion


#region File secrets

def is_file_secret_available(name: str|Path|None = None) -> bool:
    if name is None:
        path = Path.cwd().joinpath('secret')
        if not (path.is_dir() and os.access(path, os.R_OK)):
            return False

        path = Path(f'/run/secrets')
        return path.is_dir() and os.access(path, os.R_OK)
        
    path = name if isinstance(name, Path) else get_file_secret_path(name)  
    return path.is_file() and os.access(path, os.R_OK)

def get_file_secret_path(name: str) -> Path:
    if '/' in name or '\\' in name:
        return Path(name)

    path = Path.cwd().joinpath('secrets', name)
    if path.is_file() and os.access(path, os.R_OK):
        return path

    path = Path(f'/run/secrets/{name}')
    return path

@overload
def get_file_secret(name: str|Path, *, required: Literal[True]) -> str:
    ...

@overload
def get_file_secret(name: str|Path, *, required: Literal[False] = False) -> str|None:
    ...

def get_file_secret(name: str|Path, *, required = False) -> str|None:
    path = name if isinstance(name, Path) else get_file_secret_path(name)

    if not is_file_secret_available(path):
        if required:
            raise ValueError("Secret file not available: '%s'" % name)
        return None

    _logger.debug("Read secret file '%s'", path)
    text = path.read_text(encoding='utf-8-sig')
    return text.rstrip('\r\n')

#endregion


#region Env secrets

def is_env_secret_available(name: str|None = None) -> bool:
    if name is None:
        return True
    
    if os.environ.get(name):
        return True
    
    path = os.environ.get(f'{name}_FILE')
    if path:
        return is_file_secret_available(path)
    else:
        return False

@overload
def get_env_secret(name: str, *, required: Literal[True]) -> str:
    ...

@overload
def get_env_secret(name: str, *, required: Literal[False] = False) -> str|None:
    ...

def get_env_secret(name: str, *, required = False) -> str|None:
    if not is_env_secret_available(name):
        if required:
            raise ValueError("Env secret not available: '%s'" % name)
        return None

    _logger.debug("Read env secret '%s'", name)
    value = os.environ.get(name)
    if value:
        return value
    
    path = os.environ.get(f'{name}_FILE')
    if path:
        return get_file_secret(path, required=required)

    if required:
        raise ValueError("Env secret not available: '%s'" % name)
    return None

#endregion


#region Systemd creds

SYSTEMD_CREDS_ROOT = Path(os.environ['CREDENTIALS_DIRECTORY']) if os.environ.get('CREDENTIALS_DIRECTORY') else Path.cwd().joinpath('creds')
    
def is_systemd_cred_available(name: str|Path|None = None) -> bool:    
    if not which('systemd-creds'):
        return False
    
    if name is None:
        return SYSTEMD_CREDS_ROOT.is_dir() and os.access(SYSTEMD_CREDS_ROOT, os.R_OK)
    
    path = name if isinstance(name, Path) else get_systemd_cred_path(name)    
    if not (path.is_file() and os.access(path, os.R_OK)):
        return False
    return True

def get_systemd_cred_path(name: str) -> Path:
    if '/' in name or '\\' in name:
        return Path(name)
    else:
        return SYSTEMD_CREDS_ROOT.joinpath(name)

@overload
def get_systemd_cred(name: str|Path, *, required: Literal[True]) -> str:
    ...

@overload
def get_systemd_cred(name: str|Path, *, required: Literal[False] = False) -> str|None:
    ...

def get_systemd_cred(name: str|Path, *, required = False) -> str|None:
    path = name if isinstance(name, Path) else get_systemd_cred_path(name)

    if not is_systemd_cred_available(path):
        if required:
            raise ValueError("Systemd cred not available: '%s'" % name)
        return None

    _logger.debug("Read systemd cred '%s'", path)
    try:
        text = subprocess.check_output(['systemd-creds', 'decrypt', path, '-'], text=True, encoding='utf-8')
        return text
    except subprocess.CalledProcessError as err:
        from zut.process import ProcessError
        raise ProcessError(err, cmd='systemd-creds decrypt') from None

#endregion


#region Generic secrets (specified with prefixes)

def is_secret_available(spec: str|None) -> bool:
    if spec is None:
        return False
    
    elif spec.startswith('file:'):
        return is_file_secret_available(spec[len('file:'):])
    
    elif spec.startswith('pass:'):
        return is_pass_available(spec[len('pass:'):])
    
    elif spec.startswith('systemd:'):
        return is_systemd_cred_available(spec[len('systemd:'):])
    
    elif spec.startswith('env:'):
        return is_env_secret_available(spec[len('env:'):])
    
    else:
        return True


@overload
def resolve_secret(spec: str|None, *, required: Literal[True]) -> str:
    ...

@overload
def resolve_secret(spec: str|None, *, required: Literal[False] = False) -> str|None:
    ...

def resolve_secret(spec: str|None, *, required = False) -> str|None:
    if spec is None:
        if required:
            raise ValueError("Missing required secret")
        else:
            return None
    
    elif spec.startswith('file:'):
        return get_file_secret(spec[len('file:'):], required=required)
    
    elif spec.startswith('pass:'):
        return get_pass(spec[len('pass:'):], required=required)
    
    elif spec.startswith('systemd:'):
        return get_systemd_cred(spec[len('systemd:'):], required=required)
    
    elif spec.startswith('env:'):
        return get_env_secret(spec[len('env:'):], required=required)
    
    elif spec.startswith('value:'):
        return spec[len('value:'):]
    
    else:
        return spec


class Secret(str):
    def __init__(self, spec: str, *, is_resolved = False):
        self.spec = spec
        self._is_resolved = is_resolved
        self._value = None
        super().__init__()
    
    def __str__(self):
        return self.get_value(required=True)
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self.spec})"

    @property
    def is_resolved(self):
        return self._is_resolved

    @overload
    def get_value(self, *, required: Literal[True]) -> str:
        ...

    @overload
    def get_value(self, *, required: Literal[False] = False) -> str|None:
        ...
        
    def get_value(self, *, required = False) -> str|None:
        if not self._is_resolved:
            self._value = resolve_secret(self.spec, required=required)
            self._is_resolved = True
        return self._value

#endregion


#region Random utils

RANDOM_STRING_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

def get_random_string(length: int, *, allowed_chars=RANDOM_STRING_CHARS):
    """
    Return a securely generated random string.

    The bit length of the returned value can be calculated with the formula:
        log_2(len(allowed_chars)^length)

    For example, with default `allowed_chars` (26+26+10), this gives:
      * length: 12, bit length =~ 71 bits
      * length: 22, bit length =~ 131 bits
    """
    return "".join(secrets.choice(allowed_chars) for _ in range(length))

#endregion
