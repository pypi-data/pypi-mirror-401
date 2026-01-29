"""Test Result Schema"""
from typing import Optional, Union

from pydantic import BaseModel, ConfigDict, Field


class ResultBase(BaseModel):
    """Test Result Message.

    Message structure for sending the results of a `pytest` test result back
    to the Test Executor.
    """

    test_id: Optional[str] = None
    error_code: Optional[str] = Field(default=None, repr=False)
    error_msg: Optional[str] = Field(default=None, repr=False)
    test_name: Optional[str] = None
    description: Optional[str] = None
    operator_id: Optional[int] = None
    min_limit: Optional[Union[str, int, float, bool]] = None
    max_limit: Optional[Union[str, int, float, bool]] = None
    meas: Optional[Union[str, int, float, bool]] = None
    start: Optional[float] = Field(default=None, repr=False)
    stop: Optional[float] = Field(default=None, repr=False)
    duration: Optional[float] = None
    passed: Optional[bool] = None


class ResultCreate(ResultBase):
    """Test Result Create schema."""

    test_id: Optional[str] = None
    test_name: str
    operator_id: int
    start: Optional[float] = Field(default=None, repr=False)
    stop: Optional[float] = Field(default=None, repr=False)
    duration: Optional[float] = None
    passed: bool


class ResultUpdate(ResultBase):
    """Test Result Update schema."""

    passed: bool
    pass


class ResultInDBBase(ResultBase):
    """Test Result Database base schema."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    uuid: str
    run_id: Optional[int] = None
    operator_id: int


class Result(ResultInDBBase):
    """Test Result schema."""

    pass


class ResultInDB(ResultInDBBase):
    pass
