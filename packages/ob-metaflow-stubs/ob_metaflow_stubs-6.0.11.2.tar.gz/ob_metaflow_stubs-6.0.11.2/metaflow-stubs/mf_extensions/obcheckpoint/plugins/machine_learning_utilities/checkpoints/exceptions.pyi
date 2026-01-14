######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.15.3+obcheckpoint(0.2.10);ob(v1)                                                  #
# Generated on 2026-01-13T15:18:19.022377                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception

from ......exception import MetaflowException as MetaflowException

class CheckpointNotAvailableException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, message):
        ...
    ...

class CheckpointException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, message):
        ...
    ...

