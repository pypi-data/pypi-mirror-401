######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.15.3+obcheckpoint(0.2.10);ob(v1)                                                  #
# Generated on 2026-01-13T15:18:19.042249                                                            #
######################################################################################################

from __future__ import annotations


from ...exception import MetaflowException as MetaflowException
from ...exception import MetaflowInternalError as MetaflowInternalError
from .gs_exceptions import MetaflowGSPackageError as MetaflowGSPackageError

def parse_gs_full_path(gs_uri):
    ...

def check_gs_deps(func):
    """
    The decorated function checks GS dependencies (as needed for Google Cloud storage backend). This includes
    various GCP SDK packages, as well as a Python version of >=3.7
    """
    ...

def process_gs_exception(*args, **kwargs):
    ...

