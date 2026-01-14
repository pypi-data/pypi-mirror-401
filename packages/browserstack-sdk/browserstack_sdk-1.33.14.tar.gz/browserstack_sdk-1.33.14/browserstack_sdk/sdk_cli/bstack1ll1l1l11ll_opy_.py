# coding: UTF-8
import sys
bstack111l11l_opy_ = sys.version_info [0] == 2
bstack11l1_opy_ = 2048
bstack1ll1l1_opy_ = 7
def bstack1l11l1l_opy_ (bstack1111lll_opy_):
    global bstack11l1l_opy_
    bstack1l11111_opy_ = ord (bstack1111lll_opy_ [-1])
    bstack1ll111_opy_ = bstack1111lll_opy_ [:-1]
    bstack1lllll1l_opy_ = bstack1l11111_opy_ % len (bstack1ll111_opy_)
    bstack1_opy_ = bstack1ll111_opy_ [:bstack1lllll1l_opy_] + bstack1ll111_opy_ [bstack1lllll1l_opy_:]
    if bstack111l11l_opy_:
        bstack11llll_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1_opy_ - (bstack111ll1_opy_ + bstack1l11111_opy_) % bstack1ll1l1_opy_) for bstack111ll1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11llll_opy_ = str () .join ([chr (ord (char) - bstack11l1_opy_ - (bstack111ll1_opy_ + bstack1l11111_opy_) % bstack1ll1l1_opy_) for bstack111ll1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11llll_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1llll11llll_opy_ import (
    bstack1llll11l1l1_opy_,
    bstack1lll1ll1ll1_opy_,
    bstack1llll111lll_opy_,
    bstack1llll111l11_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
class bstack1ll1ll1111l_opy_(bstack1llll11l1l1_opy_):
    bstack1l1111lllll_opy_ = bstack1l11l1l_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠤᒧ")
    bstack1l11ll1l111_opy_ = bstack1l11l1l_opy_ (u"ࠥࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠥᒨ")
    bstack1l11ll11l1l_opy_ = bstack1l11l1l_opy_ (u"ࠦ࡭ࡻࡢࡠࡷࡵࡰࠧᒩ")
    bstack1l11lll111l_opy_ = bstack1l11l1l_opy_ (u"ࠧࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᒪ")
    bstack1l111l11l11_opy_ = bstack1l11l1l_opy_ (u"ࠨࡷ࠴ࡥࡨࡼࡪࡩࡵࡵࡧࡶࡧࡷ࡯ࡰࡵࠤᒫ")
    bstack1l111l11111_opy_ = bstack1l11l1l_opy_ (u"ࠢࡸ࠵ࡦࡩࡽ࡫ࡣࡶࡶࡨࡷࡨࡸࡩࡱࡶࡤࡷࡾࡴࡣࠣᒬ")
    NAME = bstack1l11l1l_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧᒭ")
    bstack1l111l11l1l_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1ll1ll1ll1l_opy_: Any
    bstack1l1111llll1_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack1l11l1l_opy_ (u"ࠤ࡯ࡥࡺࡴࡣࡩࠤᒮ"), bstack1l11l1l_opy_ (u"ࠥࡧࡴࡴ࡮ࡦࡥࡷࠦᒯ"), bstack1l11l1l_opy_ (u"ࠦࡳ࡫ࡷࡠࡲࡤ࡫ࡪࠨᒰ"), bstack1l11l1l_opy_ (u"ࠧࡩ࡬ࡰࡵࡨࠦᒱ"), bstack1l11l1l_opy_ (u"ࠨࡤࡪࡵࡳࡥࡹࡩࡨࠣᒲ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack1lll1llll1l_opy_(methods)
    def bstack1llll11l11l_opy_(self, instance: bstack1lll1ll1ll1_opy_, method_name: str, bstack1lll1ll1l1l_opy_: timedelta, *args, **kwargs):
        pass
    def bstack1llll1ll1ll_opy_(
        self,
        target: object,
        exec: Tuple[bstack1lll1ll1ll1_opy_, str],
        bstack1llll1lllll_opy_: Tuple[bstack1llll111lll_opy_, bstack1llll111l11_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1llll1l1lll_opy_, bstack1l111l111l1_opy_ = bstack1llll1lllll_opy_
        bstack1l111l111ll_opy_ = bstack1ll1ll1111l_opy_.bstack1l111l11lll_opy_(bstack1llll1lllll_opy_)
        if bstack1l111l111ll_opy_ in bstack1ll1ll1111l_opy_.bstack1l111l11l1l_opy_:
            bstack1l111l11ll1_opy_ = None
            for callback in bstack1ll1ll1111l_opy_.bstack1l111l11l1l_opy_[bstack1l111l111ll_opy_]:
                try:
                    bstack1l111l1111l_opy_ = callback(self, target, exec, bstack1llll1lllll_opy_, result, *args, **kwargs)
                    if bstack1l111l11ll1_opy_ == None:
                        bstack1l111l11ll1_opy_ = bstack1l111l1111l_opy_
                except Exception as e:
                    self.logger.error(bstack1l11l1l_opy_ (u"ࠢࡦࡴࡵࡳࡷࠦࡩ࡯ࡸࡲ࡯࡮ࡴࡧࠡࡥࡤࡰࡱࡨࡡࡤ࡭࠽ࠤࠧᒳ") + str(e) + bstack1l11l1l_opy_ (u"ࠣࠤᒴ"))
                    traceback.print_exc()
            if bstack1l111l111l1_opy_ == bstack1llll111l11_opy_.PRE and callable(bstack1l111l11ll1_opy_):
                return bstack1l111l11ll1_opy_
            elif bstack1l111l111l1_opy_ == bstack1llll111l11_opy_.POST and bstack1l111l11ll1_opy_:
                return bstack1l111l11ll1_opy_
    def bstack1llll1ll111_opy_(
        self, method_name, previous_state: bstack1llll111lll_opy_, *args, **kwargs
    ) -> bstack1llll111lll_opy_:
        if method_name == bstack1l11l1l_opy_ (u"ࠩ࡯ࡥࡺࡴࡣࡩࠩᒵ") or method_name == bstack1l11l1l_opy_ (u"ࠪࡧࡴࡴ࡮ࡦࡥࡷࠫᒶ") or method_name == bstack1l11l1l_opy_ (u"ࠫࡳ࡫ࡷࡠࡲࡤ࡫ࡪ࠭ᒷ"):
            return bstack1llll111lll_opy_.bstack1lll1lll111_opy_
        if method_name == bstack1l11l1l_opy_ (u"ࠬࡪࡩࡴࡲࡤࡸࡨ࡮ࠧᒸ"):
            return bstack1llll111lll_opy_.bstack1lll1lll11l_opy_
        if method_name == bstack1l11l1l_opy_ (u"࠭ࡣ࡭ࡱࡶࡩࠬᒹ"):
            return bstack1llll111lll_opy_.QUIT
        return bstack1llll111lll_opy_.NONE
    @staticmethod
    def bstack1l111l11lll_opy_(bstack1llll1lllll_opy_: Tuple[bstack1llll111lll_opy_, bstack1llll111l11_opy_]):
        return bstack1l11l1l_opy_ (u"ࠢ࠻ࠤᒺ").join((bstack1llll111lll_opy_(bstack1llll1lllll_opy_[0]).name, bstack1llll111l11_opy_(bstack1llll1lllll_opy_[1]).name))
    @staticmethod
    def bstack1l1llll1111_opy_(bstack1llll1lllll_opy_: Tuple[bstack1llll111lll_opy_, bstack1llll111l11_opy_], callback: Callable):
        bstack1l111l111ll_opy_ = bstack1ll1ll1111l_opy_.bstack1l111l11lll_opy_(bstack1llll1lllll_opy_)
        if not bstack1l111l111ll_opy_ in bstack1ll1ll1111l_opy_.bstack1l111l11l1l_opy_:
            bstack1ll1ll1111l_opy_.bstack1l111l11l1l_opy_[bstack1l111l111ll_opy_] = []
        bstack1ll1ll1111l_opy_.bstack1l111l11l1l_opy_[bstack1l111l111ll_opy_].append(callback)
    @staticmethod
    def bstack1ll11l11111_opy_(method_name: str):
        return True
    @staticmethod
    def bstack1ll111l111l_opy_(method_name: str, *args) -> bool:
        return True
    @staticmethod
    def bstack1ll111llll1_opy_(instance: bstack1lll1ll1ll1_opy_, default_value=None):
        return bstack1llll11l1l1_opy_.bstack1lll1llll11_opy_(instance, bstack1ll1ll1111l_opy_.bstack1l11lll111l_opy_, default_value)
    @staticmethod
    def bstack1l1ll11ll11_opy_(instance: bstack1lll1ll1ll1_opy_) -> bool:
        return True
    @staticmethod
    def bstack1l1llll11l1_opy_(instance: bstack1lll1ll1ll1_opy_, default_value=None):
        return bstack1llll11l1l1_opy_.bstack1lll1llll11_opy_(instance, bstack1ll1ll1111l_opy_.bstack1l11ll11l1l_opy_, default_value)
    @staticmethod
    def bstack1l1llll1ll1_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll11l1l1l1_opy_(method_name: str, *args):
        if not bstack1ll1ll1111l_opy_.bstack1ll11l11111_opy_(method_name):
            return False
        if not bstack1ll1ll1111l_opy_.bstack1l111l11l11_opy_ in bstack1ll1ll1111l_opy_.bstack1l111llll11_opy_(*args):
            return False
        bstack1l1ll1ll1l1_opy_ = bstack1ll1ll1111l_opy_.bstack1l1lll1111l_opy_(*args)
        return bstack1l1ll1ll1l1_opy_ and bstack1l11l1l_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࠣᒻ") in bstack1l1ll1ll1l1_opy_ and bstack1l11l1l_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᒼ") in bstack1l1ll1ll1l1_opy_[bstack1l11l1l_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࠥᒽ")]
    @staticmethod
    def bstack1ll1111l1ll_opy_(method_name: str, *args):
        if not bstack1ll1ll1111l_opy_.bstack1ll11l11111_opy_(method_name):
            return False
        if not bstack1ll1ll1111l_opy_.bstack1l111l11l11_opy_ in bstack1ll1ll1111l_opy_.bstack1l111llll11_opy_(*args):
            return False
        bstack1l1ll1ll1l1_opy_ = bstack1ll1ll1111l_opy_.bstack1l1lll1111l_opy_(*args)
        return (
            bstack1l1ll1ll1l1_opy_
            and bstack1l11l1l_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦᒾ") in bstack1l1ll1ll1l1_opy_
            and bstack1l11l1l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡵࡦࡶ࡮ࡶࡴࠣᒿ") in bstack1l1ll1ll1l1_opy_[bstack1l11l1l_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨᓀ")]
        )
    @staticmethod
    def bstack1l111llll11_opy_(*args):
        return str(bstack1ll1ll1111l_opy_.bstack1l1llll1ll1_opy_(*args)).lower()