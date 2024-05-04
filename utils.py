from datetime import datetime
from dataclasses import dataclass

@dataclass
class Request:
    dt_from: str
    dt_upto: str
    group_type: str

class Handler:
    def __init__(self, request:Request) -> None:
        self.dt_from = datetime.fromisoformat(request.dt_from)
        self.dt_upto = datetime.fromisoformat(request.dt_upto)
        self.group_type = request.group_type
        
    def __str__(self) -> str:
        return f'{self.dt_from} - {self.dt_upto}\n{self.group_type=}'
    