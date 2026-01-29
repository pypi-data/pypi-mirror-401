from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID

from pydantic import BaseModel, HttpUrl
from pydantic_extra_types.currency_code import Currency


class DataSource(str, Enum):
    ALPHA_VANTAGE = "ALPHA_VANTAGE"
    COINGECKO = "COINGECKO"
    EOD_HISTORICAL_DATA = "EOD_HISTORICAL_DATA"
    FINANCIAL_MODELING_PREP = "FINANCIAL_MODELING_PREP"
    FRED = "FRED"
    GHOSTFOLIO = "GHOSTFOLIO"
    GOOGLE_SHEETS = "GOOGLE_SHEETS"
    MANUAL = "MANUAL"
    YAHOO = "YAHOO"


class ActivityType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    DIVIDEND = "DIVIDEND"
    FEE = "FEE"
    INTEREST = "INTEREST"
    LIABILITY = "LIABILITY"
    ITEM = "ITEM"


class AccountBalance(BaseModel):
    """
    Reference: https://github.com/ghostfolio/ghostfolio/blob/main/libs/common/src/lib/interfaces/account-balance.interface.ts
    """

    date: datetime
    value: float


class Platform(BaseModel):
    """
    Reference: https://github.com/ghostfolio/ghostfolio/blob/main/prisma/schema.prisma
    """

    id: UUID
    name: str | None = None
    url: HttpUrl | None = None


class Account(BaseModel):
    """
    Reference: https://github.com/ghostfolio/ghostfolio/blob/main/libs/common/src/lib/interfaces/responses/export-response.interface.ts
    """

    id: UUID
    balance: float
    currency: Currency
    isExcluded: bool
    name: str
    platformId: UUID | None = None
    balances: list[AccountBalance] | None = None
    comment: str | None = None


class Activity(BaseModel):
    """
    Reference: https://github.com/ghostfolio/ghostfolio/blob/main/libs/common/src/lib/interfaces/activities.interface.ts
    """

    id: UUID | None = None
    accountId: UUID
    comment: str | None = None
    currency: Currency
    dataSource: DataSource | None = None
    date: datetime
    fee: float
    quantity: float
    symbol: str
    type: ActivityType
    unitPrice: float
    tags: list[Any] | None = None


class Meta(BaseModel):
    """
    Reference: https://github.com/ghostfolio/ghostfolio/blob/main/libs/common/src/lib/interfaces/responses/export-response.interface.ts
    """

    date: datetime
    version: str


class UserSettings(BaseModel):
    currency: Currency
    performanceCalculationType: str | None = None


class User(BaseModel):
    settings: UserSettings | None = None


class GhostfolioExport(BaseModel):
    """
    Reference: https://github.com/ghostfolio/ghostfolio/blob/main/libs/common/src/lib/interfaces/responses/export-response.interface.ts
    """

    meta: Meta
    accounts: list[Account]
    activities: list[Activity]
    platforms: list[Platform] | None = []
    assetProfiles: list[Any] | None = []
    tags: list[Any] | None = []
    user: User | None = None
