from datetime import datetime
from dataclasses import dataclass
import pandas as pd
from mongo import collection

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
        labels = await self._get_labels()
        dataset = [0] * len(labels)
        response = {"dataset": dataset, "labels": labels}
        
        
        pipeline = [
            {"$match": {"dt": {"$gte": self.dt_from, "$lte": self.dt_upto}}},
            {"$group": await self._get_group()},
            {"$sort": {"_id": 1}}
        ]

        result = collection.aggregate(pipeline)
        
        for res in result:
            index = response['labels'].index(res['_id']['datetime'])
            response['dataset'][index] = res['total_value']
            
        return response
    
    async def _get_group(self) -> dict:
        match self.group_type:
            case 'month':
                return {
                    '_id': {
                            'month': {'$month':'$dt'}, 
                            'datetime':{"$dateToString": {"format": "%Y-%m-01T00:00:00", "date": "$dt"}},
                        }, 
                        "total_value": {"$sum": "$value"}
                    }
            case 'day':
                return {
                    '_id': { 
                            'day': {'$dayOfMonth':'$dt'}, 
                            'datetime':{"$dateToString": {"format": "%Y-%m-%dT00:00:00", "date": "$dt"}},
                        }, 
                        "total_value": {"$sum": "$value"}
                    }
            case 'hour':
                return {
                    '_id': { 
                            'hour': {'$hour':'$dt'}, 
                            'datetime':{"$dateToString": {"format": "%Y-%m-%dT%H:00:00", "date": "$dt"}},
                        }, 
                        "total_value": {"$sum": "$value"}
                    }
            case _:
                raise ValueError('Invalid group!')

      
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
    
    