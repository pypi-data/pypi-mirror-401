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
from typing import Dict, List, Any, Callable, Tuple, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1lll11ll1ll_opy_ import bstack1lll1l1lll1_opy_
from browserstack_sdk.sdk_cli.bstack1llll11llll_opy_ import (
    bstack1llll111lll_opy_,
    bstack1llll111l11_opy_,
    bstack1lll1ll1ll1_opy_,
)
from bstack_utils.helper import  bstack1ll1ll11ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll11ll11ll_opy_ import bstack1ll1l1111l1_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll11ll1lll_opy_, bstack1lll1l1111l_opy_, bstack1ll1l1l1ll1_opy_, bstack1ll1lll1ll1_opy_
from typing import Tuple, Any
import threading
from bstack_utils.bstack11ll111lll_opy_ import bstack11l1llll11_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l11l11l_opy_ import bstack1ll1l111ll1_opy_
from bstack_utils.percy import bstack1l1l11lll_opy_
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.constants import *
import re
class bstack1ll1l1lll11_opy_(bstack1lll1l1lll1_opy_):
    def __init__(self, bstack1l11lllll1l_opy_: Dict[str, str]):
        super().__init__()
        self.bstack1l11lllll1l_opy_ = bstack1l11lllll1l_opy_
        self.percy = bstack1l1l11lll_opy_()
        self.bstack1lllllll11_opy_ = bstack11l1llll11_opy_()
        self.bstack1l11lll1ll1_opy_()
        bstack1ll1l1111l1_opy_.bstack1l1llll1111_opy_((bstack1llll111lll_opy_.bstack1lll1llllll_opy_, bstack1llll111l11_opy_.PRE), self.bstack1l11lllllll_opy_)
        TestFramework.bstack1l1llll1111_opy_((bstack1ll11ll1lll_opy_.TEST, bstack1ll1l1l1ll1_opy_.POST), self.bstack1l1lll11l1l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l1lllll1_opy_(self, instance: bstack1lll1ll1ll1_opy_, driver: object):
        bstack1l1l1ll1lll_opy_ = TestFramework.bstack1llll11l1ll_opy_(instance.context)
        for t in bstack1l1l1ll1lll_opy_:
            bstack1l1l1l1ll1l_opy_ = TestFramework.bstack1lll1llll11_opy_(t, bstack1ll1l111ll1_opy_.bstack1l1l1l1l1ll_opy_, [])
            if any(instance is d[1] for d in bstack1l1l1l1ll1l_opy_) or instance == driver:
                return t
    def bstack1l11lllllll_opy_(
        self,
        f: bstack1ll1l1111l1_opy_,
        driver: object,
        exec: Tuple[bstack1lll1ll1ll1_opy_, str],
        bstack1llll1lllll_opy_: Tuple[bstack1llll111lll_opy_, bstack1llll111l11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if not bstack1ll1l1111l1_opy_.bstack1ll11l11111_opy_(method_name):
                return
            platform_index = f.bstack1lll1llll11_opy_(instance, bstack1ll1l1111l1_opy_.bstack1l1llllll1l_opy_, 0)
            bstack1l1l1lll1l1_opy_ = self.bstack1l1l1lllll1_opy_(instance, driver)
            bstack1l11llll111_opy_ = TestFramework.bstack1lll1llll11_opy_(bstack1l1l1lll1l1_opy_, TestFramework.bstack1l11lll1lll_opy_, None)
            if not bstack1l11llll111_opy_:
                self.logger.debug(bstack1l11l1l_opy_ (u"ࠦࡴࡴ࡟ࡱࡴࡨࡣࡪࡾࡥࡤࡷࡷࡩ࠿ࠦࡲࡦࡶࡸࡶࡳ࡯࡮ࡨࠢࡤࡷࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡩࡴࠢࡱࡳࡹࠦࡹࡦࡶࠣࡷࡹࡧࡲࡵࡧࡧࠦ፮"))
                return
            driver_command = f.bstack1l1llll1ll1_opy_(*args)
            for command in bstack1l1ll111ll_opy_:
                if command == driver_command:
                    self.bstack1ll11111l1_opy_(driver, platform_index)
            bstack1111l111l_opy_ = self.percy.bstack1ll111l1l_opy_()
            if driver_command in bstack11l1l1ll_opy_[bstack1111l111l_opy_]:
                self.bstack1lllllll11_opy_.bstack1l1lllll_opy_(bstack1l11llll111_opy_, driver_command)
        except Exception as e:
            self.logger.error(bstack1l11l1l_opy_ (u"ࠧࡵ࡮ࡠࡲࡵࡩࡤ࡫ࡸࡦࡥࡸࡸࡪࡀࠠࡦࡴࡵࡳࡷࠨ፯"), e)
    def bstack1l1lll11l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1111l_opy_,
        bstack1llll1lllll_opy_: Tuple[bstack1ll11ll1lll_opy_, bstack1ll1l1l1ll1_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1lll1l111_opy_ import bstack1ll1llll11l_opy_
        bstack1l1l1l1ll1l_opy_ = f.bstack1lll1llll11_opy_(instance, bstack1ll1l111ll1_opy_.bstack1l1l1l1l1ll_opy_, [])
        if not bstack1l1l1l1ll1l_opy_:
            self.logger.debug(bstack1l11l1l_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣ፰") + str(kwargs) + bstack1l11l1l_opy_ (u"ࠢࠣ፱"))
            return
        if len(bstack1l1l1l1ll1l_opy_) > 1:
            self.logger.debug(bstack1l11l1l_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡾࡰࡪࡴࠨࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡵࠬࢁࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥ፲") + str(kwargs) + bstack1l11l1l_opy_ (u"ࠤࠥ፳"))
        bstack1l11llll1ll_opy_, bstack1l1l11111l1_opy_ = bstack1l1l1l1ll1l_opy_[0]
        driver = bstack1l11llll1ll_opy_()
        if not driver:
            self.logger.debug(bstack1l11l1l_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦ፴") + str(kwargs) + bstack1l11l1l_opy_ (u"ࠦࠧ፵"))
            return
        bstack1l1l111111l_opy_ = {
            TestFramework.bstack1l1lllll1ll_opy_: bstack1l11l1l_opy_ (u"ࠧࡺࡥࡴࡶࠣࡲࡦࡳࡥࠣ፶"),
            TestFramework.bstack1ll111111l1_opy_: bstack1l11l1l_opy_ (u"ࠨࡴࡦࡵࡷࠤࡺࡻࡩࡥࠤ፷"),
            TestFramework.bstack1l11lll1lll_opy_: bstack1l11l1l_opy_ (u"ࠢࡵࡧࡶࡸࠥࡸࡥࡳࡷࡱࠤࡳࡧ࡭ࡦࠤ፸")
        }
        bstack1l1l1111111_opy_ = { key: f.bstack1lll1llll11_opy_(instance, key) for key in bstack1l1l111111l_opy_ }
        bstack1l11llllll1_opy_ = [key for key, value in bstack1l1l1111111_opy_.items() if not value]
        if bstack1l11llllll1_opy_:
            for key in bstack1l11llllll1_opy_:
                self.logger.debug(bstack1l11l1l_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࠦ፹") + str(key) + bstack1l11l1l_opy_ (u"ࠤࠥ፺"))
            return
        platform_index = f.bstack1lll1llll11_opy_(instance, bstack1ll1l1111l1_opy_.bstack1l1llllll1l_opy_, 0)
        if self.bstack1l11lllll1l_opy_.percy_capture_mode == bstack1l11l1l_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧ፻"):
            bstack1ll1111ll1_opy_ = bstack1l1l1111111_opy_.get(TestFramework.bstack1l11lll1lll_opy_) + bstack1l11l1l_opy_ (u"ࠦ࠲ࡺࡥࡴࡶࡦࡥࡸ࡫ࠢ፼")
            bstack1l1lll11lll_opy_ = bstack1ll1llll11l_opy_.bstack1ll11l1l11l_opy_(EVENTS.bstack1l11lllll11_opy_.value)
            PercySDK.screenshot(
                driver,
                bstack1ll1111ll1_opy_,
                bstack111lll1ll_opy_=bstack1l1l1111111_opy_[TestFramework.bstack1l1lllll1ll_opy_],
                bstack11l11lll11_opy_=bstack1l1l1111111_opy_[TestFramework.bstack1ll111111l1_opy_],
                bstack11l1lllll1_opy_=platform_index
            )
            bstack1ll1llll11l_opy_.end(EVENTS.bstack1l11lllll11_opy_.value, bstack1l1lll11lll_opy_+bstack1l11l1l_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧ፽"), bstack1l1lll11lll_opy_+bstack1l11l1l_opy_ (u"ࠨ࠺ࡦࡰࡧࠦ፾"), True, None, None, None, None, test_name=bstack1ll1111ll1_opy_)
    def bstack1ll11111l1_opy_(self, driver, platform_index):
        if self.bstack1lllllll11_opy_.bstack1ll111l11_opy_() is True or self.bstack1lllllll11_opy_.capturing() is True:
            return
        self.bstack1lllllll11_opy_.bstack11lll11ll1_opy_()
        while not self.bstack1lllllll11_opy_.bstack1ll111l11_opy_():
            bstack1l11llll111_opy_ = self.bstack1lllllll11_opy_.bstack11ll1l11l1_opy_()
            self.bstack11l111lll1_opy_(driver, bstack1l11llll111_opy_, platform_index)
        self.bstack1lllllll11_opy_.bstack1l111l111_opy_()
    def bstack11l111lll1_opy_(self, driver, bstack1111l1ll_opy_, platform_index, test=None):
        from bstack_utils.bstack1lll1l111_opy_ import bstack1ll1llll11l_opy_
        bstack1l1lll11lll_opy_ = bstack1ll1llll11l_opy_.bstack1ll11l1l11l_opy_(EVENTS.bstack111ll1ll1l_opy_.value)
        if test != None:
            bstack111lll1ll_opy_ = getattr(test, bstack1l11l1l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ፿"), None)
            bstack11l11lll11_opy_ = getattr(test, bstack1l11l1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᎀ"), None)
            PercySDK.screenshot(driver, bstack1111l1ll_opy_, bstack111lll1ll_opy_=bstack111lll1ll_opy_, bstack11l11lll11_opy_=bstack11l11lll11_opy_, bstack11l1lllll1_opy_=platform_index)
        else:
            PercySDK.screenshot(driver, bstack1111l1ll_opy_)
        bstack1ll1llll11l_opy_.end(EVENTS.bstack111ll1ll1l_opy_.value, bstack1l1lll11lll_opy_+bstack1l11l1l_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᎁ"), bstack1l1lll11lll_opy_+bstack1l11l1l_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᎂ"), True, None, None, None, None, test_name=bstack1111l1ll_opy_)
    def bstack1l11lll1ll1_opy_(self):
        os.environ[bstack1l11l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࠩᎃ")] = str(self.bstack1l11lllll1l_opy_.success)
        os.environ[bstack1l11l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡋࡒࡄ࡛ࡢࡇࡆࡖࡔࡖࡔࡈࡣࡒࡕࡄࡆࠩᎄ")] = str(self.bstack1l11lllll1l_opy_.percy_capture_mode)
        self.percy.bstack1l11llll1l1_opy_(self.bstack1l11lllll1l_opy_.is_percy_auto_enabled)
        self.percy.bstack1l11llll11l_opy_(self.bstack1l11lllll1l_opy_.percy_build_id)