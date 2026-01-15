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
from datetime import datetime
import os
import threading
from browserstack_sdk.sdk_cli.bstack1lll1ll1l11_opy_ import (
    bstack1lll1l1ll11_opy_,
    bstack1llll11l111_opy_,
    bstack1llll11l11l_opy_,
    bstack1llll11l1ll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll11ll1ll_opy_ import bstack1ll11llll11_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll1lll1111_opy_, bstack1lll11ll1l1_opy_, bstack1ll1llllll1_opy_
from typing import Tuple, Dict, Any, List, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1lll1l1l1l1_opy_ import bstack1ll1l1ll1ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l11111l_opy_ import bstack1lll111lll1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1l111l_opy_ import bstack1lll11l1ll1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1ll111_opy_ import bstack1ll1l1111l1_opy_
from bstack_utils.helper import bstack1ll11l11111_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack11lll1l1ll_opy_ import bstack1ll11ll1ll1_opy_
from bstack_utils import bstack1ll1lll11_opy_
import grpc
import traceback
import json
class bstack1lll111ll11_opy_(bstack1ll1l1ll1ll_opy_):
    bstack1l1llllllll_opy_ = False
    bstack1l1llll1111_opy_ = bstack1l111l1_opy_ (u"ࠨࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࠯ࡹࡨࡦࡩࡸࡩࡷࡧࡵࠦሄ")
    bstack1ll111111l1_opy_ = bstack1l111l1_opy_ (u"ࠢࡳࡧࡰࡳࡹ࡫࠮ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴࠥህ")
    bstack1l1lllll1l1_opy_ = bstack1l111l1_opy_ (u"ࠣࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠ࡫ࡱ࡭ࡹࠨሆ")
    bstack1ll111l1l1l_opy_ = bstack1l111l1_opy_ (u"ࠤࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡ࡬ࡷࡤࡹࡣࡢࡰࡱ࡭ࡳ࡭ࠢሇ")
    bstack1l1lll111ll_opy_ = bstack1l111l1_opy_ (u"ࠥࡨࡷ࡯ࡶࡦࡴࡢ࡬ࡦࡹ࡟ࡶࡴ࡯ࠦለ")
    scripts: Dict[str, Dict[str, str]]
    commands: Dict[str, Dict[str, Dict[str, List[str]]]]
    def __init__(self, bstack1ll1ll1l1l1_opy_, bstack1ll1l11ll1l_opy_):
        super().__init__()
        self.scripts = dict()
        self.commands = dict()
        self.accessibility = False
        self.bstack1l1lll1l1ll_opy_ = False
        self.bstack1l1llll1l1l_opy_ = dict()
        self.bstack1l1111ll1_opy_ = bstack1ll1lll11_opy_.bstack1l11llll1l_opy_(__name__)
        self.bstack1ll1111ll11_opy_ = False
        self.bstack1l1lll1l11l_opy_ = dict()
        if not self.is_enabled():
            return
        self.bstack1l1lll11l1l_opy_ = bstack1ll1l11ll1l_opy_
        bstack1ll1ll1l1l1_opy_.bstack1ll111l11ll_opy_((bstack1lll1l1ll11_opy_.bstack1llll111l1l_opy_, bstack1llll11l111_opy_.PRE), self.bstack1l1ll1ll11l_opy_)
        TestFramework.bstack1ll111l11ll_opy_((bstack1ll1lll1111_opy_.TEST, bstack1lll11ll1l1_opy_.PRE), self.bstack1l1lll11lll_opy_)
        TestFramework.bstack1ll111l11ll_opy_((bstack1ll1lll1111_opy_.TEST, bstack1lll11ll1l1_opy_.POST), self.bstack1l1ll1llll1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1lll11lll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1llllll1_opy_,
        bstack1lll1ll1111_opy_: Tuple[bstack1ll1lll1111_opy_, bstack1lll11ll1l1_opy_],
        *args,
        **kwargs,
    ):
        tags = self._1ll1111111l_opy_(instance, args)
        test_framework = f.bstack1llll1l111l_opy_(instance, TestFramework.bstack1ll111ll111_opy_)
        if self.bstack1l1lll1l1ll_opy_:
            self.bstack1l1llll1l1l_opy_[bstack1l111l1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠦሉ")] = f.bstack1llll1l111l_opy_(instance, TestFramework.bstack1ll111l11l1_opy_)
        if bstack1l111l1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠩሊ") in instance.bstack1l1lll111l1_opy_:
            platform_index = f.bstack1llll1l111l_opy_(instance, TestFramework.bstack1ll1111ll1l_opy_)
            self.accessibility = self.bstack1l1lllllll1_opy_(tags, self.config[bstack1l111l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩላ")][platform_index])
        else:
            capabilities = self.bstack1l1lll11l1l_opy_.bstack1ll11111l11_opy_(f, instance, bstack1lll1ll1111_opy_, *args, **kwargs)
            if not capabilities:
                self.logger.debug(bstack1l111l1_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠤ࡫ࡵࡵ࡯ࡦࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢሌ") + str(kwargs) + bstack1l111l1_opy_ (u"ࠣࠤል"))
                return
            self.accessibility = self.bstack1l1lllllll1_opy_(tags, capabilities)
        if self.bstack1l1lll11l1l_opy_.pages and self.bstack1l1lll11l1l_opy_.pages.values():
            bstack1ll1111l11l_opy_ = list(self.bstack1l1lll11l1l_opy_.pages.values())
            if bstack1ll1111l11l_opy_ and isinstance(bstack1ll1111l11l_opy_[0], (list, tuple)) and bstack1ll1111l11l_opy_[0]:
                bstack1l1llllll1l_opy_ = bstack1ll1111l11l_opy_[0][0]
                if callable(bstack1l1llllll1l_opy_):
                    page = bstack1l1llllll1l_opy_()
                    def bstack1ll111ll1_opy_():
                        self.get_accessibility_results(page, bstack1l111l1_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨሎ"))
                    def bstack1l1lllll11l_opy_():
                        self.get_accessibility_results_summary(page, bstack1l111l1_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢሏ"))
                    setattr(page, bstack1l111l1_opy_ (u"ࠦ࡬࡫ࡴࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡒࡦࡵࡸࡰࡹࡹࠢሐ"), bstack1ll111ll1_opy_)
                    setattr(page, bstack1l111l1_opy_ (u"ࠧ࡭ࡥࡵࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡓࡧࡶࡹࡱࡺࡓࡶ࡯ࡰࡥࡷࡿࠢሑ"), bstack1l1lllll11l_opy_)
        self.logger.debug(bstack1l111l1_opy_ (u"ࠨࡳࡩࡱࡸࡰࡩࠦࡲࡶࡰࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡺࡦࡲࡵࡦ࠿ࠥሒ") + str(self.accessibility) + bstack1l111l1_opy_ (u"ࠢࠣሓ"))
    def bstack1l1ll1ll11l_opy_(
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
            bstack1ll11llll_opy_ = datetime.now()
            self.bstack1l1llll11ll_opy_(f, exec, *args, **kwargs)
            instance, method_name = exec
            instance.bstack111lll11l_opy_(bstack1l111l1_opy_ (u"ࠣࡣ࠴࠵ࡾࡀࡩ࡯࡫ࡷࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡨࡵ࡮ࡧ࡫ࡪࠦሔ"), datetime.now() - bstack1ll11llll_opy_)
            if (
                not f.bstack1ll11111111_opy_(method_name)
                or f.bstack1ll111l1ll1_opy_(method_name, *args)
                or f.bstack1l1ll1lll1l_opy_(method_name, *args)
            ):
                return
            if not f.bstack1llll1l111l_opy_(instance, bstack1lll111ll11_opy_.bstack1l1lllll1l1_opy_, False):
                if not bstack1lll111ll11_opy_.bstack1l1llllllll_opy_:
                    self.logger.warning(bstack1l111l1_opy_ (u"ࠤ࡞ࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࡁࠧሕ") + str(f.platform_index) + bstack1l111l1_opy_ (u"ࠥࡡࠥࡧ࠱࠲ࡻࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠢ࡫ࡥࡻ࡫ࠠ࡯ࡱࡷࠤࡧ࡫ࡥ࡯ࠢࡶࡩࡹࠦࡦࡰࡴࠣࡸ࡭࡯ࡳࠡࡵࡨࡷࡸ࡯࡯࡯ࠤሖ"))
                    bstack1lll111ll11_opy_.bstack1l1llllllll_opy_ = True
                return
            bstack1l1lll1111l_opy_ = self.scripts.get(f.framework_name, {})
            if not bstack1l1lll1111l_opy_:
                platform_index = f.bstack1llll1l111l_opy_(instance, bstack1ll11llll11_opy_.bstack1ll1111ll1l_opy_, 0)
                self.logger.debug(bstack1l111l1_opy_ (u"ࠦࡳࡵࠠࡢ࠳࠴ࡽࠥࡹࡣࡳ࡫ࡳࡸࡸࠦࡦࡰࡴࠣࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࡁࢀࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࢃࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࠤሗ") + str(f.framework_name) + bstack1l111l1_opy_ (u"ࠧࠨመ"))
                return
            command_name = f.bstack1l1lll11ll1_opy_(*args)
            if not command_name:
                self.logger.debug(bstack1l111l1_opy_ (u"ࠨ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࡤࡱࡰࡱࡦࡴࡤࡠࡰࡤࡱࡪࠦࡦࡰࡴࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࢀ࡬࠮ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࡾࠢࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫࠽ࠣሙ") + str(method_name) + bstack1l111l1_opy_ (u"ࠢࠣሚ"))
                return
            bstack1l1lllll111_opy_ = f.bstack1llll1l111l_opy_(instance, bstack1lll111ll11_opy_.bstack1l1lll111ll_opy_, False)
            if command_name == bstack1l111l1_opy_ (u"ࠣࡩࡨࡸࠧማ") and not bstack1l1lllll111_opy_:
                f.bstack1llll1111l1_opy_(instance, bstack1lll111ll11_opy_.bstack1l1lll111ll_opy_, True)
                bstack1l1lllll111_opy_ = True
            if not bstack1l1lllll111_opy_ and not self.bstack1l1lll1l1ll_opy_:
                self.logger.debug(bstack1l111l1_opy_ (u"ࠤࡱࡳ࡛ࠥࡒࡍࠢ࡯ࡳࡦࡪࡥࡥࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࡿ࡫࠴ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࡽࠡࡥࡲࡱࡲࡧ࡮ࡥࡡࡱࡥࡲ࡫࠽ࠣሜ") + str(command_name) + bstack1l111l1_opy_ (u"ࠥࠦም"))
                return
            scripts_to_run = self.commands.get(f.framework_name, {}).get(method_name, {}).get(command_name, [])
            if not scripts_to_run:
                self.logger.debug(bstack1l111l1_opy_ (u"ࠦࡳࡵࠠࡢ࠳࠴ࡽࠥࡹࡣࡳ࡫ࡳࡸࡸࠦࡦࡰࡴࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࢀ࡬࠮ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࡾࠢࡦࡳࡲࡳࡡ࡯ࡦࡢࡲࡦࡳࡥ࠾ࠤሞ") + str(command_name) + bstack1l111l1_opy_ (u"ࠧࠨሟ"))
                return
            self.logger.info(bstack1l111l1_opy_ (u"ࠨࡲࡶࡰࡱ࡭ࡳ࡭ࠠࡼ࡮ࡨࡲ࠭ࡹࡣࡳ࡫ࡳࡸࡸࡥࡴࡰࡡࡵࡹࡳ࠯ࡽࠡࡵࡦࡶ࡮ࡶࡴࡴࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࡿ࡫࠴ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࡽࠡࡥࡲࡱࡲࡧ࡮ࡥࡡࡱࡥࡲ࡫࠽ࠣሠ") + str(command_name) + bstack1l111l1_opy_ (u"ࠢࠣሡ"))
            scripts = [(s, bstack1l1lll1111l_opy_[s]) for s in scripts_to_run if s in bstack1l1lll1111l_opy_]
            for script_name, bstack1l1lll1llll_opy_ in scripts:
                try:
                    bstack1ll11llll_opy_ = datetime.now()
                    if script_name == bstack1l111l1_opy_ (u"ࠣࡵࡦࡥࡳࠨሢ"):
                        result = self.perform_scan(driver, method=command_name, framework_name=f.framework_name)
                        try:
                            bstack111l1l1l_opy_ = {
                                bstack1l111l1_opy_ (u"ࠤࡵࡩࡶࡻࡥࡴࡶࠥሣ"): {
                                    bstack1l111l1_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࠦሤ"): bstack1l111l1_opy_ (u"ࠦࡆ࠷࠱࡚ࡡࡖࡇࡆࡔࠢሥ"),
                                    bstack1l111l1_opy_ (u"ࠧࡶࡡࡳࡣࡰࡩࡹ࡫ࡲࡴࠤሦ"): [
                                        {
                                            bstack1l111l1_opy_ (u"ࠨ࡭ࡦࡶ࡫ࡳࡩࠨሧ"): command_name
                                        }
                                    ]
                                },
                                bstack1l111l1_opy_ (u"ࠢࡳࡧࡶࡴࡴࡴࡳࡦࠤረ"): {
                                    bstack1l111l1_opy_ (u"ࠣࡤࡲࡨࡾࠨሩ"): {
                                        bstack1l111l1_opy_ (u"ࠤࡰࡷ࡬ࠨሪ"): result.get(bstack1l111l1_opy_ (u"ࠥࡱࡸ࡭ࠢራ"), bstack1l111l1_opy_ (u"ࠦࠧሬ")) if isinstance(result, dict) else bstack1l111l1_opy_ (u"ࠧࠨር"),
                                        bstack1l111l1_opy_ (u"ࠨࡳࡶࡥࡦࡩࡸࡹࠢሮ"): result.get(bstack1l111l1_opy_ (u"ࠢࡴࡷࡦࡧࡪࡹࡳࠣሯ"), True) if isinstance(result, dict) else True
                                    }
                                }
                            }
                            self.bstack1l1111ll1_opy_.info(json.dumps(bstack111l1l1l_opy_, separators=(bstack1l111l1_opy_ (u"ࠣ࠮ࠥሰ"), bstack1l111l1_opy_ (u"ࠤ࠽ࠦሱ"))))
                        except Exception as bstack1lll11111l_opy_:
                            self.logger.debug(bstack1l111l1_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡬ࡰࡩࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡨࡧ࡮ࠡࡦࡤࡸࡦࡀࠠࠣሲ") + str(bstack1lll11111l_opy_) + bstack1l111l1_opy_ (u"ࠦࠧሳ"))
                    instance.bstack111lll11l_opy_(bstack1l111l1_opy_ (u"ࠧࡧ࠱࠲ࡻ࠽ࠦሴ") + script_name, datetime.now() - bstack1ll11llll_opy_)
                    if isinstance(result, dict) and not result.get(bstack1l111l1_opy_ (u"ࠨࡳࡶࡥࡦࡩࡸࡹࠢስ"), True):
                        self.logger.warning(bstack1l111l1_opy_ (u"ࠢࡴ࡭࡬ࡴࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡴࡧࠡࡴࡨࡱࡦ࡯࡮ࡪࡰࡪࠤࡸࡩࡲࡪࡲࡷࡷ࠿ࠦࠢሶ") + str(result) + bstack1l111l1_opy_ (u"ࠣࠤሷ"))
                        break
                except Exception as e:
                    self.logger.error(bstack1l111l1_opy_ (u"ࠤࡨࡶࡷࡵࡲࠡࡧࡻࡩࡨࡻࡴࡪࡰࡪࠤࡸࡩࡲࡪࡲࡷࡁࢀࡹࡣࡳ࡫ࡳࡸࡤࡴࡡ࡮ࡧࢀࠤࡪࡸࡲࡰࡴࡀࠦሸ") + str(e) + bstack1l111l1_opy_ (u"ࠥࠦሹ"))
        except Exception as e:
            self.logger.error(bstack1l111l1_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡦࡺࡨࡧࡺࡺࡥࠡࡧࡵࡶࡴࡸ࠽ࠣሺ") + str(e) + bstack1l111l1_opy_ (u"ࠧࠨሻ"))
    def bstack1l1ll1llll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1llllll1_opy_,
        bstack1lll1ll1111_opy_: Tuple[bstack1ll1lll1111_opy_, bstack1lll11ll1l1_opy_],
        *args,
        **kwargs,
    ):
        tags = self._1ll1111111l_opy_(instance, args)
        capabilities = self.bstack1l1lll11l1l_opy_.bstack1ll11111l11_opy_(f, instance, bstack1lll1ll1111_opy_, *args, **kwargs)
        self.accessibility = self.bstack1l1lllllll1_opy_(tags, capabilities)
        if not self.accessibility:
            self.logger.debug(bstack1l111l1_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠࡢ࠳࠴ࡽࠥࡴ࡯ࡵࠢࡨࡲࡦࡨ࡬ࡦࡦࠥሼ"))
            return
        driver = self.bstack1l1lll11l1l_opy_.bstack1ll11111l1l_opy_(f, instance, bstack1lll1ll1111_opy_, *args, **kwargs)
        test_name = f.bstack1llll1l111l_opy_(instance, TestFramework.bstack1l1llll111l_opy_)
        if not test_name:
            self.logger.debug(bstack1l111l1_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡷࡩࡸࡺࠠ࡯ࡣࡰࡩࠧሽ"))
            return
        test_uuid = f.bstack1llll1l111l_opy_(instance, TestFramework.bstack1ll111l11l1_opy_)
        if not test_uuid:
            self.logger.debug(bstack1l111l1_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡷࡸ࡭ࡩࠨሾ"))
            return
        if isinstance(self.bstack1l1lll11l1l_opy_, bstack1lll11l1ll1_opy_):
            framework_name = bstack1l111l1_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ሿ")
        else:
            framework_name = bstack1l111l1_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࠬቀ")
        self.bstack1lll1l1l_opy_(driver, test_name, framework_name, test_uuid)
    def perform_scan(self, driver: object, method: Union[None, str], framework_name: str):
        bstack1ll111ll11l_opy_ = bstack1ll11ll1ll1_opy_.bstack1ll1111l1l1_opy_(EVENTS.bstack11ll111111_opy_.value)
        if not self.accessibility:
            self.logger.debug(bstack1l111l1_opy_ (u"ࠦࡵ࡫ࡲࡧࡱࡵࡱࡤࡹࡣࡢࡰ࠽ࠤࡦ࠷࠱ࡺࠢࡱࡳࡹࠦࡥ࡯ࡣࡥࡰࡪࡪࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࢀࠤࠧቁ"))
            return
        bstack1ll11llll_opy_ = datetime.now()
        bstack1l1lll1llll_opy_ = self.scripts.get(framework_name, {}).get(bstack1l111l1_opy_ (u"ࠧࡹࡣࡢࡰࠥቂ"), None)
        if not bstack1l1lll1llll_opy_:
            self.logger.debug(bstack1l111l1_opy_ (u"ࠨࡰࡦࡴࡩࡳࡷࡳ࡟ࡴࡥࡤࡲ࠿ࠦ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࠨࡵࡦࡥࡳ࠭ࠠࡴࡥࡵ࡭ࡵࡺࠠࡧࡱࡵࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࠨቃ") + str(framework_name) + bstack1l111l1_opy_ (u"ࠢࠡࠤቄ"))
            return
        if self.bstack1l1lll1l1ll_opy_:
            arg = dict()
            arg[bstack1l111l1_opy_ (u"ࠣ࡯ࡨࡸ࡭ࡵࡤࠣቅ")] = method if method else bstack1l111l1_opy_ (u"ࠤࠥቆ")
            arg[bstack1l111l1_opy_ (u"ࠥࡸ࡭࡚ࡥࡴࡶࡕࡹࡳ࡛ࡵࡪࡦࠥቇ")] = self.bstack1l1llll1l1l_opy_[bstack1l111l1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠦቈ")]
            arg[bstack1l111l1_opy_ (u"ࠧࡺࡨࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠥ቉")] = self.bstack1l1llll1l1l_opy_[bstack1l111l1_opy_ (u"ࠨࡴࡦࡵࡷ࡬ࡺࡨ࡟ࡣࡷ࡬ࡰࡩࡥࡵࡶ࡫ࡧࠦቊ")]
            arg[bstack1l111l1_opy_ (u"ࠢࡢࡷࡷ࡬ࡍ࡫ࡡࡥࡧࡵࠦቋ")] = self.bstack1l1llll1l1l_opy_[bstack1l111l1_opy_ (u"ࠣࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡕࡱ࡮ࡩࡳࠨቌ")]
            arg[bstack1l111l1_opy_ (u"ࠤࡷ࡬ࡏࡽࡴࡕࡱ࡮ࡩࡳࠨቍ")] = self.bstack1l1llll1l1l_opy_[bstack1l111l1_opy_ (u"ࠥࡸ࡭ࡥࡪࡸࡶࡢࡸࡴࡱࡥ࡯ࠤ቎")]
            arg[bstack1l111l1_opy_ (u"ࠦࡸࡩࡡ࡯ࡖ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠦ቏")] = str(int(datetime.now().timestamp() * 1000))
            bstack1ll11111lll_opy_ = self.bstack1l1lll1lll1_opy_(bstack1l111l1_opy_ (u"ࠧࡹࡣࡢࡰࠥቐ"), self.bstack1l1llll1l1l_opy_[bstack1l111l1_opy_ (u"ࠨࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩࠨቑ")])
            if bstack1l111l1_opy_ (u"ࠢࡤࡧࡱࡸࡷࡧ࡬ࡂࡷࡷ࡬࡙ࡵ࡫ࡦࡰࠥቒ") in bstack1ll11111lll_opy_:
                bstack1ll11111lll_opy_ = bstack1ll11111lll_opy_.copy()
                bstack1ll11111lll_opy_[bstack1l111l1_opy_ (u"ࠣࡥࡨࡲࡹࡸࡡ࡭ࡃࡸࡸ࡭ࡎࡥࡢࡦࡨࡶࠧቓ")] = bstack1ll11111lll_opy_.pop(bstack1l111l1_opy_ (u"ࠤࡦࡩࡳࡺࡲࡢ࡮ࡄࡹࡹ࡮ࡔࡰ࡭ࡨࡲࠧቔ"))
            arg = bstack1ll11l11111_opy_(arg, bstack1ll11111lll_opy_)
            bstack1ll111l1l11_opy_ = bstack1l1lll1llll_opy_ % json.dumps(arg)
            driver.execute_script(bstack1ll111l1l11_opy_)
            return
        instance = bstack1llll11l11l_opy_.bstack1llll11ll1l_opy_(driver)
        if instance:
            if not bstack1llll11l11l_opy_.bstack1llll1l111l_opy_(instance, bstack1lll111ll11_opy_.bstack1ll111l1l1l_opy_, False):
                bstack1llll11l11l_opy_.bstack1llll1111l1_opy_(instance, bstack1lll111ll11_opy_.bstack1ll111l1l1l_opy_, True)
            else:
                self.logger.info(bstack1l111l1_opy_ (u"ࠥࡴࡪࡸࡦࡰࡴࡰࡣࡸࡩࡡ࡯࠼ࠣࡥࡱࡸࡥࡢࡦࡼࠤ࡮ࡴࠠࡱࡴࡲ࡫ࡷ࡫ࡳࡴࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࡿ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࠦ࡭ࡦࡶ࡫ࡳࡩࡃࠢቕ") + str(method) + bstack1l111l1_opy_ (u"ࠦࠧቖ"))
                return
        self.logger.info(bstack1l111l1_opy_ (u"ࠧࡶࡥࡳࡨࡲࡶࡲࡥࡳࡤࡣࡱ࠾ࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࡻࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࡾࠢࡰࡩࡹ࡮࡯ࡥ࠿ࠥ቗") + str(method) + bstack1l111l1_opy_ (u"ࠨࠢቘ"))
        if framework_name == bstack1l111l1_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫ቙"):
            result = self.bstack1l1lll11l1l_opy_.bstack1ll111l1lll_opy_(driver, bstack1l1lll1llll_opy_)
        else:
            result = driver.execute_async_script(bstack1l1lll1llll_opy_, {bstack1l111l1_opy_ (u"ࠣ࡯ࡨࡸ࡭ࡵࡤࠣቚ"): method if method else bstack1l111l1_opy_ (u"ࠤࠥቛ")})
        bstack1ll11ll1ll1_opy_.end(EVENTS.bstack11ll111111_opy_.value, bstack1ll111ll11l_opy_+bstack1l111l1_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥቜ"), bstack1ll111ll11l_opy_+bstack1l111l1_opy_ (u"ࠦ࠿࡫࡮ࡥࠤቝ"), True, None, command=method)
        if instance:
            bstack1llll11l11l_opy_.bstack1llll1111l1_opy_(instance, bstack1lll111ll11_opy_.bstack1ll111l1l1l_opy_, False)
            instance.bstack111lll11l_opy_(bstack1l111l1_opy_ (u"ࠧࡧ࠱࠲ࡻ࠽ࡴࡪࡸࡦࡰࡴࡰࡣࡸࡩࡡ࡯ࠤ቞"), datetime.now() - bstack1ll11llll_opy_)
        return result
        def bstack1ll111llll1_opy_(self, driver: object, framework_name, result_type: str):
            self.bstack1l1lll1l111_opy_()
            req = structs.AccessibilityResultRequest()
            req.bin_session_id = self.bin_session_id
            req.bstack1ll111lll1l_opy_ = self.bstack1l1llll1l1l_opy_[bstack1l111l1_opy_ (u"ࠨࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩࠨ቟")]
            req.result_type = result_type
            req.session_id = self.bin_session_id
            try:
                r = self.bstack1lll11l1l1l_opy_.AccessibilityResult(req)
                if not r.success:
                    self.logger.debug(bstack1l111l1_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࠤበ") + str(r) + bstack1l111l1_opy_ (u"ࠣࠤቡ"))
                else:
                    bstack1l1ll1ll1l1_opy_ = json.loads(r.bstack1ll1111llll_opy_.decode(bstack1l111l1_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨቢ")))
                    if result_type == bstack1l111l1_opy_ (u"ࠪ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࠧባ"):
                        return bstack1l1ll1ll1l1_opy_.get(bstack1l111l1_opy_ (u"ࠦࡩࡧࡴࡢࠤቤ"), [])
                    else:
                        return bstack1l1ll1ll1l1_opy_.get(bstack1l111l1_opy_ (u"ࠧࡪࡡࡵࡣࠥብ"), {})
            except grpc.RpcError as e:
                self.logger.error(bstack1l111l1_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡨࡨࡸࡨ࡮ࡩ࡯ࡩࠣ࡫ࡪࡺ࡟ࡢࡲࡳࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡷ࡫ࡳࡶ࡮ࡷࠤ࡫ࡸ࡯࡮ࠢࡦࡰ࡮ࡀࠠࠣቦ") + str(e) + bstack1l111l1_opy_ (u"ࠢࠣቧ"))
    @measure(event_name=EVENTS.bstack1111ll1l1_opy_, stage=STAGE.bstack11l11l11l1_opy_)
    def get_accessibility_results(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack1l111l1_opy_ (u"ࠣࡩࡨࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡸࡥࡴࡷ࡯ࡸࡸࡀࠠࡢ࠳࠴ࡽࠥࡴ࡯ࡵࠢࡨࡲࡦࡨ࡬ࡦࡦࠥቨ"))
            return
        if self.bstack1l1lll1l1ll_opy_:
            self.logger.debug(bstack1l111l1_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤ࡫ࡵࡲࠡࡣࡳࡴࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬቩ"))
            self.perform_scan(driver, method=None, framework_name=framework_name)
            return self.bstack1ll111llll1_opy_(driver, framework_name, bstack1l111l1_opy_ (u"ࠥ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࠢቪ"))
        bstack1l1lll1llll_opy_ = self.scripts.get(framework_name, {}).get(bstack1l111l1_opy_ (u"ࠦ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࠣቫ"), None)
        if not bstack1l1lll1llll_opy_:
            self.logger.debug(bstack1l111l1_opy_ (u"ࠧࡳࡩࡴࡵ࡬ࡲ࡬ࠦࠧࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࠫࠥࡹࡣࡳ࡫ࡳࡸࠥ࡬࡯ࡳࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࠦቬ") + str(framework_name) + bstack1l111l1_opy_ (u"ࠨࠢቭ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack1ll11llll_opy_ = datetime.now()
        if framework_name == bstack1l111l1_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫቮ"):
            result = self.bstack1l1lll11l1l_opy_.bstack1ll111l1lll_opy_(driver, bstack1l1lll1llll_opy_)
        else:
            result = driver.execute_async_script(bstack1l1lll1llll_opy_)
        instance = bstack1llll11l11l_opy_.bstack1llll11ll1l_opy_(driver)
        if instance:
            instance.bstack111lll11l_opy_(bstack1l111l1_opy_ (u"ࠣࡣ࠴࠵ࡾࡀࡧࡦࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡶࡪࡹࡵ࡭ࡶࡶࠦቯ"), datetime.now() - bstack1ll11llll_opy_)
        return result
    @measure(event_name=EVENTS.bstack11l111lll1_opy_, stage=STAGE.bstack11l11l11l1_opy_)
    def get_accessibility_results_summary(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack1l111l1_opy_ (u"ࠤࡪࡩࡹࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡲࡦࡵࡸࡰࡹࡹ࡟ࡴࡷࡰࡱࡦࡸࡹ࠻ࠢࡤ࠵࠶ࡿࠠ࡯ࡱࡷࠤࡪࡴࡡࡣ࡮ࡨࡨࠧተ"))
            return
        if self.bstack1l1lll1l1ll_opy_:
            self.perform_scan(driver, method=None, framework_name=framework_name)
            return self.bstack1ll111llll1_opy_(driver, framework_name, bstack1l111l1_opy_ (u"ࠪ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠧቱ"))
        bstack1l1lll1llll_opy_ = self.scripts.get(framework_name, {}).get(bstack1l111l1_opy_ (u"ࠦ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࡔࡷࡰࡱࡦࡸࡹࠣቲ"), None)
        if not bstack1l1lll1llll_opy_:
            self.logger.debug(bstack1l111l1_opy_ (u"ࠧࡳࡩࡴࡵ࡬ࡲ࡬ࠦࠧࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࡗࡺࡳ࡭ࡢࡴࡼࠫࠥࡹࡣࡳ࡫ࡳࡸࠥ࡬࡯ࡳࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࠦታ") + str(framework_name) + bstack1l111l1_opy_ (u"ࠨࠢቴ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack1ll11llll_opy_ = datetime.now()
        if framework_name == bstack1l111l1_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫት"):
            result = self.bstack1l1lll11l1l_opy_.bstack1ll111l1lll_opy_(driver, bstack1l1lll1llll_opy_)
        else:
            result = driver.execute_async_script(bstack1l1lll1llll_opy_)
        instance = bstack1llll11l11l_opy_.bstack1llll11ll1l_opy_(driver)
        if instance:
            instance.bstack111lll11l_opy_(bstack1l111l1_opy_ (u"ࠣࡣ࠴࠵ࡾࡀࡧࡦࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡶࡪࡹࡵ࡭ࡶࡶࡣࡸࡻ࡭࡮ࡣࡵࡽࠧቶ"), datetime.now() - bstack1ll11llll_opy_)
        return result
    @measure(event_name=EVENTS.bstack1l1llll11l1_opy_, stage=STAGE.bstack11l11l11l1_opy_)
    def bstack1l1ll1lllll_opy_(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str,
    ):
        self.bstack1l1lll1l111_opy_()
        req = structs.AccessibilityConfigRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        try:
            r = self.bstack1lll11l1l1l_opy_.AccessibilityConfig(req)
            if not r.success:
                self.logger.debug(bstack1l111l1_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦቷ") + str(r) + bstack1l111l1_opy_ (u"ࠥࠦቸ"))
            else:
                self.bstack1l1llll1l11_opy_(framework_name, r)
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l111l1_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤቹ") + str(e) + bstack1l111l1_opy_ (u"ࠧࠨቺ"))
            traceback.print_exc()
            raise e
    def bstack1l1llll1l11_opy_(self, framework_name: str, result: structs.AccessibilityConfigResponse) -> bool:
        if not result.success or not result.accessibility.success:
            self.logger.debug(bstack1l111l1_opy_ (u"ࠨ࡬ࡰࡣࡧࡣࡨࡵ࡮ࡧ࡫ࡪ࠾ࠥࡧ࠱࠲ࡻࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩࠨቻ"))
            return False
        if result.accessibility.is_app_accessibility:
            self.bstack1l1lll1l1ll_opy_ = result.accessibility.is_app_accessibility
        if result.testhub.build_hashed_id:
            self.bstack1l1llll1l1l_opy_[bstack1l111l1_opy_ (u"ࠢࡵࡧࡶࡸ࡭ࡻࡢࡠࡤࡸ࡭ࡱࡪ࡟ࡶࡷ࡬ࡨࠧቼ")] = result.testhub.build_hashed_id
        if result.testhub.jwt:
            self.bstack1l1llll1l1l_opy_[bstack1l111l1_opy_ (u"ࠣࡶ࡫ࡣ࡯ࡽࡴࡠࡶࡲ࡯ࡪࡴࠢች")] = result.testhub.jwt
        if result.accessibility.options:
            options = result.accessibility.options
            if options.capabilities:
                for caps in options.capabilities:
                    self.bstack1l1llll1l1l_opy_[caps.name] = caps.value
            if options.scripts:
                self.scripts[framework_name] = {row.name: row.command for row in options.scripts}
            if options.commands_to_wrap and options.commands_to_wrap.commands:
                scripts_to_run = [s for s in options.commands_to_wrap.scripts_to_run]
                if not scripts_to_run:
                    return False
                bstack1l1ll1ll1ll_opy_ = dict()
                for command in options.commands_to_wrap.commands:
                    if command.library == self.bstack1l1llll1111_opy_ and command.module == self.bstack1ll111111l1_opy_:
                        if command.method and not command.method in bstack1l1ll1ll1ll_opy_:
                            bstack1l1ll1ll1ll_opy_[command.method] = dict()
                        if command.name and not command.name in bstack1l1ll1ll1ll_opy_[command.method]:
                            bstack1l1ll1ll1ll_opy_[command.method][command.name] = list()
                        bstack1l1ll1ll1ll_opy_[command.method][command.name].extend(scripts_to_run)
                self.commands[framework_name] = bstack1l1ll1ll1ll_opy_
        return bool(self.commands.get(framework_name, None))
    def bstack1l1llll11ll_opy_(
        self,
        f: bstack1ll11llll11_opy_,
        exec: Tuple[bstack1llll11l1ll_opy_, str],
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if isinstance(self.bstack1l1lll11l1l_opy_, bstack1lll11l1ll1_opy_) and method_name != bstack1l111l1_opy_ (u"ࠩࡦࡳࡳࡴࡥࡤࡶࠪቾ"):
            return
        if bstack1llll11l11l_opy_.bstack1lll1ll111l_opy_(instance, bstack1lll111ll11_opy_.bstack1l1lllll1l1_opy_):
            return
        if f.bstack1ll11111ll1_opy_(method_name, *args):
            bstack1ll111ll1ll_opy_ = False
            desired_capabilities = f.bstack1l1llll1lll_opy_(instance)
            if isinstance(desired_capabilities, dict):
                hub_url = f.bstack1ll1111l111_opy_(instance)
                platform_index = f.bstack1llll1l111l_opy_(instance, bstack1ll11llll11_opy_.bstack1ll1111ll1l_opy_, 0)
                bstack1ll111111ll_opy_ = datetime.now()
                r = self.bstack1l1ll1lllll_opy_(platform_index, f.framework_name, f.framework_version, hub_url)
                instance.bstack111lll11l_opy_(bstack1l111l1_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡥࡲࡲ࡫࡯ࡧࠣቿ"), datetime.now() - bstack1ll111111ll_opy_)
                bstack1ll111ll1ll_opy_ = r.success
            else:
                self.logger.error(bstack1l111l1_opy_ (u"ࠦࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥࡪࡥࡴ࡫ࡵࡩࡩࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࡂࠨኀ") + str(desired_capabilities) + bstack1l111l1_opy_ (u"ࠧࠨኁ"))
            f.bstack1llll1111l1_opy_(instance, bstack1lll111ll11_opy_.bstack1l1lllll1l1_opy_, bstack1ll111ll1ll_opy_)
    def bstack11l1l11111_opy_(self, test_tags):
        bstack1l1ll1lllll_opy_ = self.config.get(bstack1l111l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ኂ"))
        if not bstack1l1ll1lllll_opy_:
            return True
        try:
            include_tags = bstack1l1ll1lllll_opy_[bstack1l111l1_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬኃ")] if bstack1l111l1_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ኄ") in bstack1l1ll1lllll_opy_ and isinstance(bstack1l1ll1lllll_opy_[bstack1l111l1_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧኅ")], list) else []
            exclude_tags = bstack1l1ll1lllll_opy_[bstack1l111l1_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨኆ")] if bstack1l111l1_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩኇ") in bstack1l1ll1lllll_opy_ and isinstance(bstack1l1ll1lllll_opy_[bstack1l111l1_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪኈ")], list) else []
            excluded = any(tag in exclude_tags for tag in test_tags)
            included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
            return not excluded and included
        except Exception as error:
            self.logger.debug(bstack1l111l1_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡻࡧ࡬ࡪࡦࡤࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤ࡫ࡵࡲࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡤࡨࡪࡴࡸࡥࠡࡵࡦࡥࡳࡴࡩ࡯ࡩ࠱ࠤࡊࡸࡲࡰࡴࠣ࠾ࠥࠨ኉") + str(error))
        return False
    def bstack11l11llll_opy_(self, caps):
        try:
            if self.bstack1l1lll1l1ll_opy_:
                bstack1ll1111l1ll_opy_ = caps.get(bstack1l111l1_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨኊ"))
                if bstack1ll1111l1ll_opy_ is not None and str(bstack1ll1111l1ll_opy_).lower() == bstack1l111l1_opy_ (u"ࠣࡣࡱࡨࡷࡵࡩࡥࠤኋ"):
                    bstack1ll111l1111_opy_ = caps.get(bstack1l111l1_opy_ (u"ࠤࡤࡴࡵ࡯ࡵ࡮࠼ࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦኌ")) or caps.get(bstack1l111l1_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧኍ"))
                    if bstack1ll111l1111_opy_ is not None and int(bstack1ll111l1111_opy_) < 11:
                        self.logger.warning(bstack1l111l1_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡆࡴࡤࡳࡱ࡬ࡨࠥ࠷࠱ࠡࡣࡱࡨࠥࡧࡢࡰࡸࡨ࠲ࠥࡉࡵࡳࡴࡨࡲࡹࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡀࠦ኎") + str(bstack1ll111l1111_opy_) + bstack1l111l1_opy_ (u"ࠧࠨ኏"))
                        return False
                return True
            bstack1l1lll1ll1l_opy_ = caps.get(bstack1l111l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧነ"), {}).get(bstack1l111l1_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫኑ"), caps.get(bstack1l111l1_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨኒ"), bstack1l111l1_opy_ (u"ࠩࠪና")))
            if bstack1l1lll1ll1l_opy_:
                self.logger.warning(bstack1l111l1_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡈࡪࡹ࡫ࡵࡱࡳࠤࡧࡸ࡯ࡸࡵࡨࡶࡸ࠴ࠢኔ"))
                return False
            browser = caps.get(bstack1l111l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩን"), bstack1l111l1_opy_ (u"ࠬ࠭ኖ")).lower()
            if browser != bstack1l111l1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ኗ"):
                self.logger.warning(bstack1l111l1_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡄࡪࡵࡳࡲ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࡴ࠰ࠥኘ"))
                return False
            bstack1l1lll11111_opy_ = bstack1ll111lllll_opy_
            if not self.config.get(bstack1l111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪኙ")) or self.config.get(bstack1l111l1_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠭ኚ")):
                bstack1l1lll11111_opy_ = bstack1ll1111lll1_opy_
            browser_version = caps.get(bstack1l111l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫኛ"))
            if not browser_version:
                browser_version = caps.get(bstack1l111l1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬኜ"), {}).get(bstack1l111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ኝ"), bstack1l111l1_opy_ (u"࠭ࠧኞ"))
            bstack1l1lll1ll11_opy_ = str(browser_version).lower() if browser_version is not None else bstack1l111l1_opy_ (u"ࠧࠨኟ")
            if bstack1l1lll1ll11_opy_:
                if bstack1l1lll1ll11_opy_.startswith(bstack1l111l1_opy_ (u"ࠨ࡮ࡤࡸࡪࡹࡴࠨአ")):
                    if bstack1l1lll1ll11_opy_.startswith(bstack1l111l1_opy_ (u"ࠩ࡯ࡥࡹ࡫ࡳࡵ࠯ࠪኡ")):
                        bstack1l1llll1ll1_opy_ = bstack1l1lll1ll11_opy_[len(bstack1l111l1_opy_ (u"ࠪࡰࡦࡺࡥࡴࡶ࠰ࠫኢ")):]
                        if bstack1l1llll1ll1_opy_ and not bstack1l1llll1ll1_opy_.isdigit():
                            self.logger.warning(bstack1l111l1_opy_ (u"ࠦࡎࡴࡶࡢ࡮࡬ࡨࠥࡨࡲࡰࡹࡶࡩࡷࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡧࡱࡵࡱࡦࡺࠠࠨࠤኣ") + str(browser_version) + bstack1l111l1_opy_ (u"ࠧ࠭࠻ࠡࡧࡻࡴࡪࡩࡴࡦࡦࠣࠫࡱࡧࡴࡦࡵࡷࠫࠥࡵࡲࠡࠩ࡯ࡥࡹ࡫ࡳࡵ࠯࠿ࡲࡺࡳࡢࡦࡴࡁࠫ࠳ࠨኤ"))
                            return False
                else:
                    try:
                        if int(bstack1l1lll1ll11_opy_.split(bstack1l111l1_opy_ (u"࠭࠮ࠨእ"))[0]) <= bstack1l1lll11111_opy_:
                            self.logger.warning(bstack1l111l1_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡄࡪࡵࡳࡲ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡪࡶࡪࡧࡴࡦࡴࠣࡸ࡭ࡧ࡮ࠡࠤኦ") + str(bstack1l1lll11111_opy_) + bstack1l111l1_opy_ (u"ࠣ࠰ࠥኧ"))
                            return False
                    except (ValueError, IndexError) as e:
                        self.logger.debug(bstack1l111l1_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡶࡡࡳࡵࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࠧࡼࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࢀࠫ࠿ࠦࠢከ") + str(e) + bstack1l111l1_opy_ (u"ࠥࠦኩ"))
            bstack1l1llllll11_opy_ = caps.get(bstack1l111l1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬኪ"), {}).get(bstack1l111l1_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬካ"))
            if not bstack1l1llllll11_opy_:
                bstack1l1llllll11_opy_ = caps.get(bstack1l111l1_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫኬ"), {})
            if bstack1l1llllll11_opy_ and bstack1l111l1_opy_ (u"ࠧ࠮࠯࡫ࡩࡦࡪ࡬ࡦࡵࡶࠫክ") in bstack1l1llllll11_opy_.get(bstack1l111l1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ኮ"), []):
                self.logger.warning(bstack1l111l1_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡳࡵࡴࠡࡴࡸࡲࠥࡵ࡮ࠡ࡮ࡨ࡫ࡦࡩࡹࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠢࡖࡻ࡮ࡺࡣࡩࠢࡷࡳࠥࡴࡥࡸࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦࠢࡲࡶࠥࡧࡶࡰ࡫ࡧࠤࡺࡹࡩ࡯ࡩࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧ࠱ࠦኯ"))
                return False
            return True
        except Exception as error:
            self.logger.debug(bstack1l111l1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡹࡥࡱ࡯ࡤࡢࡶࡨࠤࡦ࠷࠱ࡺࠢࡶࡹࡵࡶ࡯ࡳࡶࠣ࠾ࠧኰ") + str(error))
            return False
    def bstack1ll111lll11_opy_(self, test_uuid: str, result: structs.FetchDriverExecuteParamsEventResponse):
        bstack1l1lll1l1l1_opy_ = {
            bstack1l111l1_opy_ (u"ࠫࡹ࡮ࡔࡦࡵࡷࡖࡺࡴࡕࡶ࡫ࡧࠫ኱"): test_uuid,
        }
        bstack1ll111l111l_opy_ = {}
        if result.success:
            bstack1ll111l111l_opy_ = json.loads(result.accessibility_execute_params)
        return bstack1ll11l11111_opy_(bstack1l1lll1l1l1_opy_, bstack1ll111l111l_opy_)
    def bstack1l1lll1lll1_opy_(self, script_name: str, test_uuid: str) -> dict:
        bstack1l111l1_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡉࡩࡹࡩࡨࠡࡥࡨࡲࡹࡸࡡ࡭ࠢࡤࡹࡹ࡮ࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡩ࡬ࡺࡪࡴࠠࡴࡥࡵ࡭ࡵࡺࠠ࡯ࡣࡰࡩ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳࠡࡥࡤࡧ࡭࡫ࡤࠡࡥࡲࡲ࡫࡯ࡧࠡ࡫ࡩࠤࡦࡲࡲࡦࡣࡧࡽࠥ࡬ࡥࡵࡥ࡫ࡩࡩ࠲ࠠࡰࡶ࡫ࡩࡷࡽࡩࡴࡧࠣࡰࡴࡧࡤࡴࠢࡤࡲࡩࠦࡣࡢࡥ࡫ࡩࡸࠦࡩࡵ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡵࡦࡶ࡮ࡶࡴࡠࡰࡤࡱࡪࡀࠠࡏࡣࡰࡩࠥࡵࡦࠡࡶ࡫ࡩࠥࡹࡣࡳ࡫ࡳࡸࠥࡺ࡯ࠡࡨࡨࡸࡨ࡮ࠠࡤࡱࡱࡪ࡮࡭ࠠࡧࡱࡵࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨ࠿ࠦࡕࡖࡋࡇࠤࡴ࡬ࠠࡵࡪࡨࠤࡹ࡫ࡳࡵࠢࡵࡹࡳࠦࡦࡰࡴࠣࡻ࡭࡯ࡣࡩࠢࡷࡳࠥ࡬ࡥࡵࡥ࡫ࠤࡨࡵ࡮ࡧ࡫ࡪࠎࠥࠦࠠࠡࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡪࡩࡤࡶ࠽ࠤࡈࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤࡩ࡯ࡣࡵ࡫ࡲࡲࡦࡸࡹ࠭ࠢࡨࡱࡵࡺࡹࠡࡦ࡬ࡧࡹࠦࡩࡧࠢࡨࡶࡷࡵࡲࠡࡱࡦࡧࡺࡸࡳࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧኲ")
        try:
            if self.bstack1ll1111ll11_opy_:
                return self.bstack1l1lll1l11l_opy_
            self.bstack1l1lll1l111_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack1l111l1_opy_ (u"ࠨࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠨኳ")
            req.script_name = script_name
            r = self.bstack1lll11l1l1l_opy_.FetchDriverExecuteParamsEvent(req)
            if r.success:
                self.bstack1l1lll1l11l_opy_ = self.bstack1ll111lll11_opy_(test_uuid, r)
                self.bstack1ll1111ll11_opy_ = True
            else:
                self.logger.error(bstack1l111l1_opy_ (u"ࠢࡧࡧࡷࡧ࡭ࡉࡥ࡯ࡶࡵࡥࡱࡇࡵࡵࡪࡄ࠵࠶ࡿࡃࡰࡰࡩ࡭࡬ࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡧࡶ࡮ࡼࡥࡳࠢࡨࡼࡪࡩࡵࡵࡧࠣࡴࡦࡸࡡ࡮ࡵࠣࡪࡴࡸࠠࡼࡵࡦࡶ࡮ࡶࡴࡠࡰࡤࡱࡪࢃ࠺ࠡࠤኴ") + str(r.error) + bstack1l111l1_opy_ (u"ࠣࠤኵ"))
                self.bstack1l1lll1l11l_opy_ = dict()
            return self.bstack1l1lll1l11l_opy_
        except Exception as e:
            self.logger.error(bstack1l111l1_opy_ (u"ࠤࡩࡩࡹࡩࡨࡄࡧࡱࡸࡷࡧ࡬ࡂࡷࡷ࡬ࡆ࠷࠱ࡺࡅࡲࡲ࡫࡯ࡧ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡬ࡥࡵࡥ࡫ࠤࡩࡸࡩࡷࡧࡵࠤࡪࡾࡥࡤࡷࡷࡩࠥࡶࡡࡳࡣࡰࡷࠥ࡬࡯ࡳࠢࡾࡷࡨࡸࡩࡱࡶࡢࡲࡦࡳࡥࡾ࠼ࠣࠦ኶") + str(traceback.format_exc()) + bstack1l111l1_opy_ (u"ࠥࠦ኷"))
            return dict()
    def bstack1lll1l1l_opy_(self, driver: object, name: str, framework_name: str, test_uuid: str):
        bstack1ll111ll11l_opy_ = None
        try:
            self.bstack1l1lll1l111_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack1l111l1_opy_ (u"ࠦࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠦኸ")
            req.script_name = bstack1l111l1_opy_ (u"ࠧࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠥኹ")
            r = self.bstack1lll11l1l1l_opy_.FetchDriverExecuteParamsEvent(req)
            if not r.success:
                self.logger.debug(bstack1l111l1_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡦࡵ࡭ࡻ࡫ࡲࠡࡧࡻࡩࡨࡻࡴࡦࠢࡳࡥࡷࡧ࡭ࡴࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࠤኺ") + str(r.error) + bstack1l111l1_opy_ (u"ࠢࠣኻ"))
            else:
                bstack1l1lll1l1l1_opy_ = self.bstack1ll111lll11_opy_(test_uuid, r)
                bstack1l1lll1llll_opy_ = r.script
            self.logger.debug(bstack1l111l1_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡦࡼࡩ࡯ࡩࠣࡶࡪࡹࡵ࡭ࡶࡶࠫኼ") + str(bstack1l1lll1l1l1_opy_))
            self.perform_scan(driver, name, framework_name=framework_name)
            if not bstack1l1lll1llll_opy_:
                self.logger.debug(bstack1l111l1_opy_ (u"ࠤࡳࡩࡷ࡬࡯ࡳ࡯ࡢࡷࡨࡧ࡮࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࠫࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠩࠣࡷࡨࡸࡩࡱࡶࠣࡪࡴࡸࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࠤኽ") + str(framework_name) + bstack1l111l1_opy_ (u"ࠥࠤࠧኾ"))
                return
            bstack1ll111ll11l_opy_ = bstack1ll11ll1ll1_opy_.bstack1ll1111l1l1_opy_(EVENTS.bstack1l1lllll1ll_opy_.value)
            self.bstack1l1lll11l11_opy_(driver, bstack1l1lll1llll_opy_, bstack1l1lll1l1l1_opy_, framework_name)
            try:
                bstack1ll111ll1l1_opy_ = {
                    bstack1l111l1_opy_ (u"ࠦࡷ࡫ࡱࡶࡧࡶࡸࠧ኿"): {
                        bstack1l111l1_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࠨዀ"): bstack1l111l1_opy_ (u"ࠨࡁ࠲࠳࡜ࡣࡘࡇࡖࡆࡡࡕࡉࡘ࡛ࡌࡕࡕࠥ዁"),
                    },
                    bstack1l111l1_opy_ (u"ࠢࡳࡧࡶࡴࡴࡴࡳࡦࠤዂ"): {
                        bstack1l111l1_opy_ (u"ࠣࡤࡲࡨࡾࠨዃ"): {
                            bstack1l111l1_opy_ (u"ࠤࡰࡷ࡬ࠨዄ"): bstack1l111l1_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢ࡫ࡥࡸࠦࡥ࡯ࡦࡨࡨ࠳ࠨዅ"),
                            bstack1l111l1_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷࠧ዆"): True
                        }
                    }
                }
                self.bstack1l1111ll1_opy_.info(json.dumps(bstack1ll111ll1l1_opy_, separators=(bstack1l111l1_opy_ (u"ࠬ࠲ࠧ዇"), bstack1l111l1_opy_ (u"࠭࠺ࠨወ"))))
            except Exception as bstack1lll11111l_opy_:
                self.logger.debug(bstack1l111l1_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡰࡴ࡭ࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡣࡹࡩࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡤࡢࡶࡤ࠾ࠥࠨዉ") + str(bstack1lll11111l_opy_) + bstack1l111l1_opy_ (u"ࠣࠤዊ"))
            self.logger.info(bstack1l111l1_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣࡪࡴࡸࠠࡵࡪ࡬ࡷࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡪࡤࡷࠥ࡫࡮ࡥࡧࡧ࠲ࠧዋ"))
            bstack1ll11ll1ll1_opy_.end(EVENTS.bstack1l1lllll1ll_opy_.value, bstack1ll111ll11l_opy_+bstack1l111l1_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥዌ"), bstack1ll111ll11l_opy_+bstack1l111l1_opy_ (u"ࠦ࠿࡫࡮ࡥࠤው"), True, None, command=bstack1l111l1_opy_ (u"ࠬࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠪዎ"),test_name=name)
        except Exception as bstack1l1ll1lll11_opy_:
            self.logger.error(bstack1l111l1_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹࠠࡤࡱࡸࡰࡩࠦ࡮ࡰࡶࠣࡦࡪࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡩࡳࡷࠦࡴࡩࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࡀࠠࠣዏ") + bstack1l111l1_opy_ (u"ࠢࡴࡶࡵࠬࡵࡧࡴࡩࠫࠥዐ") + bstack1l111l1_opy_ (u"ࠣࠢࡈࡶࡷࡵࡲࠡ࠼ࠥዑ") + str(bstack1l1ll1lll11_opy_))
            bstack1ll11ll1ll1_opy_.end(EVENTS.bstack1l1lllll1ll_opy_.value, bstack1ll111ll11l_opy_+bstack1l111l1_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤዒ"), bstack1ll111ll11l_opy_+bstack1l111l1_opy_ (u"ࠥ࠾ࡪࡴࡤࠣዓ"), False, bstack1l1ll1lll11_opy_, command=bstack1l111l1_opy_ (u"ࠫࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠩዔ"),test_name=name)
    def bstack1l1lll11l11_opy_(self, driver, bstack1l1lll1llll_opy_, bstack1l1lll1l1l1_opy_, framework_name):
        if framework_name == bstack1l111l1_opy_ (u"ࠬࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩዕ"):
            self.bstack1l1lll11l1l_opy_.bstack1ll111l1lll_opy_(driver, bstack1l1lll1llll_opy_, bstack1l1lll1l1l1_opy_)
        else:
            self.logger.debug(driver.execute_async_script(bstack1l1lll1llll_opy_, bstack1l1lll1l1l1_opy_))
    def _1ll1111111l_opy_(self, instance: bstack1ll1llllll1_opy_, args: Tuple) -> list:
        bstack1l111l1_opy_ (u"ࠨࠢࠣࡇࡻࡸࡷࡧࡣࡵࠢࡷࡥ࡬ࡹࠠࡣࡣࡶࡩࡩࠦ࡯࡯ࠢࡷ࡬ࡪࠦࡴࡦࡵࡷࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠮ࠣࠤࠥዖ")
        if bstack1l111l1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫ዗") in instance.bstack1l1lll111l1_opy_:
            return args[2].tags if hasattr(args[2], bstack1l111l1_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ዘ")) else []
        if hasattr(args[0], bstack1l111l1_opy_ (u"ࠩࡲࡻࡳࡥ࡭ࡢࡴ࡮ࡩࡷࡹࠧዙ")):
            return [marker.name for marker in args[0].own_markers]
        return []
    def bstack1l1lllllll1_opy_(self, tags, capabilities):
        return self.bstack11l1l11111_opy_(tags) and self.bstack11l11llll_opy_(capabilities)