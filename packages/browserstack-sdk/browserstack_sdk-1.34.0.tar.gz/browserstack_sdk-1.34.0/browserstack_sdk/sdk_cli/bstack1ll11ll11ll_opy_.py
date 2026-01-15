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
import os
import grpc
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1lll1l1l1l1_opy_ import bstack1ll1l1ll1ll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1ll1l11_opy_ import (
    bstack1lll1l1ll11_opy_,
    bstack1llll11l111_opy_,
    bstack1llll11l1ll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll11ll1ll_opy_ import bstack1ll11llll11_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1ll1l11l_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import threading
import os
from bstack_utils.bstack11lll1l1ll_opy_ import bstack1ll11ll1ll1_opy_
class bstack1ll1l1l1lll_opy_(bstack1ll1l1ll1ll_opy_):
    bstack1l111ll1lll_opy_ = bstack1l111l1_opy_ (u"ࠧࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡪࡰ࡬ࡸࠧᐞ")
    bstack1l11l111l1l_opy_ = bstack1l111l1_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡵࡷࡥࡷࡺࠢᐟ")
    bstack1l111llllll_opy_ = bstack1l111l1_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡶࡸࡴࡶࠢᐠ")
    def __init__(self, bstack1lll1l111ll_opy_):
        super().__init__()
        bstack1ll11llll11_opy_.bstack1ll111l11ll_opy_((bstack1lll1l1ll11_opy_.bstack1lll1ll1l1l_opy_, bstack1llll11l111_opy_.PRE), self.bstack1l111ll111l_opy_)
        bstack1ll11llll11_opy_.bstack1ll111l11ll_opy_((bstack1lll1l1ll11_opy_.bstack1llll111l1l_opy_, bstack1llll11l111_opy_.PRE), self.bstack1l1ll1l1lll_opy_)
        bstack1ll11llll11_opy_.bstack1ll111l11ll_opy_((bstack1lll1l1ll11_opy_.bstack1llll111l1l_opy_, bstack1llll11l111_opy_.POST), self.bstack1l111ll1ll1_opy_)
        bstack1ll11llll11_opy_.bstack1ll111l11ll_opy_((bstack1lll1l1ll11_opy_.bstack1llll111l1l_opy_, bstack1llll11l111_opy_.POST), self.bstack1l111lll11l_opy_)
        bstack1ll11llll11_opy_.bstack1ll111l11ll_opy_((bstack1lll1l1ll11_opy_.QUIT, bstack1llll11l111_opy_.POST), self.bstack1l111l1l1ll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l111ll111l_opy_(
        self,
        f: bstack1ll11llll11_opy_,
        driver: object,
        exec: Tuple[bstack1llll11l1ll_opy_, str],
        bstack1lll1ll1111_opy_: Tuple[bstack1lll1l1ll11_opy_, bstack1llll11l111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l111l1_opy_ (u"ࠣࡡࡢ࡭ࡳ࡯ࡴࡠࡡࠥᐡ"):
            return
        def wrapped(driver, init, *args, **kwargs):
            url = None
            try:
                if isinstance(kwargs.get(bstack1l111l1_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧᐢ")), str):
                    url = kwargs.get(bstack1l111l1_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᐣ"))
                elif hasattr(kwargs.get(bstack1l111l1_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢᐤ")), bstack1l111l1_opy_ (u"ࠬࡥࡣ࡭࡫ࡨࡲࡹࡥࡣࡰࡰࡩ࡭࡬࠭ᐥ")):
                    url = kwargs.get(bstack1l111l1_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤᐦ"))._client_config.remote_server_addr
                else:
                    url = kwargs.get(bstack1l111l1_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᐧ"))._url
            except Exception as e:
                url = bstack1l111l1_opy_ (u"ࠨࠩᐨ")
                self.logger.error(bstack1l111l1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡷࡵࡰࠥ࡬ࡲࡰ࡯ࠣࡨࡷ࡯ࡶࡦࡴ࠽ࠤࢀࢃࠢᐩ").format(e))
            self.logger.info(bstack1l111l1_opy_ (u"ࠥࡖࡪࡳ࡯ࡵࡧࠣࡗࡪࡸࡶࡦࡴࠣࡅࡩࡪࡲࡦࡵࡶࠤࡧ࡫ࡩ࡯ࡩࠣࡴࡦࡹࡳࡦࡦࠣࡥࡸࠦ࠺ࠡࡽࢀࠦᐪ").format(str(url)))
            self.bstack1l111ll1l1l_opy_(instance, url, f, kwargs)
            self.logger.info(bstack1l111l1_opy_ (u"ࠦࡩࡸࡩࡷࡧࡵ࠲ࢀࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࢀࠤࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࡂࢁࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾࡽ࠻ࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࡼ࡭ࡺࡥࡷ࡭ࡳࡾࠤᐫ").format(method_name=method_name, platform_index=f.platform_index, args=args, kwargs=kwargs))
            threading.current_thread().bstackSessionDriver = driver
            return init(driver, *args, **kwargs)
        return wrapped
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
        instance, method_name = exec
        if f.bstack1llll1l111l_opy_(instance, bstack1ll1l1l1lll_opy_.bstack1l111ll1lll_opy_, False):
            return
        if not f.bstack1lll1ll111l_opy_(instance, bstack1ll11llll11_opy_.bstack1ll1111ll1l_opy_):
            return
        platform_index = f.bstack1llll1l111l_opy_(instance, bstack1ll11llll11_opy_.bstack1ll1111ll1l_opy_)
        if f.bstack1ll11111ll1_opy_(method_name, *args) and len(args) > 1:
            bstack1ll11llll_opy_ = datetime.now()
            hub_url = bstack1ll11llll11_opy_.hub_url(driver)
            self.logger.warning(bstack1l111l1_opy_ (u"ࠧ࡮ࡵࡣࡡࡸࡶࡱࡃࠢᐬ") + str(hub_url) + bstack1l111l1_opy_ (u"ࠨࠢᐭ"))
            bstack1l111ll11ll_opy_ = args[1][bstack1l111l1_opy_ (u"ࠢࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᐮ")] if isinstance(args[1], dict) and bstack1l111l1_opy_ (u"ࠣࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᐯ") in args[1] else None
            bstack1l111l1ll1l_opy_ = bstack1l111l1_opy_ (u"ࠤࡤࡰࡼࡧࡹࡴࡏࡤࡸࡨ࡮ࠢᐰ")
            if isinstance(bstack1l111ll11ll_opy_, dict):
                bstack1ll11llll_opy_ = datetime.now()
                r = self.bstack1l111lll111_opy_(
                    instance.ref(),
                    platform_index,
                    f.framework_name,
                    f.framework_version,
                    hub_url
                )
                instance.bstack111lll11l_opy_(bstack1l111l1_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡴࡨ࡫࡮ࡹࡴࡦࡴࡢ࡭ࡳ࡯ࡴࠣᐱ"), datetime.now() - bstack1ll11llll_opy_)
                try:
                    if not r.success:
                        self.logger.info(bstack1l111l1_opy_ (u"ࠦࡸࡵ࡭ࡦࡶ࡫࡭ࡳ࡭ࠠࡸࡧࡱࡸࠥࡽࡲࡰࡰࡪ࠾ࠥࠨᐲ") + str(r) + bstack1l111l1_opy_ (u"ࠧࠨᐳ"))
                        return
                    if r.hub_url:
                        f.bstack1l11l111111_opy_(instance, driver, r.hub_url)
                        f.bstack1llll1111l1_opy_(instance, bstack1ll1l1l1lll_opy_.bstack1l111ll1lll_opy_, True)
                except Exception as e:
                    self.logger.error(bstack1l111l1_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧᐴ"), e)
    def bstack1l111ll1ll1_opy_(
        self,
        f: bstack1ll11llll11_opy_,
        driver: object,
        exec: Tuple[bstack1llll11l1ll_opy_, str],
        bstack1lll1ll1111_opy_: Tuple[bstack1lll1l1ll11_opy_, bstack1llll11l111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
            session_id = bstack1ll11llll11_opy_.session_id(driver)
            if session_id:
                bstack1l11l111ll1_opy_ = bstack1l111l1_opy_ (u"ࠢࡼࡿ࠽ࡷࡹࡧࡲࡵࠤᐵ").format(session_id)
                bstack1ll11ll1ll1_opy_.mark(bstack1l11l111ll1_opy_)
    def bstack1l111lll11l_opy_(
        self,
        f: bstack1ll11llll11_opy_,
        driver: object,
        exec: Tuple[bstack1llll11l1ll_opy_, str],
        bstack1lll1ll1111_opy_: Tuple[bstack1lll1l1ll11_opy_, bstack1llll11l111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1llll1l111l_opy_(instance, bstack1ll1l1l1lll_opy_.bstack1l11l111l1l_opy_, False):
            return
        ref = instance.ref()
        hub_url = bstack1ll11llll11_opy_.hub_url(driver)
        if not hub_url:
            self.logger.warning(bstack1l111l1_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡧࡲࡴࡧࠣ࡬ࡺࡨ࡟ࡶࡴ࡯ࡁࠧᐶ") + str(hub_url) + bstack1l111l1_opy_ (u"ࠤࠥᐷ"))
            return
        framework_session_id = bstack1ll11llll11_opy_.session_id(driver)
        if not framework_session_id:
            self.logger.warning(bstack1l111l1_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡢࡴࡶࡩࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࡂࠨᐸ") + str(framework_session_id) + bstack1l111l1_opy_ (u"ࠦࠧᐹ"))
            return
        if bstack1ll11llll11_opy_.bstack1l111lll1l1_opy_(*args) == bstack1ll11llll11_opy_.bstack1l111l1llll_opy_:
            bstack1l111ll1l11_opy_ = bstack1l111l1_opy_ (u"ࠧࢁࡽ࠻ࡧࡱࡨࠧᐺ").format(framework_session_id)
            bstack1l11l111ll1_opy_ = bstack1l111l1_opy_ (u"ࠨࡻࡾ࠼ࡶࡸࡦࡸࡴࠣᐻ").format(framework_session_id)
            bstack1ll11ll1ll1_opy_.end(
                label=bstack1l111l1_opy_ (u"ࠢࡴࡦ࡮࠾ࡩࡸࡩࡷࡧࡵ࠾ࡵࡵࡳࡵ࠯࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡦࡺࡩࡰࡰࠥᐼ"),
                start=bstack1l11l111ll1_opy_,
                end=bstack1l111ll1l11_opy_,
                status=True,
                failure=None
            )
            bstack1ll11llll_opy_ = datetime.now()
            r = self.bstack1l11l1111l1_opy_(
                ref,
                f.bstack1llll1l111l_opy_(instance, bstack1ll11llll11_opy_.bstack1ll1111ll1l_opy_, 0),
                f.framework_name,
                f.framework_version,
                framework_session_id,
                hub_url,
            )
            instance.bstack111lll11l_opy_(bstack1l111l1_opy_ (u"ࠣࡩࡵࡴࡨࡀࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡵࡷࡥࡷࡺࠢᐽ"), datetime.now() - bstack1ll11llll_opy_)
            f.bstack1llll1111l1_opy_(instance, bstack1ll1l1l1lll_opy_.bstack1l11l111l1l_opy_, r.success)
    def bstack1l111l1l1ll_opy_(
        self,
        f: bstack1ll11llll11_opy_,
        driver: object,
        exec: Tuple[bstack1llll11l1ll_opy_, str],
        bstack1lll1ll1111_opy_: Tuple[bstack1lll1l1ll11_opy_, bstack1llll11l111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1llll1l111l_opy_(instance, bstack1ll1l1l1lll_opy_.bstack1l111llllll_opy_, False):
            return
        ref = instance.ref()
        framework_session_id = bstack1ll11llll11_opy_.session_id(driver)
        hub_url = bstack1ll11llll11_opy_.hub_url(driver)
        bstack1ll11llll_opy_ = datetime.now()
        r = self.bstack1l11l1111ll_opy_(
            ref,
            f.bstack1llll1l111l_opy_(instance, bstack1ll11llll11_opy_.bstack1ll1111ll1l_opy_, 0),
            f.framework_name,
            f.framework_version,
            framework_session_id,
            hub_url,
        )
        instance.bstack111lll11l_opy_(bstack1l111l1_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡶࡸࡴࡶࠢᐾ"), datetime.now() - bstack1ll11llll_opy_)
        f.bstack1llll1111l1_opy_(instance, bstack1ll1l1l1lll_opy_.bstack1l111llllll_opy_, r.success)
    @measure(event_name=EVENTS.bstack1l1ll11l_opy_, stage=STAGE.bstack11l11l11l1_opy_)
    def bstack1l11ll1l1l1_opy_(self, platform_index: int, url: str, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.hub_url = url
        self.logger.debug(bstack1l111l1_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲࡠ࡫ࡱ࡭ࡹࡀࠠࠣᐿ") + str(req) + bstack1l111l1_opy_ (u"ࠦࠧᑀ"))
        try:
            r = self.bstack1lll11l1l1l_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack1l111l1_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࡳࡶࡥࡦࡩࡸࡹ࠽ࠣᑁ") + str(r.success) + bstack1l111l1_opy_ (u"ࠨࠢᑂ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l111l1_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᑃ") + str(e) + bstack1l111l1_opy_ (u"ࠣࠤᑄ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l111llll11_opy_, stage=STAGE.bstack11l11l11l1_opy_)
    def bstack1l111lll111_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str
    ):
        self.bstack1l1lll1l111_opy_()
        req = structs.AutomationFrameworkInitRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        self.logger.debug(bstack1l111l1_opy_ (u"ࠤࡵࡩ࡬࡯ࡳࡵࡧࡵࡣ࡮ࡴࡩࡵ࠼ࠣࠦᑅ") + str(req) + bstack1l111l1_opy_ (u"ࠥࠦᑆ"))
        try:
            r = self.bstack1lll11l1l1l_opy_.AutomationFrameworkInit(req)
            if not r.success:
                self.logger.debug(bstack1l111l1_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࡹࡵࡤࡥࡨࡷࡸࡃࠢᑇ") + str(r.success) + bstack1l111l1_opy_ (u"ࠧࠨᑈ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l111l1_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦᑉ") + str(e) + bstack1l111l1_opy_ (u"ࠢࠣᑊ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l11l111l11_opy_, stage=STAGE.bstack11l11l11l1_opy_)
    def bstack1l11l1111l1_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1l1lll1l111_opy_()
        req = structs.AutomationFrameworkStartRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        self.logger.debug(bstack1l111l1_opy_ (u"ࠣࡴࡨ࡫࡮ࡹࡴࡦࡴࡢࡷࡹࡧࡲࡵ࠼ࠣࠦᑋ") + str(req) + bstack1l111l1_opy_ (u"ࠤࠥᑌ"))
        try:
            r = self.bstack1lll11l1l1l_opy_.AutomationFrameworkStart(req)
            if not r.success:
                self.logger.debug(bstack1l111l1_opy_ (u"ࠥࡶࡪࡩࡥࡪࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࠧᑍ") + str(r) + bstack1l111l1_opy_ (u"ࠦࠧᑎ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l111l1_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥᑏ") + str(e) + bstack1l111l1_opy_ (u"ࠨࠢᑐ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l111llll1l_opy_, stage=STAGE.bstack11l11l11l1_opy_)
    def bstack1l11l1111ll_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1l1lll1l111_opy_()
        req = structs.AutomationFrameworkStopRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        self.logger.debug(bstack1l111l1_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡶࡸࡴࡶ࠺ࠡࠤᑑ") + str(req) + bstack1l111l1_opy_ (u"ࠣࠤᑒ"))
        try:
            r = self.bstack1lll11l1l1l_opy_.AutomationFrameworkStop(req)
            if not r.success:
                self.logger.debug(bstack1l111l1_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦᑓ") + str(r) + bstack1l111l1_opy_ (u"ࠥࠦᑔ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l111l1_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤᑕ") + str(e) + bstack1l111l1_opy_ (u"ࠧࠨᑖ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1llll1l111_opy_, stage=STAGE.bstack11l11l11l1_opy_)
    def bstack1l111ll1l1l_opy_(self, instance: bstack1llll11l1ll_opy_, url: str, f: bstack1ll11llll11_opy_, kwargs):
        bstack1l111l1ll11_opy_ = version.parse(f.framework_version)
        bstack1l111lll1ll_opy_ = kwargs.get(bstack1l111l1_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡳࡳࡹࠢᑗ"))
        bstack1l11l11111l_opy_ = kwargs.get(bstack1l111l1_opy_ (u"ࠢࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᑘ"))
        bstack1l11l1ll11l_opy_ = {}
        bstack1l111lllll1_opy_ = {}
        bstack1l111l1lll1_opy_ = None
        bstack1l111ll11l1_opy_ = {}
        if bstack1l11l11111l_opy_ is not None or bstack1l111lll1ll_opy_ is not None: # check top level caps
            if bstack1l11l11111l_opy_ is not None:
                bstack1l111ll11l1_opy_[bstack1l111l1_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᑙ")] = bstack1l11l11111l_opy_
            if bstack1l111lll1ll_opy_ is not None and callable(getattr(bstack1l111lll1ll_opy_, bstack1l111l1_opy_ (u"ࠤࡷࡳࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᑚ"))):
                bstack1l111ll11l1_opy_[bstack1l111l1_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࡣࡦࡹ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᑛ")] = bstack1l111lll1ll_opy_.to_capabilities()
        response = self.bstack1l11ll1l1l1_opy_(f.platform_index, url, instance.ref(), json.dumps(bstack1l111ll11l1_opy_).encode(bstack1l111l1_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥᑜ")))
        if response is not None and response.capabilities:
            bstack1l11l1ll11l_opy_ = json.loads(response.capabilities.decode(bstack1l111l1_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦᑝ")))
            if not bstack1l11l1ll11l_opy_: # empty caps bstack1l11l1lllll_opy_ bstack1l11l1llll1_opy_ bstack1l11ll111ll_opy_ bstack1ll1l1l1111_opy_ or error in processing
                return
            bstack1l111l1lll1_opy_ = f.bstack1ll1ll111l1_opy_[bstack1l111l1_opy_ (u"ࠨࡣࡳࡧࡤࡸࡪࡥ࡯ࡱࡶ࡬ࡳࡳࡹ࡟ࡧࡴࡲࡱࡤࡩࡡࡱࡵࠥᑞ")](bstack1l11l1ll11l_opy_)
        if bstack1l111lll1ll_opy_ is not None and bstack1l111l1ll11_opy_ >= version.parse(bstack1l111l1_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ᑟ")):
            bstack1l111lllll1_opy_ = None
        if (
                not bstack1l111lll1ll_opy_ and not bstack1l11l11111l_opy_
        ) or (
                bstack1l111l1ll11_opy_ < version.parse(bstack1l111l1_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧᑠ"))
        ):
            bstack1l111lllll1_opy_ = {}
            bstack1l111lllll1_opy_.update(bstack1l11l1ll11l_opy_)
        self.logger.info(bstack1ll1l11l_opy_)
        if os.environ.get(bstack1l111l1_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠧᑡ")).lower().__eq__(bstack1l111l1_opy_ (u"ࠥࡸࡷࡻࡥࠣᑢ")):
            kwargs.update(
                {
                    bstack1l111l1_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢᑣ"): f.bstack1l111ll1111_opy_,
                }
            )
        if bstack1l111l1ll11_opy_ >= version.parse(bstack1l111l1_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬᑤ")):
            if bstack1l11l11111l_opy_ is not None:
                del kwargs[bstack1l111l1_opy_ (u"ࠨࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᑥ")]
            kwargs.update(
                {
                    bstack1l111l1_opy_ (u"ࠢࡰࡲࡷ࡭ࡴࡴࡳࠣᑦ"): bstack1l111l1lll1_opy_,
                    bstack1l111l1_opy_ (u"ࠣ࡭ࡨࡩࡵࡥࡡ࡭࡫ࡹࡩࠧᑧ"): True,
                    bstack1l111l1_opy_ (u"ࠤࡩ࡭ࡱ࡫࡟ࡥࡧࡷࡩࡨࡺ࡯ࡳࠤᑨ"): None,
                }
            )
        elif bstack1l111l1ll11_opy_ >= version.parse(bstack1l111l1_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩᑩ")):
            kwargs.update(
                {
                    bstack1l111l1_opy_ (u"ࠦࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᑪ"): bstack1l111lllll1_opy_,
                    bstack1l111l1_opy_ (u"ࠧࡵࡰࡵ࡫ࡲࡲࡸࠨᑫ"): bstack1l111l1lll1_opy_,
                    bstack1l111l1_opy_ (u"ࠨ࡫ࡦࡧࡳࡣࡦࡲࡩࡷࡧࠥᑬ"): True,
                    bstack1l111l1_opy_ (u"ࠢࡧ࡫࡯ࡩࡤࡪࡥࡵࡧࡦࡸࡴࡸࠢᑭ"): None,
                }
            )
        elif bstack1l111l1ll11_opy_ >= version.parse(bstack1l111l1_opy_ (u"ࠨ࠴࠱࠹࠸࠴࠰ࠨᑮ")):
            kwargs.update(
                {
                    bstack1l111l1_opy_ (u"ࠤࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᑯ"): bstack1l111lllll1_opy_,
                    bstack1l111l1_opy_ (u"ࠥ࡯ࡪ࡫ࡰࡠࡣ࡯࡭ࡻ࡫ࠢᑰ"): True,
                    bstack1l111l1_opy_ (u"ࠦ࡫࡯࡬ࡦࡡࡧࡩࡹ࡫ࡣࡵࡱࡵࠦᑱ"): None,
                }
            )
        else:
            kwargs.update(
                {
                    bstack1l111l1_opy_ (u"ࠧࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᑲ"): bstack1l111lllll1_opy_,
                    bstack1l111l1_opy_ (u"ࠨ࡫ࡦࡧࡳࡣࡦࡲࡩࡷࡧࠥᑳ"): True,
                    bstack1l111l1_opy_ (u"ࠢࡧ࡫࡯ࡩࡤࡪࡥࡵࡧࡦࡸࡴࡸࠢᑴ"): None,
                }
            )