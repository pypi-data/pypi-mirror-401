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
from datetime import datetime, timezone
import os
import builtins
from pathlib import Path
from typing import Any, Tuple, Callable, List
from browserstack_sdk.sdk_cli.bstack1lll1ll1l11_opy_ import bstack1llll11l1ll_opy_, bstack1lll1l1ll11_opy_, bstack1llll11l111_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1l1l1_opy_ import bstack1ll1l1ll1ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l11111l_opy_ import bstack1lll111lll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll11ll1ll_opy_ import bstack1ll11llll11_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll1lll1111_opy_, bstack1ll1llllll1_opy_, bstack1lll11ll1l1_opy_, bstack1ll11ll111l_opy_
from json import dumps, JSONEncoder
import grpc
from browserstack_sdk import sdk_pb2 as structs
import sys
import traceback
import time
import json
from bstack_utils.helper import bstack1l1l1l11l1l_opy_, bstack1l1l1lll1ll_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
bstack1l1l11ll1l1_opy_ = [bstack1l111l1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥግ"), bstack1l111l1_opy_ (u"ࠨࡰࡢࡴࡨࡲࡹࠨጎ"), bstack1l111l1_opy_ (u"ࠢࡤࡱࡱࡪ࡮࡭ࠢጏ"), bstack1l111l1_opy_ (u"ࠣࡵࡨࡷࡸ࡯࡯࡯ࠤጐ"), bstack1l111l1_opy_ (u"ࠤࡳࡥࡹ࡮ࠢ጑")]
bstack1l11lllll11_opy_ = bstack1l1l1lll1ll_opy_()
bstack1l1l1l1l111_opy_ = bstack1l111l1_opy_ (u"࡙ࠥࡵࡲ࡯ࡢࡦࡨࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴ࠯ࠥጒ")
bstack1l1l1ll1lll_opy_ = {
    bstack1l111l1_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡵࡿࡴࡩࡱࡱ࠲ࡎࡺࡥ࡮ࠤጓ"): bstack1l1l11ll1l1_opy_,
    bstack1l111l1_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡶࡹࡵࡪࡲࡲ࠳ࡖࡡࡤ࡭ࡤ࡫ࡪࠨጔ"): bstack1l1l11ll1l1_opy_,
    bstack1l111l1_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡰࡺࡶ࡫ࡳࡳ࠴ࡍࡰࡦࡸࡰࡪࠨጕ"): bstack1l1l11ll1l1_opy_,
    bstack1l111l1_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡱࡻࡷ࡬ࡴࡴ࠮ࡄ࡮ࡤࡷࡸࠨ጖"): bstack1l1l11ll1l1_opy_,
    bstack1l111l1_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡲࡼࡸ࡭ࡵ࡮࠯ࡈࡸࡲࡨࡺࡩࡰࡰࠥ጗"): bstack1l1l11ll1l1_opy_
    + [
        bstack1l111l1_opy_ (u"ࠤࡲࡶ࡮࡭ࡩ࡯ࡣ࡯ࡲࡦࡳࡥࠣጘ"),
        bstack1l111l1_opy_ (u"ࠥ࡯ࡪࡿࡷࡰࡴࡧࡷࠧጙ"),
        bstack1l111l1_opy_ (u"ࠦ࡫࡯ࡸࡵࡷࡵࡩ࡮ࡴࡦࡰࠤጚ"),
        bstack1l111l1_opy_ (u"ࠧࡱࡥࡺࡹࡲࡶࡩࡹࠢጛ"),
        bstack1l111l1_opy_ (u"ࠨࡣࡢ࡮࡯ࡷࡵ࡫ࡣࠣጜ"),
        bstack1l111l1_opy_ (u"ࠢࡤࡣ࡯ࡰࡴࡨࡪࠣጝ"),
        bstack1l111l1_opy_ (u"ࠣࡵࡷࡥࡷࡺࠢጞ"),
        bstack1l111l1_opy_ (u"ࠤࡶࡸࡴࡶࠢጟ"),
        bstack1l111l1_opy_ (u"ࠥࡨࡺࡸࡡࡵ࡫ࡲࡲࠧጠ"),
        bstack1l111l1_opy_ (u"ࠦࡼ࡮ࡥ࡯ࠤጡ"),
    ],
    bstack1l111l1_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡳࡡࡪࡰ࠱ࡗࡪࡹࡳࡪࡱࡱࠦጢ"): [bstack1l111l1_opy_ (u"ࠨࡳࡵࡣࡵࡸࡵࡧࡴࡩࠤጣ"), bstack1l111l1_opy_ (u"ࠢࡵࡧࡶࡸࡸ࡬ࡡࡪ࡮ࡨࡨࠧጤ"), bstack1l111l1_opy_ (u"ࠣࡶࡨࡷࡹࡹࡣࡰ࡮࡯ࡩࡨࡺࡥࡥࠤጥ"), bstack1l111l1_opy_ (u"ࠤ࡬ࡸࡪࡳࡳࠣጦ")],
    bstack1l111l1_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡧࡴࡴࡦࡪࡩ࠱ࡇࡴࡴࡦࡪࡩࠥጧ"): [bstack1l111l1_opy_ (u"ࠦ࡮ࡴࡶࡰࡥࡤࡸ࡮ࡵ࡮ࡠࡲࡤࡶࡦࡳࡳࠣጨ"), bstack1l111l1_opy_ (u"ࠧࡧࡲࡨࡵࠥጩ")],
    bstack1l111l1_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡦࡪࡺࡷࡹࡷ࡫ࡳ࠯ࡈ࡬ࡼࡹࡻࡲࡦࡆࡨࡪࠧጪ"): [bstack1l111l1_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨጫ"), bstack1l111l1_opy_ (u"ࠣࡣࡵ࡫ࡳࡧ࡭ࡦࠤጬ"), bstack1l111l1_opy_ (u"ࠤࡩࡹࡳࡩࠢጭ"), bstack1l111l1_opy_ (u"ࠥࡴࡦࡸࡡ࡮ࡵࠥጮ"), bstack1l111l1_opy_ (u"ࠦࡺࡴࡩࡵࡶࡨࡷࡹࠨጯ"), bstack1l111l1_opy_ (u"ࠧ࡯ࡤࡴࠤጰ")],
    bstack1l111l1_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡦࡪࡺࡷࡹࡷ࡫ࡳ࠯ࡕࡸࡦࡗ࡫ࡱࡶࡧࡶࡸࠧጱ"): [bstack1l111l1_opy_ (u"ࠢࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࠧጲ"), bstack1l111l1_opy_ (u"ࠣࡲࡤࡶࡦࡳࠢጳ"), bstack1l111l1_opy_ (u"ࠤࡳࡥࡷࡧ࡭ࡠ࡫ࡱࡨࡪࡾࠢጴ")],
    bstack1l111l1_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡶࡺࡴ࡮ࡦࡴ࠱ࡇࡦࡲ࡬ࡊࡰࡩࡳࠧጵ"): [bstack1l111l1_opy_ (u"ࠦࡼ࡮ࡥ࡯ࠤጶ"), bstack1l111l1_opy_ (u"ࠧࡸࡥࡴࡷ࡯ࡸࠧጷ")],
    bstack1l111l1_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴࡭ࡢࡴ࡮࠲ࡸࡺࡲࡶࡥࡷࡹࡷ࡫ࡳ࠯ࡐࡲࡨࡪࡑࡥࡺࡹࡲࡶࡩࡹࠢጸ"): [bstack1l111l1_opy_ (u"ࠢ࡯ࡱࡧࡩࠧጹ"), bstack1l111l1_opy_ (u"ࠣࡲࡤࡶࡪࡴࡴࠣጺ")],
    bstack1l111l1_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡰࡥࡷࡱ࠮ࡴࡶࡵࡹࡨࡺࡵࡳࡧࡶ࠲ࡒࡧࡲ࡬ࠤጻ"): [bstack1l111l1_opy_ (u"ࠥࡲࡦࡳࡥࠣጼ"), bstack1l111l1_opy_ (u"ࠦࡦࡸࡧࡴࠤጽ"), bstack1l111l1_opy_ (u"ࠧࡱࡷࡢࡴࡪࡷࠧጾ")],
}
_1l1l1lll1l1_opy_ = set()
class bstack1ll1l11llll_opy_(bstack1ll1l1ll1ll_opy_):
    bstack1l1l1l1111l_opy_ = bstack1l111l1_opy_ (u"ࠨࡴࡦࡵࡷࡣࡩ࡫ࡦࡦࡴࡵࡩࡩࠨጿ")
    bstack1l1l11ll111_opy_ = bstack1l111l1_opy_ (u"ࠢࡊࡐࡉࡓࠧፀ")
    bstack1l1l111111l_opy_ = bstack1l111l1_opy_ (u"ࠣࡇࡕࡖࡔࡘࠢፁ")
    bstack1l1l111llll_opy_: Callable
    bstack1l1l1l1l11l_opy_: Callable
    def __init__(self, bstack1ll1ll1l1l1_opy_, bstack1ll1l11ll1l_opy_):
        super().__init__()
        self.bstack1l1lll11l1l_opy_ = bstack1ll1l11ll1l_opy_
        if os.getenv(bstack1l111l1_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡊࡑࡇࡇࡠࡑ࠴࠵࡞ࠨፂ"), bstack1l111l1_opy_ (u"ࠥ࠵ࠧፃ")) != bstack1l111l1_opy_ (u"ࠦ࠶ࠨፄ") or not self.is_enabled():
            self.logger.warning(bstack1l111l1_opy_ (u"ࠧࠨፅ") + str(self.__class__.__name__) + bstack1l111l1_opy_ (u"ࠨࠠࡥ࡫ࡶࡥࡧࡲࡥࡥࠤፆ"))
            return
        TestFramework.bstack1ll111l11ll_opy_((bstack1ll1lll1111_opy_.TEST, bstack1lll11ll1l1_opy_.PRE), self.bstack1l1lll11lll_opy_)
        TestFramework.bstack1ll111l11ll_opy_((bstack1ll1lll1111_opy_.TEST, bstack1lll11ll1l1_opy_.POST), self.bstack1l1ll1llll1_opy_)
        for event in bstack1ll1lll1111_opy_:
            for state in bstack1lll11ll1l1_opy_:
                TestFramework.bstack1ll111l11ll_opy_((event, state), self.bstack1l1l111l11l_opy_)
        bstack1ll1ll1l1l1_opy_.bstack1ll111l11ll_opy_((bstack1lll1l1ll11_opy_.bstack1llll111l1l_opy_, bstack1llll11l111_opy_.POST), self.bstack1l1l1111lll_opy_)
        self.bstack1l1l111llll_opy_ = sys.stdout.write
        sys.stdout.write = self.bstack1l1l11l1ll1_opy_(bstack1ll1l11llll_opy_.bstack1l1l11ll111_opy_, self.bstack1l1l111llll_opy_)
        self.bstack1l1l1l1l11l_opy_ = sys.stderr.write
        sys.stderr.write = self.bstack1l1l11l1ll1_opy_(bstack1ll1l11llll_opy_.bstack1l1l111111l_opy_, self.bstack1l1l1l1l11l_opy_)
        self.bstack1l1l1ll111l_opy_ = builtins.print
        builtins.print = self.bstack1l1l1ll1l11_opy_()
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l111l11l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1llllll1_opy_,
        bstack1lll1ll1111_opy_: Tuple[bstack1ll1lll1111_opy_, bstack1lll11ll1l1_opy_],
        *args,
        **kwargs,
    ):
        if f.bstack1l1l1l11lll_opy_() and instance:
            bstack1l1l11111ll_opy_ = datetime.now()
            test_framework_state, test_hook_state = bstack1lll1ll1111_opy_
            if test_framework_state == bstack1ll1lll1111_opy_.SETUP_FIXTURE:
                return
            elif test_framework_state == bstack1ll1lll1111_opy_.LOG:
                bstack1ll11llll_opy_ = datetime.now()
                entries = f.bstack1l1l1111111_opy_(instance, bstack1lll1ll1111_opy_)
                if entries:
                    self.bstack1l1l11ll1ll_opy_(instance, entries)
                    instance.bstack111lll11l_opy_(bstack1l111l1_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡥ࡯ࡦࡢࡰࡴ࡭࡟ࡤࡴࡨࡥࡹ࡫ࡤࡠࡧࡹࡩࡳࡺࠢፇ"), datetime.now() - bstack1ll11llll_opy_)
                    f.bstack1l1l1ll1l1l_opy_(instance, bstack1lll1ll1111_opy_)
                instance.bstack111lll11l_opy_(bstack1l111l1_opy_ (u"ࠣࡱ࠴࠵ࡾࡀ࡯࡯ࡡࡤࡰࡱࡥࡴࡦࡵࡷࡣࡪࡼࡥ࡯ࡶࡶࠦፈ"), datetime.now() - bstack1l1l11111ll_opy_)
                return # bstack1l1l111ll11_opy_ not send this event with the bstack1l1l1lllll1_opy_ bstack1l1l11lll11_opy_
            elif (
                test_framework_state == bstack1ll1lll1111_opy_.TEST
                and test_hook_state == bstack1lll11ll1l1_opy_.POST
                and not f.bstack1lll1ll111l_opy_(instance, TestFramework.bstack1l1l11lll1l_opy_)
            ):
                self.logger.warning(bstack1l111l1_opy_ (u"ࠤࡧࡶࡴࡶࡰࡪࡰࡪࠤࡩࡻࡥࠡࡶࡲࠤࡱࡧࡣ࡬ࠢࡲࡪࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࠢፉ") + str(TestFramework.bstack1lll1ll111l_opy_(instance, TestFramework.bstack1l1l11lll1l_opy_)) + bstack1l111l1_opy_ (u"ࠥࠦፊ"))
                f.bstack1llll1111l1_opy_(instance, bstack1ll1l11llll_opy_.bstack1l1l1l1111l_opy_, True)
                return # bstack1l1l111ll11_opy_ not send this event bstack1l11llll11l_opy_ bstack1l1l11l1l1l_opy_
            elif (
                f.bstack1llll1l111l_opy_(instance, bstack1ll1l11llll_opy_.bstack1l1l1l1111l_opy_, False)
                and test_framework_state == bstack1ll1lll1111_opy_.LOG_REPORT
                and test_hook_state == bstack1lll11ll1l1_opy_.POST
                and f.bstack1lll1ll111l_opy_(instance, TestFramework.bstack1l1l11lll1l_opy_)
            ):
                self.logger.warning(bstack1l111l1_opy_ (u"ࠦ࡮ࡴࡪࡦࡥࡷ࡭ࡳ࡭ࠠࡕࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࡓࡵࡣࡷࡩ࠳࡚ࡅࡔࡖ࠯ࠤ࡙࡫ࡳࡵࡊࡲࡳࡰ࡙ࡴࡢࡶࡨ࠲ࡕࡕࡓࡕࠢࠥፋ") + str(TestFramework.bstack1lll1ll111l_opy_(instance, TestFramework.bstack1l1l11lll1l_opy_)) + bstack1l111l1_opy_ (u"ࠧࠨፌ"))
                self.bstack1l1l111l11l_opy_(f, instance, (bstack1ll1lll1111_opy_.TEST, bstack1lll11ll1l1_opy_.POST), *args, **kwargs)
            bstack1ll11llll_opy_ = datetime.now()
            data = instance.data.copy()
            bstack1l1l11lllll_opy_ = sorted(
                filter(lambda x: x.get(bstack1l111l1_opy_ (u"ࠨࡥࡷࡧࡱࡸࡤࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠤፍ"), None), data.pop(bstack1l111l1_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࡹࠢፎ"), {}).values()),
                key=lambda x: x[bstack1l111l1_opy_ (u"ࠣࡧࡹࡩࡳࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠦፏ")],
            )
            if bstack1lll111lll1_opy_.bstack1l1l11l111l_opy_ in data:
                data.pop(bstack1lll111lll1_opy_.bstack1l1l11l111l_opy_)
            data.update({bstack1l111l1_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴࠤፐ"): bstack1l1l11lllll_opy_})
            instance.bstack111lll11l_opy_(bstack1l111l1_opy_ (u"ࠥ࡮ࡸࡵ࡮࠻ࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫ࡳࠣፑ"), datetime.now() - bstack1ll11llll_opy_)
            bstack1ll11llll_opy_ = datetime.now()
            event_json = dumps(data, cls=bstack1l1l1l11ll1_opy_)
            instance.bstack111lll11l_opy_(bstack1l111l1_opy_ (u"ࠦ࡯ࡹ࡯࡯࠼ࡲࡲࡤࡧ࡬࡭ࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡹࠢፒ"), datetime.now() - bstack1ll11llll_opy_)
            self.bstack1l1l11lll11_opy_(instance, bstack1lll1ll1111_opy_, event_json=event_json)
            instance.bstack111lll11l_opy_(bstack1l111l1_opy_ (u"ࠧࡵ࠱࠲ࡻ࠽ࡳࡳࡥࡡ࡭࡮ࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺࡳࠣፓ"), datetime.now() - bstack1l1l11111ll_opy_)
    def bstack1l1lll11lll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1llllll1_opy_,
        bstack1lll1ll1111_opy_: Tuple[bstack1ll1lll1111_opy_, bstack1lll11ll1l1_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack11lll1l1ll_opy_ import bstack1ll11ll1ll1_opy_
        bstack1ll111ll11l_opy_ = bstack1ll11ll1ll1_opy_.bstack1ll1111l1l1_opy_(EVENTS.bstack1lll1l1111_opy_.value)
        self.bstack1l1lll11l1l_opy_.bstack1l1l1ll1111_opy_(instance, f, bstack1lll1ll1111_opy_, *args, **kwargs)
        req = self.bstack1l1lll11l1l_opy_.bstack1l1l1l11111_opy_(instance, f, bstack1lll1ll1111_opy_, *args, **kwargs)
        self.bstack1l1l1lll11l_opy_(f, instance, req)
        bstack1ll11ll1ll1_opy_.end(EVENTS.bstack1lll1l1111_opy_.value, bstack1ll111ll11l_opy_ + bstack1l111l1_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨፔ"), bstack1ll111ll11l_opy_ + bstack1l111l1_opy_ (u"ࠢ࠻ࡧࡱࡨࠧፕ"), status=True, failure=None, test_name=None)
    def bstack1l1ll1llll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1llllll1_opy_,
        bstack1lll1ll1111_opy_: Tuple[bstack1ll1lll1111_opy_, bstack1lll11ll1l1_opy_],
        *args,
        **kwargs,
    ):
        if not f.bstack1llll1l111l_opy_(instance, self.bstack1l1lll11l1l_opy_.bstack1l1l1llll1l_opy_, False):
            req = self.bstack1l1lll11l1l_opy_.bstack1l1l1l11111_opy_(instance, f, bstack1lll1ll1111_opy_, *args, **kwargs)
            self.bstack1l1l1lll11l_opy_(f, instance, req)
    @measure(event_name=EVENTS.bstack1l1l1l11l11_opy_, stage=STAGE.bstack11l11l11l1_opy_)
    def bstack1l1l1lll11l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1llllll1_opy_,
        req: structs.TestSessionEventRequest
    ):
        if not req:
            self.logger.debug(bstack1l111l1_opy_ (u"ࠣࡕ࡮࡭ࡵࡶࡩ࡯ࡩࠣࡘࡪࡹࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡆࡸࡨࡲࡹࠦࡧࡓࡒࡆࠤࡨࡧ࡬࡭࠼ࠣࡒࡴࠦࡶࡢ࡮࡬ࡨࠥࡸࡥࡲࡷࡨࡷࡹࠦࡤࡢࡶࡤࠦፖ"))
            return
        bstack1ll11llll_opy_ = datetime.now()
        try:
            r = self.bstack1lll11l1l1l_opy_.TestSessionEvent(req)
            instance.bstack111lll11l_opy_(bstack1l111l1_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡺࡥࡴࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡪࡼࡥ࡯ࡶࠥፗ"), datetime.now() - bstack1ll11llll_opy_)
            f.bstack1llll1111l1_opy_(instance, self.bstack1l1lll11l1l_opy_.bstack1l1l1llll1l_opy_, r.success)
            if not r.success:
                self.logger.info(bstack1l111l1_opy_ (u"ࠥࡶࡪࡩࡥࡪࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࠧፘ") + str(r) + bstack1l111l1_opy_ (u"ࠦࠧፙ"))
        except grpc.RpcError as e:
            self.logger.error(bstack1l111l1_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥፚ") + str(e) + bstack1l111l1_opy_ (u"ࠨࠢ፛"))
            traceback.print_exc()
            raise e
    def bstack1l1l1111lll_opy_(
        self,
        f: bstack1ll11llll11_opy_,
        _driver: object,
        exec: Tuple[bstack1llll11l1ll_opy_, str],
        _1l11llllll1_opy_: Tuple[bstack1lll1l1ll11_opy_, bstack1llll11l111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if not bstack1ll11llll11_opy_.bstack1ll11111111_opy_(method_name):
            return
        if f.bstack1l1lll11ll1_opy_(*args) == bstack1ll11llll11_opy_.bstack1l1l1111l11_opy_:
            bstack1l1l11111ll_opy_ = datetime.now()
            screenshot = result.get(bstack1l111l1_opy_ (u"ࠢࡷࡣ࡯ࡹࡪࠨ፜"), None) if isinstance(result, dict) else None
            if not isinstance(screenshot, str) or len(screenshot) <= 0:
                self.logger.warning(bstack1l111l1_opy_ (u"ࠣ࡫ࡱࡺࡦࡲࡩࡥࠢࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠦࡩ࡮ࡣࡪࡩࠥࡨࡡࡴࡧ࠹࠸ࠥࡹࡴࡳࠤ፝"))
                return
            bstack1l1l11l11ll_opy_ = self.bstack1l1l111lll1_opy_(instance)
            if bstack1l1l11l11ll_opy_:
                entry = bstack1ll11ll111l_opy_(TestFramework.bstack1l1l1l111l1_opy_, screenshot)
                self.bstack1l1l11ll1ll_opy_(bstack1l1l11l11ll_opy_, [entry])
                instance.bstack111lll11l_opy_(bstack1l111l1_opy_ (u"ࠤࡲ࠵࠶ࡿ࠺ࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡨࡼࡪࡩࡵࡵࡧࠥ፞"), datetime.now() - bstack1l1l11111ll_opy_)
            else:
                self.logger.warning(bstack1l111l1_opy_ (u"ࠥࡹࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡷࡩࡸࡺࠠࡧࡱࡵࠤࡼ࡮ࡩࡤࡪࠣࡸ࡭࡯ࡳࠡࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠥࡽࡡࡴࠢࡷࡥࡰ࡫࡮ࠡࡤࡼࠤࡩࡸࡩࡷࡧࡵࡁࠥࢁࡽࠣ፟").format(instance.ref()))
        event = {}
        bstack1l1l11l11ll_opy_ = self.bstack1l1l111lll1_opy_(instance)
        if bstack1l1l11l11ll_opy_:
            self.bstack1l1l111l1ll_opy_(event, bstack1l1l11l11ll_opy_)
            if event.get(bstack1l111l1_opy_ (u"ࠦࡱࡵࡧࡴࠤ፠")):
                self.bstack1l1l11ll1ll_opy_(bstack1l1l11l11ll_opy_, event[bstack1l111l1_opy_ (u"ࠧࡲ࡯ࡨࡵࠥ፡")])
            else:
                self.logger.debug(bstack1l111l1_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥࡲ࡯ࡨࡵࠣࡪࡴࡸࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠤࡪࡼࡥ࡯ࡶࠥ።"))
    @measure(event_name=EVENTS.bstack1l1l11l1l11_opy_, stage=STAGE.bstack11l11l11l1_opy_)
    def bstack1l1l11ll1ll_opy_(
        self,
        bstack1l1l11l11ll_opy_: bstack1ll1llllll1_opy_,
        entries: List[bstack1ll11ll111l_opy_],
    ):
        self.bstack1l1lll1l111_opy_()
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1llll1l111l_opy_(bstack1l1l11l11ll_opy_, TestFramework.bstack1ll1111ll1l_opy_)
        req.execution_context.hash = str(bstack1l1l11l11ll_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1l11l11ll_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1l11l11ll_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1llll1l111l_opy_(bstack1l1l11l11ll_opy_, TestFramework.bstack1ll111ll111_opy_)
            log_entry.test_framework_version = TestFramework.bstack1llll1l111l_opy_(bstack1l1l11l11ll_opy_, TestFramework.bstack1l1l1llllll_opy_)
            log_entry.uuid = TestFramework.bstack1llll1l111l_opy_(bstack1l1l11l11ll_opy_, TestFramework.bstack1ll111l11l1_opy_)
            log_entry.test_framework_state = bstack1l1l11l11ll_opy_.state.name
            log_entry.message = entry.message.encode(bstack1l111l1_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨ፣"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack1l111l1_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥ፤"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1l111ll1l_opy_
                log_entry.file_path = entry.bstack11lll_opy_
        def bstack1l1l11l1111_opy_():
            bstack1ll11llll_opy_ = datetime.now()
            try:
                self.bstack1lll11l1l1l_opy_.LogCreatedEvent(req)
                if entry.kind == TestFramework.bstack1l1l1l111l1_opy_:
                    bstack1l1l11l11ll_opy_.bstack111lll11l_opy_(bstack1l111l1_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࡡࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠨ፥"), datetime.now() - bstack1ll11llll_opy_)
                elif entry.kind == TestFramework.bstack1l11llll1l1_opy_:
                    bstack1l1l11l11ll_opy_.bstack111lll11l_opy_(bstack1l111l1_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࡢࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠢ፦"), datetime.now() - bstack1ll11llll_opy_)
                else:
                    bstack1l1l11l11ll_opy_.bstack111lll11l_opy_(bstack1l111l1_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡱࡵࡧࠣ፧"), datetime.now() - bstack1ll11llll_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1l111l1_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥ፨") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1llll1llll1_opy_.enqueue(bstack1l1l11l1111_opy_)
    @measure(event_name=EVENTS.bstack1l11lllllll_opy_, stage=STAGE.bstack11l11l11l1_opy_)
    def bstack1l1l11lll11_opy_(
        self,
        instance: bstack1ll1llllll1_opy_,
        bstack1lll1ll1111_opy_: Tuple[bstack1ll1lll1111_opy_, bstack1lll11ll1l1_opy_],
        event_json=None,
    ):
        self.bstack1l1lll1l111_opy_()
        req = structs.TestFrameworkEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1llll1l111l_opy_(instance, TestFramework.bstack1ll1111ll1l_opy_)
        req.test_framework_name = TestFramework.bstack1llll1l111l_opy_(instance, TestFramework.bstack1ll111ll111_opy_)
        req.test_framework_version = TestFramework.bstack1llll1l111l_opy_(instance, TestFramework.bstack1l1l1llllll_opy_)
        req.test_framework_state = bstack1lll1ll1111_opy_[0].name
        req.test_hook_state = bstack1lll1ll1111_opy_[1].name
        started_at = TestFramework.bstack1llll1l111l_opy_(instance, TestFramework.bstack1l1l1l1lll1_opy_, None)
        if started_at:
            req.started_at = started_at.isoformat()
        ended_at = TestFramework.bstack1llll1l111l_opy_(instance, TestFramework.bstack1l1l1llll11_opy_, None)
        if ended_at:
            req.ended_at = ended_at.isoformat()
        req.uuid = instance.ref()
        req.event_json = (event_json if event_json else dumps(instance.data, cls=bstack1l1l1l11ll1_opy_)).encode(bstack1l111l1_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧ፩"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        def bstack1l1l11l1111_opy_():
            bstack1ll11llll_opy_ = datetime.now()
            try:
                self.bstack1lll11l1l1l_opy_.TestFrameworkEvent(req)
                instance.bstack111lll11l_opy_(bstack1l111l1_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡥ࡯ࡦࡢࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡪࡼࡥ࡯ࡶࠥ፪"), datetime.now() - bstack1ll11llll_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1l111l1_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨ፫") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1llll1llll1_opy_.enqueue(bstack1l1l11l1111_opy_)
    def bstack1l1l111lll1_opy_(self, instance: bstack1llll11l1ll_opy_):
        bstack1l1l1l1ll1l_opy_ = TestFramework.bstack1llll111111_opy_(instance.context)
        for t in bstack1l1l1l1ll1l_opy_:
            bstack1l1l1lll111_opy_ = TestFramework.bstack1llll1l111l_opy_(t, bstack1lll111lll1_opy_.bstack1l1l11l111l_opy_, [])
            if any(instance is d[1] for d in bstack1l1l1lll111_opy_):
                return t
    def bstack1l11lllll1l_opy_(self, message):
        self.bstack1l1l111llll_opy_(message + bstack1l111l1_opy_ (u"ࠤ࡟ࡲࠧ፬"))
    def log_error(self, message):
        self.bstack1l1l1l1l11l_opy_(message + bstack1l111l1_opy_ (u"ࠥࡠࡳࠨ፭"))
    def bstack1l1l11l1ll1_opy_(self, level, original_func):
        def bstack1l1l1l1l1l1_opy_(*args):
            try:
                try:
                    return_value = original_func(*args)
                except Exception:
                    return None
                try:
                    if not args or not isinstance(args[0], str) or not args[0].strip():
                        return return_value
                    message = args[0].strip()
                    if bstack1l111l1_opy_ (u"ࠦࡊࡼࡥ࡯ࡶࡇ࡭ࡸࡶࡡࡵࡥ࡫ࡩࡷࡓ࡯ࡥࡷ࡯ࡩࠧ፮") in message or bstack1l111l1_opy_ (u"ࠧࡡࡓࡅࡍࡆࡐࡎࡣࠢ፯") in message or bstack1l111l1_opy_ (u"ࠨ࡛ࡘࡧࡥࡈࡷ࡯ࡶࡦࡴࡐࡳࡩࡻ࡬ࡦ࡟ࠥ፰") in message:
                        return return_value
                    bstack1l1l1l1ll1l_opy_ = TestFramework.bstack1l1l11l1lll_opy_()
                    if not bstack1l1l1l1ll1l_opy_:
                        return return_value
                    bstack1l1l11l11ll_opy_ = next(
                        (
                            instance
                            for instance in bstack1l1l1l1ll1l_opy_
                            if TestFramework.bstack1lll1ll111l_opy_(instance, TestFramework.bstack1ll111l11l1_opy_)
                        ),
                        None,
                    )
                    if not bstack1l1l11l11ll_opy_:
                        return return_value
                    entry = bstack1ll11ll111l_opy_(TestFramework.bstack1l1l111l111_opy_, message, level)
                    self.bstack1l1l11ll1ll_opy_(bstack1l1l11l11ll_opy_, [entry])
                except Exception:
                    pass
                return return_value
            except Exception:
                return None
        return bstack1l1l1l1l1l1_opy_
    def bstack1l1l1ll1l11_opy_(self):
        def bstack1l1l1l1ll11_opy_(*args, **kwargs):
            try:
                self.bstack1l1l1ll111l_opy_(*args, **kwargs)
                if not args:
                    return
                message = bstack1l111l1_opy_ (u"ࠧࠡࠩ፱").join(str(arg) for arg in args)
                if not message.strip():
                    return
                if bstack1l111l1_opy_ (u"ࠣࡇࡹࡩࡳࡺࡄࡪࡵࡳࡥࡹࡩࡨࡦࡴࡐࡳࡩࡻ࡬ࡦࠤ፲") in message:
                    return
                bstack1l1l1l1ll1l_opy_ = TestFramework.bstack1l1l11l1lll_opy_()
                if not bstack1l1l1l1ll1l_opy_:
                    return
                bstack1l1l11l11ll_opy_ = next(
                    (
                        instance
                        for instance in bstack1l1l1l1ll1l_opy_
                        if TestFramework.bstack1lll1ll111l_opy_(instance, TestFramework.bstack1ll111l11l1_opy_)
                    ),
                    None,
                )
                if not bstack1l1l11l11ll_opy_:
                    return
                entry = bstack1ll11ll111l_opy_(TestFramework.bstack1l1l111l111_opy_, message, bstack1ll1l11llll_opy_.bstack1l1l11ll111_opy_)
                self.bstack1l1l11ll1ll_opy_(bstack1l1l11l11ll_opy_, [entry])
            except Exception as e:
                try:
                    self.bstack1l1l1ll111l_opy_(bstack1ll1ll1111l_opy_ (u"ࠤ࡞ࡉࡻ࡫࡮ࡵࡆ࡬ࡷࡵࡧࡴࡤࡪࡨࡶࡒࡵࡤࡶ࡮ࡨࡡࠥࡒ࡯ࡨࠢࡦࡥࡵࡺࡵࡳࡧࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࡪࢃࠢ፳"))
                except:
                    pass
        return bstack1l1l1l1ll11_opy_
    def bstack1l1l111l1ll_opy_(self, event: dict, instance=None) -> None:
        global _1l1l1lll1l1_opy_
        levels = [bstack1l111l1_opy_ (u"ࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨ፴"), bstack1l111l1_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣ፵")]
        bstack1l1l1111ll1_opy_ = bstack1l111l1_opy_ (u"ࠧࠨ፶")
        if instance is not None:
            try:
                bstack1l1l1111ll1_opy_ = TestFramework.bstack1llll1l111l_opy_(instance, TestFramework.bstack1ll111l11l1_opy_)
            except Exception as e:
                self.logger.warning(bstack1l111l1_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡵࡶ࡫ࡧࠤ࡫ࡸ࡯࡮ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠦ፷").format(e))
        bstack1l1l111l1l1_opy_ = []
        try:
            for level in levels:
                platform_index = os.environ[bstack1l111l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧ፸")]
                bstack1l1l1ll1ll1_opy_ = os.path.join(bstack1l11lllll11_opy_, (bstack1l1l1l1l111_opy_ + str(platform_index)), level)
                if not os.path.isdir(bstack1l1l1ll1ll1_opy_):
                    self.logger.debug(bstack1l111l1_opy_ (u"ࠣࡆ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡳࡵࡴࠡࡲࡵࡩࡸ࡫࡮ࡵࠢࡩࡳࡷࠦࡰࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡘࡪࡹࡴࠡࡣࡱࡨࠥࡈࡵࡪ࡮ࡧࠤࡱ࡫ࡶࡦ࡮ࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡽࢀࠦ፹").format(bstack1l1l1ll1ll1_opy_))
                    continue
                file_names = os.listdir(bstack1l1l1ll1ll1_opy_)
                for file_name in file_names:
                    file_path = os.path.join(bstack1l1l1ll1ll1_opy_, file_name)
                    abs_path = os.path.abspath(file_path)
                    if abs_path in _1l1l1lll1l1_opy_:
                        self.logger.info(bstack1l111l1_opy_ (u"ࠤࡓࡥࡹ࡮ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤࢀࢃࠢ፺").format(abs_path))
                        continue
                    if os.path.isfile(file_path):
                        try:
                            bstack1l1l1l1l1ll_opy_ = os.path.getmtime(file_path)
                            timestamp = datetime.fromtimestamp(bstack1l1l1l1l1ll_opy_, tz=timezone.utc).isoformat()
                            file_size = os.path.getsize(file_path)
                            if level == bstack1l111l1_opy_ (u"ࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨ፻"):
                                entry = bstack1ll11ll111l_opy_(
                                    kind=bstack1l111l1_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨ፼"),
                                    message=bstack1l111l1_opy_ (u"ࠧࠨ፽"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l1l111ll1l_opy_=file_size,
                                    bstack1l1l1ll11ll_opy_=bstack1l111l1_opy_ (u"ࠨࡍࡂࡐࡘࡅࡑࡥࡕࡑࡎࡒࡅࡉࠨ፾"),
                                    bstack11lll_opy_=os.path.abspath(file_path),
                                    bstack11l11111l_opy_=bstack1l1l1111ll1_opy_
                                )
                            elif level == bstack1l111l1_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦ፿"):
                                entry = bstack1ll11ll111l_opy_(
                                    kind=bstack1l111l1_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥᎀ"),
                                    message=bstack1l111l1_opy_ (u"ࠤࠥᎁ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l1l111ll1l_opy_=file_size,
                                    bstack1l1l1ll11ll_opy_=bstack1l111l1_opy_ (u"ࠥࡑࡆࡔࡕࡂࡎࡢ࡙ࡕࡒࡏࡂࡆࠥᎂ"),
                                    bstack11lll_opy_=os.path.abspath(file_path),
                                    bstack1l1l11l11l1_opy_=bstack1l1l1111ll1_opy_
                                )
                            bstack1l1l111l1l1_opy_.append(entry)
                            _1l1l1lll1l1_opy_.add(abs_path)
                        except Exception as bstack1l1l1l111ll_opy_:
                            self.logger.error(bstack1l111l1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡳࡣ࡬ࡷࡪࡪࠠࡸࡪࡨࡲࠥࡶࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡼࡿࠥᎃ").format(bstack1l1l1l111ll_opy_))
        except Exception as e:
            self.logger.error(bstack1l111l1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡴࡤ࡭ࡸ࡫ࡤࠡࡹ࡫ࡩࡳࠦࡰࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡽࢀࠦᎄ").format(e))
        event[bstack1l111l1_opy_ (u"ࠨ࡬ࡰࡩࡶࠦᎅ")] = bstack1l1l111l1l1_opy_
class bstack1l1l1l11ll1_opy_(JSONEncoder):
    def __init__(self, **kwargs):
        self.bstack1l1l1ll11l1_opy_ = set()
        kwargs[bstack1l111l1_opy_ (u"ࠢࡴ࡭࡬ࡴࡰ࡫ࡹࡴࠤᎆ")] = True
        super().__init__(**kwargs)
    def default(self, obj):
        return bstack1l1l1111l1l_opy_(obj, self.bstack1l1l1ll11l1_opy_)
def bstack1l1l11llll1_opy_(obj):
    return isinstance(obj, (str, int, float, bool, type(None)))
def bstack1l1l1111l1l_opy_(obj, bstack1l1l1ll11l1_opy_=None, max_depth=3):
    if bstack1l1l1ll11l1_opy_ is None:
        bstack1l1l1ll11l1_opy_ = set()
    if id(obj) in bstack1l1l1ll11l1_opy_ or max_depth <= 0:
        return None
    max_depth -= 1
    bstack1l1l1ll11l1_opy_.add(id(obj))
    if isinstance(obj, datetime):
        return obj.isoformat()
    bstack1l11llll1ll_opy_ = TestFramework.bstack1l1l11111l1_opy_(obj)
    bstack1l1l1l1llll_opy_ = next((k.lower() in bstack1l11llll1ll_opy_.lower() for k in bstack1l1l1ll1lll_opy_.keys()), None)
    if bstack1l1l1l1llll_opy_:
        obj = TestFramework.bstack1l1l11ll11l_opy_(obj, bstack1l1l1ll1lll_opy_[bstack1l1l1l1llll_opy_])
    if not isinstance(obj, dict):
        keys = []
        if hasattr(obj, bstack1l111l1_opy_ (u"ࠣࡡࡢࡷࡱࡵࡴࡴࡡࡢࠦᎇ")):
            keys = getattr(obj, bstack1l111l1_opy_ (u"ࠤࡢࡣࡸࡲ࡯ࡵࡵࡢࡣࠧᎈ"), [])
        elif hasattr(obj, bstack1l111l1_opy_ (u"ࠥࡣࡤࡪࡩࡤࡶࡢࡣࠧᎉ")):
            keys = getattr(obj, bstack1l111l1_opy_ (u"ࠦࡤࡥࡤࡪࡥࡷࡣࡤࠨᎊ"), {}).keys()
        else:
            keys = dir(obj)
        obj = {k: getattr(obj, k, None) for k in keys if not str(k).startswith(bstack1l111l1_opy_ (u"ࠧࡥࠢᎋ"))}
        if not obj and bstack1l11llll1ll_opy_ == bstack1l111l1_opy_ (u"ࠨࡰࡢࡶ࡫ࡰ࡮ࡨ࠮ࡑࡱࡶ࡭ࡽࡖࡡࡵࡪࠥᎌ"):
            obj = {bstack1l111l1_opy_ (u"ࠢࡱࡣࡷ࡬ࠧᎍ"): str(obj)}
    result = {}
    for key, value in obj.items():
        if not bstack1l1l11llll1_opy_(key) or str(key).startswith(bstack1l111l1_opy_ (u"ࠣࡡࠥᎎ")):
            continue
        if value is not None and bstack1l1l11llll1_opy_(value):
            result[key] = value
        elif isinstance(value, dict):
            r = bstack1l1l1111l1l_opy_(value, bstack1l1l1ll11l1_opy_, max_depth)
            if r is not None:
                result[key] = r
        elif isinstance(value, (list, tuple, set, frozenset)):
            result[key] = list(filter(None, [bstack1l1l1111l1l_opy_(o, bstack1l1l1ll11l1_opy_, max_depth) for o in value]))
    return result or None