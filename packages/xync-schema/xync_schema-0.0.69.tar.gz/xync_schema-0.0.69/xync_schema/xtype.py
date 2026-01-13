from datetime import datetime
from typing import Literal

from pydantic import BaseModel, model_validator

from xync_schema.enums import AdStatus, OrderStatus
from xync_schema import models


class UnitEx(BaseModel):
    exid: int | str
    ticker: str
    scale: int = None
    rate: float | None = None


class CoinEx(UnitEx):
    p2p: bool = None
    minimum: float | None = None


class CurEx(UnitEx):
    scale: int | None = None
    minimum: int | None = None


class PmExBank(BaseModel):
    # id: int | None = None
    exid: str
    name: str


class BaseAd(BaseModel):
    amount: float
    auto_msg: str
    created_at: int  # utc(0) seconds
    exid: int
    id: int = None
    max_fiat: int
    min_fiat: int
    premium: int
    price: int
    quantity: int
    status: Literal[AdStatus.active, AdStatus.defActive, AdStatus.soldOut]  # 10: online; 20: offline; 30: completed

    cond_id: int | None = None
    maker_id: int
    pair_side_id: int

    pm_ids: list[int | str]

    _unq = "exid", "maker_id"

    @model_validator(mode="after")
    def check_a_or_b(self):
        if not self.amount and not self.quantity:
            raise ValueError("either amount or quantity is required")
        return self


class AdBuy(BaseAd):
    pmexs_: list[models.PmEx]

    class Config:
        arbitrary_types_allowed = True


class AdSale(BaseAd):
    credexs_: list[models.CredEx]

    class Config:
        arbitrary_types_allowed = True


class BaseOrder(BaseModel):
    exid: int  #
    amount: float
    ad_id: int
    cred_id: int
    taker_id: int
    status: OrderStatus = OrderStatus.created
    created_at: datetime
    payed_at: datetime | None = None
    confirmed_at: datetime | None = None
    appealed_at: datetime | None = None

    _unq = "id", "exid", "amount", "ad_id", "cred_id", "taker_id"


class OrderIn(BaseModel):
    exid: int
    amount: float
    created_at: datetime
    ad: models.Ad
    cred: models.Cred
    taker: models.Actor
    id: int = None
    maker_topic: int | None = None
    taker_topic: int | None = None
    status: OrderStatus = OrderStatus.created
    payed_at: datetime | None = None
    confirmed_at: datetime | None = None
    appealed_at: datetime | None = None
    _unq = "id", "exid", "amount", "maker_topic", "taker_topic", "ad", "cred", "taker"

    class Config:
        arbitrary_types_allowed = True
