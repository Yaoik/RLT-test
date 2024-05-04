from datetime import datetime
from dataclasses import dataclass
import pandas as pd


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
    
    async def request_to_responce(self) -> dict[str, list]:
        return {}
    
    async def _get_labels(self) -> list[str]:
        match self.group_type:
            case 'month':
                labels = pd.date_range(self.dt_from, self.dt_upto, freq='MS').strftime("%Y-%m-%dT%H:00:00").tolist()
            case 'day':
                labels = pd.date_range(self.dt_from, self.dt_upto, freq='D').strftime("%Y-%m-%dT%H:00:00").tolist()
            case 'hour':
                labels =  pd.date_range(self.dt_from, self.dt_upto, freq='H').strftime("%Y-%m-%dT%H:00:00").tolist()
            case _:
                raise ValueError('Invalid group!')
        return labels
    
    