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
import json
import os
import grpc
import copy
import asyncio
import threading
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1lll11ll1ll_opy_ import bstack1lll1l1lll1_opy_
from browserstack_sdk.sdk_cli.bstack1llll11llll_opy_ import (
    bstack1llll111lll_opy_,
    bstack1llll111l11_opy_,
    bstack1lll1ll1ll1_opy_,
)
from bstack_utils.constants import *
from typing import Any, List, Union, Dict
from pathlib import Path
from browserstack_sdk.sdk_cli.bstack1ll1l1l11ll_opy_ import bstack1ll1ll1111l_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1ll1111l1l_opy_
from bstack_utils.helper import bstack1l1l11ll1ll_opy_
import threading
import os
import urllib.parse
class bstack1ll11ll1ll1_opy_(bstack1lll1l1lll1_opy_):
    def __init__(self, bstack1lll1ll1111_opy_):
        super().__init__()
        bstack1ll1ll1111l_opy_.bstack1l1llll1111_opy_((bstack1llll111lll_opy_.bstack1lll1lll111_opy_, bstack1llll111l11_opy_.PRE), self.bstack1l11lll11ll_opy_)
        bstack1ll1ll1111l_opy_.bstack1l1llll1111_opy_((bstack1llll111lll_opy_.bstack1lll1lll111_opy_, bstack1llll111l11_opy_.PRE), self.bstack1l11ll1l1l1_opy_)
        bstack1ll1ll1111l_opy_.bstack1l1llll1111_opy_((bstack1llll111lll_opy_.bstack1lll1lll11l_opy_, bstack1llll111l11_opy_.PRE), self.bstack1l11ll11lll_opy_)
        bstack1ll1ll1111l_opy_.bstack1l1llll1111_opy_((bstack1llll111lll_opy_.bstack1lll1llllll_opy_, bstack1llll111l11_opy_.PRE), self.bstack1l11ll1l1ll_opy_)
        bstack1ll1ll1111l_opy_.bstack1l1llll1111_opy_((bstack1llll111lll_opy_.bstack1lll1lll111_opy_, bstack1llll111l11_opy_.PRE), self.bstack1l11lll11l1_opy_)
        bstack1ll1ll1111l_opy_.bstack1l1llll1111_opy_((bstack1llll111lll_opy_.QUIT, bstack1llll111l11_opy_.PRE), self.on_close)
        self.bstack1lll1ll1111_opy_ = bstack1lll1ll1111_opy_
    def is_enabled(self) -> bool:
        return True
    def bstack1l11lll11ll_opy_(
        self,
        f: bstack1ll1ll1111l_opy_,
        bstack1l11ll1ll11_opy_: object,
        exec: Tuple[bstack1lll1ll1ll1_opy_, str],
        bstack1llll1lllll_opy_: Tuple[bstack1llll111lll_opy_, bstack1llll111l11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l11l1l_opy_ (u"ࠨ࡬ࡢࡷࡱࡧ࡭ࠨᎅ"):
            return
        if not bstack1l1l11ll1ll_opy_():
            self.logger.debug(bstack1l11l1l_opy_ (u"ࠢࡓࡧࡷࡹࡷࡴࡩ࡯ࡩࠣ࡭ࡳࠦ࡬ࡢࡷࡱࡧ࡭ࠦ࡭ࡦࡶ࡫ࡳࡩ࠲ࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦᎆ"))
            return
        def wrapped(bstack1l11ll1ll11_opy_, launch, *args, **kwargs):
            response = self.bstack1l11lll1l11_opy_(f.platform_index, instance.ref(), json.dumps({bstack1l11l1l_opy_ (u"ࠨ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧᎇ"): True}).encode(bstack1l11l1l_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣᎈ")))
            if response is not None and response.capabilities:
                if not bstack1l1l11ll1ll_opy_():
                    browser = launch(bstack1l11ll1ll11_opy_)
                    return browser
                bstack1l11ll1l11l_opy_ = json.loads(response.capabilities.decode(bstack1l11l1l_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤᎉ")))
                if not bstack1l11ll1l11l_opy_: # empty caps bstack1l11ll111ll_opy_ bstack1l11ll11ll1_opy_ bstack1l11lll1111_opy_ bstack1lll11111l1_opy_ or error in processing
                    return
                bstack1l11lll1l1l_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l11ll1l11l_opy_))
                f.bstack1llll1l111l_opy_(instance, bstack1ll1ll1111l_opy_.bstack1l11ll11l1l_opy_, bstack1l11lll1l1l_opy_)
                f.bstack1llll1l111l_opy_(instance, bstack1ll1ll1111l_opy_.bstack1l11lll111l_opy_, bstack1l11ll1l11l_opy_)
                browser = bstack1l11ll1ll11_opy_.connect(bstack1l11lll1l1l_opy_)
                return browser
        return wrapped
    def bstack1l11ll11lll_opy_(
        self,
        f: bstack1ll1ll1111l_opy_,
        Connection: object,
        exec: Tuple[bstack1lll1ll1ll1_opy_, str],
        bstack1llll1lllll_opy_: Tuple[bstack1llll111lll_opy_, bstack1llll111l11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l11l1l_opy_ (u"ࠦࡩ࡯ࡳࡱࡣࡷࡧ࡭ࠨᎊ"):
            self.logger.debug(bstack1l11l1l_opy_ (u"ࠧࡘࡥࡵࡷࡵࡲ࡮ࡴࡧࠡ࡫ࡱࠤࡩ࡯ࡳࡱࡣࡷࡧ࡭ࠦ࡭ࡦࡶ࡫ࡳࡩ࠲ࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦᎋ"))
            return
        if not bstack1l1l11ll1ll_opy_():
            return
        def wrapped(Connection, dispatch, *args, **kwargs):
            data = args[0]
            try:
                if args and args[0].get(bstack1l11l1l_opy_ (u"࠭ࡰࡢࡴࡤࡱࡸ࠭ᎌ"), {}).get(bstack1l11l1l_opy_ (u"ࠧࡣࡵࡓࡥࡷࡧ࡭ࡴࠩᎍ")):
                    bstack1l11ll1ll1l_opy_ = args[0][bstack1l11l1l_opy_ (u"ࠣࡲࡤࡶࡦࡳࡳࠣᎎ")][bstack1l11l1l_opy_ (u"ࠤࡥࡷࡕࡧࡲࡢ࡯ࡶࠦᎏ")]
                    session_id = bstack1l11ll1ll1l_opy_.get(bstack1l11l1l_opy_ (u"ࠥࡷࡪࡹࡳࡪࡱࡱࡍࡩࠨ᎐"))
                    f.bstack1llll1l111l_opy_(instance, bstack1ll1ll1111l_opy_.bstack1l11ll1l111_opy_, session_id)
            except Exception as e:
                self.logger.debug(bstack1l11l1l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡨ࡮ࡹࡰࡢࡶࡦ࡬ࠥࡳࡥࡵࡪࡲࡨ࠿ࠦࠢ᎑"), e)
            dispatch(Connection, *args)
        return wrapped
    def bstack1l11lll11l1_opy_(
        self,
        f: bstack1ll1ll1111l_opy_,
        bstack1l11ll1ll11_opy_: object,
        exec: Tuple[bstack1lll1ll1ll1_opy_, str],
        bstack1llll1lllll_opy_: Tuple[bstack1llll111lll_opy_, bstack1llll111l11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l11l1l_opy_ (u"ࠧࡩ࡯࡯ࡰࡨࡧࡹࠨ᎒"):
            return
        if not bstack1l1l11ll1ll_opy_():
            self.logger.debug(bstack1l11l1l_opy_ (u"ࠨࡒࡦࡶࡸࡶࡳ࡯࡮ࡨࠢ࡬ࡲࠥࡩ࡯࡯ࡰࡨࡧࡹࠦ࡭ࡦࡶ࡫ࡳࡩ࠲ࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦ᎓"))
            return
        def wrapped(bstack1l11ll1ll11_opy_, connect, *args, **kwargs):
            response = self.bstack1l11lll1l11_opy_(f.platform_index, instance.ref(), json.dumps({bstack1l11l1l_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭᎔"): True}).encode(bstack1l11l1l_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢ᎕")))
            if response is not None and response.capabilities:
                bstack1l11ll1l11l_opy_ = json.loads(response.capabilities.decode(bstack1l11l1l_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣ᎖")))
                if not bstack1l11ll1l11l_opy_:
                    return
                bstack1l11lll1l1l_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l11ll1l11l_opy_))
                if bstack1l11ll1l11l_opy_.get(bstack1l11l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ᎗")):
                    browser = bstack1l11ll1ll11_opy_.bstack1l11ll1lll1_opy_(bstack1l11lll1l1l_opy_)
                    return browser
                else:
                    args = list(args)
                    args[0] = bstack1l11lll1l1l_opy_
                    return connect(bstack1l11ll1ll11_opy_, *args, **kwargs)
        return wrapped
    def bstack1l11ll1l1l1_opy_(
        self,
        f: bstack1ll1ll1111l_opy_,
        bstack1l1ll1l1l1l_opy_: object,
        exec: Tuple[bstack1lll1ll1ll1_opy_, str],
        bstack1llll1lllll_opy_: Tuple[bstack1llll111lll_opy_, bstack1llll111l11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l11l1l_opy_ (u"ࠦࡳ࡫ࡷࡠࡲࡤ࡫ࡪࠨ᎘"):
            return
        if not bstack1l1l11ll1ll_opy_():
            self.logger.debug(bstack1l11l1l_opy_ (u"ࠧࡘࡥࡵࡷࡵࡲ࡮ࡴࡧࠡ࡫ࡱࠤࡳ࡫ࡷࡠࡲࡤ࡫ࡪࠦ࡭ࡦࡶ࡫ࡳࡩ࠲ࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦ᎙"))
            return
        def wrapped(bstack1l1ll1l1l1l_opy_, bstack1l11ll11l11_opy_, *args, **kwargs):
            contexts = bstack1l1ll1l1l1l_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack1l11l1l_opy_ (u"ࠨࡡࡣࡱࡸࡸ࠿ࡨ࡬ࡢࡰ࡮ࠦ᎚") in page.url:
                                return page
                            else:
                                return bstack1l11ll11l11_opy_(bstack1l1ll1l1l1l_opy_)
                    else:
                        return bstack1l11ll11l11_opy_(bstack1l1ll1l1l1l_opy_)
        return wrapped
    def bstack1l11lll1l11_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        self.logger.debug(bstack1l11l1l_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡺࡩࡧࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡪࡶ࠽ࠤࠧ᎛") + str(req) + bstack1l11l1l_opy_ (u"ࠣࠤ᎜"))
        try:
            r = self.bstack1lll1l11ll1_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack1l11l1l_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࡷࡺࡩࡣࡦࡵࡶࡁࠧ᎝") + str(r.success) + bstack1l11l1l_opy_ (u"ࠥࠦ᎞"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l11l1l_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤ᎟") + str(e) + bstack1l11l1l_opy_ (u"ࠧࠨᎠ"))
            traceback.print_exc()
            raise e
    def bstack1l11ll1l1ll_opy_(
        self,
        f: bstack1ll1ll1111l_opy_,
        Connection: object,
        exec: Tuple[bstack1lll1ll1ll1_opy_, str],
        bstack1llll1lllll_opy_: Tuple[bstack1llll111lll_opy_, bstack1llll111l11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l11l1l_opy_ (u"ࠨ࡟ࡴࡧࡱࡨࡤࡳࡥࡴࡵࡤ࡫ࡪࡥࡴࡰࡡࡶࡩࡷࡼࡥࡳࠤᎡ"):
            return
        if not bstack1l1l11ll1ll_opy_():
            return
        def wrapped(Connection, bstack1l11ll1llll_opy_, *args, **kwargs):
            return bstack1l11ll1llll_opy_(Connection, *args, **kwargs)
        return wrapped
    def on_close(
        self,
        f: bstack1ll1ll1111l_opy_,
        bstack1l11ll1ll11_opy_: object,
        exec: Tuple[bstack1lll1ll1ll1_opy_, str],
        bstack1llll1lllll_opy_: Tuple[bstack1llll111lll_opy_, bstack1llll111l11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l11l1l_opy_ (u"ࠢࡤ࡮ࡲࡷࡪࠨᎢ"):
            return
        if not bstack1l1l11ll1ll_opy_():
            self.logger.debug(bstack1l11l1l_opy_ (u"ࠣࡔࡨࡸࡺࡸ࡮ࡪࡰࡪࠤ࡮ࡴࠠࡤ࡮ࡲࡷࡪࠦ࡭ࡦࡶ࡫ࡳࡩ࠲ࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦᎣ"))
            return
        def wrapped(Connection, close, *args, **kwargs):
            return close(Connection)
        return wrapped