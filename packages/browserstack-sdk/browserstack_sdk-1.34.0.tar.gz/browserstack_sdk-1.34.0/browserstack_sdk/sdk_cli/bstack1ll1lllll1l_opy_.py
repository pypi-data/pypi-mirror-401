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
from typing import Dict, List, Any, Callable, Tuple, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1lll1l1l1l1_opy_ import bstack1ll1l1ll1ll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1ll1l11_opy_ import (
    bstack1lll1l1ll11_opy_,
    bstack1llll11l111_opy_,
    bstack1llll11l1ll_opy_,
)
from bstack_utils.helper import  bstack1l1l1l111_opy_
from browserstack_sdk.sdk_cli.bstack1lll11ll1ll_opy_ import bstack1ll11llll11_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll1lll1111_opy_, bstack1ll1llllll1_opy_, bstack1lll11ll1l1_opy_, bstack1ll11ll111l_opy_
from typing import Tuple, Any
import threading
from bstack_utils.bstack11l11l11_opy_ import bstack111llll1ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l11111l_opy_ import bstack1lll111lll1_opy_
from bstack_utils.percy import bstack11ll11111_opy_
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.constants import *
import re
class bstack1ll1l1l11l1_opy_(bstack1ll1l1ll1ll_opy_):
    def __init__(self, bstack1l11ll1llll_opy_: Dict[str, str]):
        super().__init__()
        self.bstack1l11ll1llll_opy_ = bstack1l11ll1llll_opy_
        self.percy = bstack11ll11111_opy_()
        self.bstack1l111lll1_opy_ = bstack111llll1ll_opy_()
        self.bstack1l11llll111_opy_()
        bstack1ll11llll11_opy_.bstack1ll111l11ll_opy_((bstack1lll1l1ll11_opy_.bstack1llll111l1l_opy_, bstack1llll11l111_opy_.PRE), self.bstack1l11lll111l_opy_)
        TestFramework.bstack1ll111l11ll_opy_((bstack1ll1lll1111_opy_.TEST, bstack1lll11ll1l1_opy_.POST), self.bstack1l1ll1llll1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l111lll1_opy_(self, instance: bstack1llll11l1ll_opy_, driver: object):
        bstack1l1l1l1ll1l_opy_ = TestFramework.bstack1llll111111_opy_(instance.context)
        for t in bstack1l1l1l1ll1l_opy_:
            bstack1l1l1lll111_opy_ = TestFramework.bstack1llll1l111l_opy_(t, bstack1lll111lll1_opy_.bstack1l1l11l111l_opy_, [])
            if any(instance is d[1] for d in bstack1l1l1lll111_opy_) or instance == driver:
                return t
    def bstack1l11lll111l_opy_(
        self,
        f: bstack1ll11llll11_opy_,
        driver: object,
        exec: Tuple[bstack1llll11l1ll_opy_, str],
        bstack1lll1ll1111_opy_: Tuple[bstack1lll1l1ll11_opy_, bstack1llll11l111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if not bstack1ll11llll11_opy_.bstack1ll11111111_opy_(method_name):
                return
            platform_index = f.bstack1llll1l111l_opy_(instance, bstack1ll11llll11_opy_.bstack1ll1111ll1l_opy_, 0)
            bstack1l1l11l11ll_opy_ = self.bstack1l1l111lll1_opy_(instance, driver)
            bstack1l11lll11ll_opy_ = TestFramework.bstack1llll1l111l_opy_(bstack1l1l11l11ll_opy_, TestFramework.bstack1l11ll1ll11_opy_, None)
            if not bstack1l11lll11ll_opy_:
                self.logger.debug(bstack1l111l1_opy_ (u"ࠤࡲࡲࡤࡶࡲࡦࡡࡨࡼࡪࡩࡵࡵࡧ࠽ࠤࡷ࡫ࡴࡶࡴࡱ࡭ࡳ࡭ࠠࡢࡵࠣࡷࡪࡹࡳࡪࡱࡱࠤ࡮ࡹࠠ࡯ࡱࡷࠤࡾ࡫ࡴࠡࡵࡷࡥࡷࡺࡥࡥࠤᎏ"))
                return
            driver_command = f.bstack1l1lll11ll1_opy_(*args)
            for command in bstack11ll11ll1l_opy_:
                if command == driver_command:
                    self.bstack1lllll1l1_opy_(driver, platform_index)
            bstack1ll1111111_opy_ = self.percy.bstack1l1ll1ll1l_opy_()
            if driver_command in bstack11lll111l1_opy_[bstack1ll1111111_opy_]:
                self.bstack1l111lll1_opy_.bstack11lll1ll11_opy_(bstack1l11lll11ll_opy_, driver_command)
        except Exception as e:
            self.logger.error(bstack1l111l1_opy_ (u"ࠥࡳࡳࡥࡰࡳࡧࡢࡩࡽ࡫ࡣࡶࡶࡨ࠾ࠥ࡫ࡲࡳࡱࡵࠦ᎐"), e)
    def bstack1l1ll1llll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1llllll1_opy_,
        bstack1lll1ll1111_opy_: Tuple[bstack1ll1lll1111_opy_, bstack1lll11ll1l1_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack11lll1l1ll_opy_ import bstack1ll11ll1ll1_opy_
        bstack1l1l1lll111_opy_ = f.bstack1llll1l111l_opy_(instance, bstack1lll111lll1_opy_.bstack1l1l11l111l_opy_, [])
        if not bstack1l1l1lll111_opy_:
            self.logger.debug(bstack1l111l1_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨ᎑") + str(kwargs) + bstack1l111l1_opy_ (u"ࠧࠨ᎒"))
            return
        if len(bstack1l1l1lll111_opy_) > 1:
            self.logger.debug(bstack1l111l1_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠࡼ࡮ࡨࡲ࠭ࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳࠪࡿࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣ᎓") + str(kwargs) + bstack1l111l1_opy_ (u"ࠢࠣ᎔"))
        bstack1l11lll1l11_opy_, bstack1l11lll1111_opy_ = bstack1l1l1lll111_opy_[0]
        driver = bstack1l11lll1l11_opy_()
        if not driver:
            self.logger.debug(bstack1l111l1_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤ᎕") + str(kwargs) + bstack1l111l1_opy_ (u"ࠤࠥ᎖"))
            return
        bstack1l11ll1lll1_opy_ = {
            TestFramework.bstack1l1llll111l_opy_: bstack1l111l1_opy_ (u"ࠥࡸࡪࡹࡴࠡࡰࡤࡱࡪࠨ᎗"),
            TestFramework.bstack1ll111l11l1_opy_: bstack1l111l1_opy_ (u"ࠦࡹ࡫ࡳࡵࠢࡸࡹ࡮ࡪࠢ᎘"),
            TestFramework.bstack1l11ll1ll11_opy_: bstack1l111l1_opy_ (u"ࠧࡺࡥࡴࡶࠣࡶࡪࡸࡵ࡯ࠢࡱࡥࡲ࡫ࠢ᎙")
        }
        bstack1l11lll1lll_opy_ = { key: f.bstack1llll1l111l_opy_(instance, key) for key in bstack1l11ll1lll1_opy_ }
        bstack1l11ll1ll1l_opy_ = [key for key, value in bstack1l11lll1lll_opy_.items() if not value]
        if bstack1l11ll1ll1l_opy_:
            for key in bstack1l11ll1ll1l_opy_:
                self.logger.debug(bstack1l111l1_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠ࡮࡫ࡶࡷ࡮ࡴࡧࠡࠤ᎚") + str(key) + bstack1l111l1_opy_ (u"ࠢࠣ᎛"))
            return
        platform_index = f.bstack1llll1l111l_opy_(instance, bstack1ll11llll11_opy_.bstack1ll1111ll1l_opy_, 0)
        if self.bstack1l11ll1llll_opy_.percy_capture_mode == bstack1l111l1_opy_ (u"ࠣࡶࡨࡷࡹࡩࡡࡴࡧࠥ᎜"):
            bstack111llll11l_opy_ = bstack1l11lll1lll_opy_.get(TestFramework.bstack1l11ll1ll11_opy_) + bstack1l111l1_opy_ (u"ࠤ࠰ࡸࡪࡹࡴࡤࡣࡶࡩࠧ᎝")
            bstack1ll111ll11l_opy_ = bstack1ll11ll1ll1_opy_.bstack1ll1111l1l1_opy_(EVENTS.bstack1l11lll11l1_opy_.value)
            PercySDK.screenshot(
                driver,
                bstack111llll11l_opy_,
                bstack1111l11ll_opy_=bstack1l11lll1lll_opy_[TestFramework.bstack1l1llll111l_opy_],
                bstack1lll1lll1l_opy_=bstack1l11lll1lll_opy_[TestFramework.bstack1ll111l11l1_opy_],
                bstack11lllllll_opy_=platform_index
            )
            bstack1ll11ll1ll1_opy_.end(EVENTS.bstack1l11lll11l1_opy_.value, bstack1ll111ll11l_opy_+bstack1l111l1_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥ᎞"), bstack1ll111ll11l_opy_+bstack1l111l1_opy_ (u"ࠦ࠿࡫࡮ࡥࠤ᎟"), True, None, None, None, None, test_name=bstack111llll11l_opy_)
    def bstack1lllll1l1_opy_(self, driver, platform_index):
        if self.bstack1l111lll1_opy_.bstack1ll1111l1l_opy_() is True or self.bstack1l111lll1_opy_.capturing() is True:
            return
        self.bstack1l111lll1_opy_.bstack11l1l1l11_opy_()
        while not self.bstack1l111lll1_opy_.bstack1ll1111l1l_opy_():
            bstack1l11lll11ll_opy_ = self.bstack1l111lll1_opy_.bstack1ll1111l11_opy_()
            self.bstack11l1111lll_opy_(driver, bstack1l11lll11ll_opy_, platform_index)
        self.bstack1l111lll1_opy_.bstack1ll1111l1_opy_()
    def bstack11l1111lll_opy_(self, driver, bstack111ll1ll1_opy_, platform_index, test=None):
        from bstack_utils.bstack11lll1l1ll_opy_ import bstack1ll11ll1ll1_opy_
        bstack1ll111ll11l_opy_ = bstack1ll11ll1ll1_opy_.bstack1ll1111l1l1_opy_(EVENTS.bstack1ll1lll1l_opy_.value)
        if test != None:
            bstack1111l11ll_opy_ = getattr(test, bstack1l111l1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᎠ"), None)
            bstack1lll1lll1l_opy_ = getattr(test, bstack1l111l1_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᎡ"), None)
            PercySDK.screenshot(driver, bstack111ll1ll1_opy_, bstack1111l11ll_opy_=bstack1111l11ll_opy_, bstack1lll1lll1l_opy_=bstack1lll1lll1l_opy_, bstack11lllllll_opy_=platform_index)
        else:
            PercySDK.screenshot(driver, bstack111ll1ll1_opy_)
        bstack1ll11ll1ll1_opy_.end(EVENTS.bstack1ll1lll1l_opy_.value, bstack1ll111ll11l_opy_+bstack1l111l1_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᎢ"), bstack1ll111ll11l_opy_+bstack1l111l1_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᎣ"), True, None, None, None, None, test_name=bstack111ll1ll1_opy_)
    def bstack1l11llll111_opy_(self):
        os.environ[bstack1l111l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡈࡖࡈ࡟ࠧᎤ")] = str(self.bstack1l11ll1llll_opy_.success)
        os.environ[bstack1l111l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡉࡗࡉ࡙ࡠࡅࡄࡔ࡙࡛ࡒࡆࡡࡐࡓࡉࡋࠧᎥ")] = str(self.bstack1l11ll1llll_opy_.percy_capture_mode)
        self.percy.bstack1l11lll1l1l_opy_(self.bstack1l11ll1llll_opy_.is_percy_auto_enabled)
        self.percy.bstack1l11lll1ll1_opy_(self.bstack1l11ll1llll_opy_.percy_build_id)