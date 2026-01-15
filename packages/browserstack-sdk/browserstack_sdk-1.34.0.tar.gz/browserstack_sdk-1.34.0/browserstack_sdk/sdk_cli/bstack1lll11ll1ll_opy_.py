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
from bstack_utils.bstack11lll1l1ll_opy_ import bstack1ll11ll1ll1_opy_
from bstack_utils.constants import EVENTS
class bstack1ll11llll11_opy_(bstack1llll11l11l_opy_):
    bstack1l1111l1l1l_opy_ = bstack1l111l1_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠥᘰ")
    NAME = bstack1l111l1_opy_ (u"ࠦࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠨᘱ")
    bstack1l11ll1111l_opy_ = bstack1l111l1_opy_ (u"ࠧ࡮ࡵࡣࡡࡸࡶࡱࠨᘲ")
    bstack1l11l1ll1ll_opy_ = bstack1l111l1_opy_ (u"ࠨࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠨᘳ")
    bstack11ll1ll1lll_opy_ = bstack1l111l1_opy_ (u"ࠢࡪࡰࡳࡹࡹࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᘴ")
    bstack1l11ll11lll_opy_ = bstack1l111l1_opy_ (u"ࠣࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᘵ")
    bstack1l1111lllll_opy_ = bstack1l111l1_opy_ (u"ࠤ࡬ࡷࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣ࡭ࡻࡢࠣᘶ")
    bstack11ll1lll111_opy_ = bstack1l111l1_opy_ (u"ࠥࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠢᘷ")
    bstack11ll1lll1ll_opy_ = bstack1l111l1_opy_ (u"ࠦࡪࡴࡤࡦࡦࡢࡥࡹࠨᘸ")
    bstack1ll1111ll1l_opy_ = bstack1l111l1_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࠨᘹ")
    bstack1l111l1llll_opy_ = bstack1l111l1_opy_ (u"ࠨ࡮ࡦࡹࡶࡩࡸࡹࡩࡰࡰࠥᘺ")
    bstack11ll1ll1l1l_opy_ = bstack1l111l1_opy_ (u"ࠢࡨࡧࡷࠦᘻ")
    bstack1l1l1111l11_opy_ = bstack1l111l1_opy_ (u"ࠣࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧᘼ")
    bstack1l1111ll11l_opy_ = bstack1l111l1_opy_ (u"ࠤࡺ࠷ࡨ࡫ࡸࡦࡥࡸࡸࡪࡹࡣࡳ࡫ࡳࡸࠧᘽ")
    bstack1l1111ll1l1_opy_ = bstack1l111l1_opy_ (u"ࠥࡻ࠸ࡩࡥࡹࡧࡦࡹࡹ࡫ࡳࡤࡴ࡬ࡴࡹࡧࡳࡺࡰࡦࠦᘾ")
    bstack11ll1lll1l1_opy_ = bstack1l111l1_opy_ (u"ࠦࡶࡻࡩࡵࠤᘿ")
    bstack11ll1ll1ll1_opy_: Dict[str, List[Callable]] = dict()
    bstack1l111ll1111_opy_: str
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1ll1ll111l1_opy_: Any
    bstack1l1111l1lll_opy_: Dict
    def __init__(
        self,
        bstack1l111ll1111_opy_: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        bstack1ll1ll111l1_opy_: Dict[str, Any],
        methods=[bstack1l111l1_opy_ (u"ࠧࡥ࡟ࡪࡰ࡬ࡸࡤࡥࠢᙀ"), bstack1l111l1_opy_ (u"ࠨࡳࡵࡣࡵࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࠨᙁ"), bstack1l111l1_opy_ (u"ࠢࡦࡺࡨࡧࡺࡺࡥࠣᙂ"), bstack1l111l1_opy_ (u"ࠣࡳࡸ࡭ࡹࠨᙃ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.bstack1l111ll1111_opy_ = bstack1l111ll1111_opy_
        self.platform_index = platform_index
        self.bstack1lll1lllll1_opy_(methods)
        self.bstack1ll1ll111l1_opy_ = bstack1ll1ll111l1_opy_
    @staticmethod
    def session_id(target: object, strict=True):
        return bstack1llll11l11l_opy_.get_data(bstack1ll11llll11_opy_.bstack1l11l1ll1ll_opy_, target, strict)
    @staticmethod
    def hub_url(target: object, strict=True):
        return bstack1llll11l11l_opy_.get_data(bstack1ll11llll11_opy_.bstack1l11ll1111l_opy_, target, strict)
    @staticmethod
    def bstack11ll1lll11l_opy_(target: object, strict=True):
        return bstack1llll11l11l_opy_.get_data(bstack1ll11llll11_opy_.bstack11ll1ll1lll_opy_, target, strict)
    @staticmethod
    def capabilities(target: object, strict=True):
        return bstack1llll11l11l_opy_.get_data(bstack1ll11llll11_opy_.bstack1l11ll11lll_opy_, target, strict)
    @staticmethod
    def bstack1l1ll11l11l_opy_(instance: bstack1llll11l1ll_opy_) -> bool:
        return bstack1llll11l11l_opy_.bstack1llll1l111l_opy_(instance, bstack1ll11llll11_opy_.bstack1l1111lllll_opy_, False)
    @staticmethod
    def bstack1ll1111l111_opy_(instance: bstack1llll11l1ll_opy_, default_value=None):
        return bstack1llll11l11l_opy_.bstack1llll1l111l_opy_(instance, bstack1ll11llll11_opy_.bstack1l11ll1111l_opy_, default_value)
    @staticmethod
    def bstack1l1llll1lll_opy_(instance: bstack1llll11l1ll_opy_, default_value=None):
        return bstack1llll11l11l_opy_.bstack1llll1l111l_opy_(instance, bstack1ll11llll11_opy_.bstack1l11ll11lll_opy_, default_value)
    @staticmethod
    def bstack1l1ll1l11ll_opy_(hub_url: str, bstack11ll1ll1l11_opy_=bstack1l111l1_opy_ (u"ࠤ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲࠨᙄ")):
        try:
            bstack11ll1ll11ll_opy_ = str(urlparse(hub_url).netloc) if hub_url else None
            return bstack11ll1ll11ll_opy_.endswith(bstack11ll1ll1l11_opy_)
        except:
            pass
        return False
    @staticmethod
    def bstack1ll11111111_opy_(method_name: str):
        return method_name == bstack1l111l1_opy_ (u"ࠥࡩࡽ࡫ࡣࡶࡶࡨࠦᙅ")
    @staticmethod
    def bstack1ll11111ll1_opy_(method_name: str, *args):
        return (
            bstack1ll11llll11_opy_.bstack1ll11111111_opy_(method_name)
            and bstack1ll11llll11_opy_.bstack1l111lll1l1_opy_(*args) == bstack1ll11llll11_opy_.bstack1l111l1llll_opy_
        )
    @staticmethod
    def bstack1ll111l1ll1_opy_(method_name: str, *args):
        if not bstack1ll11llll11_opy_.bstack1ll11111111_opy_(method_name):
            return False
        if not bstack1ll11llll11_opy_.bstack1l1111ll11l_opy_ in bstack1ll11llll11_opy_.bstack1l111lll1l1_opy_(*args):
            return False
        bstack1l1ll1l1l11_opy_ = bstack1ll11llll11_opy_.bstack1l1ll1ll111_opy_(*args)
        return bstack1l1ll1l1l11_opy_ and bstack1l111l1_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦᙆ") in bstack1l1ll1l1l11_opy_ and bstack1l111l1_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᙇ") in bstack1l1ll1l1l11_opy_[bstack1l111l1_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨᙈ")]
    @staticmethod
    def bstack1l1ll1lll1l_opy_(method_name: str, *args):
        if not bstack1ll11llll11_opy_.bstack1ll11111111_opy_(method_name):
            return False
        if not bstack1ll11llll11_opy_.bstack1l1111ll11l_opy_ in bstack1ll11llll11_opy_.bstack1l111lll1l1_opy_(*args):
            return False
        bstack1l1ll1l1l11_opy_ = bstack1ll11llll11_opy_.bstack1l1ll1ll111_opy_(*args)
        return (
            bstack1l1ll1l1l11_opy_
            and bstack1l111l1_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢᙉ") in bstack1l1ll1l1l11_opy_
            and bstack1l111l1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡸࡩࡲࡪࡲࡷࠦᙊ") in bstack1l1ll1l1l11_opy_[bstack1l111l1_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤᙋ")]
        )
    @staticmethod
    def bstack1l111lll1l1_opy_(*args):
        return str(bstack1ll11llll11_opy_.bstack1l1lll11ll1_opy_(*args)).lower()
    @staticmethod
    def bstack1l1lll11ll1_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1l1ll1ll111_opy_(*args):
        return args[1] if len(args) > 1 and isinstance(args[1], dict) else None
    @staticmethod
    def bstack1lllllll11_opy_(driver):
        command_executor = getattr(driver, bstack1l111l1_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᙌ"), None)
        if not command_executor:
            return None
        hub_url = str(command_executor) if isinstance(command_executor, (str, bytes)) else None
        hub_url = str(command_executor._url) if not hub_url and getattr(command_executor, bstack1l111l1_opy_ (u"ࠦࡤࡻࡲ࡭ࠤᙍ"), None) else None
        if not hub_url:
            client_config = getattr(command_executor, bstack1l111l1_opy_ (u"ࠧࡥࡣ࡭࡫ࡨࡲࡹࡥࡣࡰࡰࡩ࡭࡬ࠨᙎ"), None)
            if not client_config:
                return None
            hub_url = getattr(client_config, bstack1l111l1_opy_ (u"ࠨࡲࡦ࡯ࡲࡸࡪࡥࡳࡦࡴࡹࡩࡷࡥࡡࡥࡦࡵࠦᙏ"), None)
        return hub_url
    def bstack1l11l111111_opy_(self, instance, driver, hub_url: str):
        result = False
        if not hub_url:
            return result
        command_executor = getattr(driver, bstack1l111l1_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᙐ"), None)
        if command_executor:
            if isinstance(command_executor, (str, bytes)):
                setattr(driver, bstack1l111l1_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦᙑ"), hub_url)
                result = True
            elif hasattr(command_executor, bstack1l111l1_opy_ (u"ࠤࡢࡹࡷࡲࠢᙒ")):
                setattr(command_executor, bstack1l111l1_opy_ (u"ࠥࡣࡺࡸ࡬ࠣᙓ"), hub_url)
                result = True
        if result:
            self.bstack1l111ll1111_opy_ = hub_url
            bstack1ll11llll11_opy_.bstack1llll1111l1_opy_(instance, bstack1ll11llll11_opy_.bstack1l11ll1111l_opy_, hub_url)
            bstack1ll11llll11_opy_.bstack1llll1111l1_opy_(
                instance, bstack1ll11llll11_opy_.bstack1l1111lllll_opy_, bstack1ll11llll11_opy_.bstack1l1ll1l11ll_opy_(hub_url)
            )
        return result
    @staticmethod
    def bstack1l1111ll111_opy_(bstack1lll1ll1111_opy_: Tuple[bstack1lll1l1ll11_opy_, bstack1llll11l111_opy_]):
        return bstack1l111l1_opy_ (u"ࠦ࠿ࠨᙔ").join((bstack1lll1l1ll11_opy_(bstack1lll1ll1111_opy_[0]).name, bstack1llll11l111_opy_(bstack1lll1ll1111_opy_[1]).name))
    @staticmethod
    def bstack1ll111l11ll_opy_(bstack1lll1ll1111_opy_: Tuple[bstack1lll1l1ll11_opy_, bstack1llll11l111_opy_], callback: Callable):
        bstack1l1111lll1l_opy_ = bstack1ll11llll11_opy_.bstack1l1111ll111_opy_(bstack1lll1ll1111_opy_)
        if not bstack1l1111lll1l_opy_ in bstack1ll11llll11_opy_.bstack11ll1ll1ll1_opy_:
            bstack1ll11llll11_opy_.bstack11ll1ll1ll1_opy_[bstack1l1111lll1l_opy_] = []
        bstack1ll11llll11_opy_.bstack11ll1ll1ll1_opy_[bstack1l1111lll1l_opy_].append(callback)
    def bstack1llll11lll1_opy_(self, instance: bstack1llll11l1ll_opy_, method_name: str, bstack1llll11ll11_opy_: timedelta, *args, **kwargs):
        if not instance or method_name in (bstack1l111l1_opy_ (u"ࠧࡹࡴࡢࡴࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠧᙕ")):
            return
        cmd = args[0] if method_name == bstack1l111l1_opy_ (u"ࠨࡥࡹࡧࡦࡹࡹ࡫ࠢᙖ") and args and type(args) in [list, tuple] and isinstance(args[0], str) else None
        bstack11ll1ll11l1_opy_ = bstack1l111l1_opy_ (u"ࠢ࠻ࠤᙗ").join(map(str, filter(None, [method_name, cmd])))
        instance.bstack111lll11l_opy_(bstack1l111l1_opy_ (u"ࠣࡦࡵ࡭ࡻ࡫ࡲ࠻ࠤᙘ") + bstack11ll1ll11l1_opy_, bstack1llll11ll11_opy_)
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
        bstack1l1111lll1l_opy_ = bstack1ll11llll11_opy_.bstack1l1111ll111_opy_(bstack1lll1ll1111_opy_)
        self.logger.debug(bstack1l111l1_opy_ (u"ࠤࡲࡲࡤ࡮࡯ࡰ࡭࠽ࠤࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦ࠿ࡾࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥࡾࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᙙ") + str(kwargs) + bstack1l111l1_opy_ (u"ࠥࠦᙚ"))
        if bstack1lll1llllll_opy_ == bstack1lll1l1ll11_opy_.QUIT:
            if bstack1l1111l1ll1_opy_ == bstack1llll11l111_opy_.PRE:
                bstack1ll111ll11l_opy_ = bstack1ll11ll1ll1_opy_.bstack1ll1111l1l1_opy_(EVENTS.bstack1ll1l1l11l_opy_.value)
                bstack1llll11l11l_opy_.bstack1llll1111l1_opy_(instance, EVENTS.bstack1ll1l1l11l_opy_.value, bstack1ll111ll11l_opy_)
                self.logger.debug(bstack1l111l1_opy_ (u"ࠦ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡾࠢࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫࠽ࡼࡿࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࡂࢁࡽࠡࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࡂࢁࡽࠣᙛ").format(instance, method_name, bstack1lll1llllll_opy_, bstack1l1111l1ll1_opy_))
        if bstack1lll1llllll_opy_ == bstack1lll1l1ll11_opy_.bstack1lll1ll1l1l_opy_:
            if bstack1l1111l1ll1_opy_ == bstack1llll11l111_opy_.POST and not bstack1ll11llll11_opy_.bstack1l11l1ll1ll_opy_ in instance.data:
                session_id = getattr(target, bstack1l111l1_opy_ (u"ࠧࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠤᙜ"), None)
                if session_id:
                    instance.data[bstack1ll11llll11_opy_.bstack1l11l1ll1ll_opy_] = session_id
        elif (
            bstack1lll1llllll_opy_ == bstack1lll1l1ll11_opy_.bstack1llll111l1l_opy_
            and bstack1ll11llll11_opy_.bstack1l111lll1l1_opy_(*args) == bstack1ll11llll11_opy_.bstack1l111l1llll_opy_
        ):
            if bstack1l1111l1ll1_opy_ == bstack1llll11l111_opy_.PRE:
                hub_url = bstack1ll11llll11_opy_.bstack1lllllll11_opy_(target)
                if hub_url:
                    instance.data.update(
                        {
                            bstack1ll11llll11_opy_.bstack1l11ll1111l_opy_: hub_url,
                            bstack1ll11llll11_opy_.bstack1l1111lllll_opy_: bstack1ll11llll11_opy_.bstack1l1ll1l11ll_opy_(hub_url),
                            bstack1ll11llll11_opy_.bstack1ll1111ll1l_opy_: int(
                                os.environ.get(bstack1l111l1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝ࠨᙝ"), str(self.platform_index))
                            ),
                        }
                    )
                bstack1l1ll1l1l11_opy_ = bstack1ll11llll11_opy_.bstack1l1ll1ll111_opy_(*args)
                bstack11ll1lll11l_opy_ = bstack1l1ll1l1l11_opy_.get(bstack1l111l1_opy_ (u"ࠢࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᙞ"), None) if bstack1l1ll1l1l11_opy_ else None
                if isinstance(bstack11ll1lll11l_opy_, dict):
                    instance.data[bstack1ll11llll11_opy_.bstack11ll1ll1lll_opy_] = copy.deepcopy(bstack11ll1lll11l_opy_)
                    instance.data[bstack1ll11llll11_opy_.bstack1l11ll11lll_opy_] = bstack11ll1lll11l_opy_
            elif bstack1l1111l1ll1_opy_ == bstack1llll11l111_opy_.POST:
                if isinstance(result, dict):
                    framework_session_id = result.get(bstack1l111l1_opy_ (u"ࠣࡸࡤࡰࡺ࡫ࠢᙟ"), dict()).get(bstack1l111l1_opy_ (u"ࠤࡶࡩࡸࡹࡩࡰࡰࡌࡨࠧᙠ"), None)
                    if framework_session_id:
                        instance.data.update(
                            {
                                bstack1ll11llll11_opy_.bstack1l11l1ll1ll_opy_: framework_session_id,
                                bstack1ll11llll11_opy_.bstack11ll1lll111_opy_: datetime.now(tz=timezone.utc),
                            }
                        )
        elif (
            bstack1lll1llllll_opy_ == bstack1lll1l1ll11_opy_.bstack1llll111l1l_opy_
            and bstack1ll11llll11_opy_.bstack1l111lll1l1_opy_(*args) == bstack1ll11llll11_opy_.bstack11ll1lll1l1_opy_
            and bstack1l1111l1ll1_opy_ == bstack1llll11l111_opy_.POST
        ):
            instance.data[bstack1ll11llll11_opy_.bstack11ll1lll1ll_opy_] = datetime.now(tz=timezone.utc)
        if bstack1l1111lll1l_opy_ in bstack1ll11llll11_opy_.bstack11ll1ll1ll1_opy_:
            bstack1l1111lll11_opy_ = None
            for callback in bstack1ll11llll11_opy_.bstack11ll1ll1ll1_opy_[bstack1l1111lll1l_opy_]:
                try:
                    bstack1l1111ll1ll_opy_ = callback(self, target, exec, bstack1lll1ll1111_opy_, result, *args, **kwargs)
                    if bstack1l1111lll11_opy_ == None:
                        bstack1l1111lll11_opy_ = bstack1l1111ll1ll_opy_
                except Exception as e:
                    self.logger.error(bstack1l111l1_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠢ࡬ࡲࡻࡵ࡫ࡪࡰࡪࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࡀࠠࠣᙡ") + str(e) + bstack1l111l1_opy_ (u"ࠦࠧᙢ"))
                    traceback.print_exc()
            if bstack1lll1llllll_opy_ == bstack1lll1l1ll11_opy_.QUIT:
                if bstack1l1111l1ll1_opy_ == bstack1llll11l111_opy_.POST:
                    bstack1ll111ll11l_opy_ = bstack1llll11l11l_opy_.bstack1llll1l111l_opy_(instance, EVENTS.bstack1ll1l1l11l_opy_.value)
                    if bstack1ll111ll11l_opy_!=None:
                        bstack1ll11ll1ll1_opy_.end(EVENTS.bstack1ll1l1l11l_opy_.value, bstack1ll111ll11l_opy_+bstack1l111l1_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᙣ"), bstack1ll111ll11l_opy_+bstack1l111l1_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᙤ"), True, None)
            if bstack1l1111l1ll1_opy_ == bstack1llll11l111_opy_.PRE and callable(bstack1l1111lll11_opy_):
                return bstack1l1111lll11_opy_
            elif bstack1l1111l1ll1_opy_ == bstack1llll11l111_opy_.POST and bstack1l1111lll11_opy_:
                return bstack1l1111lll11_opy_
    def bstack1lll1lll1ll_opy_(
        self, method_name, previous_state: bstack1lll1l1ll11_opy_, *args, **kwargs
    ) -> bstack1lll1l1ll11_opy_:
        if method_name == bstack1l111l1_opy_ (u"ࠢࡠࡡ࡬ࡲ࡮ࡺ࡟ࡠࠤᙥ") or method_name == bstack1l111l1_opy_ (u"ࠣࡵࡷࡥࡷࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠣᙦ"):
            return bstack1lll1l1ll11_opy_.bstack1lll1ll1l1l_opy_
        if method_name == bstack1l111l1_opy_ (u"ࠤࡴࡹ࡮ࡺࠢᙧ"):
            return bstack1lll1l1ll11_opy_.QUIT
        if method_name == bstack1l111l1_opy_ (u"ࠥࡩࡽ࡫ࡣࡶࡶࡨࠦᙨ"):
            if previous_state != bstack1lll1l1ll11_opy_.NONE:
                command_name = bstack1ll11llll11_opy_.bstack1l111lll1l1_opy_(*args)
                if command_name == bstack1ll11llll11_opy_.bstack1l111l1llll_opy_:
                    return bstack1lll1l1ll11_opy_.bstack1lll1ll1l1l_opy_
            return bstack1lll1l1ll11_opy_.bstack1llll111l1l_opy_
        return bstack1lll1l1ll11_opy_.NONE