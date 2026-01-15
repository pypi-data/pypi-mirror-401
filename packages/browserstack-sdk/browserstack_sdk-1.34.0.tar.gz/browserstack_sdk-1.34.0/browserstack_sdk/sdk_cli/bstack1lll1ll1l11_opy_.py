# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstack1ll_opy_ = 7
def bstack1l111l1_opy_ (bstack11l_opy_):
    global bstack11ll1ll_opy_
    bstack111l_opy_ = ord (bstack11l_opy_ [-1])
    bstack1l1ll_opy_ = bstack11l_opy_ [:-1]
    bstack11l1ll1_opy_ = bstack111l_opy_ % len (bstack1l1ll_opy_)
    bstack11l1ll_opy_ = bstack1l1ll_opy_ [:bstack11l1ll1_opy_] + bstack1l1ll_opy_ [bstack11l1ll1_opy_:]
    if bstack1lll_opy_:
        bstack11ll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack1l11l11_opy_ + bstack111l_opy_) % bstack1ll_opy_) for bstack1l11l11_opy_, char in enumerate (bstack11l1ll_opy_)])
    else:
        bstack11ll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack1l11l11_opy_ + bstack111l_opy_) % bstack1ll_opy_) for bstack1l11l11_opy_, char in enumerate (bstack11l1ll_opy_)])
    return eval (bstack11ll_opy_)
import logging
from enum import Enum
from typing import Dict, Tuple, Callable, Type, List, Any
import abc
from datetime import datetime, timezone, timedelta
from browserstack_sdk.sdk_cli.bstack1llll111l11_opy_ import bstack1llll1l1l1l_opy_, bstack1lll1llll11_opy_
import os
import threading
class bstack1llll11l111_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack1l111l1_opy_ (u"ࠤࡋࡳࡴࡱࡓࡵࡣࡷࡩ࠳ࢁࡽࠣᄒ").format(self.name)
class bstack1lll1l1ll11_opy_(Enum):
    NONE = 0
    bstack1lll1ll1l1l_opy_ = 1
    bstack1lll1ll1ll1_opy_ = 3
    bstack1llll111l1l_opy_ = 4
    bstack1lll1lll111_opy_ = 5
    QUIT = 6
    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented
    def __repr__(self) -> str:
        return bstack1l111l1_opy_ (u"ࠥࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࡕࡷࡥࡹ࡫࠮ࡼࡿࠥᄓ").format(self.name)
class bstack1llll11l1ll_opy_(bstack1llll1l1l1l_opy_):
    framework_name: str
    framework_version: str
    state: bstack1lll1l1ll11_opy_
    previous_state: bstack1lll1l1ll11_opy_
    bstack1llll11111l_opy_: datetime
    bstack1lll1l1lll1_opy_: datetime
    def __init__(
        self,
        context: bstack1lll1llll11_opy_,
        framework_name: str,
        framework_version: str,
        state=bstack1lll1l1ll11_opy_.NONE,
    ):
        super().__init__(context)
        self.framework_name = framework_name
        self.framework_version = framework_version
        self.state = state
        self.previous_state = bstack1lll1l1ll11_opy_.NONE
        self.bstack1llll11111l_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1lll1l1lll1_opy_ = datetime.now(tz=timezone.utc)
    def bstack1llll1111l1_opy_(self, bstack1lll1lll11l_opy_: bstack1lll1l1ll11_opy_):
        bstack1llll1ll11l_opy_ = bstack1lll1l1ll11_opy_(bstack1lll1lll11l_opy_).name
        if not bstack1llll1ll11l_opy_:
            return False
        if bstack1lll1lll11l_opy_ == self.state:
            return False
        if self.state == bstack1lll1l1ll11_opy_.bstack1lll1ll1ll1_opy_: # bstack1lll1lll1l1_opy_ bstack1lll1ll1lll_opy_ for bstack1lll1l1l1ll_opy_ in bstack1lll1ll11l1_opy_, it bstack1llll1l1ll1_opy_ bstack1llll1l1111_opy_ bstack1llll1ll111_opy_ times bstack1llll111ll1_opy_ a new state
            return True
        if (
            bstack1lll1lll11l_opy_ == bstack1lll1l1ll11_opy_.NONE
            or (self.state != bstack1lll1l1ll11_opy_.NONE and bstack1lll1lll11l_opy_ == bstack1lll1l1ll11_opy_.bstack1lll1ll1l1l_opy_)
            or (self.state < bstack1lll1l1ll11_opy_.bstack1lll1ll1l1l_opy_ and bstack1lll1lll11l_opy_ == bstack1lll1l1ll11_opy_.bstack1llll111l1l_opy_)
            or (self.state < bstack1lll1l1ll11_opy_.bstack1lll1ll1l1l_opy_ and bstack1lll1lll11l_opy_ == bstack1lll1l1ll11_opy_.QUIT)
        ):
            raise ValueError(bstack1l111l1_opy_ (u"ࠦ࡮ࡴࡶࡢ࡮࡬ࡨࠥࡹࡴࡢࡶࡨࠤࡹࡸࡡ࡯ࡵ࡬ࡸ࡮ࡵ࡮࠻ࠢࠥᄔ") + str(self.state) + bstack1l111l1_opy_ (u"ࠧࠦ࠽࠿ࠢࠥᄕ") + str(bstack1lll1lll11l_opy_))
        self.previous_state = self.state
        self.state = bstack1lll1lll11l_opy_
        self.bstack1lll1l1lll1_opy_ = datetime.now(tz=timezone.utc)
        return True
