from pydantic import BaseModel

class UnifiedAsset(BaseModel):
    asset_id: str
    name: str
    symbol: str
    price_usd: float
    source: str
