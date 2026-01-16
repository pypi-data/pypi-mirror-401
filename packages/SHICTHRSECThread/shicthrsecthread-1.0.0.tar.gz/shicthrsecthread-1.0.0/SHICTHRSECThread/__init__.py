# *-* coding: utf-8 *-*
# src\__init__.py
# SHICTHRS ECThread
# AUTHOR : SHICTHRS-JNTMTMTM
# Copyright : © 2025-2026 SHICTHRS, Std. All rights reserved.
# lICENSE : GPL-3.0

import threading
from colorama import init
init()

print('\033[1mWelcome to use SHRECThread - better mult-threads library based on threading\033[0m\n|  \033[1;34mGithub : https://github.com/JNTMTMTM/SHICTHRS_ECThread\033[0m')
print('|  \033[1mAlgorithms = rule ; Questioning = approval\033[0m')
print('|  \033[1mCopyright : © 2025-2026 SHICTHRS, Std. All rights reserved.\033[0m\n')

__all__ = ['SHRECThread']

class SHRECThreadException(Exception):
    def __init__(self , message: str) -> None:
        self.message = message
    
    def __str__(self):
        return self.message

class SHRECThread(threading.Thread):
    def __init__(self, *args , **kwargs):
        super().__init__(*args , **kwargs)
        self.exception = None
        self.result = None

    def run(self):
        try:
            if self._target:
                self.result = self._target(*self._args , **self._kwargs)
        except Exception as e:
            self.exception = e

    def join(self , *args , **kwargs):
        super().join(*args ,  **kwargs)
        if self.exception:
            raise SHRECThreadException(f"SHRECThread [ERROR.9000] error occurred while thread running | {self.exception}")
        return self.result