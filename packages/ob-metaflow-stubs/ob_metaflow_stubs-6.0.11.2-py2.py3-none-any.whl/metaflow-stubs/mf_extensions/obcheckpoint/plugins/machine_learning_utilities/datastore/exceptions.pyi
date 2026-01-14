######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.15.3+obcheckpoint(0.2.10);ob(v1)                                                  #
# Generated on 2026-01-13T15:18:19.144291                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception

from ......exception import MetaflowException as MetaflowException

class DatastoreReadInitException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, message):
        ...
    ...

class DatastoreWriteInitException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, message):
        ...
    ...

class DatastoreNotReadyException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, message):
        ...
    ...

