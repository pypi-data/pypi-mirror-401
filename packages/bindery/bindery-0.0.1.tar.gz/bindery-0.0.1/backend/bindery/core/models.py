from typing import List, Optional
from pydantic import BaseModel

class MethodNode(BaseModel):
    name: str
    return_type: str
    arguments: List[str]
    is_const: bool = False
    is_static: bool = False

class ClassNode(BaseModel):
    name: str
    methods: List[MethodNode]
    namespace: Optional[str] = None
    header_file: str
