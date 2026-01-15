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
import json
import time
import os
import threading
import asyncio
from browserstack_sdk.sdk_cli.bstack1lll1ll1l11_opy_ import (
    bstack1lll1l1ll11_opy_,
    bstack1llll11l111_opy_,
    bstack1llll11l1ll_opy_,
    bstack1lll1llll11_opy_,
)
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l1l1l11l1l_opy_, bstack1lllllll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll11ll1ll_opy_ import bstack1ll11llll11_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll1lll1111_opy_, bstack1lll11ll1l1_opy_, bstack1ll1llllll1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1ll111_opy_ import bstack1ll1l1111l1_opy_
from browserstack_sdk.sdk_cli.bstack1l1ll11111l_opy_ import bstack1l1ll11l1ll_opy_
from typing import Tuple, List, Any
from bstack_utils.bstack1l1111ll_opy_ import bstack11l111llll_opy_, bstack11llll1ll_opy_, bstack11ll1lll11_opy_
from browserstack_sdk import sdk_pb2 as structs
class bstack1lll11l1ll1_opy_(bstack1l1ll11l1ll_opy_):
    bstack1l11l1l11l1_opy_ = bstack1l111l1_opy_ (u"ࠢࡵࡧࡶࡸࡤࡪࡲࡪࡸࡨࡶࡸࠨᏅ")
    bstack1l1l11l111l_opy_ = bstack1l111l1_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡹࠢᏆ")
    bstack1l11l11l1ll_opy_ = bstack1l111l1_opy_ (u"ࠤࡱࡳࡳࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡶࡩࡸࡹࡩࡰࡰࡶࠦᏇ")
    bstack1l11l11l11l_opy_ = bstack1l111l1_opy_ (u"ࠥࡸࡪࡹࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡵࠥᏈ")
    bstack1l11l1l1l11_opy_ = bstack1l111l1_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡢࡶࡪ࡬ࡳࠣᏉ")
    bstack1l1l1llll1l_opy_ = bstack1l111l1_opy_ (u"ࠧࡩࡢࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡧࡷ࡫ࡡࡵࡧࡧࠦᏊ")
    bstack1l11l1l11ll_opy_ = bstack1l111l1_opy_ (u"ࠨࡣࡣࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡳࡧ࡭ࡦࠤᏋ")
    bstack1l11l1l111l_opy_ = bstack1l111l1_opy_ (u"ࠢࡤࡤࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡹࡴࡢࡶࡸࡷࠧᏌ")
    def __init__(self):
        super().__init__(bstack1l1ll111lll_opy_=self.bstack1l11l1l11l1_opy_, frameworks=[bstack1ll11llll11_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1ll111l11ll_opy_((bstack1ll1lll1111_opy_.BEFORE_EACH, bstack1lll11ll1l1_opy_.POST), self.bstack1l11l111lll_opy_)
        if bstack1lllllll1_opy_():
            TestFramework.bstack1ll111l11ll_opy_((bstack1ll1lll1111_opy_.TEST, bstack1lll11ll1l1_opy_.POST), self.bstack1l1lll11lll_opy_)
        else:
            TestFramework.bstack1ll111l11ll_opy_((bstack1ll1lll1111_opy_.TEST, bstack1lll11ll1l1_opy_.PRE), self.bstack1l1lll11lll_opy_)
        TestFramework.bstack1ll111l11ll_opy_((bstack1ll1lll1111_opy_.TEST, bstack1lll11ll1l1_opy_.POST), self.bstack1l1ll1llll1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l11l111lll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1llllll1_opy_,
        bstack1lll1ll1111_opy_: Tuple[bstack1ll1lll1111_opy_, bstack1lll11ll1l1_opy_],
        *args,
        **kwargs,
    ):
        bstack1l11l11l111_opy_ = self.bstack1l11l1ll111_opy_(instance.context)
        if not bstack1l11l11l111_opy_:
            self.logger.debug(bstack1l111l1_opy_ (u"ࠣࡵࡨࡸࡤࡧࡣࡵ࡫ࡹࡩࡤࡶࡡࡨࡧ࠽ࠤࡳࡵࠠࡱࡣࡪࡩࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࠨᏍ") + str(bstack1lll1ll1111_opy_) + bstack1l111l1_opy_ (u"ࠤࠥᏎ"))
            return
        f.bstack1llll1111l1_opy_(instance, bstack1lll11l1ll1_opy_.bstack1l1l11l111l_opy_, bstack1l11l11l111_opy_)
    def bstack1l11l1ll111_opy_(self, context: bstack1lll1llll11_opy_, bstack1l11l11ll1l_opy_= True):
        if bstack1l11l11ll1l_opy_:
            bstack1l11l11l111_opy_ = self.bstack1l1ll1111l1_opy_(context, reverse=True)
        else:
            bstack1l11l11l111_opy_ = self.bstack1l1ll1111ll_opy_(context, reverse=True)
        return [f for f in bstack1l11l11l111_opy_ if f[1].state != bstack1lll1l1ll11_opy_.QUIT]
    def bstack1l1lll11lll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1llllll1_opy_,
        bstack1lll1ll1111_opy_: Tuple[bstack1ll1lll1111_opy_, bstack1lll11ll1l1_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11l111lll_opy_(f, instance, bstack1lll1ll1111_opy_, *args, **kwargs)
        if not bstack1l1l1l11l1l_opy_:
            self.logger.debug(bstack1l111l1_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᏏ") + str(kwargs) + bstack1l111l1_opy_ (u"ࠦࠧᏐ"))
            return
        bstack1l11l11l111_opy_ = f.bstack1llll1l111l_opy_(instance, bstack1lll11l1ll1_opy_.bstack1l1l11l111l_opy_, [])
        if not bstack1l11l11l111_opy_:
            self.logger.debug(bstack1l111l1_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᏑ") + str(kwargs) + bstack1l111l1_opy_ (u"ࠨࠢᏒ"))
            return
        if len(bstack1l11l11l111_opy_) > 1:
            self.logger.debug(
                bstack1ll1ll1111l_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡾࡰࡪࡴࠨࡱࡣࡪࡩࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳࠪࡿࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࡼ࡭ࡺࡥࡷ࡭ࡳࡾࠤᏓ"))
        bstack1l11l1l1l1l_opy_, bstack1l11lll1111_opy_ = bstack1l11l11l111_opy_[0]
        page = bstack1l11l1l1l1l_opy_()
        if not page:
            self.logger.debug(bstack1l111l1_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡰࡢࡩࡨࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᏔ") + str(kwargs) + bstack1l111l1_opy_ (u"ࠤࠥᏕ"))
            return
        bstack111l1l11_opy_ = getattr(args[0], bstack1l111l1_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᏖ"), None)
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1l111l1_opy_ (u"ࠦࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠤᏗ")).get(bstack1l111l1_opy_ (u"ࠧࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢᏘ")):
            try:
                page.evaluate(bstack1l111l1_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢᏙ"),
                            bstack1l111l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠫᏚ") + json.dumps(
                                bstack111l1l11_opy_) + bstack1l111l1_opy_ (u"ࠣࡿࢀࠦᏛ"))
            except Exception as e:
                self.logger.debug(bstack1l111l1_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤࢀࢃࠢᏜ"), e)
    def bstack1l1ll1llll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1llllll1_opy_,
        bstack1lll1ll1111_opy_: Tuple[bstack1ll1lll1111_opy_, bstack1lll11ll1l1_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11l111lll_opy_(f, instance, bstack1lll1ll1111_opy_, *args, **kwargs)
        if not bstack1l1l1l11l1l_opy_:
            self.logger.debug(bstack1l111l1_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᏝ") + str(kwargs) + bstack1l111l1_opy_ (u"ࠦࠧᏞ"))
            return
        bstack1l11l11l111_opy_ = f.bstack1llll1l111l_opy_(instance, bstack1lll11l1ll1_opy_.bstack1l1l11l111l_opy_, [])
        if not bstack1l11l11l111_opy_:
            self.logger.debug(bstack1l111l1_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᏟ") + str(kwargs) + bstack1l111l1_opy_ (u"ࠨࠢᏠ"))
            return
        if len(bstack1l11l11l111_opy_) > 1:
            self.logger.debug(
                bstack1ll1ll1111l_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡾࡰࡪࡴࠨࡱࡣࡪࡩࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳࠪࡿࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࡼ࡭ࡺࡥࡷ࡭ࡳࡾࠤᏡ"))
        bstack1l11l1l1l1l_opy_, bstack1l11lll1111_opy_ = bstack1l11l11l111_opy_[0]
        page = bstack1l11l1l1l1l_opy_()
        if not page:
            self.logger.debug(bstack1l111l1_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡰࡢࡩࡨࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᏢ") + str(kwargs) + bstack1l111l1_opy_ (u"ࠤࠥᏣ"))
            return
        status = f.bstack1llll1l111l_opy_(instance, TestFramework.bstack1l11l11l1l1_opy_, None)
        if not status:
            self.logger.debug(bstack1l111l1_opy_ (u"ࠥࡲࡴࠦࡳࡵࡣࡷࡹࡸࠦࡦࡰࡴࠣࡸࡪࡹࡴ࠭ࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࠨᏤ") + str(bstack1lll1ll1111_opy_) + bstack1l111l1_opy_ (u"ࠦࠧᏥ"))
            return
        bstack1l11l11lll1_opy_ = {bstack1l111l1_opy_ (u"ࠧࡹࡴࡢࡶࡸࡷࠧᏦ"): status.lower()}
        bstack1l11l1l1111_opy_ = f.bstack1llll1l111l_opy_(instance, TestFramework.bstack1l11l11llll_opy_, None)
        if status.lower() == bstack1l111l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭Ꮷ") and bstack1l11l1l1111_opy_ is not None:
            bstack1l11l11lll1_opy_[bstack1l111l1_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧᏨ")] = bstack1l11l1l1111_opy_[0][bstack1l111l1_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫᏩ")][0] if isinstance(bstack1l11l1l1111_opy_, list) else str(bstack1l11l1l1111_opy_)
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1l111l1_opy_ (u"ࠤࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠢᏪ")).get(bstack1l111l1_opy_ (u"ࠥࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢᏫ")):
            try:
                page.evaluate(
                        bstack1l111l1_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧᏬ"),
                        bstack1l111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࠪᏭ")
                        + json.dumps(bstack1l11l11lll1_opy_)
                        + bstack1l111l1_opy_ (u"ࠨࡽࠣᏮ")
                    )
            except Exception as e:
                self.logger.debug(bstack1l111l1_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤࢀࢃࠢᏯ"), e)
    def bstack1l1l1ll1111_opy_(
        self,
        instance: bstack1ll1llllll1_opy_,
        f: TestFramework,
        bstack1lll1ll1111_opy_: Tuple[bstack1ll1lll1111_opy_, bstack1lll11ll1l1_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11l111lll_opy_(f, instance, bstack1lll1ll1111_opy_, *args, **kwargs)
        if not bstack1l1l1l11l1l_opy_:
            self.logger.debug(
                bstack1ll1ll1111l_opy_ (u"ࠣ࡯ࡤࡶࡰࡥ࡯࠲࠳ࡼࡣࡸࡿ࡮ࡤ࠼ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠬࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࡼ࡭ࡺࡥࡷ࡭ࡳࡾࠤᏰ"))
            return
        bstack1l11l11l111_opy_ = f.bstack1llll1l111l_opy_(instance, bstack1lll11l1ll1_opy_.bstack1l1l11l111l_opy_, [])
        if not bstack1l11l11l111_opy_:
            self.logger.debug(bstack1l111l1_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᏱ") + str(kwargs) + bstack1l111l1_opy_ (u"ࠥࠦᏲ"))
            return
        if len(bstack1l11l11l111_opy_) > 1:
            self.logger.debug(
                bstack1ll1ll1111l_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦࡻ࡭ࡧࡱࠬࡵࡧࡧࡦࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷ࠮ࢃࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࢀࡱࡷࡢࡴࡪࡷࢂࠨᏳ"))
        bstack1l11l1l1l1l_opy_, bstack1l11lll1111_opy_ = bstack1l11l11l111_opy_[0]
        page = bstack1l11l1l1l1l_opy_()
        if not page:
            self.logger.debug(bstack1l111l1_opy_ (u"ࠧࡳࡡࡳ࡭ࡢࡳ࠶࠷ࡹࡠࡵࡼࡲࡨࡀࠠ࡯ࡱࠣࡴࡦ࡭ࡥࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᏴ") + str(kwargs) + bstack1l111l1_opy_ (u"ࠨࠢᏵ"))
            return
        timestamp = int(time.time() * 1000)
        data = bstack1l111l1_opy_ (u"ࠢࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࡓࡺࡰࡦ࠾ࠧ᏶") + str(timestamp)
        try:
            page.evaluate(
                bstack1l111l1_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤ᏷"),
                bstack1l111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧᏸ").format(
                    json.dumps(
                        {
                            bstack1l111l1_opy_ (u"ࠥࡥࡨࡺࡩࡰࡰࠥᏹ"): bstack1l111l1_opy_ (u"ࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨᏺ"),
                            bstack1l111l1_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣᏻ"): {
                                bstack1l111l1_opy_ (u"ࠨࡴࡺࡲࡨࠦᏼ"): bstack1l111l1_opy_ (u"ࠢࡂࡰࡱࡳࡹࡧࡴࡪࡱࡱࠦᏽ"),
                                bstack1l111l1_opy_ (u"ࠣࡦࡤࡸࡦࠨ᏾"): data,
                                bstack1l111l1_opy_ (u"ࠤ࡯ࡩࡻ࡫࡬ࠣ᏿"): bstack1l111l1_opy_ (u"ࠥࡨࡪࡨࡵࡨࠤ᐀")
                            }
                        }
                    )
                )
            )
        except Exception as e:
            self.logger.debug(bstack1l111l1_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡰ࠳࠴ࡽࠥࡧ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠢࡰࡥࡷࡱࡩ࡯ࡩࠣࡿࢂࠨᐁ"), e)
    def bstack1l1l1l11111_opy_(
        self,
        instance: bstack1ll1llllll1_opy_,
        f: TestFramework,
        bstack1lll1ll1111_opy_: Tuple[bstack1ll1lll1111_opy_, bstack1lll11ll1l1_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11l111lll_opy_(f, instance, bstack1lll1ll1111_opy_, *args, **kwargs)
        if f.bstack1llll1l111l_opy_(instance, bstack1lll11l1ll1_opy_.bstack1l1l1llll1l_opy_, False):
            return
        self.bstack1l1lll1l111_opy_()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1llll1l111l_opy_(instance, TestFramework.bstack1ll1111ll1l_opy_)
        req.test_framework_name = TestFramework.bstack1llll1l111l_opy_(instance, TestFramework.bstack1ll111ll111_opy_)
        req.test_framework_version = TestFramework.bstack1llll1l111l_opy_(instance, TestFramework.bstack1l1l1llllll_opy_)
        req.test_framework_state = bstack1lll1ll1111_opy_[0].name
        req.test_hook_state = bstack1lll1ll1111_opy_[1].name
        req.test_uuid = TestFramework.bstack1llll1l111l_opy_(instance, TestFramework.bstack1ll111l11l1_opy_)
        for bstack1l11l1l1lll_opy_ in bstack1ll1l1111l1_opy_.bstack1llll11llll_opy_.values():
            session = req.automation_sessions.add()
            session.provider = (
                bstack1l111l1_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠦᐂ")
                if bstack1l1l1l11l1l_opy_
                else bstack1l111l1_opy_ (u"ࠨࡵ࡯࡭ࡱࡳࡼࡴ࡟ࡨࡴ࡬ࡨࠧᐃ")
            )
            session.ref = bstack1l11l1l1lll_opy_.ref()
            session.hub_url = bstack1ll1l1111l1_opy_.bstack1llll1l111l_opy_(bstack1l11l1l1lll_opy_, bstack1ll1l1111l1_opy_.bstack1l11ll1111l_opy_, bstack1l111l1_opy_ (u"ࠢࠣᐄ"))
            session.framework_name = bstack1l11l1l1lll_opy_.framework_name
            session.framework_version = bstack1l11l1l1lll_opy_.framework_version
            session.framework_session_id = bstack1ll1l1111l1_opy_.bstack1llll1l111l_opy_(bstack1l11l1l1lll_opy_, bstack1ll1l1111l1_opy_.bstack1l11l1ll1ll_opy_, bstack1l111l1_opy_ (u"ࠣࠤᐅ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1ll11111l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1llllll1_opy_,
        bstack1lll1ll1111_opy_: Tuple[bstack1ll1lll1111_opy_, bstack1lll11ll1l1_opy_],
        *args,
        **kwargs
    ):
        bstack1l11l11l111_opy_ = f.bstack1llll1l111l_opy_(instance, bstack1lll11l1ll1_opy_.bstack1l1l11l111l_opy_, [])
        if not bstack1l11l11l111_opy_:
            self.logger.debug(bstack1l111l1_opy_ (u"ࠤࡪࡩࡹࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡨࡷ࡯ࡶࡦࡴ࠽ࠤࡳࡵࠠࡱࡣࡪࡩࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᐆ") + str(kwargs) + bstack1l111l1_opy_ (u"ࠥࠦᐇ"))
            return
        if len(bstack1l11l11l111_opy_) > 1:
            self.logger.debug(bstack1l111l1_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡪࡲࡪࡸࡨࡶ࠿ࠦࡻ࡭ࡧࡱࠬࡵࡧࡧࡦࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷ࠮ࢃࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᐈ") + str(kwargs) + bstack1l111l1_opy_ (u"ࠧࠨᐉ"))
        bstack1l11l1l1l1l_opy_, bstack1l11lll1111_opy_ = bstack1l11l11l111_opy_[0]
        page = bstack1l11l1l1l1l_opy_()
        if not page:
            self.logger.debug(bstack1l111l1_opy_ (u"ࠨࡧࡦࡶࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡰࡲࠤࡵࡧࡧࡦࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᐊ") + str(kwargs) + bstack1l111l1_opy_ (u"ࠢࠣᐋ"))
            return
        return page
    def bstack1ll11111l11_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1llllll1_opy_,
        bstack1lll1ll1111_opy_: Tuple[bstack1ll1lll1111_opy_, bstack1lll11ll1l1_opy_],
        *args,
        **kwargs
    ):
        caps = {}
        bstack1l11l1l1ll1_opy_ = {}
        for bstack1l11l1l1lll_opy_ in bstack1ll1l1111l1_opy_.bstack1llll11llll_opy_.values():
            caps = bstack1ll1l1111l1_opy_.bstack1llll1l111l_opy_(bstack1l11l1l1lll_opy_, bstack1ll1l1111l1_opy_.bstack1l11ll11lll_opy_, bstack1l111l1_opy_ (u"ࠣࠤᐌ"))
        bstack1l11l1l1ll1_opy_[bstack1l111l1_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠢᐍ")] = caps.get(bstack1l111l1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࠦᐎ"), bstack1l111l1_opy_ (u"ࠦࠧᐏ"))
        bstack1l11l1l1ll1_opy_[bstack1l111l1_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠦᐐ")] = caps.get(bstack1l111l1_opy_ (u"ࠨ࡯ࡴࠤᐑ"), bstack1l111l1_opy_ (u"ࠢࠣᐒ"))
        bstack1l11l1l1ll1_opy_[bstack1l111l1_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥᐓ")] = caps.get(bstack1l111l1_opy_ (u"ࠤࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳࠨᐔ"), bstack1l111l1_opy_ (u"ࠥࠦᐕ"))
        bstack1l11l1l1ll1_opy_[bstack1l111l1_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠧᐖ")] = caps.get(bstack1l111l1_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠢᐗ"), bstack1l111l1_opy_ (u"ࠨࠢᐘ"))
        return bstack1l11l1l1ll1_opy_
    def bstack1ll111l1lll_opy_(self, page: object, bstack1l1lll1llll_opy_, args={}):
        try:
            bstack1l11l11ll11_opy_ = bstack1l111l1_opy_ (u"ࠢࠣࠤࠫࡪࡺࡴࡣࡵ࡫ࡲࡲࠥ࠮࠮࠯࠰ࡥࡷࡹࡧࡣ࡬ࡕࡧ࡯ࡆࡸࡧࡴࠫࠣࡿࢀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡴࡨࡸࡺࡸ࡮ࠡࡰࡨࡻࠥࡖࡲࡰ࡯࡬ࡷࡪ࠮ࠨࡳࡧࡶࡳࡱࡼࡥ࠭ࠢࡵࡩ࡯࡫ࡣࡵࠫࠣࡁࡃࠦࡻࡼࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡤࡶࡸࡦࡩ࡫ࡔࡦ࡮ࡅࡷ࡭ࡳ࠯ࡲࡸࡷ࡭࠮ࡲࡦࡵࡲࡰࡻ࡫ࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡽࡩࡲࡤࡨ࡯ࡥࡻࢀࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࡾࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࢁ࠮࠮ࡻࡢࡴࡪࡣ࡯ࡹ࡯࡯ࡿࠬࠦࠧࠨᐙ")
            bstack1l1lll1llll_opy_ = bstack1l1lll1llll_opy_.replace(bstack1l111l1_opy_ (u"ࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦᐚ"), bstack1l111l1_opy_ (u"ࠤࡥࡷࡹࡧࡣ࡬ࡕࡧ࡯ࡆࡸࡧࡴࠤᐛ"))
            script = bstack1l11l11ll11_opy_.format(fn_body=bstack1l1lll1llll_opy_, arg_json=json.dumps(args))
            return page.evaluate(script)
        except Exception as e:
            self.logger.error(bstack1l111l1_opy_ (u"ࠥࡥ࠶࠷ࡹࡠࡵࡦࡶ࡮ࡶࡴࡠࡧࡻࡩࡨࡻࡴࡦ࠼ࠣࡉࡷࡸ࡯ࡳࠢࡨࡼࡪࡩࡵࡵ࡫ࡱ࡫ࠥࡺࡨࡦࠢࡤ࠵࠶ࡿࠠࡴࡥࡵ࡭ࡵࡺࠬࠡࠤᐜ") + str(e) + bstack1l111l1_opy_ (u"ࠦࠧᐝ"))