from pydantic import BaseModel, Extra, Field, validator
from typing import Literal, Optional
import logging

logger = logging.getLogger(__name__)


class Load(BaseModel, extra=Extra.forbid, allow_population_by_field_name=True):
    """Select external files (``NetCDF`` or ``json`` datagrams, ``pkl`` tables) to load."""

    as_: str = Field(alias="as")
    """Name under which the loaded object will be stored in memory."""

    path: str
    """Path to the file containing the object to be loaded."""

    type: Literal["netcdf", "datagram", "table"] = "datagram"
    """Type of the loaded object. Can be either a ``netcdf`` file created e.g. using
    ``yadg~5.0``, a ``datagram`` file in JSON format created using ``yadg~4.0``, or a
    ``table`` stored in a ``pkl`` file as created by Pandas."""

    check: Optional[bool] = None
    """
    .. deprecated:: 2.1

        The ``check`` attribute of :class:`Load` has been deprecated. The passed value
        is currently ignored, however it **will cause an error** in future versions of
        :class:`~dgbowl_schemas.dgpost.Recipe`.

    """

    @validator("check")
    def check_is_deprecated(cls, v):
        if isinstance(v, bool):
            logger.warning("Recipe->Load->check has been deprecated in Recipe-2.1.")
            return None
        else:
            return v
