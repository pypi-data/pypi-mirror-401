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
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1lllll111ll_opy_ import bstack1llll1111ll_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1l1l11ll_opy_ import bstack1l1111lll1l_opy_
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1ll11ll1lll_opy_,
    bstack1lll1l1111l_opy_,
    bstack1ll1l1l1ll1_opy_,
    bstack11llll1l111_opy_,
    bstack1ll1lll1ll1_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack1l1l1ll11ll_opy_
from bstack_utils.bstack1lll1l111_opy_ import bstack1ll1llll11l_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack1lllll1l111_opy_ import bstack1lllll11l11_opy_
from browserstack_sdk.sdk_cli.utils.bstack1ll1ll1ll11_opy_ import bstack1lll11l1111_opy_
from bstack_utils.bstack111l1l1111_opy_ import bstack1l1l1lllll_opy_
bstack1l1l1ll11l1_opy_ = bstack1l1l1ll11ll_opy_()
bstack1l1111111ll_opy_ = 1.0
bstack1l1l1llll1l_opy_ = bstack1l11l1l_opy_ (u"࡚ࠦࡶ࡬ࡰࡣࡧࡩࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵ࠰ࠦᕴ")
bstack11lll11l1ll_opy_ = bstack1l11l1l_opy_ (u"࡚ࠧࡥࡴࡶࡏࡩࡻ࡫࡬ࠣᕵ")
bstack11lll11l11l_opy_ = bstack1l11l1l_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥᕶ")
bstack11lll111ll1_opy_ = bstack1l11l1l_opy_ (u"ࠢࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠥᕷ")
bstack11lll111lll_opy_ = bstack1l11l1l_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠢᕸ")
_1l1l11lll1l_opy_ = set()
class bstack1ll11lll11l_opy_(TestFramework):
    bstack1l111111l1l_opy_ = bstack1l11l1l_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴࠤᕹ")
    bstack11lllll11l1_opy_ = bstack1l11l1l_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠣᕺ")
    bstack11lllll1111_opy_ = bstack1l11l1l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࠥᕻ")
    bstack11lll1ll111_opy_ = bstack1l11l1l_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠ࡮ࡤࡷࡹࡥࡳࡵࡣࡵࡸࡪࡪࠢᕼ")
    bstack11lll1l11l1_opy_ = bstack1l11l1l_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡ࡯ࡥࡸࡺ࡟ࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࠤᕽ")
    bstack1l1111lll11_opy_: bool
    bstack1lllll1l111_opy_: bstack1lllll11l11_opy_  = None
    bstack1lll1l11ll1_opy_ = None
    bstack1l1111l1ll1_opy_ = [
        bstack1ll11ll1lll_opy_.BEFORE_ALL,
        bstack1ll11ll1lll_opy_.AFTER_ALL,
        bstack1ll11ll1lll_opy_.BEFORE_EACH,
        bstack1ll11ll1lll_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack11lll1l1111_opy_: Dict[str, str],
        bstack1l1lll11l11_opy_: List[str]=[bstack1l11l1l_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺࠢᕾ")],
        bstack1lllll1l111_opy_: bstack1lllll11l11_opy_=None,
        bstack1lll1l11ll1_opy_=None
    ):
        super().__init__(bstack1l1lll11l11_opy_, bstack11lll1l1111_opy_, bstack1lllll1l111_opy_)
        self.bstack1l1111lll11_opy_ = any(bstack1l11l1l_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴࠣᕿ") in item.lower() for item in bstack1l1lll11l11_opy_)
        self.bstack1lll1l11ll1_opy_ = bstack1lll1l11ll1_opy_
    def track_event(
        self,
        context: bstack11llll1l111_opy_,
        test_framework_state: bstack1ll11ll1lll_opy_,
        test_hook_state: bstack1ll1l1l1ll1_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack1ll11ll1lll_opy_.TEST or test_framework_state in bstack1ll11lll11l_opy_.bstack1l1111l1ll1_opy_:
            bstack1l1111lll1l_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1ll11ll1lll_opy_.NONE:
            self.logger.warning(bstack1l11l1l_opy_ (u"ࠤ࡬࡫ࡳࡵࡲࡦࡦࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯ࠥࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦ࠿ࠥᖀ") + str(test_hook_state) + bstack1l11l1l_opy_ (u"ࠥࠦᖁ"))
            return
        if not self.bstack1l1111lll11_opy_:
            self.logger.warning(bstack1l11l1l_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳࡹࡵࡱࡲࡲࡶࡹ࡫ࡤࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡁࠧᖂ") + str(str(self.bstack1l1lll11l11_opy_)) + bstack1l11l1l_opy_ (u"ࠧࠨᖃ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1l11l1l_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡦࡺࡳࡩࡨࡺࡥࡥࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᖄ") + str(kwargs) + bstack1l11l1l_opy_ (u"ࠢࠣᖅ"))
            return
        instance = self.__11llll111l1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1l11l1l_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡣࡵ࡫ࡸࡃࠢᖆ") + str(args) + bstack1l11l1l_opy_ (u"ࠤࠥᖇ"))
            return
        try:
            if instance!= None and test_framework_state in bstack1ll11lll11l_opy_.bstack1l1111l1ll1_opy_ and test_hook_state == bstack1ll1l1l1ll1_opy_.PRE:
                bstack1l1lll11lll_opy_ = bstack1ll1llll11l_opy_.bstack1ll11l1l11l_opy_(EVENTS.bstack1l1111l111_opy_.value)
                name = str(EVENTS.bstack1l1111l111_opy_.name)+bstack1l11l1l_opy_ (u"ࠥ࠾ࠧᖈ")+str(test_framework_state.name)
                TestFramework.bstack11llllll111_opy_(instance, name, bstack1l1lll11lll_opy_)
        except Exception as e:
            self.logger.debug(bstack1l11l1l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡴࡵ࡫ࠡࡧࡵࡶࡴࡸࠠࡱࡴࡨ࠾ࠥࢁࡽࠣᖉ").format(e))
        try:
            if not TestFramework.bstack1llll11ll11_opy_(instance, TestFramework.bstack11lll1lll11_opy_) and test_hook_state == bstack1ll1l1l1ll1_opy_.PRE:
                test = bstack1ll11lll11l_opy_.__11llllllll1_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack1l11l1l_opy_ (u"ࠧࡲ࡯ࡢࡦࡨࡨࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡶࡪ࡬ࠨࠪࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧᖊ") + str(test_hook_state) + bstack1l11l1l_opy_ (u"ࠨࠢᖋ"))
            if test_framework_state == bstack1ll11ll1lll_opy_.TEST:
                if test_hook_state == bstack1ll1l1l1ll1_opy_.PRE and not TestFramework.bstack1llll11ll11_opy_(instance, TestFramework.bstack1l1l1l1lll1_opy_):
                    TestFramework.bstack1llll1l111l_opy_(instance, TestFramework.bstack1l1l1l1lll1_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1l11l1l_opy_ (u"ࠢࡴࡧࡷࠤࡹ࡫ࡳࡵ࠯ࡶࡸࡦࡸࡴࠡࡨࡲࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡶࡪ࡬ࠨࠪࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧᖌ") + str(test_hook_state) + bstack1l11l1l_opy_ (u"ࠣࠤᖍ"))
                elif test_hook_state == bstack1ll1l1l1ll1_opy_.POST and not TestFramework.bstack1llll11ll11_opy_(instance, TestFramework.bstack1l1l11l1l1l_opy_):
                    TestFramework.bstack1llll1l111l_opy_(instance, TestFramework.bstack1l1l11l1l1l_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1l11l1l_opy_ (u"ࠤࡶࡩࡹࠦࡴࡦࡵࡷ࠱ࡪࡴࡤࠡࡨࡲࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡶࡪ࡬ࠨࠪࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧᖎ") + str(test_hook_state) + bstack1l11l1l_opy_ (u"ࠥࠦᖏ"))
            elif test_framework_state == bstack1ll11ll1lll_opy_.LOG and test_hook_state == bstack1ll1l1l1ll1_opy_.POST:
                bstack1ll11lll11l_opy_.__11llll1111l_opy_(instance, *args)
            elif test_framework_state == bstack1ll11ll1lll_opy_.LOG_REPORT and test_hook_state == bstack1ll1l1l1ll1_opy_.POST:
                self.__11lll1llll1_opy_(instance, *args)
                self.__1l11111l1l1_opy_(instance)
            elif test_framework_state in bstack1ll11lll11l_opy_.bstack1l1111l1ll1_opy_:
                self.__1l11111111l_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1l11l1l_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࠧᖐ") + str(instance.ref()) + bstack1l11l1l_opy_ (u"ࠧࠨᖑ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack11lllll11ll_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in bstack1ll11lll11l_opy_.bstack1l1111l1ll1_opy_ and test_hook_state == bstack1ll1l1l1ll1_opy_.POST:
                name = str(EVENTS.bstack1l1111l111_opy_.name)+bstack1l11l1l_opy_ (u"ࠨ࠺ࠣᖒ")+str(test_framework_state.name)
                bstack1l1lll11lll_opy_ = TestFramework.bstack11llll1l1l1_opy_(instance, name)
                bstack1ll1llll11l_opy_.end(EVENTS.bstack1l1111l111_opy_.value, bstack1l1lll11lll_opy_+bstack1l11l1l_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᖓ"), bstack1l1lll11lll_opy_+bstack1l11l1l_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᖔ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1l11l1l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡲࡳࡰࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠤᖕ").format(e))
    def bstack1l1l11l1lll_opy_(self):
        return self.bstack1l1111lll11_opy_
    def __11llll1l1ll_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1l11l1l_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡳࡧࡶࡹࡱࡺࠢᖖ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l1l11ll111_opy_(rep, [bstack1l11l1l_opy_ (u"ࠦࡼ࡮ࡥ࡯ࠤᖗ"), bstack1l11l1l_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨᖘ"), bstack1l11l1l_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨᖙ"), bstack1l11l1l_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢᖚ"), bstack1l11l1l_opy_ (u"ࠣࡵ࡮࡭ࡵࡶࡥࡥࠤᖛ"), bstack1l11l1l_opy_ (u"ࠤ࡯ࡳࡳ࡭ࡲࡦࡲࡵࡸࡪࡾࡴࠣᖜ")])
        return None
    def __11lll1llll1_opy_(self, instance: bstack1lll1l1111l_opy_, *args):
        result = self.__11llll1l1ll_opy_(*args)
        if not result:
            return
        failure = None
        bstack1lllll1ll11_opy_ = None
        if result.get(bstack1l11l1l_opy_ (u"ࠥࡳࡺࡺࡣࡰ࡯ࡨࠦᖝ"), None) == bstack1l11l1l_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦᖞ") and len(args) > 1 and getattr(args[1], bstack1l11l1l_opy_ (u"ࠧ࡫ࡸࡤ࡫ࡱࡪࡴࠨᖟ"), None) is not None:
            failure = [{bstack1l11l1l_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩᖠ"): [args[1].excinfo.exconly(), result.get(bstack1l11l1l_opy_ (u"ࠢ࡭ࡱࡱ࡫ࡷ࡫ࡰࡳࡶࡨࡼࡹࠨᖡ"), None)]}]
            bstack1lllll1ll11_opy_ = bstack1l11l1l_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࡉࡷࡸ࡯ࡳࠤᖢ") if bstack1l11l1l_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࠧᖣ") in getattr(args[1].excinfo, bstack1l11l1l_opy_ (u"ࠥࡸࡾࡶࡥ࡯ࡣࡰࡩࠧᖤ"), bstack1l11l1l_opy_ (u"ࠦࠧᖥ")) else bstack1l11l1l_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨᖦ")
        bstack11lllllll1l_opy_ = result.get(bstack1l11l1l_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢᖧ"), TestFramework.bstack11llll11l11_opy_)
        if bstack11lllllll1l_opy_ != TestFramework.bstack11llll11l11_opy_:
            TestFramework.bstack1llll1l111l_opy_(instance, TestFramework.bstack1l1l1l1l1l1_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack1l1111l1lll_opy_(instance, {
            TestFramework.bstack1l11l1lll11_opy_: failure,
            TestFramework.bstack1l1111l1l1l_opy_: bstack1lllll1ll11_opy_,
            TestFramework.bstack1l11l1l111l_opy_: bstack11lllllll1l_opy_,
        })
    def __11llll111l1_opy_(
        self,
        context: bstack11llll1l111_opy_,
        test_framework_state: bstack1ll11ll1lll_opy_,
        test_hook_state: bstack1ll1l1l1ll1_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack1ll11ll1lll_opy_.SETUP_FIXTURE:
            instance = self.__1l1111ll1l1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack11lll11llll_opy_ bstack11llll1llll_opy_ this to be bstack1l11l1l_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᖨ")
            if test_framework_state == bstack1ll11ll1lll_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__11lll1l1l11_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1ll11ll1lll_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack1l11l1l_opy_ (u"ࠣࡰࡲࡨࡪࠨᖩ"), None), bstack1l11l1l_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤᖪ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1l11l1l_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᖫ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1llll11111l_opy_(target) if target else None
        return instance
    def __1l11111111l_opy_(
        self,
        instance: bstack1lll1l1111l_opy_,
        test_framework_state: bstack1ll11ll1lll_opy_,
        test_hook_state: bstack1ll1l1l1ll1_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack1l1111l111l_opy_ = TestFramework.bstack1lll1llll11_opy_(instance, bstack1ll11lll11l_opy_.bstack11lllll11l1_opy_, {})
        if not key in bstack1l1111l111l_opy_:
            bstack1l1111l111l_opy_[key] = []
        bstack1l11111llll_opy_ = TestFramework.bstack1lll1llll11_opy_(instance, bstack1ll11lll11l_opy_.bstack11lllll1111_opy_, {})
        if not key in bstack1l11111llll_opy_:
            bstack1l11111llll_opy_[key] = []
        bstack1l111111lll_opy_ = {
            bstack1ll11lll11l_opy_.bstack11lllll11l1_opy_: bstack1l1111l111l_opy_,
            bstack1ll11lll11l_opy_.bstack11lllll1111_opy_: bstack1l11111llll_opy_,
        }
        if test_hook_state == bstack1ll1l1l1ll1_opy_.PRE:
            hook = {
                bstack1l11l1l_opy_ (u"ࠦࡰ࡫ࡹࠣᖬ"): key,
                TestFramework.bstack1l1111ll1ll_opy_: uuid4().__str__(),
                TestFramework.bstack1l11111l1ll_opy_: TestFramework.bstack11llllll1ll_opy_,
                TestFramework.bstack11lllllll11_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack11llllll1l1_opy_: [],
                TestFramework.bstack11lll1l1ll1_opy_: args[1] if len(args) > 1 else bstack1l11l1l_opy_ (u"ࠬ࠭ᖭ"),
                TestFramework.bstack11llll1ll11_opy_: bstack1lll11l1111_opy_.bstack11lll1lllll_opy_()
            }
            bstack1l1111l111l_opy_[key].append(hook)
            bstack1l111111lll_opy_[bstack1ll11lll11l_opy_.bstack11lll1ll111_opy_] = key
        elif test_hook_state == bstack1ll1l1l1ll1_opy_.POST:
            bstack11lllll111l_opy_ = bstack1l1111l111l_opy_.get(key, [])
            hook = bstack11lllll111l_opy_.pop() if bstack11lllll111l_opy_ else None
            if hook:
                result = self.__11llll1l1ll_opy_(*args)
                if result:
                    bstack11lll1ll1l1_opy_ = result.get(bstack1l11l1l_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢᖮ"), TestFramework.bstack11llllll1ll_opy_)
                    if bstack11lll1ll1l1_opy_ != TestFramework.bstack11llllll1ll_opy_:
                        hook[TestFramework.bstack1l11111l1ll_opy_] = bstack11lll1ll1l1_opy_
                hook[TestFramework.bstack11lllll1lll_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack11llll1ll11_opy_]= bstack1lll11l1111_opy_.bstack11lll1lllll_opy_()
                self.bstack11lllll1l1l_opy_(hook)
                logs = hook.get(TestFramework.bstack1l1111ll111_opy_, [])
                if logs: self.bstack1l1l11ll11l_opy_(instance, logs)
                bstack1l11111llll_opy_[key].append(hook)
                bstack1l111111lll_opy_[bstack1ll11lll11l_opy_.bstack11lll1l11l1_opy_] = key
        TestFramework.bstack1l1111l1lll_opy_(instance, bstack1l111111lll_opy_)
        self.logger.debug(bstack1l11l1l_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡨࡰࡱ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࡃࡻ࡬ࡧࡼࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢ࡫ࡳࡴࡱࡳࡠࡵࡷࡥࡷࡺࡥࡥ࠿ࡾ࡬ࡴࡵ࡫ࡴࡡࡶࡸࡦࡸࡴࡦࡦࢀࠤ࡭ࡵ࡯࡬ࡵࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࡂࠨᖯ") + str(bstack1l11111llll_opy_) + bstack1l11l1l_opy_ (u"ࠣࠤᖰ"))
    def __1l1111ll1l1_opy_(
        self,
        context: bstack11llll1l111_opy_,
        test_framework_state: bstack1ll11ll1lll_opy_,
        test_hook_state: bstack1ll1l1l1ll1_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l1l11ll111_opy_(args[0], [bstack1l11l1l_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣᖱ"), bstack1l11l1l_opy_ (u"ࠥࡥࡷ࡭࡮ࡢ࡯ࡨࠦᖲ"), bstack1l11l1l_opy_ (u"ࠦࡵࡧࡲࡢ࡯ࡶࠦᖳ"), bstack1l11l1l_opy_ (u"ࠧ࡯ࡤࡴࠤᖴ"), bstack1l11l1l_opy_ (u"ࠨࡵ࡯࡫ࡷࡸࡪࡹࡴࠣᖵ"), bstack1l11l1l_opy_ (u"ࠢࡣࡣࡶࡩ࡮ࡪࠢᖶ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scope = request.scope if hasattr(request, bstack1l11l1l_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢᖷ")) else fixturedef.get(bstack1l11l1l_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣᖸ"), None)
        fixturename = request.fixturename if hasattr(request, bstack1l11l1l_opy_ (u"ࠥࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࠣᖹ")) else None
        node = request.node if hasattr(request, bstack1l11l1l_opy_ (u"ࠦࡳࡵࡤࡦࠤᖺ")) else None
        target = request.node.nodeid if hasattr(node, bstack1l11l1l_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᖻ")) else None
        baseid = fixturedef.get(bstack1l11l1l_opy_ (u"ࠨࡢࡢࡵࡨ࡭ࡩࠨᖼ"), None) or bstack1l11l1l_opy_ (u"ࠢࠣᖽ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1l11l1l_opy_ (u"ࠣࡡࡳࡽ࡫ࡻ࡮ࡤ࡫ࡷࡩࡲࠨᖾ")):
            target = bstack1ll11lll11l_opy_.__1l11111lll1_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1l11l1l_opy_ (u"ࠤ࡯ࡳࡨࡧࡴࡪࡱࡱࠦᖿ")) else None
            if target and not TestFramework.bstack1llll11111l_opy_(target):
                self.__11lll1l1l11_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1l11l1l_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡪࡦࡲ࡬ࡣࡣࡦ࡯ࠥࡺࡡࡳࡩࡨࡸࡂࢁࡴࡢࡴࡪࡩࡹࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡴ࡯ࡥࡧࡀࡿࡳࡵࡤࡦࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧᗀ") + str(test_hook_state) + bstack1l11l1l_opy_ (u"ࠦࠧᗁ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack1l11l1l_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫ࡤࡦࡨࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡩ࡫ࡦࡾࠢࡶࡧࡴࡶࡥ࠾ࡽࡶࡧࡴࡶࡥࡾࠢࡷࡥࡷ࡭ࡥࡵ࠿ࠥᗂ") + str(target) + bstack1l11l1l_opy_ (u"ࠨࠢᗃ"))
            return None
        instance = TestFramework.bstack1llll11111l_opy_(target)
        if not instance:
            self.logger.warning(bstack1l11l1l_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡢࡢࡵࡨ࡭ࡩࡃࡻࡣࡣࡶࡩ࡮ࡪࡽࠡࡶࡤࡶ࡬࡫ࡴ࠾ࠤᗄ") + str(target) + bstack1l11l1l_opy_ (u"ࠣࠤᗅ"))
            return None
        bstack11lll1l11ll_opy_ = TestFramework.bstack1lll1llll11_opy_(instance, bstack1ll11lll11l_opy_.bstack1l111111l1l_opy_, {})
        if os.getenv(bstack1l11l1l_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡊࡑࡇࡇࡠࡈࡌ࡜࡙࡛ࡒࡆࡕࠥᗆ"), bstack1l11l1l_opy_ (u"ࠥ࠵ࠧᗇ")) == bstack1l11l1l_opy_ (u"ࠦ࠶ࠨᗈ"):
            bstack1l1111l11l1_opy_ = bstack1l11l1l_opy_ (u"ࠧࡀࠢᗉ").join((scope, fixturename))
            bstack11llll11ll1_opy_ = datetime.now(tz=timezone.utc)
            bstack11lll1l1l1l_opy_ = {
                bstack1l11l1l_opy_ (u"ࠨ࡫ࡦࡻࠥᗊ"): bstack1l1111l11l1_opy_,
                bstack1l11l1l_opy_ (u"ࠢࡵࡣࡪࡷࠧᗋ"): bstack1ll11lll11l_opy_.__11llll1ll1l_opy_(request.node),
                bstack1l11l1l_opy_ (u"ࠣࡨ࡬ࡼࡹࡻࡲࡦࠤᗌ"): fixturedef,
                bstack1l11l1l_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣᗍ"): scope,
                bstack1l11l1l_opy_ (u"ࠥࡸࡾࡶࡥࠣᗎ"): None,
            }
            try:
                if test_hook_state == bstack1ll1l1l1ll1_opy_.POST and callable(getattr(args[-1], bstack1l11l1l_opy_ (u"ࠦ࡬࡫ࡴࡠࡴࡨࡷࡺࡲࡴࠣᗏ"), None)):
                    bstack11lll1l1l1l_opy_[bstack1l11l1l_opy_ (u"ࠧࡺࡹࡱࡧࠥᗐ")] = TestFramework.bstack1l1l1ll1l1l_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1ll1l1l1ll1_opy_.PRE:
                bstack11lll1l1l1l_opy_[bstack1l11l1l_opy_ (u"ࠨࡵࡶ࡫ࡧࠦᗑ")] = uuid4().__str__()
                bstack11lll1l1l1l_opy_[bstack1ll11lll11l_opy_.bstack11lllllll11_opy_] = bstack11llll11ll1_opy_
            elif test_hook_state == bstack1ll1l1l1ll1_opy_.POST:
                bstack11lll1l1l1l_opy_[bstack1ll11lll11l_opy_.bstack11lllll1lll_opy_] = bstack11llll11ll1_opy_
            if bstack1l1111l11l1_opy_ in bstack11lll1l11ll_opy_:
                bstack11lll1l11ll_opy_[bstack1l1111l11l1_opy_].update(bstack11lll1l1l1l_opy_)
                self.logger.debug(bstack1l11l1l_opy_ (u"ࠢࡶࡲࡧࡥࡹ࡫ࡤࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫࠽ࠣᗒ") + str(bstack11lll1l11ll_opy_[bstack1l1111l11l1_opy_]) + bstack1l11l1l_opy_ (u"ࠣࠤᗓ"))
            else:
                bstack11lll1l11ll_opy_[bstack1l1111l11l1_opy_] = bstack11lll1l1l1l_opy_
                self.logger.debug(bstack1l11l1l_opy_ (u"ࠤࡶࡥࡻ࡫ࡤࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫࠽ࡼࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫ࡽࠡࡶࡵࡥࡨࡱࡥࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࡁࠧᗔ") + str(len(bstack11lll1l11ll_opy_)) + bstack1l11l1l_opy_ (u"ࠥࠦᗕ"))
        TestFramework.bstack1llll1l111l_opy_(instance, bstack1ll11lll11l_opy_.bstack1l111111l1l_opy_, bstack11lll1l11ll_opy_)
        self.logger.debug(bstack1l11l1l_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣࡪ࡮ࡾࡴࡶࡴࡨࡷࡂࢁ࡬ࡦࡰࠫࡸࡷࡧࡣ࡬ࡧࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࡸ࠯ࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦᗖ") + str(instance.ref()) + bstack1l11l1l_opy_ (u"ࠧࠨᗗ"))
        return instance
    def __11lll1l1l11_opy_(
        self,
        context: bstack11llll1l111_opy_,
        test_framework_state: bstack1ll11ll1lll_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack1llll1111ll_opy_.create_context(target)
        ob = bstack1lll1l1111l_opy_(ctx, self.bstack1l1lll11l11_opy_, self.bstack11lll1l1111_opy_, test_framework_state)
        TestFramework.bstack1l1111l1lll_opy_(ob, {
            TestFramework.bstack1ll111l1l1l_opy_: context.test_framework_name,
            TestFramework.bstack1l1l11l111l_opy_: context.test_framework_version,
            TestFramework.bstack11llll11l1l_opy_: [],
            bstack1ll11lll11l_opy_.bstack1l111111l1l_opy_: {},
            bstack1ll11lll11l_opy_.bstack11lllll1111_opy_: {},
            bstack1ll11lll11l_opy_.bstack11lllll11l1_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1llll1l111l_opy_(ob, TestFramework.bstack11lll1ll1ll_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1llll1l111l_opy_(ob, TestFramework.bstack1l1llllll1l_opy_, context.platform_index)
        TestFramework.bstack1llll1lll11_opy_[ctx.id] = ob
        self.logger.debug(bstack1l11l1l_opy_ (u"ࠨࡳࡢࡸࡨࡨࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠠࡤࡶࡻ࠲࡮ࡪ࠽ࡼࡥࡷࡼ࠳࡯ࡤࡾࠢࡷࡥࡷ࡭ࡥࡵ࠿ࡾࡸࡦࡸࡧࡦࡶࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷࡂࠨᗘ") + str(TestFramework.bstack1llll1lll11_opy_.keys()) + bstack1l11l1l_opy_ (u"ࠢࠣᗙ"))
        return ob
    def bstack1l1l1ll1111_opy_(self, instance: bstack1lll1l1111l_opy_, bstack1llll1lllll_opy_: Tuple[bstack1ll11ll1lll_opy_, bstack1ll1l1l1ll1_opy_]):
        bstack11lll1lll1l_opy_ = (
            bstack1ll11lll11l_opy_.bstack11lll1ll111_opy_
            if bstack1llll1lllll_opy_[1] == bstack1ll1l1l1ll1_opy_.PRE
            else bstack1ll11lll11l_opy_.bstack11lll1l11l1_opy_
        )
        hook = bstack1ll11lll11l_opy_.bstack1l111111ll1_opy_(instance, bstack11lll1lll1l_opy_)
        entries = hook.get(TestFramework.bstack11llllll1l1_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1lll1llll11_opy_(instance, TestFramework.bstack11llll11l1l_opy_, []))
        return entries
    def bstack1l1l11l1l11_opy_(self, instance: bstack1lll1l1111l_opy_, bstack1llll1lllll_opy_: Tuple[bstack1ll11ll1lll_opy_, bstack1ll1l1l1ll1_opy_]):
        bstack11lll1lll1l_opy_ = (
            bstack1ll11lll11l_opy_.bstack11lll1ll111_opy_
            if bstack1llll1lllll_opy_[1] == bstack1ll1l1l1ll1_opy_.PRE
            else bstack1ll11lll11l_opy_.bstack11lll1l11l1_opy_
        )
        bstack1ll11lll11l_opy_.bstack11lll1l111l_opy_(instance, bstack11lll1lll1l_opy_)
        TestFramework.bstack1lll1llll11_opy_(instance, TestFramework.bstack11llll11l1l_opy_, []).clear()
    def bstack11lllll1l1l_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1l11l1l_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡖࡲࡰࡥࡨࡷࡸ࡫ࡳࠡࡶ࡫ࡩࠥࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡳࡪ࡯࡬ࡰࡦࡸࠠࡵࡱࠣࡸ࡭࡫ࠠࡋࡣࡹࡥࠥ࡯࡭ࡱ࡮ࡨࡱࡪࡴࡴࡢࡶ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡖ࡫࡭ࡸࠦ࡭ࡦࡶ࡫ࡳࡩࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡉࡨࡦࡥ࡮ࡷࠥࡺࡨࡦࠢࡋࡳࡴࡱࡌࡦࡸࡨࡰࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡ࡫ࡱࡷ࡮ࡪࡥࠡࢀ࠲࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠲࡙ࡵࡲ࡯ࡢࡦࡨࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡈࡲࡶࠥ࡫ࡡࡤࡪࠣࡪ࡮ࡲࡥࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࡡ࡯ࡩࡻ࡫࡬ࡠࡨ࡬ࡰࡪࡹࠬࠡࡴࡨࡴࡱࡧࡣࡦࡵ࡙ࠣࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢࠡࡹ࡬ࡸ࡭ࠦࠢࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠥࠤ࡮ࡴࠠࡪࡶࡶࠤࡵࡧࡴࡩ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡋࡩࠤࡦࠦࡦࡪ࡮ࡨࠤ࡮ࡴࠠࡵࡪࡨࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠ࡮ࡣࡷࡧ࡭࡫ࡳࠡࡣࠣࡱࡴࡪࡩࡧ࡫ࡨࡨࠥ࡮࡯ࡰ࡭࠰ࡰࡪࡼࡥ࡭ࠢࡩ࡭ࡱ࡫ࠬࠡ࡫ࡷࠤࡨࡸࡥࡢࡶࡨࡷࠥࡧࠠࡍࡱࡪࡉࡳࡺࡲࡺࠢࡲࡦ࡯࡫ࡣࡵࠢࡺ࡭ࡹ࡮ࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠤࡩ࡫ࡴࡢ࡫࡯ࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡘ࡯࡭ࡪ࡮ࡤࡶࡱࡿࠬࠡ࡫ࡷࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢ࡯ࡳࡨࡧࡴࡦࡦࠣ࡭ࡳࠦࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭࠱ࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠡࡤࡼࠤࡷ࡫ࡰ࡭ࡣࡦ࡭ࡳ࡭ࠠࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧࠦࡷࡪࡶ࡫ࠤࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬࠰ࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠢ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡕࡪࡨࠤࡨࡸࡥࡢࡶࡨࡨࠥࡒ࡯ࡨࡇࡱࡸࡷࡿࠠࡰࡤ࡭ࡩࡨࡺࡳࠡࡣࡵࡩࠥࡧࡤࡥࡧࡧࠤࡹࡵࠠࡵࡪࡨࠤ࡭ࡵ࡯࡬ࠩࡶࠤࠧࡲ࡯ࡨࡵࠥࠤࡱ࡯ࡳࡵ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡪࡲࡳࡰࡀࠠࡕࡪࡨࠤࡪࡼࡥ࡯ࡶࠣࡨ࡮ࡩࡴࡪࡱࡱࡥࡷࡿࠠࡤࡱࡱࡸࡦ࡯࡮ࡪࡰࡪࠤࡪࡾࡩࡴࡶ࡬ࡲ࡬ࠦ࡬ࡰࡩࡶࠤࡦࡴࡤࠡࡪࡲࡳࡰࠦࡩ࡯ࡨࡲࡶࡲࡧࡴࡪࡱࡱ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࡬ࡴࡵ࡫ࡠ࡮ࡨࡺࡪࡲ࡟ࡧ࡫࡯ࡩࡸࡀࠠࡍ࡫ࡶࡸࠥࡵࡦࠡࡒࡤࡸ࡭ࠦ࡯ࡣ࡬ࡨࡧࡹࡹࠠࡧࡴࡲࡱࠥࡺࡨࡦࠢࡗࡩࡸࡺࡌࡦࡸࡨࡰࠥࡳ࡯࡯࡫ࡷࡳࡷ࡯࡮ࡨ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡤࡸ࡭ࡱࡪ࡟࡭ࡧࡹࡩࡱࡥࡦࡪ࡮ࡨࡷ࠿ࠦࡌࡪࡵࡷࠤࡴ࡬ࠠࡑࡣࡷ࡬ࠥࡵࡢ࡫ࡧࡦࡸࡸࠦࡦࡳࡱࡰࠤࡹ࡮ࡥࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠥࡳ࡯࡯࡫ࡷࡳࡷ࡯࡮ࡨ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢᗚ")
        global _1l1l11lll1l_opy_
        platform_index = os.environ[bstack1l11l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᗛ")]
        bstack1l1l11l1111_opy_ = os.path.join(bstack1l1l1ll11l1_opy_, (bstack1l1l1llll1l_opy_ + str(platform_index)), bstack11lll111ll1_opy_)
        if not os.path.exists(bstack1l1l11l1111_opy_) or not os.path.isdir(bstack1l1l11l1111_opy_):
            self.logger.debug(bstack1l11l1l_opy_ (u"ࠥࡈ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡧࡻ࡭ࡸࡺࡳࠡࡶࡲࠤࡵࡸ࡯ࡤࡧࡶࡷࠥࢁࡽࠣᗜ").format(bstack1l1l11l1111_opy_))
            return
        logs = hook.get(bstack1l11l1l_opy_ (u"ࠦࡱࡵࡧࡴࠤᗝ"), [])
        with os.scandir(bstack1l1l11l1111_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l1l11lll1l_opy_:
                    self.logger.info(bstack1l11l1l_opy_ (u"ࠧࡖࡡࡵࡪࠣࡥࡱࡸࡥࡢࡦࡼࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡼࡿࠥᗞ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1l11l1l_opy_ (u"ࠨࠢᗟ")
                    log_entry = bstack1ll1lll1ll1_opy_(
                        kind=bstack1l11l1l_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤᗠ"),
                        message=bstack1l11l1l_opy_ (u"ࠣࠤᗡ"),
                        level=bstack1l11l1l_opy_ (u"ࠤࠥᗢ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l1ll11111l_opy_=entry.stat().st_size,
                        bstack1l1l1l11111_opy_=bstack1l11l1l_opy_ (u"ࠥࡑࡆࡔࡕࡂࡎࡢ࡙ࡕࡒࡏࡂࡆࠥᗣ"),
                        bstack11ll_opy_=os.path.abspath(entry.path),
                        bstack11lll1ll11l_opy_=hook.get(TestFramework.bstack1l1111ll1ll_opy_)
                    )
                    logs.append(log_entry)
                    _1l1l11lll1l_opy_.add(abs_path)
        platform_index = os.environ[bstack1l11l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᗤ")]
        bstack1l111111l11_opy_ = os.path.join(bstack1l1l1ll11l1_opy_, (bstack1l1l1llll1l_opy_ + str(platform_index)), bstack11lll111ll1_opy_, bstack11lll111lll_opy_)
        if not os.path.exists(bstack1l111111l11_opy_) or not os.path.isdir(bstack1l111111l11_opy_):
            self.logger.info(bstack1l11l1l_opy_ (u"ࠧࡔ࡯ࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡࡨࡲࡹࡳࡪࠠࡢࡶ࠽ࠤࢀࢃࠢᗥ").format(bstack1l111111l11_opy_))
        else:
            self.logger.info(bstack1l11l1l_opy_ (u"ࠨࡐࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡧࡴࡲࡱࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹ࠻ࠢࡾࢁࠧᗦ").format(bstack1l111111l11_opy_))
            with os.scandir(bstack1l111111l11_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l1l11lll1l_opy_:
                        self.logger.info(bstack1l11l1l_opy_ (u"ࠢࡑࡣࡷ࡬ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡾࢁࠧᗧ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1l11l1l_opy_ (u"ࠣࠤᗨ")
                        log_entry = bstack1ll1lll1ll1_opy_(
                            kind=bstack1l11l1l_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦᗩ"),
                            message=bstack1l11l1l_opy_ (u"ࠥࠦᗪ"),
                            level=bstack1l11l1l_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣᗫ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l1ll11111l_opy_=entry.stat().st_size,
                            bstack1l1l1l11111_opy_=bstack1l11l1l_opy_ (u"ࠧࡓࡁࡏࡗࡄࡐࡤ࡛ࡐࡍࡑࡄࡈࠧᗬ"),
                            bstack11ll_opy_=os.path.abspath(entry.path),
                            bstack1l1l111l1l1_opy_=hook.get(TestFramework.bstack1l1111ll1ll_opy_)
                        )
                        logs.append(log_entry)
                        _1l1l11lll1l_opy_.add(abs_path)
        hook[bstack1l11l1l_opy_ (u"ࠨ࡬ࡰࡩࡶࠦᗭ")] = logs
    def bstack1l1l11ll11l_opy_(
        self,
        bstack1l1l1lll1l1_opy_: bstack1lll1l1111l_opy_,
        entries: List[bstack1ll1lll1ll1_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1l11l1l_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡆࡎࡔ࡟ࡔࡇࡖࡗࡎࡕࡎࡠࡋࡇࠦᗮ"))
        req.platform_index = TestFramework.bstack1lll1llll11_opy_(bstack1l1l1lll1l1_opy_, TestFramework.bstack1l1llllll1l_opy_)
        req.execution_context.hash = str(bstack1l1l1lll1l1_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1l1lll1l1_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1l1lll1l1_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1lll1llll11_opy_(bstack1l1l1lll1l1_opy_, TestFramework.bstack1ll111l1l1l_opy_)
            log_entry.test_framework_version = TestFramework.bstack1lll1llll11_opy_(bstack1l1l1lll1l1_opy_, TestFramework.bstack1l1l11l111l_opy_)
            log_entry.uuid = entry.bstack11lll1ll11l_opy_
            log_entry.test_framework_state = bstack1l1l1lll1l1_opy_.state.name
            log_entry.message = entry.message.encode(bstack1l11l1l_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢᗯ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack1l11l1l_opy_ (u"ࠤࠥᗰ")
            if entry.kind == bstack1l11l1l_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧᗱ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1ll11111l_opy_
                log_entry.file_path = entry.bstack11ll_opy_
        def bstack1l1l11lllll_opy_():
            bstack11l11llll1_opy_ = datetime.now()
            try:
                self.bstack1lll1l11ll1_opy_.LogCreatedEvent(req)
                bstack1l1l1lll1l1_opy_.bstack1lll11lll_opy_(bstack1l11l1l_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠣᗲ"), datetime.now() - bstack11l11llll1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1l11l1l_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡࡽࢀࠦᗳ").format(str(e)))
                traceback.print_exc()
        self.bstack1lllll1l111_opy_.enqueue(bstack1l1l11lllll_opy_)
    def __1l11111l1l1_opy_(self, instance) -> None:
        bstack1l11l1l_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡐࡴࡧࡤࡴࠢࡦࡹࡸࡺ࡯࡮ࠢࡷࡥ࡬ࡹࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡩ࡬ࡺࡪࡴࠠࡵࡧࡶࡸࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡉࡲࡦࡣࡷࡩࡸࠦࡡࠡࡦ࡬ࡧࡹࠦࡣࡰࡰࡷࡥ࡮ࡴࡩ࡯ࡩࠣࡸࡪࡹࡴࠡ࡮ࡨࡺࡪࡲࠠࡤࡷࡶࡸࡴࡳࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡵࡩࡹࡸࡩࡦࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡈࡻࡳࡵࡱࡰࡘࡦ࡭ࡍࡢࡰࡤ࡫ࡪࡸࠠࡢࡰࡧࠤࡺࡶࡤࡢࡶࡨࡷࠥࡺࡨࡦࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤࡸࡺࡡࡵࡧࠣࡹࡸ࡯࡮ࡨࠢࡶࡩࡹࡥࡳࡵࡣࡷࡩࡤ࡫࡮ࡵࡴ࡬ࡩࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᗴ")
        bstack1l111111lll_opy_ = {bstack1l11l1l_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳ࡟࡮ࡧࡷࡥࡩࡧࡴࡢࠤᗵ"): bstack1lll11l1111_opy_.bstack11lll1lllll_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack1l1111l1lll_opy_(instance, bstack1l111111lll_opy_)
    @staticmethod
    def bstack1l111111ll1_opy_(instance: bstack1lll1l1111l_opy_, bstack11lll1lll1l_opy_: str):
        bstack11lll1l1lll_opy_ = (
            bstack1ll11lll11l_opy_.bstack11lllll1111_opy_
            if bstack11lll1lll1l_opy_ == bstack1ll11lll11l_opy_.bstack11lll1l11l1_opy_
            else bstack1ll11lll11l_opy_.bstack11lllll11l1_opy_
        )
        bstack11lllllllll_opy_ = TestFramework.bstack1lll1llll11_opy_(instance, bstack11lll1lll1l_opy_, None)
        bstack1l11111l111_opy_ = TestFramework.bstack1lll1llll11_opy_(instance, bstack11lll1l1lll_opy_, None) if bstack11lllllllll_opy_ else None
        return (
            bstack1l11111l111_opy_[bstack11lllllllll_opy_][-1]
            if isinstance(bstack1l11111l111_opy_, dict) and len(bstack1l11111l111_opy_.get(bstack11lllllllll_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack11lll1l111l_opy_(instance: bstack1lll1l1111l_opy_, bstack11lll1lll1l_opy_: str):
        hook = bstack1ll11lll11l_opy_.bstack1l111111ll1_opy_(instance, bstack11lll1lll1l_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack11llllll1l1_opy_, []).clear()
    @staticmethod
    def __11llll1111l_opy_(instance: bstack1lll1l1111l_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1l11l1l_opy_ (u"ࠣࡩࡨࡸࡤࡸࡥࡤࡱࡵࡨࡸࠨᗶ"), None)):
            return
        if os.getenv(bstack1l11l1l_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡊࡑࡇࡇࡠࡎࡒࡋࡘࠨᗷ"), bstack1l11l1l_opy_ (u"ࠥ࠵ࠧᗸ")) != bstack1l11l1l_opy_ (u"ࠦ࠶ࠨᗹ"):
            bstack1ll11lll11l_opy_.logger.warning(bstack1l11l1l_opy_ (u"ࠧ࡯ࡧ࡯ࡱࡵ࡭ࡳ࡭ࠠࡤࡣࡳࡰࡴ࡭ࠢᗺ"))
            return
        bstack11lll11ll11_opy_ = {
            bstack1l11l1l_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧᗻ"): (bstack1ll11lll11l_opy_.bstack11lll1ll111_opy_, bstack1ll11lll11l_opy_.bstack11lllll11l1_opy_),
            bstack1l11l1l_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤᗼ"): (bstack1ll11lll11l_opy_.bstack11lll1l11l1_opy_, bstack1ll11lll11l_opy_.bstack11lllll1111_opy_),
        }
        for when in (bstack1l11l1l_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢᗽ"), bstack1l11l1l_opy_ (u"ࠤࡦࡥࡱࡲࠢᗾ"), bstack1l11l1l_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧᗿ")):
            bstack1l11111l11l_opy_ = args[1].get_records(when)
            if not bstack1l11111l11l_opy_:
                continue
            records = [
                bstack1ll1lll1ll1_opy_(
                    kind=TestFramework.bstack1l1ll111ll1_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1l11l1l_opy_ (u"ࠦࡱ࡫ࡶࡦ࡮ࡱࡥࡲ࡫ࠢᘀ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1l11l1l_opy_ (u"ࠧࡩࡲࡦࡣࡷࡩࡩࠨᘁ")) and r.created
                        else None
                    ),
                )
                for r in bstack1l11111l11l_opy_
                if isinstance(getattr(r, bstack1l11l1l_opy_ (u"ࠨ࡭ࡦࡵࡶࡥ࡬࡫ࠢᘂ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack11lllll1l11_opy_, bstack11lll1l1lll_opy_ = bstack11lll11ll11_opy_.get(when, (None, None))
            bstack11llll111ll_opy_ = TestFramework.bstack1lll1llll11_opy_(instance, bstack11lllll1l11_opy_, None) if bstack11lllll1l11_opy_ else None
            bstack1l11111l111_opy_ = TestFramework.bstack1lll1llll11_opy_(instance, bstack11lll1l1lll_opy_, None) if bstack11llll111ll_opy_ else None
            if isinstance(bstack1l11111l111_opy_, dict) and len(bstack1l11111l111_opy_.get(bstack11llll111ll_opy_, [])) > 0:
                hook = bstack1l11111l111_opy_[bstack11llll111ll_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack11llllll1l1_opy_ in hook:
                    hook[TestFramework.bstack11llllll1l1_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1lll1llll11_opy_(instance, TestFramework.bstack11llll11l1l_opy_, [])
            logs.extend(records)
    @staticmethod
    def __11llllllll1_opy_(test) -> Dict[str, Any]:
        bstack11ll11lll_opy_ = bstack1ll11lll11l_opy_.__1l11111lll1_opy_(test.location) if hasattr(test, bstack1l11l1l_opy_ (u"ࠢ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠤᘃ")) else getattr(test, bstack1l11l1l_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᘄ"), None)
        test_name = test.name if hasattr(test, bstack1l11l1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᘅ")) else None
        bstack1l11111ll1l_opy_ = test.fspath.strpath if hasattr(test, bstack1l11l1l_opy_ (u"ࠥࡪࡸࡶࡡࡵࡪࠥᘆ")) and test.fspath else None
        if not bstack11ll11lll_opy_ or not test_name or not bstack1l11111ll1l_opy_:
            return None
        code = None
        if hasattr(test, bstack1l11l1l_opy_ (u"ࠦࡴࡨࡪࠣᘇ")):
            try:
                import inspect
                code = inspect.getsource(test.obj)
            except:
                pass
        bstack11lll11l111_opy_ = []
        try:
            bstack11lll11l111_opy_ = bstack1l1l1lllll_opy_.bstack1111lll1l1_opy_(test)
        except:
            bstack1ll11lll11l_opy_.logger.warning(bstack1l11l1l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡨ࡬ࡲࡩࠦࡴࡦࡵࡷࠤࡸࡩ࡯ࡱࡧࡶ࠰ࠥࡺࡥࡴࡶࠣࡷࡨࡵࡰࡦࡵࠣࡻ࡮ࡲ࡬ࠡࡤࡨࠤࡷ࡫ࡳࡰ࡮ࡹࡩࡩࠦࡩ࡯ࠢࡆࡐࡎࠨᘈ"))
        return {
            TestFramework.bstack1ll111111l1_opy_: uuid4().__str__(),
            TestFramework.bstack11lll1lll11_opy_: bstack11ll11lll_opy_,
            TestFramework.bstack1l1lllll1ll_opy_: test_name,
            TestFramework.bstack1l11lll1lll_opy_: getattr(test, bstack1l11l1l_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᘉ"), None),
            TestFramework.bstack1l1111l1l11_opy_: bstack1l11111ll1l_opy_,
            TestFramework.bstack11llll11111_opy_: bstack1ll11lll11l_opy_.__11llll1ll1l_opy_(test),
            TestFramework.bstack11lll11lll1_opy_: code,
            TestFramework.bstack1l11l1l111l_opy_: TestFramework.bstack11llll11l11_opy_,
            TestFramework.bstack1l111ll11ll_opy_: bstack11ll11lll_opy_,
            TestFramework.bstack11lll11l1l1_opy_: bstack11lll11l111_opy_
        }
    @staticmethod
    def __11llll1ll1l_opy_(test) -> List[str]:
        markers = []
        current = test
        while current:
            own_markers = getattr(current, bstack1l11l1l_opy_ (u"ࠢࡰࡹࡱࡣࡲࡧࡲ࡬ࡧࡵࡷࠧᘊ"), [])
            markers.extend([getattr(m, bstack1l11l1l_opy_ (u"ࠣࡰࡤࡱࡪࠨᘋ"), None) for m in own_markers if getattr(m, bstack1l11l1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᘌ"), None)])
            current = getattr(current, bstack1l11l1l_opy_ (u"ࠥࡴࡦࡸࡥ࡯ࡶࠥᘍ"), None)
        return markers
    @staticmethod
    def __1l11111lll1_opy_(location):
        return bstack1l11l1l_opy_ (u"ࠦ࠿ࡀࠢᘎ").join(filter(lambda x: isinstance(x, str), location))