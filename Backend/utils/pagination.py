from typing import Generic, TypeVar, List
from pydantic.generics import GenericModel

T = TypeVar("T")

class Page(GenericModel, Generic[T]):
    content: List[T]
    total_elements: int
    total_pages: int
    page: int
    size: int
