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
from browserstack_sdk.sdk_cli.bstack1lll1l1l1l1_opy_ import bstack1ll1l1ll1ll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1ll1l11_opy_ import (
    bstack1lll1l1ll11_opy_,
    bstack1llll11l111_opy_,
    bstack1llll11l1ll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll11ll1ll_opy_ import bstack1ll11llll11_opy_
from typing import Tuple, Callable, Any
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1lll1l1l1l1_opy_ import bstack1ll1l1ll1ll_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import traceback
import os
import time
class bstack1ll11llllll_opy_(bstack1ll1l1ll1ll_opy_):
    bstack1l1llllllll_opy_ = False
    def __init__(self):
        super().__init__()
        bstack1ll11llll11_opy_.bstack1ll111l11ll_opy_((bstack1lll1l1ll11_opy_.bstack1llll111l1l_opy_, bstack1llll11l111_opy_.PRE), self.bstack1l1ll1l1lll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1ll1l1lll_opy_(
        self,
        f: bstack1ll11llll11_opy_,
        driver: object,
        exec: Tuple[bstack1llll11l1ll_opy_, str],
        bstack1lll1ll1111_opy_: Tuple[bstack1lll1l1ll11_opy_, bstack1llll11l111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        hub_url = f.hub_url(driver)
        if f.bstack1l1ll1l11ll_opy_(hub_url):
            if not bstack1ll11llllll_opy_.bstack1l1llllllll_opy_:
                self.logger.warning(bstack1l111l1_opy_ (u"ࠥࡰࡴࡩࡡ࡭ࠢࡶࡩࡱ࡬࠭ࡩࡧࡤࡰࠥ࡬࡬ࡰࡹࠣࡨ࡮ࡹࡡࡣ࡮ࡨࡨࠥ࡬࡯ࡳࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡ࡫ࡱࡪࡷࡧࠠࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠢ࡫ࡹࡧࡥࡵࡳ࡮ࡀࠦዚ") + str(hub_url) + bstack1l111l1_opy_ (u"ࠦࠧዛ"))
                bstack1ll11llllll_opy_.bstack1l1llllllll_opy_ = True
            return
        command_name = f.bstack1l1lll11ll1_opy_(*args)
        bstack1l1ll1l1l11_opy_ = f.bstack1l1ll1ll111_opy_(*args)
        if command_name and command_name.lower() == bstack1l111l1_opy_ (u"ࠧ࡬ࡩ࡯ࡦࡨࡰࡪࡳࡥ࡯ࡶࠥዜ") and bstack1l1ll1l1l11_opy_:
            framework_session_id = f.session_id(driver)
            locator_type, locator_value = bstack1l1ll1l1l11_opy_.get(bstack1l111l1_opy_ (u"ࠨࡵࡴ࡫ࡱ࡫ࠧዝ"), None), bstack1l1ll1l1l11_opy_.get(bstack1l111l1_opy_ (u"ࠢࡷࡣ࡯ࡹࡪࠨዞ"), None)
            if not framework_session_id or not locator_type or not locator_value:
                self.logger.warning(bstack1l111l1_opy_ (u"ࠣࡽࡦࡳࡲࡳࡡ࡯ࡦࡢࡲࡦࡳࡥࡾ࠼ࠣࡱ࡮ࡹࡳࡪࡰࡪࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠤࡴࡸࠠࡢࡴࡪࡷ࠳ࡻࡳࡪࡰࡪࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࢁࠥࡵࡲࠡࡣࡵ࡫ࡸ࠴ࡶࡢ࡮ࡸࡩࡂࠨዟ") + str(locator_value) + bstack1l111l1_opy_ (u"ࠤࠥዠ"))
                return
            def bstack1llll111lll_opy_(driver, bstack1l1ll1l1l1l_opy_, *args, **kwargs):
                from selenium.common.exceptions import NoSuchElementException
                try:
                    result = bstack1l1ll1l1l1l_opy_(driver, *args, **kwargs)
                    response = self.bstack1l1ll1l1ll1_opy_(
                        framework_session_id=framework_session_id,
                        is_success=True,
                        locator_type=locator_type,
                        locator_value=locator_value,
                    )
                    if response and response.execute_script:
                        driver.execute_script(response.execute_script)
                        self.logger.info(bstack1l111l1_opy_ (u"ࠥࡷࡺࡩࡣࡦࡵࡶ࠱ࡸࡩࡲࡪࡲࡷ࠾ࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࢁࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࡂࠨዡ") + str(locator_value) + bstack1l111l1_opy_ (u"ࠦࠧዢ"))
                    else:
                        self.logger.warning(bstack1l111l1_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸ࠳࡮ࡰ࠯ࡶࡧࡷ࡯ࡰࡵ࠼ࠣࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦࡿࠣࡰࡴࡩࡡࡵࡱࡵࡣࡻࡧ࡬ࡶࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࢁࠥࡸࡥࡴࡲࡲࡲࡸ࡫࠽ࠣዣ") + str(response) + bstack1l111l1_opy_ (u"ࠨࠢዤ"))
                    return result
                except NoSuchElementException as e:
                    locator = (locator_type, locator_value)
                    return self.__1l1ll11llll_opy_(
                        driver, bstack1l1ll1l1l1l_opy_, e, framework_session_id, locator, *args, **kwargs
                    )
            bstack1llll111lll_opy_.__name__ = command_name
            return bstack1llll111lll_opy_
    def __1l1ll11llll_opy_(
        self,
        driver,
        bstack1l1ll1l1l1l_opy_: Callable,
        exception,
        framework_session_id: str,
        locator: Tuple[str, str],
        *args,
        **kwargs,
    ):
        try:
            locator_type, locator_value = locator
            response = self.bstack1l1ll1l1ll1_opy_(
                framework_session_id=framework_session_id,
                is_success=False,
                locator_type=locator_type,
                locator_value=locator_value,
            )
            if response and response.execute_script:
                driver.execute_script(response.execute_script)
                self.logger.info(bstack1l111l1_opy_ (u"ࠢࡧࡣ࡬ࡰࡺࡸࡥ࠮ࡪࡨࡥࡱ࡯࡮ࡨ࠯ࡷࡶ࡮࡭ࡧࡦࡴࡨࡨ࠿ࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࢂࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࡃࠢዥ") + str(locator_value) + bstack1l111l1_opy_ (u"ࠣࠤዦ"))
                bstack1l1ll1l11l1_opy_ = self.bstack1l1ll1l111l_opy_(
                    framework_session_id=framework_session_id,
                    locator_type=locator_type,
                )
                self.logger.info(bstack1l111l1_opy_ (u"ࠤࡩࡥ࡮ࡲࡵࡳࡧ࠰࡬ࡪࡧ࡬ࡪࡰࡪ࠱ࡷ࡫ࡳࡶ࡮ࡷ࠾ࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࢁࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࢃࠠࡩࡧࡤࡰ࡮ࡴࡧࡠࡴࡨࡷࡺࡲࡴ࠾ࠤዧ") + str(bstack1l1ll1l11l1_opy_) + bstack1l111l1_opy_ (u"ࠥࠦየ"))
                if bstack1l1ll1l11l1_opy_.success and args and len(args) > 1:
                    args[1].update(
                        {
                            bstack1l111l1_opy_ (u"ࠦࡺࡹࡩ࡯ࡩࠥዩ"): bstack1l1ll1l11l1_opy_.locator_type,
                            bstack1l111l1_opy_ (u"ࠧࡼࡡ࡭ࡷࡨࠦዪ"): bstack1l1ll1l11l1_opy_.locator_value,
                        }
                    )
                    return bstack1l1ll1l1l1l_opy_(driver, *args, **kwargs)
                elif os.environ.get(bstack1l111l1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡉࡠࡆࡈࡆ࡚ࡍࠢያ"), False):
                    self.logger.info(bstack1ll1ll1111l_opy_ (u"ࠢࡧࡣ࡬ࡰࡺࡸࡥ࠮ࡪࡨࡥࡱ࡯࡮ࡨ࠯ࡵࡩࡸࡻ࡬ࡵ࠯ࡰ࡭ࡸࡹࡩ࡯ࡩ࠽ࠤࡸࡲࡥࡦࡲࠫ࠷࠵࠯ࠠ࡭ࡧࡷࡸ࡮ࡴࡧࠡࡻࡲࡹࠥ࡯࡮ࡴࡲࡨࡧࡹࠦࡴࡩࡧࠣࡦࡷࡵࡷࡴࡧࡵࠤࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࠠ࡭ࡱࡪࡷࠧዬ"))
                    time.sleep(300)
            else:
                self.logger.warning(bstack1l111l1_opy_ (u"ࠣࡨࡤ࡭ࡱࡻࡲࡦ࠯ࡱࡳ࠲ࡹࡣࡳ࡫ࡳࡸ࠿ࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࢂࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫ࡽࠡࡴࡨࡷࡵࡵ࡮ࡴࡧࡀࠦይ") + str(response) + bstack1l111l1_opy_ (u"ࠤࠥዮ"))
        except Exception as err:
            self.logger.warning(bstack1l111l1_opy_ (u"ࠥࡪࡦ࡯࡬ࡶࡴࡨ࠱࡭࡫ࡡ࡭࡫ࡱ࡫࠲ࡸࡥࡴࡷ࡯ࡸ࠿ࠦࡥࡳࡴࡲࡶ࠿ࠦࠢዯ") + str(err) + bstack1l111l1_opy_ (u"ࠦࠧደ"))
        raise exception
    @measure(event_name=EVENTS.bstack1l1ll1l1111_opy_, stage=STAGE.bstack11l11l11l1_opy_)
    def bstack1l1ll1l1ll1_opy_(
        self,
        framework_session_id: str,
        is_success: bool,
        locator_type: str,
        locator_value: str,
        platform_index=bstack1l111l1_opy_ (u"ࠧ࠶ࠢዱ"),
    ):
        self.bstack1l1lll1l111_opy_()
        req = structs.AISelfHealStepRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.is_success = is_success
        req.test_name = bstack1l111l1_opy_ (u"ࠨࠢዲ")
        req.locator_type = locator_type
        req.locator_value = locator_value
        try:
            r = self.bstack1lll11l1l1l_opy_.AISelfHealStep(req)
            self.logger.info(bstack1l111l1_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࠤዳ") + str(r) + bstack1l111l1_opy_ (u"ࠣࠤዴ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l111l1_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢድ") + str(e) + bstack1l111l1_opy_ (u"ࠥࠦዶ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1ll11lll1_opy_, stage=STAGE.bstack11l11l11l1_opy_)
    def bstack1l1ll1l111l_opy_(self, framework_session_id: str, locator_type: str, platform_index=bstack1l111l1_opy_ (u"ࠦ࠵ࠨዷ")):
        self.bstack1l1lll1l111_opy_()
        req = structs.AISelfHealGetRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.locator_type = locator_type
        try:
            r = self.bstack1lll11l1l1l_opy_.AISelfHealGetResult(req)
            self.logger.info(bstack1l111l1_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢዸ") + str(r) + bstack1l111l1_opy_ (u"ࠨࠢዹ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l111l1_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧዺ") + str(e) + bstack1l111l1_opy_ (u"ࠣࠤዻ"))
            traceback.print_exc()
            raise e