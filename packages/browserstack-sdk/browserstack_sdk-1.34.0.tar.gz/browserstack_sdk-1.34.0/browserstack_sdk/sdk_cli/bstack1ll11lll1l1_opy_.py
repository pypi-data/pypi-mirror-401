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
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1llll111l11_opy_ import bstack1llll1l1l1l_opy_
from browserstack_sdk.sdk_cli.utils.bstack11lll1l1l_opy_ import bstack11lllllll11_opy_
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1ll1lll1111_opy_,
    bstack1ll1llllll1_opy_,
    bstack1lll11ll1l1_opy_,
    bstack1l11111l1l1_opy_,
    bstack1ll11ll111l_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack1l1l1lll1ll_opy_
from bstack_utils.bstack11lll1l1ll_opy_ import bstack1ll11ll1ll1_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack1llll1llll1_opy_ import bstack1llll1lllll_opy_
from browserstack_sdk.sdk_cli.utils.bstack1ll1llll11l_opy_ import bstack1lll111llll_opy_
from bstack_utils.bstack111l1ll11l_opy_ import bstack11ll11l11_opy_
bstack1l11lllll11_opy_ = bstack1l1l1lll1ll_opy_()
bstack11lll1ll1l1_opy_ = 1.0
bstack1l1l1l1l111_opy_ = bstack1l111l1_opy_ (u"ࠤࡘࡴࡱࡵࡡࡥࡧࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠮ࠤᖕ")
bstack11ll1llll11_opy_ = bstack1l111l1_opy_ (u"ࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨᖖ")
bstack11lll11111l_opy_ = bstack1l111l1_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣᖗ")
bstack11ll1llll1l_opy_ = bstack1l111l1_opy_ (u"ࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠣᖘ")
bstack11lll111111_opy_ = bstack1l111l1_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠧᖙ")
_1l1l1lll1l1_opy_ = set()
class bstack1lll11l11ll_opy_(TestFramework):
    bstack11llll1llll_opy_ = bstack1l111l1_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࡹࠢᖚ")
    bstack1l1111111l1_opy_ = bstack1l111l1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࡤࡹࡴࡢࡴࡷࡩࡩࠨᖛ")
    bstack11lllll11l1_opy_ = bstack1l111l1_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤࠣᖜ")
    bstack11llllll111_opy_ = bstack1l111l1_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥ࡬ࡢࡵࡷࡣࡸࡺࡡࡳࡶࡨࡨࠧᖝ")
    bstack11llll11lll_opy_ = bstack1l111l1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟࡭ࡣࡶࡸࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࠢᖞ")
    bstack11lllll111l_opy_: bool
    bstack1llll1llll1_opy_: bstack1llll1lllll_opy_  = None
    bstack1lll11l1l1l_opy_ = None
    bstack1l111111ll1_opy_ = [
        bstack1ll1lll1111_opy_.BEFORE_ALL,
        bstack1ll1lll1111_opy_.AFTER_ALL,
        bstack1ll1lll1111_opy_.BEFORE_EACH,
        bstack1ll1lll1111_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack11lll111l11_opy_: Dict[str, str],
        bstack1l1lll111l1_opy_: List[str]=[bstack1l111l1_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࠧᖟ")],
        bstack1llll1llll1_opy_: bstack1llll1lllll_opy_=None,
        bstack1lll11l1l1l_opy_=None
    ):
        super().__init__(bstack1l1lll111l1_opy_, bstack11lll111l11_opy_, bstack1llll1llll1_opy_)
        self.bstack11lllll111l_opy_ = any(bstack1l111l1_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࠨᖠ") in item.lower() for item in bstack1l1lll111l1_opy_)
        self.bstack1lll11l1l1l_opy_ = bstack1lll11l1l1l_opy_
    def track_event(
        self,
        context: bstack1l11111l1l1_opy_,
        test_framework_state: bstack1ll1lll1111_opy_,
        test_hook_state: bstack1lll11ll1l1_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack1ll1lll1111_opy_.TEST or test_framework_state in bstack1lll11l11ll_opy_.bstack1l111111ll1_opy_:
            bstack11lllllll11_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1ll1lll1111_opy_.NONE:
            self.logger.warning(bstack1l111l1_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡫ࡤࠡࡥࡤࡰࡱࡨࡡࡤ࡭ࠣࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁࠥࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫࠽ࠣᖡ") + str(test_hook_state) + bstack1l111l1_opy_ (u"ࠣࠤᖢ"))
            return
        if not self.bstack11lllll111l_opy_:
            self.logger.warning(bstack1l111l1_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱࡷࡺࡶࡰࡰࡴࡷࡩࡩࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠿ࠥᖣ") + str(str(self.bstack1l1lll111l1_opy_)) + bstack1l111l1_opy_ (u"ࠥࠦᖤ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1l111l1_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡫ࡸࡱࡧࡦࡸࡪࡪࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᖥ") + str(kwargs) + bstack1l111l1_opy_ (u"ࠧࠨᖦ"))
            return
        instance = self.__11llll1111l_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1l111l1_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡡࡳࡩࡶࡁࠧᖧ") + str(args) + bstack1l111l1_opy_ (u"ࠢࠣᖨ"))
            return
        try:
            if instance!= None and test_framework_state in bstack1lll11l11ll_opy_.bstack1l111111ll1_opy_ and test_hook_state == bstack1lll11ll1l1_opy_.PRE:
                bstack1ll111ll11l_opy_ = bstack1ll11ll1ll1_opy_.bstack1ll1111l1l1_opy_(EVENTS.bstack11l11ll1l1_opy_.value)
                name = str(EVENTS.bstack11l11ll1l1_opy_.name)+bstack1l111l1_opy_ (u"ࠣ࠼ࠥᖩ")+str(test_framework_state.name)
                TestFramework.bstack11llll1l111_opy_(instance, name, bstack1ll111ll11l_opy_)
        except Exception as e:
            self.logger.debug(bstack1l111l1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡲࡳࡰࠦࡥࡳࡴࡲࡶࠥࡶࡲࡦ࠼ࠣࡿࢂࠨᖪ").format(e))
        try:
            if not TestFramework.bstack1lll1ll111l_opy_(instance, TestFramework.bstack11lll1l1111_opy_) and test_hook_state == bstack1lll11ll1l1_opy_.PRE:
                test = bstack1lll11l11ll_opy_.__1l11111ll11_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack1l111l1_opy_ (u"ࠥࡰࡴࡧࡤࡦࡦࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥᖫ") + str(test_hook_state) + bstack1l111l1_opy_ (u"ࠦࠧᖬ"))
            if test_framework_state == bstack1ll1lll1111_opy_.TEST:
                if test_hook_state == bstack1lll11ll1l1_opy_.PRE and not TestFramework.bstack1lll1ll111l_opy_(instance, TestFramework.bstack1l1l1l1lll1_opy_):
                    TestFramework.bstack1llll1111l1_opy_(instance, TestFramework.bstack1l1l1l1lll1_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1l111l1_opy_ (u"ࠧࡹࡥࡵࠢࡷࡩࡸࡺ࠭ࡴࡶࡤࡶࡹࠦࡦࡰࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥᖭ") + str(test_hook_state) + bstack1l111l1_opy_ (u"ࠨࠢᖮ"))
                elif test_hook_state == bstack1lll11ll1l1_opy_.POST and not TestFramework.bstack1lll1ll111l_opy_(instance, TestFramework.bstack1l1l1llll11_opy_):
                    TestFramework.bstack1llll1111l1_opy_(instance, TestFramework.bstack1l1l1llll11_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1l111l1_opy_ (u"ࠢࡴࡧࡷࠤࡹ࡫ࡳࡵ࠯ࡨࡲࡩࠦࡦࡰࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥᖯ") + str(test_hook_state) + bstack1l111l1_opy_ (u"ࠣࠤᖰ"))
            elif test_framework_state == bstack1ll1lll1111_opy_.LOG and test_hook_state == bstack1lll11ll1l1_opy_.POST:
                bstack1lll11l11ll_opy_.__11lllllllll_opy_(instance, *args)
            elif test_framework_state == bstack1ll1lll1111_opy_.LOG_REPORT and test_hook_state == bstack1lll11ll1l1_opy_.POST:
                self.__11lll1ll11l_opy_(instance, *args)
                self.__11lll111l1l_opy_(instance)
            elif test_framework_state in bstack1lll11l11ll_opy_.bstack1l111111ll1_opy_:
                self.__11llll1l1l1_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1l111l1_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥᖱ") + str(instance.ref()) + bstack1l111l1_opy_ (u"ࠥࠦᖲ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1l11111l1ll_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in bstack1lll11l11ll_opy_.bstack1l111111ll1_opy_ and test_hook_state == bstack1lll11ll1l1_opy_.POST:
                name = str(EVENTS.bstack11l11ll1l1_opy_.name)+bstack1l111l1_opy_ (u"ࠦ࠿ࠨᖳ")+str(test_framework_state.name)
                bstack1ll111ll11l_opy_ = TestFramework.bstack11llll1ll1l_opy_(instance, name)
                bstack1ll11ll1ll1_opy_.end(EVENTS.bstack11l11ll1l1_opy_.value, bstack1ll111ll11l_opy_+bstack1l111l1_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᖴ"), bstack1ll111ll11l_opy_+bstack1l111l1_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᖵ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1l111l1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡰࡱ࡮ࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢᖶ").format(e))
    def bstack1l1l1l11lll_opy_(self):
        return self.bstack11lllll111l_opy_
    def __11llll1lll1_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1l111l1_opy_ (u"ࠣࡩࡨࡸࡤࡸࡥࡴࡷ࡯ࡸࠧᖷ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l1l11ll11l_opy_(rep, [bstack1l111l1_opy_ (u"ࠤࡺ࡬ࡪࡴࠢᖸ"), bstack1l111l1_opy_ (u"ࠥࡳࡺࡺࡣࡰ࡯ࡨࠦᖹ"), bstack1l111l1_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦᖺ"), bstack1l111l1_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧᖻ"), bstack1l111l1_opy_ (u"ࠨࡳ࡬࡫ࡳࡴࡪࡪࠢᖼ"), bstack1l111l1_opy_ (u"ࠢ࡭ࡱࡱ࡫ࡷ࡫ࡰࡳࡶࡨࡼࡹࠨᖽ")])
        return None
    def __11lll1ll11l_opy_(self, instance: bstack1ll1llllll1_opy_, *args):
        result = self.__11llll1lll1_opy_(*args)
        if not result:
            return
        failure = None
        bstack1lllll111ll_opy_ = None
        if result.get(bstack1l111l1_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤᖾ"), None) == bstack1l111l1_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤᖿ") and len(args) > 1 and getattr(args[1], bstack1l111l1_opy_ (u"ࠥࡩࡽࡩࡩ࡯ࡨࡲࠦᗀ"), None) is not None:
            failure = [{bstack1l111l1_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧᗁ"): [args[1].excinfo.exconly(), result.get(bstack1l111l1_opy_ (u"ࠧࡲ࡯࡯ࡩࡵࡩࡵࡸࡴࡦࡺࡷࠦᗂ"), None)]}]
            bstack1lllll111ll_opy_ = bstack1l111l1_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢᗃ") if bstack1l111l1_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࠥᗄ") in getattr(args[1].excinfo, bstack1l111l1_opy_ (u"ࠣࡶࡼࡴࡪࡴࡡ࡮ࡧࠥᗅ"), bstack1l111l1_opy_ (u"ࠤࠥᗆ")) else bstack1l111l1_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦᗇ")
        bstack11lll1lllll_opy_ = result.get(bstack1l111l1_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧᗈ"), TestFramework.bstack11lll1lll11_opy_)
        if bstack11lll1lllll_opy_ != TestFramework.bstack11lll1lll11_opy_:
            TestFramework.bstack1llll1111l1_opy_(instance, TestFramework.bstack1l1l11lll1l_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack11lll111ll1_opy_(instance, {
            TestFramework.bstack1l11l11llll_opy_: failure,
            TestFramework.bstack1l1111111ll_opy_: bstack1lllll111ll_opy_,
            TestFramework.bstack1l11l11l1l1_opy_: bstack11lll1lllll_opy_,
        })
    def __11llll1111l_opy_(
        self,
        context: bstack1l11111l1l1_opy_,
        test_framework_state: bstack1ll1lll1111_opy_,
        test_hook_state: bstack1lll11ll1l1_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack1ll1lll1111_opy_.SETUP_FIXTURE:
            instance = self.__11lll1l111l_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack11llll1ll11_opy_ bstack11lll11llll_opy_ this to be bstack1l111l1_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᗉ")
            if test_framework_state == bstack1ll1lll1111_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__1l1111l11ll_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1ll1lll1111_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack1l111l1_opy_ (u"ࠨ࡮ࡰࡦࡨࠦᗊ"), None), bstack1l111l1_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᗋ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1l111l1_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᗌ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1llll11ll1l_opy_(target) if target else None
        return instance
    def __11llll1l1l1_opy_(
        self,
        instance: bstack1ll1llllll1_opy_,
        test_framework_state: bstack1ll1lll1111_opy_,
        test_hook_state: bstack1lll11ll1l1_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack1l111111l11_opy_ = TestFramework.bstack1llll1l111l_opy_(instance, bstack1lll11l11ll_opy_.bstack1l1111111l1_opy_, {})
        if not key in bstack1l111111l11_opy_:
            bstack1l111111l11_opy_[key] = []
        bstack11lll111lll_opy_ = TestFramework.bstack1llll1l111l_opy_(instance, bstack1lll11l11ll_opy_.bstack11lllll11l1_opy_, {})
        if not key in bstack11lll111lll_opy_:
            bstack11lll111lll_opy_[key] = []
        bstack1l11111llll_opy_ = {
            bstack1lll11l11ll_opy_.bstack1l1111111l1_opy_: bstack1l111111l11_opy_,
            bstack1lll11l11ll_opy_.bstack11lllll11l1_opy_: bstack11lll111lll_opy_,
        }
        if test_hook_state == bstack1lll11ll1l1_opy_.PRE:
            hook = {
                bstack1l111l1_opy_ (u"ࠤ࡮ࡩࡾࠨᗍ"): key,
                TestFramework.bstack1l11111111l_opy_: uuid4().__str__(),
                TestFramework.bstack11lllll1lll_opy_: TestFramework.bstack11lllll1111_opy_,
                TestFramework.bstack11llll111ll_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack11lll1l11ll_opy_: [],
                TestFramework.bstack11lll1111ll_opy_: args[1] if len(args) > 1 else bstack1l111l1_opy_ (u"ࠪࠫᗎ"),
                TestFramework.bstack11lll11l11l_opy_: bstack1lll111llll_opy_.bstack11llll11l1l_opy_()
            }
            bstack1l111111l11_opy_[key].append(hook)
            bstack1l11111llll_opy_[bstack1lll11l11ll_opy_.bstack11llllll111_opy_] = key
        elif test_hook_state == bstack1lll11ll1l1_opy_.POST:
            bstack11llllll11l_opy_ = bstack1l111111l11_opy_.get(key, [])
            hook = bstack11llllll11l_opy_.pop() if bstack11llllll11l_opy_ else None
            if hook:
                result = self.__11llll1lll1_opy_(*args)
                if result:
                    bstack11lllllll1l_opy_ = result.get(bstack1l111l1_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧᗏ"), TestFramework.bstack11lllll1111_opy_)
                    if bstack11lllllll1l_opy_ != TestFramework.bstack11lllll1111_opy_:
                        hook[TestFramework.bstack11lllll1lll_opy_] = bstack11lllllll1l_opy_
                hook[TestFramework.bstack11lll1111l1_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack11lll11l11l_opy_]= bstack1lll111llll_opy_.bstack11llll11l1l_opy_()
                self.bstack11lll11ll1l_opy_(hook)
                logs = hook.get(TestFramework.bstack1l11111ll1l_opy_, [])
                if logs: self.bstack1l1l11ll1ll_opy_(instance, logs)
                bstack11lll111lll_opy_[key].append(hook)
                bstack1l11111llll_opy_[bstack1lll11l11ll_opy_.bstack11llll11lll_opy_] = key
        TestFramework.bstack11lll111ll1_opy_(instance, bstack1l11111llll_opy_)
        self.logger.debug(bstack1l111l1_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡭ࡵ࡯࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࡱࡥࡺࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡩࡱࡲ࡯ࡸࡥࡳࡵࡣࡵࡸࡪࡪ࠽ࡼࡪࡲࡳࡰࡹ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡾࠢ࡫ࡳࡴࡱࡳࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡀࠦᗐ") + str(bstack11lll111lll_opy_) + bstack1l111l1_opy_ (u"ࠨࠢᗑ"))
    def __11lll1l111l_opy_(
        self,
        context: bstack1l11111l1l1_opy_,
        test_framework_state: bstack1ll1lll1111_opy_,
        test_hook_state: bstack1lll11ll1l1_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l1l11ll11l_opy_(args[0], [bstack1l111l1_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨᗒ"), bstack1l111l1_opy_ (u"ࠣࡣࡵ࡫ࡳࡧ࡭ࡦࠤᗓ"), bstack1l111l1_opy_ (u"ࠤࡳࡥࡷࡧ࡭ࡴࠤᗔ"), bstack1l111l1_opy_ (u"ࠥ࡭ࡩࡹࠢᗕ"), bstack1l111l1_opy_ (u"ࠦࡺࡴࡩࡵࡶࡨࡷࡹࠨᗖ"), bstack1l111l1_opy_ (u"ࠧࡨࡡࡴࡧ࡬ࡨࠧᗗ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scope = request.scope if hasattr(request, bstack1l111l1_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧᗘ")) else fixturedef.get(bstack1l111l1_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨᗙ"), None)
        fixturename = request.fixturename if hasattr(request, bstack1l111l1_opy_ (u"ࠣࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࠨᗚ")) else None
        node = request.node if hasattr(request, bstack1l111l1_opy_ (u"ࠤࡱࡳࡩ࡫ࠢᗛ")) else None
        target = request.node.nodeid if hasattr(node, bstack1l111l1_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᗜ")) else None
        baseid = fixturedef.get(bstack1l111l1_opy_ (u"ࠦࡧࡧࡳࡦ࡫ࡧࠦᗝ"), None) or bstack1l111l1_opy_ (u"ࠧࠨᗞ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1l111l1_opy_ (u"ࠨ࡟ࡱࡻࡩࡹࡳࡩࡩࡵࡧࡰࠦᗟ")):
            target = bstack1lll11l11ll_opy_.__1l111111111_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1l111l1_opy_ (u"ࠢ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠤᗠ")) else None
            if target and not TestFramework.bstack1llll11ll1l_opy_(target):
                self.__1l1111l11ll_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1l111l1_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡧࡹࡩࡳࡺ࠺ࠡࡨࡤࡰࡱࡨࡡࡤ࡭ࠣࡸࡦࡸࡧࡦࡶࡀࡿࡹࡧࡲࡨࡧࡷࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࡿࠣࡲࡴࡪࡥ࠾ࡽࡱࡳࡩ࡫ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥᗡ") + str(test_hook_state) + bstack1l111l1_opy_ (u"ࠤࠥᗢ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack1l111l1_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡩ࡫ࡦ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡧࡩ࡫ࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡵࡣࡵ࡫ࡪࡺ࠽ࠣᗣ") + str(target) + bstack1l111l1_opy_ (u"ࠦࠧᗤ"))
            return None
        instance = TestFramework.bstack1llll11ll1l_opy_(target)
        if not instance:
            self.logger.warning(bstack1l111l1_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤࡧࡧࡳࡦ࡫ࡧࡁࢀࡨࡡࡴࡧ࡬ࡨࢂࠦࡴࡢࡴࡪࡩࡹࡃࠢᗥ") + str(target) + bstack1l111l1_opy_ (u"ࠨࠢᗦ"))
            return None
        bstack11llll11111_opy_ = TestFramework.bstack1llll1l111l_opy_(instance, bstack1lll11l11ll_opy_.bstack11llll1llll_opy_, {})
        if os.getenv(bstack1l111l1_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡈࡏࡅࡌࡥࡆࡊ࡚ࡗ࡙ࡗࡋࡓࠣᗧ"), bstack1l111l1_opy_ (u"ࠣ࠳ࠥᗨ")) == bstack1l111l1_opy_ (u"ࠤ࠴ࠦᗩ"):
            bstack11lll1l1l1l_opy_ = bstack1l111l1_opy_ (u"ࠥ࠾ࠧᗪ").join((scope, fixturename))
            bstack11lll11lll1_opy_ = datetime.now(tz=timezone.utc)
            bstack11lll11l111_opy_ = {
                bstack1l111l1_opy_ (u"ࠦࡰ࡫ࡹࠣᗫ"): bstack11lll1l1l1l_opy_,
                bstack1l111l1_opy_ (u"ࠧࡺࡡࡨࡵࠥᗬ"): bstack1lll11l11ll_opy_.__11lll1ll111_opy_(request.node),
                bstack1l111l1_opy_ (u"ࠨࡦࡪࡺࡷࡹࡷ࡫ࠢᗭ"): fixturedef,
                bstack1l111l1_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨᗮ"): scope,
                bstack1l111l1_opy_ (u"ࠣࡶࡼࡴࡪࠨᗯ"): None,
            }
            try:
                if test_hook_state == bstack1lll11ll1l1_opy_.POST and callable(getattr(args[-1], bstack1l111l1_opy_ (u"ࠤࡪࡩࡹࡥࡲࡦࡵࡸࡰࡹࠨᗰ"), None)):
                    bstack11lll11l111_opy_[bstack1l111l1_opy_ (u"ࠥࡸࡾࡶࡥࠣᗱ")] = TestFramework.bstack1l1l11111l1_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1lll11ll1l1_opy_.PRE:
                bstack11lll11l111_opy_[bstack1l111l1_opy_ (u"ࠦࡺࡻࡩࡥࠤᗲ")] = uuid4().__str__()
                bstack11lll11l111_opy_[bstack1lll11l11ll_opy_.bstack11llll111ll_opy_] = bstack11lll11lll1_opy_
            elif test_hook_state == bstack1lll11ll1l1_opy_.POST:
                bstack11lll11l111_opy_[bstack1lll11l11ll_opy_.bstack11lll1111l1_opy_] = bstack11lll11lll1_opy_
            if bstack11lll1l1l1l_opy_ in bstack11llll11111_opy_:
                bstack11llll11111_opy_[bstack11lll1l1l1l_opy_].update(bstack11lll11l111_opy_)
                self.logger.debug(bstack1l111l1_opy_ (u"ࠧࡻࡰࡥࡣࡷࡩࡩࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡂࠨᗳ") + str(bstack11llll11111_opy_[bstack11lll1l1l1l_opy_]) + bstack1l111l1_opy_ (u"ࠨࠢᗴ"))
            else:
                bstack11llll11111_opy_[bstack11lll1l1l1l_opy_] = bstack11lll11l111_opy_
                self.logger.debug(bstack1l111l1_opy_ (u"ࠢࡴࡣࡹࡩࡩࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡂࢁࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࢂࠦࡴࡳࡣࡦ࡯ࡪࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴ࠿ࠥᗵ") + str(len(bstack11llll11111_opy_)) + bstack1l111l1_opy_ (u"ࠣࠤᗶ"))
        TestFramework.bstack1llll1111l1_opy_(instance, bstack1lll11l11ll_opy_.bstack11llll1llll_opy_, bstack11llll11111_opy_)
        self.logger.debug(bstack1l111l1_opy_ (u"ࠤࡶࡥࡻ࡫ࡤࠡࡨ࡬ࡼࡹࡻࡲࡦࡵࡀࡿࡱ࡫࡮ࠩࡶࡵࡥࡨࡱࡥࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࡶ࠭ࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤᗷ") + str(instance.ref()) + bstack1l111l1_opy_ (u"ࠥࠦᗸ"))
        return instance
    def __1l1111l11ll_opy_(
        self,
        context: bstack1l11111l1l1_opy_,
        test_framework_state: bstack1ll1lll1111_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack1llll1l1l1l_opy_.create_context(target)
        ob = bstack1ll1llllll1_opy_(ctx, self.bstack1l1lll111l1_opy_, self.bstack11lll111l11_opy_, test_framework_state)
        TestFramework.bstack11lll111ll1_opy_(ob, {
            TestFramework.bstack1ll111ll111_opy_: context.test_framework_name,
            TestFramework.bstack1l1l1llllll_opy_: context.test_framework_version,
            TestFramework.bstack11lllll1l11_opy_: [],
            bstack1lll11l11ll_opy_.bstack11llll1llll_opy_: {},
            bstack1lll11l11ll_opy_.bstack11lllll11l1_opy_: {},
            bstack1lll11l11ll_opy_.bstack1l1111111l1_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1llll1111l1_opy_(ob, TestFramework.bstack11lll11l1ll_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1llll1111l1_opy_(ob, TestFramework.bstack1ll1111ll1l_opy_, context.platform_index)
        TestFramework.bstack1llll11llll_opy_[ctx.id] = ob
        self.logger.debug(bstack1l111l1_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥࡩࡴࡹ࠰࡬ࡨࡂࢁࡣࡵࡺ࠱࡭ࡩࢃࠠࡵࡣࡵ࡫ࡪࡺ࠽ࡼࡶࡤࡶ࡬࡫ࡴࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦࡵࡀࠦᗹ") + str(TestFramework.bstack1llll11llll_opy_.keys()) + bstack1l111l1_opy_ (u"ࠧࠨᗺ"))
        return ob
    def bstack1l1l1111111_opy_(self, instance: bstack1ll1llllll1_opy_, bstack1lll1ll1111_opy_: Tuple[bstack1ll1lll1111_opy_, bstack1lll11ll1l1_opy_]):
        bstack1l11111l111_opy_ = (
            bstack1lll11l11ll_opy_.bstack11llllll111_opy_
            if bstack1lll1ll1111_opy_[1] == bstack1lll11ll1l1_opy_.PRE
            else bstack1lll11l11ll_opy_.bstack11llll11lll_opy_
        )
        hook = bstack1lll11l11ll_opy_.bstack11lll11ll11_opy_(instance, bstack1l11111l111_opy_)
        entries = hook.get(TestFramework.bstack11lll1l11ll_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1llll1l111l_opy_(instance, TestFramework.bstack11lllll1l11_opy_, []))
        return entries
    def bstack1l1l1ll1l1l_opy_(self, instance: bstack1ll1llllll1_opy_, bstack1lll1ll1111_opy_: Tuple[bstack1ll1lll1111_opy_, bstack1lll11ll1l1_opy_]):
        bstack1l11111l111_opy_ = (
            bstack1lll11l11ll_opy_.bstack11llllll111_opy_
            if bstack1lll1ll1111_opy_[1] == bstack1lll11ll1l1_opy_.PRE
            else bstack1lll11l11ll_opy_.bstack11llll11lll_opy_
        )
        bstack1lll11l11ll_opy_.bstack11lllll1l1l_opy_(instance, bstack1l11111l111_opy_)
        TestFramework.bstack1llll1l111l_opy_(instance, TestFramework.bstack11lllll1l11_opy_, []).clear()
    def bstack11lll11ll1l_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1l111l1_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡔࡷࡵࡣࡦࡵࡶࡩࡸࠦࡴࡩࡧࠣࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࡸ࡯࡭ࡪ࡮ࡤࡶࠥࡺ࡯ࠡࡶ࡫ࡩࠥࡐࡡࡷࡣࠣ࡭ࡲࡶ࡬ࡦ࡯ࡨࡲࡹࡧࡴࡪࡱࡱ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡔࡩ࡫ࡶࠤࡲ࡫ࡴࡩࡱࡧ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡇ࡭࡫ࡣ࡬ࡵࠣࡸ࡭࡫ࠠࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡩ࡯ࡵ࡬ࡨࡪࠦࡾ࠰࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠰ࡗࡳࡰࡴࡧࡤࡦࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡆࡰࡴࠣࡩࡦࡩࡨࠡࡨ࡬ࡰࡪࠦࡩ࡯ࠢ࡫ࡳࡴࡱ࡟࡭ࡧࡹࡩࡱࡥࡦࡪ࡮ࡨࡷ࠱ࠦࡲࡦࡲ࡯ࡥࡨ࡫ࡳࠡࠤࡗࡩࡸࡺࡌࡦࡸࡨࡰࠧࠦࡷࡪࡶ࡫ࠤࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠣࠢ࡬ࡲࠥ࡯ࡴࡴࠢࡳࡥࡹ࡮࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡉࡧࠢࡤࠤ࡫࡯࡬ࡦࠢ࡬ࡲࠥࡺࡨࡦࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡳࡡࡵࡥ࡫ࡩࡸࠦࡡࠡ࡯ࡲࡨ࡮࡬ࡩࡦࡦࠣ࡬ࡴࡵ࡫࠮࡮ࡨࡺࡪࡲࠠࡧ࡫࡯ࡩ࠱ࠦࡩࡵࠢࡦࡶࡪࡧࡴࡦࡵࠣࡥࠥࡒ࡯ࡨࡇࡱࡸࡷࡿࠠࡰࡤ࡭ࡩࡨࡺࠠࡸ࡫ࡷ࡬ࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡧࡩࡹࡧࡩ࡭ࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡖ࡭ࡲ࡯࡬ࡢࡴ࡯ࡽ࠱ࠦࡩࡵࠢࡳࡶࡴࡩࡥࡴࡵࡨࡷࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠ࡭ࡱࡦࡥࡹ࡫ࡤࠡ࡫ࡱࠤࡍࡵ࡯࡬ࡎࡨࡺࡪࡲ࠯ࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠦࡢࡺࠢࡵࡩࡵࡲࡡࡤ࡫ࡱ࡫ࠥࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥࠤࡼ࡯ࡴࡩࠢࠥࡌࡴࡵ࡫ࡍࡧࡹࡩࡱ࠵ࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠧ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱࡚ࠥࡨࡦࠢࡦࡶࡪࡧࡴࡦࡦࠣࡐࡴ࡭ࡅ࡯ࡶࡵࡽࠥࡵࡢ࡫ࡧࡦࡸࡸࠦࡡࡳࡧࠣࡥࡩࡪࡥࡥࠢࡷࡳࠥࡺࡨࡦࠢ࡫ࡳࡴࡱࠧࡴࠢࠥࡰࡴ࡭ࡳࠣࠢ࡯࡭ࡸࡺ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡨࡰࡱ࡮࠾࡚ࠥࡨࡦࠢࡨࡺࡪࡴࡴࠡࡦ࡬ࡧࡹ࡯࡯࡯ࡣࡵࡽࠥࡩ࡯࡯ࡶࡤ࡭ࡳ࡯࡮ࡨࠢࡨࡼ࡮ࡹࡴࡪࡰࡪࠤࡱࡵࡧࡴࠢࡤࡲࡩࠦࡨࡰࡱ࡮ࠤ࡮ࡴࡦࡰࡴࡰࡥࡹ࡯࡯࡯࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡪࡲࡳࡰࡥ࡬ࡦࡸࡨࡰࡤ࡬ࡩ࡭ࡧࡶ࠾ࠥࡒࡩࡴࡶࠣࡳ࡫ࠦࡐࡢࡶ࡫ࠤࡴࡨࡪࡦࡥࡷࡷࠥ࡬ࡲࡰ࡯ࠣࡸ࡭࡫ࠠࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠣࡱࡴࡴࡩࡵࡱࡵ࡭ࡳ࡭࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡢࡶ࡫࡯ࡨࡤࡲࡥࡷࡧ࡯ࡣ࡫࡯࡬ࡦࡵ࠽ࠤࡑ࡯ࡳࡵࠢࡲࡪࠥࡖࡡࡵࡪࠣࡳࡧࡰࡥࡤࡶࡶࠤ࡫ࡸ࡯࡮ࠢࡷ࡬ࡪࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠣࡱࡴࡴࡩࡵࡱࡵ࡭ࡳ࡭࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᗻ")
        global _1l1l1lll1l1_opy_
        platform_index = os.environ[bstack1l111l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᗼ")]
        bstack1l1l1ll1ll1_opy_ = os.path.join(bstack1l11lllll11_opy_, (bstack1l1l1l1l111_opy_ + str(platform_index)), bstack11ll1llll1l_opy_)
        if not os.path.exists(bstack1l1l1ll1ll1_opy_) or not os.path.isdir(bstack1l1l1ll1ll1_opy_):
            self.logger.debug(bstack1l111l1_opy_ (u"ࠣࡆ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡥࡹ࡫ࡶࡸࡸࠦࡴࡰࠢࡳࡶࡴࡩࡥࡴࡵࠣࡿࢂࠨᗽ").format(bstack1l1l1ll1ll1_opy_))
            return
        logs = hook.get(bstack1l111l1_opy_ (u"ࠤ࡯ࡳ࡬ࡹࠢᗾ"), [])
        with os.scandir(bstack1l1l1ll1ll1_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l1l1lll1l1_opy_:
                    self.logger.info(bstack1l111l1_opy_ (u"ࠥࡔࡦࡺࡨࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥࢁࡽࠣᗿ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1l111l1_opy_ (u"ࠦࠧᘀ")
                    log_entry = bstack1ll11ll111l_opy_(
                        kind=bstack1l111l1_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢᘁ"),
                        message=bstack1l111l1_opy_ (u"ࠨࠢᘂ"),
                        level=bstack1l111l1_opy_ (u"ࠢࠣᘃ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l1l111ll1l_opy_=entry.stat().st_size,
                        bstack1l1l1ll11ll_opy_=bstack1l111l1_opy_ (u"ࠣࡏࡄࡒ࡚ࡇࡌࡠࡗࡓࡐࡔࡇࡄࠣᘄ"),
                        bstack11lll_opy_=os.path.abspath(entry.path),
                        bstack11lll1l11l1_opy_=hook.get(TestFramework.bstack1l11111111l_opy_)
                    )
                    logs.append(log_entry)
                    _1l1l1lll1l1_opy_.add(abs_path)
        platform_index = os.environ[bstack1l111l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᘅ")]
        bstack1l1111l11l1_opy_ = os.path.join(bstack1l11lllll11_opy_, (bstack1l1l1l1l111_opy_ + str(platform_index)), bstack11ll1llll1l_opy_, bstack11lll111111_opy_)
        if not os.path.exists(bstack1l1111l11l1_opy_) or not os.path.isdir(bstack1l1111l11l1_opy_):
            self.logger.info(bstack1l111l1_opy_ (u"ࠥࡒࡴࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡦࡰࡷࡱࡨࠥࡧࡴ࠻ࠢࡾࢁࠧᘆ").format(bstack1l1111l11l1_opy_))
        else:
            self.logger.info(bstack1l111l1_opy_ (u"ࠦࡕࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥ࡬ࡲࡰ࡯ࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࡀࠠࡼࡿࠥᘇ").format(bstack1l1111l11l1_opy_))
            with os.scandir(bstack1l1111l11l1_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l1l1lll1l1_opy_:
                        self.logger.info(bstack1l111l1_opy_ (u"ࠧࡖࡡࡵࡪࠣࡥࡱࡸࡥࡢࡦࡼࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡼࡿࠥᘈ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1l111l1_opy_ (u"ࠨࠢᘉ")
                        log_entry = bstack1ll11ll111l_opy_(
                            kind=bstack1l111l1_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤᘊ"),
                            message=bstack1l111l1_opy_ (u"ࠣࠤᘋ"),
                            level=bstack1l111l1_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨᘌ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l1l111ll1l_opy_=entry.stat().st_size,
                            bstack1l1l1ll11ll_opy_=bstack1l111l1_opy_ (u"ࠥࡑࡆࡔࡕࡂࡎࡢ࡙ࡕࡒࡏࡂࡆࠥᘍ"),
                            bstack11lll_opy_=os.path.abspath(entry.path),
                            bstack1l1l11l11l1_opy_=hook.get(TestFramework.bstack1l11111111l_opy_)
                        )
                        logs.append(log_entry)
                        _1l1l1lll1l1_opy_.add(abs_path)
        hook[bstack1l111l1_opy_ (u"ࠦࡱࡵࡧࡴࠤᘎ")] = logs
    def bstack1l1l11ll1ll_opy_(
        self,
        bstack1l1l11l11ll_opy_: bstack1ll1llllll1_opy_,
        entries: List[bstack1ll11ll111l_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1l111l1_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡒࡉࡠࡄࡌࡒࡤ࡙ࡅࡔࡕࡌࡓࡓࡥࡉࡅࠤᘏ"))
        req.platform_index = TestFramework.bstack1llll1l111l_opy_(bstack1l1l11l11ll_opy_, TestFramework.bstack1ll1111ll1l_opy_)
        req.execution_context.hash = str(bstack1l1l11l11ll_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1l11l11ll_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1l11l11ll_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1llll1l111l_opy_(bstack1l1l11l11ll_opy_, TestFramework.bstack1ll111ll111_opy_)
            log_entry.test_framework_version = TestFramework.bstack1llll1l111l_opy_(bstack1l1l11l11ll_opy_, TestFramework.bstack1l1l1llllll_opy_)
            log_entry.uuid = entry.bstack11lll1l11l1_opy_
            log_entry.test_framework_state = bstack1l1l11l11ll_opy_.state.name
            log_entry.message = entry.message.encode(bstack1l111l1_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᘐ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack1l111l1_opy_ (u"ࠢࠣᘑ")
            if entry.kind == bstack1l111l1_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥᘒ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1l111ll1l_opy_
                log_entry.file_path = entry.bstack11lll_opy_
        def bstack1l1l11l1111_opy_():
            bstack1ll11llll_opy_ = datetime.now()
            try:
                self.bstack1lll11l1l1l_opy_.LogCreatedEvent(req)
                bstack1l1l11l11ll_opy_.bstack111lll11l_opy_(bstack1l111l1_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࡡࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠨᘓ"), datetime.now() - bstack1ll11llll_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1l111l1_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࡡࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡻࡾࠤᘔ").format(str(e)))
                traceback.print_exc()
        self.bstack1llll1llll1_opy_.enqueue(bstack1l1l11l1111_opy_)
    def __11lll111l1l_opy_(self, instance) -> None:
        bstack1l111l1_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡎࡲࡥࡩࡹࠠࡤࡷࡶࡸࡴࡳࠠࡵࡣࡪࡷࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡧࡪࡸࡨࡲࠥࡺࡥࡴࡶࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡇࡷ࡫ࡡࡵࡧࡶࠤࡦࠦࡤࡪࡥࡷࠤࡨࡵ࡮ࡵࡣ࡬ࡲ࡮ࡴࡧࠡࡶࡨࡷࡹࠦ࡬ࡦࡸࡨࡰࠥࡩࡵࡴࡶࡲࡱࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࡦࠣࡪࡷࡵ࡭ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆࡹࡸࡺ࡯࡮ࡖࡤ࡫ࡒࡧ࡮ࡢࡩࡨࡶࠥࡧ࡮ࡥࠢࡸࡴࡩࡧࡴࡦࡵࠣࡸ࡭࡫ࠠࡪࡰࡶࡸࡦࡴࡣࡦࠢࡶࡸࡦࡺࡥࠡࡷࡶ࡭ࡳ࡭ࠠࡴࡧࡷࡣࡸࡺࡡࡵࡧࡢࡩࡳࡺࡲࡪࡧࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᘕ")
        bstack1l11111llll_opy_ = {bstack1l111l1_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱࡤࡳࡥࡵࡣࡧࡥࡹࡧࠢᘖ"): bstack1lll111llll_opy_.bstack11llll11l1l_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack11lll111ll1_opy_(instance, bstack1l11111llll_opy_)
    @staticmethod
    def bstack11lll11ll11_opy_(instance: bstack1ll1llllll1_opy_, bstack1l11111l111_opy_: str):
        bstack11lll11l1l1_opy_ = (
            bstack1lll11l11ll_opy_.bstack11lllll11l1_opy_
            if bstack1l11111l111_opy_ == bstack1lll11l11ll_opy_.bstack11llll11lll_opy_
            else bstack1lll11l11ll_opy_.bstack1l1111111l1_opy_
        )
        bstack11llllllll1_opy_ = TestFramework.bstack1llll1l111l_opy_(instance, bstack1l11111l111_opy_, None)
        bstack1l1111l1111_opy_ = TestFramework.bstack1llll1l111l_opy_(instance, bstack11lll11l1l1_opy_, None) if bstack11llllllll1_opy_ else None
        return (
            bstack1l1111l1111_opy_[bstack11llllllll1_opy_][-1]
            if isinstance(bstack1l1111l1111_opy_, dict) and len(bstack1l1111l1111_opy_.get(bstack11llllllll1_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack11lllll1l1l_opy_(instance: bstack1ll1llllll1_opy_, bstack1l11111l111_opy_: str):
        hook = bstack1lll11l11ll_opy_.bstack11lll11ll11_opy_(instance, bstack1l11111l111_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack11lll1l11ll_opy_, []).clear()
    @staticmethod
    def __11lllllllll_opy_(instance: bstack1ll1llllll1_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1l111l1_opy_ (u"ࠨࡧࡦࡶࡢࡶࡪࡩ࡯ࡳࡦࡶࠦᘗ"), None)):
            return
        if os.getenv(bstack1l111l1_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡈࡏࡅࡌࡥࡌࡐࡉࡖࠦᘘ"), bstack1l111l1_opy_ (u"ࠣ࠳ࠥᘙ")) != bstack1l111l1_opy_ (u"ࠤ࠴ࠦᘚ"):
            bstack1lll11l11ll_opy_.logger.warning(bstack1l111l1_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳ࡫ࡱ࡫ࠥࡩࡡࡱ࡮ࡲ࡫ࠧᘛ"))
            return
        bstack11lll1l1ll1_opy_ = {
            bstack1l111l1_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥᘜ"): (bstack1lll11l11ll_opy_.bstack11llllll111_opy_, bstack1lll11l11ll_opy_.bstack1l1111111l1_opy_),
            bstack1l111l1_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢᘝ"): (bstack1lll11l11ll_opy_.bstack11llll11lll_opy_, bstack1lll11l11ll_opy_.bstack11lllll11l1_opy_),
        }
        for when in (bstack1l111l1_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧᘞ"), bstack1l111l1_opy_ (u"ࠢࡤࡣ࡯ࡰࠧᘟ"), bstack1l111l1_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥᘠ")):
            bstack11llll1l11l_opy_ = args[1].get_records(when)
            if not bstack11llll1l11l_opy_:
                continue
            records = [
                bstack1ll11ll111l_opy_(
                    kind=TestFramework.bstack1l1l111l111_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1l111l1_opy_ (u"ࠤ࡯ࡩࡻ࡫࡬࡯ࡣࡰࡩࠧᘡ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1l111l1_opy_ (u"ࠥࡧࡷ࡫ࡡࡵࡧࡧࠦᘢ")) and r.created
                        else None
                    ),
                )
                for r in bstack11llll1l11l_opy_
                if isinstance(getattr(r, bstack1l111l1_opy_ (u"ࠦࡲ࡫ࡳࡴࡣࡪࡩࠧᘣ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack1l11111lll1_opy_, bstack11lll11l1l1_opy_ = bstack11lll1l1ll1_opy_.get(when, (None, None))
            bstack11lll1ll1ll_opy_ = TestFramework.bstack1llll1l111l_opy_(instance, bstack1l11111lll1_opy_, None) if bstack1l11111lll1_opy_ else None
            bstack1l1111l1111_opy_ = TestFramework.bstack1llll1l111l_opy_(instance, bstack11lll11l1l1_opy_, None) if bstack11lll1ll1ll_opy_ else None
            if isinstance(bstack1l1111l1111_opy_, dict) and len(bstack1l1111l1111_opy_.get(bstack11lll1ll1ll_opy_, [])) > 0:
                hook = bstack1l1111l1111_opy_[bstack11lll1ll1ll_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack11lll1l11ll_opy_ in hook:
                    hook[TestFramework.bstack11lll1l11ll_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1llll1l111l_opy_(instance, TestFramework.bstack11lllll1l11_opy_, [])
            logs.extend(records)
    @staticmethod
    def __1l11111ll11_opy_(test) -> Dict[str, Any]:
        bstack1lll11ll_opy_ = bstack1lll11l11ll_opy_.__1l111111111_opy_(test.location) if hasattr(test, bstack1l111l1_opy_ (u"ࠧࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠢᘤ")) else getattr(test, bstack1l111l1_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᘥ"), None)
        test_name = test.name if hasattr(test, bstack1l111l1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᘦ")) else None
        bstack11lll1lll1l_opy_ = test.fspath.strpath if hasattr(test, bstack1l111l1_opy_ (u"ࠣࡨࡶࡴࡦࡺࡨࠣᘧ")) and test.fspath else None
        if not bstack1lll11ll_opy_ or not test_name or not bstack11lll1lll1l_opy_:
            return None
        code = None
        if hasattr(test, bstack1l111l1_opy_ (u"ࠤࡲࡦ࡯ࠨᘨ")):
            try:
                import inspect
                code = inspect.getsource(test.obj)
            except:
                pass
        bstack11ll1llllll_opy_ = []
        try:
            bstack11ll1llllll_opy_ = bstack11ll11l11_opy_.bstack1111ll11l1_opy_(test)
        except:
            bstack1lll11l11ll_opy_.logger.warning(bstack1l111l1_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪࡰࡧࠤࡹ࡫ࡳࡵࠢࡶࡧࡴࡶࡥࡴ࠮ࠣࡸࡪࡹࡴࠡࡵࡦࡳࡵ࡫ࡳࠡࡹ࡬ࡰࡱࠦࡢࡦࠢࡵࡩࡸࡵ࡬ࡷࡧࡧࠤ࡮ࡴࠠࡄࡎࡌࠦᘩ"))
        return {
            TestFramework.bstack1ll111l11l1_opy_: uuid4().__str__(),
            TestFramework.bstack11lll1l1111_opy_: bstack1lll11ll_opy_,
            TestFramework.bstack1l1llll111l_opy_: test_name,
            TestFramework.bstack1l11ll1ll11_opy_: getattr(test, bstack1l111l1_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᘪ"), None),
            TestFramework.bstack1l1111l111l_opy_: bstack11lll1lll1l_opy_,
            TestFramework.bstack1l111111lll_opy_: bstack1lll11l11ll_opy_.__11lll1ll111_opy_(test),
            TestFramework.bstack11llllll1l1_opy_: code,
            TestFramework.bstack1l11l11l1l1_opy_: TestFramework.bstack11lll1lll11_opy_,
            TestFramework.bstack1l111l111l1_opy_: bstack1lll11ll_opy_,
            TestFramework.bstack11ll1lllll1_opy_: bstack11ll1llllll_opy_
        }
    @staticmethod
    def __11lll1ll111_opy_(test) -> List[str]:
        markers = []
        current = test
        while current:
            own_markers = getattr(current, bstack1l111l1_opy_ (u"ࠧࡵࡷ࡯ࡡࡰࡥࡷࡱࡥࡳࡵࠥᘫ"), [])
            markers.extend([getattr(m, bstack1l111l1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᘬ"), None) for m in own_markers if getattr(m, bstack1l111l1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᘭ"), None)])
            current = getattr(current, bstack1l111l1_opy_ (u"ࠣࡲࡤࡶࡪࡴࡴࠣᘮ"), None)
        return markers
    @staticmethod
    def __1l111111111_opy_(location):
        return bstack1l111l1_opy_ (u"ࠤ࠽࠾ࠧᘯ").join(filter(lambda x: isinstance(x, str), location))