class bstack1llll11l11l_opy_(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1llll11llll_opy_: Dict[str, bstack1llll11l1ll_opy_] = dict()
    framework_name: str
    framework_version: str
    classes: List[Type]
    def __init__(
        self,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
    ):
        self.framework_name = framework_name
        self.framework_version = framework_version
        self.classes = classes
    @abc.abstractmethod
    def bstack1llll11lll1_opy_(self, instance: bstack1llll11l1ll_opy_, method_name: str, bstack1llll11ll11_opy_: timedelta, *args, **kwargs):
        return
    @abc.abstractmethod
    def bstack1lll1lll1ll_opy_(
        self, method_name, previous_state: bstack1lll1l1ll11_opy_, *args, **kwargs
    ) -> bstack1lll1l1ll11_opy_:
        return
    @abc.abstractmethod
    def bstack1llll1l1lll_opy_(
        self,
        target: object,
        exec: Tuple[bstack1llll11l1ll_opy_, str],
        bstack1lll1ll1111_opy_: Tuple[bstack1lll1l1ll11_opy_, bstack1llll11l111_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable:
        return
    def bstack1lll1lllll1_opy_(self, bstack1llll1111ll_opy_: List[str]):
        for clazz in self.classes:
            for method_name in bstack1llll1111ll_opy_:
                bstack1llll1l11ll_opy_ = getattr(clazz, method_name, None)
                if not callable(bstack1llll1l11ll_opy_):
                    self.logger.warning(bstack1l111l1_opy_ (u"ࠨࡵ࡯ࡲࡤࡸࡨ࡮ࡥࡥࠢࡰࡩࡹ࡮࡯ࡥ࠼ࠣࠦᄖ") + str(method_name) + bstack1l111l1_opy_ (u"ࠢࠣᄗ"))
                    continue
                bstack1lll1llllll_opy_ = self.bstack1lll1lll1ll_opy_(
                    method_name, previous_state=bstack1lll1l1ll11_opy_.NONE
                )
                bstack1lll1llll1l_opy_ = self.bstack1lll1l1llll_opy_(
                    method_name,
                    (bstack1lll1llllll_opy_ if bstack1lll1llllll_opy_ else bstack1lll1l1ll11_opy_.NONE),
                    bstack1llll1l11ll_opy_,
                )
                if not callable(bstack1lll1llll1l_opy_):
                    self.logger.warning(bstack1l111l1_opy_ (u"ࠣ࡯ࡨࡸ࡭ࡵࡤࠡࡰࡲࡸࠥࡶࡡࡵࡥ࡫ࡩࡩࡀࠠࡼ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࢃࠠࠩࡽࡶࡩࡱ࡬࠮ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࡾ࠼ࠣࠦᄘ") + str(self.framework_version) + bstack1l111l1_opy_ (u"ࠤࠬࠦᄙ"))
                    continue
                setattr(clazz, method_name, bstack1lll1llll1l_opy_)
    def bstack1lll1l1llll_opy_(
        self,
        method_name: str,
        bstack1lll1llllll_opy_: bstack1lll1l1ll11_opy_,
        bstack1llll1l11ll_opy_: Callable,
    ):
        def wrapped(target, *args, **kwargs):
            bstack1ll11llll_opy_ = datetime.now()
            (bstack1lll1llllll_opy_,) = wrapped.__vars__
            bstack1lll1llllll_opy_ = (
                bstack1lll1llllll_opy_
                if bstack1lll1llllll_opy_ and bstack1lll1llllll_opy_ != bstack1lll1l1ll11_opy_.NONE
                else self.bstack1lll1lll1ll_opy_(method_name, previous_state=bstack1lll1llllll_opy_, *args, **kwargs)
            )
            if bstack1lll1llllll_opy_ == bstack1lll1l1ll11_opy_.bstack1lll1ll1l1l_opy_:
                ctx = bstack1llll1l1l1l_opy_.create_context(self.bstack1lll1ll11ll_opy_(target))
                if not self.bstack1lll1l1ll1l_opy_() or ctx.id not in bstack1llll11l11l_opy_.bstack1llll11llll_opy_:
                    bstack1llll11l11l_opy_.bstack1llll11llll_opy_[ctx.id] = bstack1llll11l1ll_opy_(
                        ctx, self.framework_name, self.framework_version, bstack1lll1llllll_opy_
                    )
                self.logger.debug(bstack1l111l1_opy_ (u"ࠥࡻࡷࡧࡰࡱࡧࡧࠤࡲ࡫ࡴࡩࡱࡧࠤࡨࡸࡥࡢࡶࡨࡨ࠿ࠦࡻࡵࡣࡵ࡫ࡪࡺ࠮ࡠࡡࡦࡰࡦࡹࡳࡠࡡࢀࠤࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦ࠿ࡾࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥࡾࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࡁࢀ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡥࡷࡼࡂࢁࡣࡵࡺ࠱࡭ࡩࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦࡵࡀࠦᄚ") + str(bstack1llll11l11l_opy_.bstack1llll11llll_opy_.keys()) + bstack1l111l1_opy_ (u"ࠦࠧᄛ"))
            else:
                self.logger.debug(bstack1l111l1_opy_ (u"ࠧࡽࡲࡢࡲࡳࡩࡩࠦ࡭ࡦࡶ࡫ࡳࡩࠦࡩ࡯ࡸࡲ࡯ࡪࡪ࠺ࠡࡽࡷࡥࡷ࡭ࡥࡵ࠰ࡢࡣࡨࡲࡡࡴࡵࡢࡣࢂࠦ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࡁࢀࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࢀࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡸࡃࠢᄜ") + str(bstack1llll11l11l_opy_.bstack1llll11llll_opy_.keys()) + bstack1l111l1_opy_ (u"ࠨࠢᄝ"))
            instance = bstack1llll11l11l_opy_.bstack1llll11ll1l_opy_(self.bstack1lll1ll11ll_opy_(target))
            if bstack1lll1llllll_opy_ == bstack1lll1l1ll11_opy_.NONE or not instance:
                ctx = bstack1llll1l1l1l_opy_.create_context(self.bstack1lll1ll11ll_opy_(target))
                self.logger.warning(bstack1l111l1_opy_ (u"ࠢࡸࡴࡤࡴࡵ࡫ࡤࠡ࡯ࡨࡸ࡭ࡵࡤࠡࡷࡱࡸࡷࡧࡣ࡬ࡧࡧ࠾ࠥࢁ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࢁࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀࠤࡨࡺࡸ࠾ࡽࡦࡸࡽࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦࡵࡀࠦᄞ") + str(bstack1llll11l11l_opy_.bstack1llll11llll_opy_.keys()) + bstack1l111l1_opy_ (u"ࠣࠤᄟ"))
                return bstack1llll1l11ll_opy_(target, *args, **kwargs)
            bstack1llll111lll_opy_ = self.bstack1llll1l1lll_opy_(
                target,
                (instance, method_name),
                (bstack1lll1llllll_opy_, bstack1llll11l111_opy_.PRE),
                None,
                *args,
                **kwargs,
            )
            if instance.bstack1llll1111l1_opy_(bstack1lll1llllll_opy_):
                self.logger.debug(bstack1l111l1_opy_ (u"ࠤࡤࡴࡵࡲࡩࡦࡦࠣࡷࡹࡧࡴࡦ࠯ࡷࡶࡦࡴࡳࡪࡶ࡬ࡳࡳࡀࠠࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡴࡷ࡫ࡶࡪࡱࡸࡷࡤࡹࡴࡢࡶࡨࢁࠥࡃ࠾ࠡࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡸࡺࡡࡵࡧࢀࠤ࠭ࢁࡴࡺࡲࡨࠬࡹࡧࡲࡨࡧࡷ࠭ࢂ࠴ࡻ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࢂࠦࡻࡢࡴࡪࡷࢂ࠯ࠠ࡜ࠤᄠ") + str(instance.ref()) + bstack1l111l1_opy_ (u"ࠥࡡࠧᄡ"))
            result = (
                bstack1llll111lll_opy_(target, bstack1llll1l11ll_opy_, *args, **kwargs)
                if callable(bstack1llll111lll_opy_)
                else bstack1llll1l11ll_opy_(target, *args, **kwargs)
            )
            bstack1llll1l11l1_opy_ = self.bstack1llll1l1lll_opy_(
                target,
                (instance, method_name),
                (bstack1lll1llllll_opy_, bstack1llll11l111_opy_.POST),
                result,
                *args,
                **kwargs,
            )
            self.bstack1llll11lll1_opy_(instance, method_name, datetime.now() - bstack1ll11llll_opy_, *args, **kwargs)
            return bstack1llll1l11l1_opy_ if bstack1llll1l11l1_opy_ else result
        wrapped.__name__ = method_name
        wrapped.__vars__ = (bstack1lll1llllll_opy_,)
        return wrapped
    @staticmethod
    def bstack1llll11ll1l_opy_(target: object, strict=True):
        ctx = bstack1llll1l1l1l_opy_.create_context(target)
        instance = bstack1llll11l11l_opy_.bstack1llll11llll_opy_.get(ctx.id, None)
        if instance and instance.bstack1llll1l1l11_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1llll111111_opy_(
        ctx: bstack1lll1llll11_opy_, state: bstack1lll1l1ll11_opy_, reverse=True
    ) -> List[bstack1llll11l1ll_opy_]:
        return sorted(
            filter(
                lambda t: t.state == state
                and t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                bstack1llll11l11l_opy_.bstack1llll11llll_opy_.values(),
            ),
            key=lambda t: t.bstack1llll11111l_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1lll1ll111l_opy_(instance: bstack1llll11l1ll_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1llll1l111l_opy_(instance: bstack1llll11l1ll_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1llll1111l1_opy_(instance: bstack1llll11l1ll_opy_, key: str, value: Any) -> bool:
        instance.data[key] = value
        bstack1llll11l11l_opy_.logger.debug(bstack1l111l1_opy_ (u"ࠦࡸ࡫ࡴࡠࡵࡷࡥࡹ࡫࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࡲࡦࡨࠫ࠭ࢂࠦ࡫ࡦࡻࡀࡿࡰ࡫ࡹࡾࠢࡹࡥࡱࡻࡥ࠾ࠤᄢ") + str(value) + bstack1l111l1_opy_ (u"ࠧࠨᄣ"))
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = bstack1llll11l11l_opy_.bstack1llll11ll1l_opy_(target, strict)
        return bstack1llll11l11l_opy_.bstack1llll1l111l_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = bstack1llll11l11l_opy_.bstack1llll11ll1l_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    def bstack1lll1l1ll1l_opy_(self):
        return self.framework_name == bstack1l111l1_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᄤ")
    def bstack1lll1ll11ll_opy_(self, target):
        return target if not self.bstack1lll1l1ll1l_opy_() else self.bstack1llll11l1l1_opy_()
    @staticmethod
    def bstack1llll11l1l1_opy_():
        return str(os.getpid()) + str(threading.get_ident())