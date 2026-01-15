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
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1lll1ll1l11_opy_ import (
    bstack1llll11l11l_opy_,
    bstack1llll11l1ll_opy_,
    bstack1lll1l1ll11_opy_,
    bstack1llll11l111_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
class bstack1ll1l1111l1_opy_(bstack1llll11l11l_opy_):
    bstack1l1111l1l1l_opy_ = bstack1l111l1_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠢᓈ")
    bstack1l11l1ll1ll_opy_ = bstack1l111l1_opy_ (u"ࠣࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠣᓉ")
    bstack1l11ll1111l_opy_ = bstack1l111l1_opy_ (u"ࠤ࡫ࡹࡧࡥࡵࡳ࡮ࠥᓊ")
    bstack1l11ll11lll_opy_ = bstack1l111l1_opy_ (u"ࠥࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᓋ")
    bstack1l1111ll11l_opy_ = bstack1l111l1_opy_ (u"ࠦࡼ࠹ࡣࡦࡺࡨࡧࡺࡺࡥࡴࡥࡵ࡭ࡵࡺࠢᓌ")
    bstack1l1111ll1l1_opy_ = bstack1l111l1_opy_ (u"ࠧࡽ࠳ࡤࡧࡻࡩࡨࡻࡴࡦࡵࡦࡶ࡮ࡶࡴࡢࡵࡼࡲࡨࠨᓍ")
    NAME = bstack1l111l1_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥᓎ")
    bstack1l1111l1l11_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1ll1ll111l1_opy_: Any
    bstack1l1111l1lll_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack1l111l1_opy_ (u"ࠢ࡭ࡣࡸࡲࡨ࡮ࠢᓏ"), bstack1l111l1_opy_ (u"ࠣࡥࡲࡲࡳ࡫ࡣࡵࠤᓐ"), bstack1l111l1_opy_ (u"ࠤࡱࡩࡼࡥࡰࡢࡩࡨࠦᓑ"), bstack1l111l1_opy_ (u"ࠥࡧࡱࡵࡳࡦࠤᓒ"), bstack1l111l1_opy_ (u"ࠦࡩ࡯ࡳࡱࡣࡷࡧ࡭ࠨᓓ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack1lll1lllll1_opy_(methods)
    def bstack1llll11lll1_opy_(self, instance: bstack1llll11l1ll_opy_, method_name: str, bstack1llll11ll11_opy_: timedelta, *args, **kwargs):
        pass
    def bstack1llll1l1lll_opy_(
        self,
        target: object,
        exec: Tuple[bstack1llll11l1ll_opy_, str],
        bstack1lll1ll1111_opy_: Tuple[bstack1lll1l1ll11_opy_, bstack1llll11l111_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1lll1llllll_opy_, bstack1l1111l1ll1_opy_ = bstack1lll1ll1111_opy_
        bstack1l1111lll1l_opy_ = bstack1ll1l1111l1_opy_.bstack1l1111ll111_opy_(bstack1lll1ll1111_opy_)
        if bstack1l1111lll1l_opy_ in bstack1ll1l1111l1_opy_.bstack1l1111l1l11_opy_:
            bstack1l1111lll11_opy_ = None
            for callback in bstack1ll1l1111l1_opy_.bstack1l1111l1l11_opy_[bstack1l1111lll1l_opy_]:
                try:
                    bstack1l1111ll1ll_opy_ = callback(self, target, exec, bstack1lll1ll1111_opy_, result, *args, **kwargs)
                    if bstack1l1111lll11_opy_ == None:
                        bstack1l1111lll11_opy_ = bstack1l1111ll1ll_opy_
                except Exception as e:
                    self.logger.error(bstack1l111l1_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠤ࡮ࡴࡶࡰ࡭࡬ࡲ࡬ࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫࠻ࠢࠥᓔ") + str(e) + bstack1l111l1_opy_ (u"ࠨࠢᓕ"))
                    traceback.print_exc()
            if bstack1l1111l1ll1_opy_ == bstack1llll11l111_opy_.PRE and callable(bstack1l1111lll11_opy_):
                return bstack1l1111lll11_opy_
            elif bstack1l1111l1ll1_opy_ == bstack1llll11l111_opy_.POST and bstack1l1111lll11_opy_:
                return bstack1l1111lll11_opy_
    def bstack1lll1lll1ll_opy_(
        self, method_name, previous_state: bstack1lll1l1ll11_opy_, *args, **kwargs
    ) -> bstack1lll1l1ll11_opy_:
        if method_name == bstack1l111l1_opy_ (u"ࠧ࡭ࡣࡸࡲࡨ࡮ࠧᓖ") or method_name == bstack1l111l1_opy_ (u"ࠨࡥࡲࡲࡳ࡫ࡣࡵࠩᓗ") or method_name == bstack1l111l1_opy_ (u"ࠩࡱࡩࡼࡥࡰࡢࡩࡨࠫᓘ"):
            return bstack1lll1l1ll11_opy_.bstack1lll1ll1l1l_opy_
        if method_name == bstack1l111l1_opy_ (u"ࠪࡨ࡮ࡹࡰࡢࡶࡦ࡬ࠬᓙ"):
            return bstack1lll1l1ll11_opy_.bstack1lll1ll1ll1_opy_
        if method_name == bstack1l111l1_opy_ (u"ࠫࡨࡲ࡯ࡴࡧࠪᓚ"):
            return bstack1lll1l1ll11_opy_.QUIT
        return bstack1lll1l1ll11_opy_.NONE
    @staticmethod
    def bstack1l1111ll111_opy_(bstack1lll1ll1111_opy_: Tuple[bstack1lll1l1ll11_opy_, bstack1llll11l111_opy_]):
        return bstack1l111l1_opy_ (u"ࠧࡀࠢᓛ").join((bstack1lll1l1ll11_opy_(bstack1lll1ll1111_opy_[0]).name, bstack1llll11l111_opy_(bstack1lll1ll1111_opy_[1]).name))
    @staticmethod
    def bstack1ll111l11ll_opy_(bstack1lll1ll1111_opy_: Tuple[bstack1lll1l1ll11_opy_, bstack1llll11l111_opy_], callback: Callable):
        bstack1l1111lll1l_opy_ = bstack1ll1l1111l1_opy_.bstack1l1111ll111_opy_(bstack1lll1ll1111_opy_)
        if not bstack1l1111lll1l_opy_ in bstack1ll1l1111l1_opy_.bstack1l1111l1l11_opy_:
            bstack1ll1l1111l1_opy_.bstack1l1111l1l11_opy_[bstack1l1111lll1l_opy_] = []
        bstack1ll1l1111l1_opy_.bstack1l1111l1l11_opy_[bstack1l1111lll1l_opy_].append(callback)
    @staticmethod
    def bstack1ll11111111_opy_(method_name: str):
        return True
    @staticmethod
    def bstack1ll11111ll1_opy_(method_name: str, *args) -> bool:
        return True
    @staticmethod
    def bstack1l1llll1lll_opy_(instance: bstack1llll11l1ll_opy_, default_value=None):
        return bstack1llll11l11l_opy_.bstack1llll1l111l_opy_(instance, bstack1ll1l1111l1_opy_.bstack1l11ll11lll_opy_, default_value)
    @staticmethod
    def bstack1l1ll11l11l_opy_(instance: bstack1llll11l1ll_opy_) -> bool:
        return True
    @staticmethod
    def bstack1ll1111l111_opy_(instance: bstack1llll11l1ll_opy_, default_value=None):
        return bstack1llll11l11l_opy_.bstack1llll1l111l_opy_(instance, bstack1ll1l1111l1_opy_.bstack1l11ll1111l_opy_, default_value)
    @staticmethod
    def bstack1l1lll11ll1_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll111l1ll1_opy_(method_name: str, *args):
        if not bstack1ll1l1111l1_opy_.bstack1ll11111111_opy_(method_name):
            return False
        if not bstack1ll1l1111l1_opy_.bstack1l1111ll11l_opy_ in bstack1ll1l1111l1_opy_.bstack1l111lll1l1_opy_(*args):
            return False
        bstack1l1ll1l1l11_opy_ = bstack1ll1l1111l1_opy_.bstack1l1ll1ll111_opy_(*args)
        return bstack1l1ll1l1l11_opy_ and bstack1l111l1_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨᓜ") in bstack1l1ll1l1l11_opy_ and bstack1l111l1_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣᓝ") in bstack1l1ll1l1l11_opy_[bstack1l111l1_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࠣᓞ")]
    @staticmethod
    def bstack1l1ll1lll1l_opy_(method_name: str, *args):
        if not bstack1ll1l1111l1_opy_.bstack1ll11111111_opy_(method_name):
            return False
        if not bstack1ll1l1111l1_opy_.bstack1l1111ll11l_opy_ in bstack1ll1l1111l1_opy_.bstack1l111lll1l1_opy_(*args):
            return False
        bstack1l1ll1l1l11_opy_ = bstack1ll1l1111l1_opy_.bstack1l1ll1ll111_opy_(*args)
        return (
            bstack1l1ll1l1l11_opy_
            and bstack1l111l1_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤᓟ") in bstack1l1ll1l1l11_opy_
            and bstack1l111l1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡳࡤࡴ࡬ࡴࡹࠨᓠ") in bstack1l1ll1l1l11_opy_[bstack1l111l1_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦᓡ")]
        )
    @staticmethod
    def bstack1l111lll1l1_opy_(*args):
        return str(bstack1ll1l1111l1_opy_.bstack1l1lll11ll1_opy_(*args)).lower()