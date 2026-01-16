# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import Literal

from ..._models import BaseModel
from ..job_file import JobFile

__all__ = ["FileListResponse"]


class FileListResponse(BaseModel):
    """Response containing a list of files for a job"""

    data: List[JobFile]

    status: Literal["success"]
    """Status indicates the response status "success" """
