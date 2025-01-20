from __future__ import annotations

from typing import Any, Callable, List, Literal, NamedTuple, Optional, Tuple, TypedDict, Union, cast

from typing_extensions import NotRequired

Any = Any
Option = Optional
cast = cast
Callable = Callable
NamedTuple = NamedTuple
NotRequired = NotRequired


class AssetInfo(TypedDict):
    name: str
    szDecimals: int


class Meta(TypedDict):
    universe: list[AssetInfo]


Side = Union[Literal["A"], Literal["B"]]
SIDES: list[Side] = ["A", "B"]


class SpotAssetInfo(TypedDict):
    name: str
    tokens: list[int]
    index: int
    isCanonical: bool


class SpotTokenInfo(TypedDict):
    name: str
    szDecimals: int
    weiDecimals: int
    index: int
    tokenId: str
    isCanonical: bool
    evmContract: str | None
    fullName: str | None


class SpotMeta(TypedDict):
    universe: list[SpotAssetInfo]
    tokens: list[SpotTokenInfo]


class SpotAssetCtx(TypedDict):
    dayNtlVlm: str
    markPx: str
    midPx: str | None
    prevDayPx: str
    circulatingSupply: str
    coin: str


SpotMetaAndAssetCtxs = Tuple[SpotMeta, List[SpotAssetCtx]]


class AllMidsSubscription(TypedDict):
    type: Literal["allMids"]


class L2BookSubscription(TypedDict):
    type: Literal["l2Book"]
    coin: str


class TradesSubscription(TypedDict):
    type: Literal["trades"]
    coin: str


class UserEventsSubscription(TypedDict):
    type: Literal["userEvents"]
    user: str


class UserFillsSubscription(TypedDict):
    type: Literal["userFills"]
    user: str


class CandleSubscription(TypedDict):
    type: Literal["candle"]
    coin: str
    interval: str


class OrderUpdatesSubscription(TypedDict):
    type: Literal["orderUpdates"]
    user: str


class UserFundingsSubscription(TypedDict):
    type: Literal["userFundings"]
    user: str


class UserNonFundingLedgerUpdatesSubscription(TypedDict):
    type: Literal["userNonFundingLedgerUpdates"]
    user: str


class WebData2Subscription(TypedDict):
    type: Literal["webData2"]
    user: str


# If adding new subscription types that contain coin's don't forget to handle automatically rewrite name to coin in info.subscribe
Subscription = Union[
    AllMidsSubscription,
    L2BookSubscription,
    TradesSubscription,
    UserEventsSubscription,
    UserFillsSubscription,
    CandleSubscription,
    OrderUpdatesSubscription,
    UserFundingsSubscription,
    UserNonFundingLedgerUpdatesSubscription,
    WebData2Subscription,
]


class AllMidsData(TypedDict):
    mids: dict[str, str]


class AllMidsMsg(TypedDict):
    channel: Literal["allMids"]
    data: AllMidsData


class L2Level(TypedDict):
    px: str
    sz: str
    n: int


class L2BookData(TypedDict):
    coin: str
    levels: tuple[list[L2Level]]
    time: int


class L2BookMsg(TypedDict):
    channel: Literal["l2Book"]
    data: L2BookData


class PongMsg(TypedDict):
    channel: Literal["pong"]


class Trade(TypedDict):
    coin: str
    side: Side
    px: str
    sz: int
    hash: str
    time: int


class TradesMsg(TypedDict):
    channel: Literal["trades"]
    data: list[Trade]


class Fill(TypedDict):
    coin: str
    px: str
    sz: str
    side: Side
    time: int
    startPosition: str
    dir: str
    closedPnl: str
    hash: str
    oid: int
    crossed: bool
    fee: str
    tid: int
    feeToken: str


# TODO: handle other types of user events
class UserEventsData(TypedDict, total=False):
    fills: list[Fill]


class UserEventsMsg(TypedDict):
    channel: Literal["user"]
    data: UserEventsData


class UserFillsData(TypedDict):
    user: str
    isSnapshot: bool
    fills: list[Fill]


class UserFillsMsg(TypedDict):
    channel: Literal["userFills"]
    data: UserFillsData


class OtherWsMsg(TypedDict, total=False):
    channel: (
        Literal["candle"]
        | Literal["orderUpdates"]
        | Literal["userFundings"]
        | Literal["userNonFundingLedgerUpdates"]
        | Literal["webData2"]
    )
    data: Any


WsMsg = Union[AllMidsMsg, L2BookMsg, TradesMsg, UserEventsMsg, PongMsg, UserFillsMsg, OtherWsMsg]


# b is the public address of the builder, f is the amount of the fee in tenths of basis points. e.g. 10 means 1 basis point
class BuilderInfo(TypedDict):
    b: str
    f: int


class Cloid:
    def __init__(self, raw_cloid: str):
        self._raw_cloid: str = raw_cloid
        self._validate()

    def _validate(self):
        if not self._raw_cloid[:2] == "0x":
            raise TypeError("cloid is not a hex string")
        if not len(self._raw_cloid[2:]) == 32:
            raise TypeError("cloid is not 16 bytes")

    def __str__(self):
        return str(self._raw_cloid)

    def __repr__(self):
        return str(self._raw_cloid)

    @staticmethod
    def from_int(cloid: int) -> Cloid:
        return Cloid(f"{cloid:#034x}")

    @staticmethod
    def from_str(cloid: str) -> Cloid:
        return Cloid(cloid)

    def to_raw(self):
        return self._raw_cloid
