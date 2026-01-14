"""
This file supports Inventory Pattern for nanocore
"""

from datetime import datetime, timedelta
import random
import uuid
from dateutil.parser import parse

from typing import Union, List, Tuple, Dict
from typing_extensions import Annotated


from syncmodels.model import BaseModel, field_validator, Field
from syncmodels.mapper import *

# from models.generic.price import PriceSpecification
# from models.generic.schedules import OpeningHoursSpecificationSpec

from .base import *

# TODO: extend model corpus classes, a.k.a: the pydantic based thesaurus foundations classes
# TODO: this classes may be included in the main thesaurus when project is stable
# TODO: and others projects can benefit from them, making the thesaurus bigger and more powerful


# ---------------------------------------------------------
# NanocoreItem
# ---------------------------------------------------------
# TODO: Inherit from smartmodels.model.app (or similar)
class NanocoreItem(Item):
    """A Nanocore Item model"""

    pass


# ---------------------------------------------------------
# A base NanocoreRequest
# ---------------------------------------------------------
class NanocoreRequest(Request):
    """A Nanocore request to task manager.
    Contains all query data and search parameters.
    """

    pass


# ---------------------------------------------------------
# A base NanocoreResponse
# ---------------------------------------------------------
class NanocoreResponse(Response):
    """A Nanocore response to task manager.
    Contains the search results given by a request.
    """

    data: Dict[UID_TYPE, Item] = {}


# ---------------------------------------------------------
# NanocoreApp
# ---------------------------------------------------------
# TODO: Inherit from smartmodels.model.app (or similar)
class NanocoreApp(Item):
    """A Nanocore App model"""

    pass
