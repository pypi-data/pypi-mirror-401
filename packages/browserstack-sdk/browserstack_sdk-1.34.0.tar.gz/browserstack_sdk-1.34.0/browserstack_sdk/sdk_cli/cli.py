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
import subprocess
import threading
import time
import sys
import grpc
import os
from browserstack_sdk import sdk_pb2_grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1llll1llll1_opy_ import bstack1llll1lllll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1l1l1_opy_ import bstack1ll1l1ll1ll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l111ll_opy_ import bstack1lll111ll11_opy_
from browserstack_sdk.sdk_cli.bstack1lll11l1lll_opy_ import bstack1ll11llllll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1lllll1l_opy_ import bstack1ll1l1l11l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll11ll11ll_opy_ import bstack1ll1l1l1lll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l11111l_opy_ import bstack1lll111lll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l11l11_opy_ import bstack1ll1ll1ll11_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1l111l_opy_ import bstack1lll11l1ll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll111l1ll_opy_ import bstack1ll1l11llll_opy_
from browserstack_sdk.sdk_cli.bstack11ll111ll_opy_ import bstack11ll111ll_opy_, bstack1lll1ll1_opy_, bstack1ll1lll11l_opy_
from browserstack_sdk.sdk_cli.pytest_bdd_framework import PytestBDDFramework
from browserstack_sdk.sdk_cli.bstack1ll11lll1l1_opy_ import bstack1lll11l11ll_opy_
from browserstack_sdk.sdk_cli.bstack1lll11ll1ll_opy_ import bstack1ll11llll11_opy_
from browserstack_sdk.sdk_cli.bstack1lll1ll1l11_opy_ import bstack1llll11l11l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1ll111_opy_ import bstack1ll1l1111l1_opy_
from bstack_utils.helper import Notset, bstack1lll111111l_opy_, get_cli_dir, bstack1ll1ll1ll1l_opy_, bstack1lllllll1_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework
from browserstack_sdk.sdk_cli.utils.bstack1ll1llll11l_opy_ import bstack1lll111llll_opy_
from browserstack_sdk.sdk_cli.utils.bstack11lll1l1l_opy_ import bstack11l11l1l1_opy_
from bstack_utils.helper import Notset, bstack1lll111111l_opy_, get_cli_dir, bstack1ll1ll1ll1l_opy_, bstack1lllllll1_opy_, bstack11l1l1l1l_opy_, bstack1l11l1l1ll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll1lll1111_opy_, bstack1ll1llllll1_opy_, bstack1lll11ll1l1_opy_, bstack1ll11ll111l_opy_
from browserstack_sdk.sdk_cli.bstack1lll1ll1l11_opy_ import bstack1llll11l1ll_opy_, bstack1lll1l1ll11_opy_, bstack1llll11l111_opy_
from bstack_utils.constants import *
from bstack_utils.bstack11l1lll1l1_opy_ import bstack11ll11ll1_opy_
from bstack_utils import bstack1ll1lll11_opy_
from typing import Any, List, Union, Dict
import traceback
from google.protobuf.json_format import MessageToDict
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path
from functools import wraps
from bstack_utils.measure import measure
from bstack_utils.messages import bstack11l1l1l1l1_opy_, bstack111ll1l1l_opy_
logger = bstack1ll1lll11_opy_.get_logger(__name__, bstack1ll1lll11_opy_.bstack1ll1ll11l1l_opy_())
def bstack1lll1l11l1l_opy_(bs_config):
    bstack1ll1l1ll1l1_opy_ = None
    bstack1ll1l11l1ll_opy_ = None
    try:
        bstack1ll1l11l1ll_opy_ = get_cli_dir()
        bstack1ll1l1ll1l1_opy_ = bstack1ll1ll1ll1l_opy_(bstack1ll1l11l1ll_opy_)
        bstack1ll1ll11lll_opy_ = bstack1lll111111l_opy_(bstack1ll1l1ll1l1_opy_, bstack1ll1l11l1ll_opy_, bs_config)
        bstack1ll1l1ll1l1_opy_ = bstack1ll1ll11lll_opy_ if bstack1ll1ll11lll_opy_ else bstack1ll1l1ll1l1_opy_
        if not bstack1ll1l1ll1l1_opy_:
            raise ValueError(bstack1l111l1_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡕࡇࡏࡤࡉࡌࡊࡡࡅࡍࡓࡥࡐࡂࡖࡋࠦᄥ"))
    except Exception as ex:
        logger.debug(bstack1l111l1_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡤࡰࡹࡱࡰࡴࡧࡤࡪࡰࡪࠤࡹ࡮ࡥࠡ࡮ࡤࡸࡪࡹࡴࠡࡤ࡬ࡲࡦࡸࡹࠡࡽࢀࠦᄦ").format(ex))
        bstack1ll1l1ll1l1_opy_ = os.environ.get(bstack1l111l1_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡆࡎࡔ࡟ࡑࡃࡗࡌࠧᄧ"))
        if bstack1ll1l1ll1l1_opy_:
            logger.debug(bstack1l111l1_opy_ (u"ࠥࡊࡦࡲ࡬ࡪࡰࡪࠤࡧࡧࡣ࡬ࠢࡷࡳ࡙ࠥࡄࡌࡡࡆࡐࡎࡥࡂࡊࡐࡢࡔࡆ࡚ࡈࠡࡨࡵࡳࡲࠦࡥ࡯ࡸ࡬ࡶࡴࡴ࡭ࡦࡰࡷ࠾ࠥࠨᄨ") + str(bstack1ll1l1ll1l1_opy_) + bstack1l111l1_opy_ (u"ࠦࠧᄩ"))
        else:
            logger.debug(bstack1l111l1_opy_ (u"ࠧࡔ࡯ࠡࡸࡤࡰ࡮ࡪࠠࡔࡆࡎࡣࡈࡒࡉࡠࡄࡌࡒࡤࡖࡁࡕࡊࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥ࡫࡮ࡷ࡫ࡵࡳࡳࡳࡥ࡯ࡶ࠾ࠤࡸ࡫ࡴࡶࡲࠣࡱࡦࡿࠠࡣࡧࠣ࡭ࡳࡩ࡯࡮ࡲ࡯ࡩࡹ࡫࠮ࠣᄪ"))
    return bstack1ll1l1ll1l1_opy_, bstack1ll1l11l1ll_opy_
bstack1lll1l1l111_opy_ = bstack1l111l1_opy_ (u"ࠨ࠹࠺࠻࠼ࠦᄫ")
bstack1ll1l111l1l_opy_ = bstack1l111l1_opy_ (u"ࠢࡳࡧࡤࡨࡾࠨᄬ")
bstack1ll11ll1lll_opy_ = bstack1l111l1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡇࡏࡎࡠࡕࡈࡗࡘࡏࡏࡏࡡࡌࡈࠧᄭ")
bstack1ll1lll1ll1_opy_ = bstack1l111l1_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡏࡍࡤࡈࡉࡏࡡࡏࡍࡘ࡚ࡅࡏࡡࡄࡈࡉࡘࠢᄮ")
bstack11l1ll1l1_opy_ = bstack1l111l1_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓࠨᄯ")
bstack1ll1l1lll11_opy_ = re.compile(bstack1l111l1_opy_ (u"ࡶࠧ࠮࠿ࡪࠫ࠱࠮࠭ࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࢀࡇ࡙ࠩ࠯ࠬࠥᄰ"))
bstack1ll11ll11l1_opy_ = bstack1l111l1_opy_ (u"ࠧࡪࡥࡷࡧ࡯ࡳࡵࡳࡥ࡯ࡶࠥᄱ")
bstack1ll1llll111_opy_ = bstack1l111l1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡏࡓࡅࡈࡣࡋࡇࡌࡍࡄࡄࡇࡐࠨᄲ")
bstack1ll1l11ll11_opy_ = [
    bstack1lll1ll1_opy_.bstack11111111l_opy_,
    bstack1lll1ll1_opy_.CONNECT,
    bstack1lll1ll1_opy_.bstack1lll11l1l_opy_,
]
class SDKCLI:
    _1ll11l1llll_opy_ = None
    process: Union[None, Any]
    bstack1ll1l1lllll_opy_: bool
    bstack1ll1lll1l1l_opy_: bool
    bstack1ll11lll11l_opy_: bool
    bin_session_id: Union[None, str]
    cli_bin_session_id: Union[None, str]
    cli_listen_addr: Union[None, str]
    bstack1ll1l11l11l_opy_: Union[None, grpc.Channel]
    bstack1lll11l111l_opy_: str
    test_framework: TestFramework
    bstack1lll1ll1l11_opy_: bstack1llll11l11l_opy_
    session_framework: str
    config: Union[None, Dict[str, Any]]
    bstack1ll1l1ll11l_opy_: bstack1ll1l11llll_opy_
    accessibility: bstack1lll111ll11_opy_
    bstack11lll1l1l_opy_: bstack11l11l1l1_opy_
    ai: bstack1ll11llllll_opy_
    bstack1lll11lll1l_opy_: bstack1ll1l1l11l1_opy_
    bstack1lll111ll1l_opy_: List[bstack1ll1l1ll1ll_opy_]
    config_testhub: Any
    config_observability: Any
    config_accessibility: Any
    bstack1ll1lll1lll_opy_: Any
    bstack1ll11l1ll1l_opy_: Dict[str, timedelta]
    bstack1lll1l1l11l_opy_: str
    bstack1llll1llll1_opy_: bstack1llll1lllll_opy_
    def __new__(cls):
        if not cls._1ll11l1llll_opy_:
            cls._1ll11l1llll_opy_ = super(SDKCLI, cls).__new__(cls)
        return cls._1ll11l1llll_opy_
    def __init__(self):
        self.process = None
        self.bstack1ll1l1lllll_opy_ = False
        self.bstack1ll1l11l11l_opy_ = None
        self.bstack1lll11l1l1l_opy_ = None
        self.cli_bin_session_id = None
        self.cli_listen_addr = os.environ.get(bstack1ll1lll1ll1_opy_, None)
        self.bstack1lll1111lll_opy_ = os.environ.get(bstack1ll11ll1lll_opy_, bstack1l111l1_opy_ (u"ࠢࠣᄳ")) == bstack1l111l1_opy_ (u"ࠣࠤᄴ")
        self.bstack1ll1lll1l1l_opy_ = False
        self.bstack1ll11lll11l_opy_ = False
        self.config = None
        self.config_testhub = None
        self.config_observability = None
        self.config_accessibility = None
        self.bstack1ll1lll1lll_opy_ = None
        self.test_framework = None
        self.bstack1lll1ll1l11_opy_ = None
        self.bstack1lll11l111l_opy_=bstack1l111l1_opy_ (u"ࠤࠥᄵ")
        self.session_framework = None
        self.logger = bstack1ll1lll11_opy_.get_logger(self.__class__.__name__, bstack1ll1lll11_opy_.bstack1ll1ll11l1l_opy_())
        self.bstack1ll11l1ll1l_opy_ = defaultdict(lambda: timedelta(microseconds=0))
        self.bstack1llll1llll1_opy_ = bstack1llll1lllll_opy_()
        self.bstack1ll1ll1l1l1_opy_ = None
        self.bstack1ll1l11ll1l_opy_ = None
        self.bstack1ll1l1ll11l_opy_ = None
        self.accessibility = None
        self.ai = None
        self.percy = None
        self.bstack1lll111ll1l_opy_ = []
    def bstack11lll1lll_opy_(self):
        return os.environ.get(bstack11l1ll1l1_opy_).lower().__eq__(bstack1l111l1_opy_ (u"ࠥࡸࡷࡻࡥࠣᄶ"))
    def is_enabled(self, config):
        if os.environ.get(bstack1ll1llll111_opy_, bstack1l111l1_opy_ (u"ࠫࠬᄷ")).lower() in [bstack1l111l1_opy_ (u"ࠬࡺࡲࡶࡧࠪᄸ"), bstack1l111l1_opy_ (u"࠭࠱ࠨᄹ"), bstack1l111l1_opy_ (u"ࠧࡺࡧࡶࠫᄺ")]:
            self.logger.debug(bstack1l111l1_opy_ (u"ࠣࡈࡲࡶࡨ࡯࡮ࡨࠢࡩࡥࡱࡲࡢࡢࡥ࡮ࠤࡲࡵࡤࡦࠢࡧࡹࡪࠦࡴࡰࠢࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡒࡖࡈࡋ࡟ࡇࡃࡏࡐࡇࡇࡃࡌࠢࡨࡲࡻ࡯ࡲࡰࡰࡰࡩࡳࡺࠠࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠤᄻ"))
            os.environ[bstack1l111l1_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡌࡒࡆࡘ࡙ࡠࡋࡖࡣࡗ࡛ࡎࡏࡋࡑࡋࠧᄼ")] = bstack1l111l1_opy_ (u"ࠥࡊࡦࡲࡳࡦࠤᄽ")
            return False
        if bstack1l111l1_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨᄾ") in config and str(config[bstack1l111l1_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩᄿ")]).lower() != bstack1l111l1_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬᅀ"):
            return False
        bstack1lll111l111_opy_ = [bstack1l111l1_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺࠢᅁ"), bstack1l111l1_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠧᅂ")]
        bstack1ll1l11l111_opy_ = config.get(bstack1l111l1_opy_ (u"ࠤࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠧᅃ")) in bstack1lll111l111_opy_ or os.environ.get(bstack1l111l1_opy_ (u"ࠪࡊࡗࡇࡍࡆ࡙ࡒࡖࡐࡥࡕࡔࡇࡇࠫᅄ")) in bstack1lll111l111_opy_
        os.environ[bstack1l111l1_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆࡎࡔࡁࡓ࡛ࡢࡍࡘࡥࡒࡖࡐࡑࡍࡓࡍࠢᅅ")] = str(bstack1ll1l11l111_opy_) # bstack1ll1l11l1l1_opy_ bstack1ll1l1l1l11_opy_ VAR to bstack1ll1ll1l111_opy_ is binary running
        return bstack1ll1l11l111_opy_
    def bstack11l1llll1l_opy_(self):
        for event in bstack1ll1l11ll11_opy_:
            bstack11ll111ll_opy_.register(
                event, lambda event_name, *args, **kwargs: bstack11ll111ll_opy_.logger.debug(bstack1l111l1_opy_ (u"ࠧࢁࡥࡷࡧࡱࡸࡤࡴࡡ࡮ࡧࢀࠤࡂࡄࠠࡼࡣࡵ࡫ࡸࢃࠠࠣᅆ") + str(kwargs) + bstack1l111l1_opy_ (u"ࠨࠢᅇ"))
            )
        bstack11ll111ll_opy_.register(bstack1lll1ll1_opy_.bstack11111111l_opy_, self.__1ll1l111l11_opy_)
        bstack11ll111ll_opy_.register(bstack1lll1ll1_opy_.CONNECT, self.__1ll1lllll11_opy_)
        bstack11ll111ll_opy_.register(bstack1lll1ll1_opy_.bstack1lll11l1l_opy_, self.__1ll11llll1l_opy_)
        bstack11ll111ll_opy_.register(bstack1lll1ll1_opy_.bstack1l1lll1ll1_opy_, self.__1ll1l1111ll_opy_)
    def bstack1llll11111_opy_(self):
        return not self.bstack1lll1111lll_opy_ and os.environ.get(bstack1ll11ll1lll_opy_, bstack1l111l1_opy_ (u"ࠢࠣᅈ")) != bstack1l111l1_opy_ (u"ࠣࠤᅉ")
    def is_running(self):
        if self.bstack1lll1111lll_opy_:
            return self.bstack1ll1l1lllll_opy_
        else:
            return bool(self.bstack1ll1l11l11l_opy_)
    def bstack1ll1l1llll1_opy_(self, module):
        return any(isinstance(m, module) for m in self.bstack1lll111ll1l_opy_) and cli.is_running()
    def __1ll11lllll1_opy_(self, bstack1ll1ll111ll_opy_=10):
        if self.bstack1lll11l1l1l_opy_:
            return
        bstack1ll11llll_opy_ = datetime.now()
        cli_listen_addr = os.environ.get(bstack1ll1lll1ll1_opy_, self.cli_listen_addr)
        self.logger.debug(bstack1l111l1_opy_ (u"ࠤ࡞ࠦᅊ") + str(id(self)) + bstack1l111l1_opy_ (u"ࠥࡡࠥࡩ࡯࡯ࡰࡨࡧࡹ࡯࡮ࡨࠤᅋ"))
        channel = grpc.insecure_channel(cli_listen_addr, options=[(bstack1l111l1_opy_ (u"ࠦ࡬ࡸࡰࡤ࠰ࡨࡲࡦࡨ࡬ࡦࡡ࡫ࡸࡹࡶ࡟ࡱࡴࡲࡼࡾࠨᅌ"), 0), (bstack1l111l1_opy_ (u"ࠧ࡭ࡲࡱࡥ࠱ࡩࡳࡧࡢ࡭ࡧࡢ࡬ࡹࡺࡰࡴࡡࡳࡶࡴࡾࡹࠣᅍ"), 0)])
        grpc.channel_ready_future(channel).result(timeout=bstack1ll1ll111ll_opy_)
        self.bstack1ll1l11l11l_opy_ = channel
        self.bstack1lll11l1l1l_opy_ = sdk_pb2_grpc.SDKStub(self.bstack1ll1l11l11l_opy_)
        self.bstack111lll11l_opy_(bstack1l111l1_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡨࡵ࡮࡯ࡧࡦࡸࠧᅎ"), datetime.now() - bstack1ll11llll_opy_)
        self.cli_listen_addr = cli_listen_addr
        os.environ[bstack1ll1lll1ll1_opy_] = self.cli_listen_addr
        self.logger.debug(bstack1l111l1_opy_ (u"ࠢ࡜ࡽ࡬ࡨ࠭ࡹࡥ࡭ࡨࠬࢁࡢࠦࡣࡰࡰࡱࡩࡨࡺࡥࡥ࠼ࠣ࡭ࡸࡥࡣࡩ࡫࡯ࡨࡤࡶࡲࡰࡥࡨࡷࡸࡃࠢᅏ") + str(self.bstack1llll11111_opy_()) + bstack1l111l1_opy_ (u"ࠣࠤᅐ"))
    def __1ll11llll1l_opy_(self, event_name):
        if self.bstack1llll11111_opy_():
            self.logger.debug(bstack1l111l1_opy_ (u"ࠤࡦ࡬࡮ࡲࡤ࠮ࡲࡵࡳࡨ࡫ࡳࡴ࠼ࠣࡷࡹࡵࡰࡱ࡫ࡱ࡫ࠥࡉࡌࡊࠤᅑ"))
        self.__1ll11l1l1l1_opy_()
    def __1ll1l1111ll_opy_(self, event_name, bstack1lll1l11lll_opy_ = None, exit_code=1):
        if exit_code == 1:
            self.logger.error(bstack1l111l1_opy_ (u"ࠥࡗࡴࡳࡥࡵࡪ࡬ࡲ࡬ࠦࡷࡦࡰࡷࠤࡼࡸ࡯࡯ࡩࠥᅒ"))
        bstack1lll11l11l1_opy_ = Path(bstack1ll1ll1111l_opy_ (u"ࠦࢀࡹࡥ࡭ࡨ࠱ࡧࡱ࡯࡟ࡥ࡫ࡵࢁ࠴ࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࡹ࠮࡫ࡵࡲࡲࠧᅓ"))
        if self.bstack1ll1l11l1ll_opy_ and bstack1lll11l11l1_opy_.exists():
            with open(bstack1lll11l11l1_opy_, bstack1l111l1_opy_ (u"ࠬࡸࠧᅔ"), encoding=bstack1l111l1_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬᅕ")) as fp:
                data = json.load(fp)
                try:
                    bstack11l1l1l1l_opy_(bstack1l111l1_opy_ (u"ࠧࡑࡑࡖࡘࠬᅖ"), bstack11ll11ll1_opy_(bstack1l1l1111ll_opy_), data, {
                        bstack1l111l1_opy_ (u"ࠨࡣࡸࡸ࡭࠭ᅗ"): (self.config[bstack1l111l1_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫᅘ")], self.config[bstack1l111l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ᅙ")])
                    })
                except Exception as e:
                    logger.debug(bstack111ll1l1l_opy_.format(str(e)))
            bstack1lll11l11l1_opy_.unlink()
        sys.exit(exit_code)
    @measure(event_name=EVENTS.bstack1lll1l111l1_opy_, stage=STAGE.bstack11l11l11l1_opy_)
    def __1ll1l111l11_opy_(self, event_name: str, data):
        from bstack_utils.bstack11lll1l1ll_opy_ import bstack1ll11ll1ll1_opy_
        self.bstack1lll11l111l_opy_, self.bstack1ll1l11l1ll_opy_ = bstack1lll1l11l1l_opy_(data.bs_config)
        os.environ[bstack1l111l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡛ࡗࡏࡔࡂࡄࡏࡉࡤࡊࡉࡓࠩᅚ")] = self.bstack1ll1l11l1ll_opy_
        if not self.bstack1lll11l111l_opy_ or not self.bstack1ll1l11l1ll_opy_:
            raise ValueError(bstack1l111l1_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡨ࡬ࡲࡩࠦࡴࡩࡧࠣࡗࡉࡑࠠࡄࡎࡌࠤࡧ࡯࡮ࡢࡴࡼࠦᅛ"))
        if self.bstack1llll11111_opy_():
            self.__1ll1lllll11_opy_(event_name, bstack1ll1lll11l_opy_())
            return
        try:
            bstack1ll11ll1ll1_opy_.end(EVENTS.bstack1l1l11ll1_opy_.value, EVENTS.bstack1l1l11ll1_opy_.value + bstack1l111l1_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᅜ"), EVENTS.bstack1l1l11ll1_opy_.value + bstack1l111l1_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᅝ"), status=True, failure=None, test_name=None)
            logger.debug(bstack1l111l1_opy_ (u"ࠣࡅࡲࡱࡵࡲࡥࡵࡧࠣࡗࡉࡑࠠࡔࡧࡷࡹࡵ࠴ࠢᅞ"))
        except Exception as e:
            logger.debug(bstack1l111l1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡲࡧࡲ࡬࡫ࡱ࡫ࠥࡱࡥࡺࠢࡰࡩࡹࡸࡩࡤࡵࠣࡿࢂࠨᅟ").format(e))
        start = datetime.now()
        is_started = self.__1ll1ll11l11_opy_()
        self.bstack111lll11l_opy_(bstack1l111l1_opy_ (u"ࠥࡷࡵࡧࡷ࡯ࡡࡷ࡭ࡲ࡫ࠢᅠ"), datetime.now() - start)
        if is_started:
            start = datetime.now()
            self.__1ll11lllll1_opy_()
            self.bstack111lll11l_opy_(bstack1l111l1_opy_ (u"ࠦࡨࡵ࡮࡯ࡧࡦࡸࡤࡺࡩ࡮ࡧࠥᅡ"), datetime.now() - start)
            start = datetime.now()
            self.__1ll1lll11l1_opy_(data)
            self.bstack111lll11l_opy_(bstack1l111l1_opy_ (u"ࠧࡹࡴࡢࡴࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡺࡩ࡮ࡧࠥᅢ"), datetime.now() - start)
    @measure(event_name=EVENTS.bstack1ll1lll111l_opy_, stage=STAGE.bstack11l11l11l1_opy_)
    def __1ll1lllll11_opy_(self, event_name: str, data: bstack1ll1lll11l_opy_):
        if not self.bstack1llll11111_opy_():
            self.logger.debug(bstack1l111l1_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡦࡳࡳࡴࡥࡤࡶ࠽ࠤࡳࡵࡴࠡࡣࠣࡧ࡭࡯࡬ࡥ࠯ࡳࡶࡴࡩࡥࡴࡵࠥᅣ"))
            return
        bin_session_id = os.environ.get(bstack1ll11ll1lll_opy_)
        start = datetime.now()
        self.__1ll11lllll1_opy_()
        self.bstack111lll11l_opy_(bstack1l111l1_opy_ (u"ࠢࡤࡱࡱࡲࡪࡩࡴࡠࡶ࡬ࡱࡪࠨᅤ"), datetime.now() - start)
        self.cli_bin_session_id = bin_session_id
        self.logger.debug(bstack1l111l1_opy_ (u"ࠣ࡝ࡾ࡭ࡩ࠮ࡳࡦ࡮ࡩ࠭ࢂࡣࠠࡤࡪ࡬ࡰࡩ࠳ࡰࡳࡱࡦࡩࡸࡹ࠺ࠡࡥࡲࡲࡳ࡫ࡣࡵࡧࡧࠤࡹࡵࠠࡦࡺ࡬ࡷࡹ࡯࡮ࡨࠢࡆࡐࡎࠦࠢᅥ") + str(bin_session_id) + bstack1l111l1_opy_ (u"ࠤࠥᅦ"))
        start = datetime.now()
        self.__1lll1111l1l_opy_()
        self.bstack111lll11l_opy_(bstack1l111l1_opy_ (u"ࠥࡷࡹࡧࡲࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡸ࡮ࡳࡥࠣᅧ"), datetime.now() - start)
    def __1ll1llll1ll_opy_(self):
        if not self.bstack1lll11l1l1l_opy_ or not self.cli_bin_session_id:
            self.logger.debug(bstack1l111l1_opy_ (u"ࠦࡨࡧ࡮࡯ࡱࡷࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷ࡫ࠠ࡮ࡱࡧࡹࡱ࡫ࡳࠣᅨ"))
            return
        bstack1ll11l1l11l_opy_ = {
            bstack1l111l1_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤᅩ"): (bstack1ll1ll1ll11_opy_, bstack1lll11l1ll1_opy_, bstack1ll1l1111l1_opy_),
            bstack1l111l1_opy_ (u"ࠨࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠣᅪ"): (bstack1ll1l1l1lll_opy_, bstack1lll111lll1_opy_, bstack1ll11llll11_opy_),
        }
        if not self.bstack1ll1ll1l1l1_opy_ and self.session_framework in bstack1ll11l1l11l_opy_:
            bstack1ll1lll1l11_opy_, bstack1lll1111ll1_opy_, bstack1ll11ll1l1l_opy_ = bstack1ll11l1l11l_opy_[self.session_framework]
            bstack1lll11ll111_opy_ = bstack1lll1111ll1_opy_()
            self.bstack1ll1l11ll1l_opy_ = bstack1lll11ll111_opy_
            self.bstack1ll1ll1l1l1_opy_ = bstack1ll11ll1l1l_opy_
            self.bstack1lll111ll1l_opy_.append(bstack1lll11ll111_opy_)
            self.bstack1lll111ll1l_opy_.append(bstack1ll1lll1l11_opy_(self.bstack1ll1l11ll1l_opy_))
        if not self.bstack1ll1l1ll11l_opy_ and self.config_observability and self.config_observability.success: # bstack1ll1l1l1111_opy_
            self.bstack1ll1l1ll11l_opy_ = bstack1ll1l11llll_opy_(self.bstack1ll1ll1l1l1_opy_, self.bstack1ll1l11ll1l_opy_) # bstack1ll1l1l11ll_opy_
            self.bstack1lll111ll1l_opy_.append(self.bstack1ll1l1ll11l_opy_)
        if not self.accessibility and self.config_accessibility and self.config_accessibility.success:
            self.accessibility = bstack1lll111ll11_opy_(self.bstack1ll1ll1l1l1_opy_, self.bstack1ll1l11ll1l_opy_)
            self.bstack1lll111ll1l_opy_.append(self.accessibility)
        if not self.ai and isinstance(self.config, dict) and self.config.get(bstack1l111l1_opy_ (u"ࠢࡴࡧ࡯ࡪࡍ࡫ࡡ࡭ࠤᅫ"), False) == True:
            self.ai = bstack1ll11llllll_opy_()
            self.bstack1lll111ll1l_opy_.append(self.ai)
        if not self.percy and self.bstack1ll1lll1lll_opy_ and self.bstack1ll1lll1lll_opy_.success:
            self.percy = bstack1ll1l1l11l1_opy_(self.bstack1ll1lll1lll_opy_)
            self.bstack1lll111ll1l_opy_.append(self.percy)
        for mod in self.bstack1lll111ll1l_opy_:
            if not mod.bstack1ll11lll1ll_opy_():
                mod.configure(self.bstack1lll11l1l1l_opy_, self.config, self.cli_bin_session_id, self.bstack1llll1llll1_opy_)
    def __1lll111l1l1_opy_(self):
        for mod in self.bstack1lll111ll1l_opy_:
            if mod.bstack1ll11lll1ll_opy_():
                mod.configure(self.bstack1lll11l1l1l_opy_, None, None, None)
    @measure(event_name=EVENTS.bstack1ll11ll1111_opy_, stage=STAGE.bstack11l11l11l1_opy_)
    def __1ll1lll11l1_opy_(self, data):
        if not self.cli_bin_session_id or self.bstack1ll1lll1l1l_opy_:
            return
        self.__1ll1l111lll_opy_(data)
        bstack1ll11llll_opy_ = datetime.now()
        req = structs.StartBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.path_project = os.getcwd()
        req.language = bstack1l111l1_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࠣᅬ")
        req.sdk_language = bstack1l111l1_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯ࠤᅭ")
        req.path_config = data.path_config
        req.sdk_version = data.sdk_version
        req.test_framework = data.test_framework
        req.frameworks.extend(data.frameworks)
        req.framework_versions.update(data.framework_versions)
        req.env_vars.update({key: value for key, value in os.environ.items() if bool(bstack1ll1l1lll11_opy_.search(key))})
        req.cli_args.extend(sys.argv)
        try:
            self.logger.debug(bstack1l111l1_opy_ (u"ࠥ࡟ࠧᅮ") + str(id(self)) + bstack1l111l1_opy_ (u"ࠦࡢࠦ࡭ࡢ࡫ࡱ࠱ࡵࡸ࡯ࡤࡧࡶࡷ࠿ࠦࡳࡵࡣࡵࡸࡤࡨࡩ࡯ࡡࡶࡩࡸࡹࡩࡰࡰࠥᅯ"))
            r = self.bstack1lll11l1l1l_opy_.StartBinSession(req)
            self.bstack111lll11l_opy_(bstack1l111l1_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡹࡧࡲࡵࡡࡥ࡭ࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࠢᅰ"), datetime.now() - bstack1ll11llll_opy_)
            os.environ[bstack1ll11ll1lll_opy_] = r.bin_session_id
            self.__1ll11ll1l11_opy_(r)
            self.__1ll1llll1ll_opy_()
            self.bstack1llll1llll1_opy_.start()
            self.bstack1ll1lll1l1l_opy_ = True
            self.logger.debug(bstack1l111l1_opy_ (u"ࠨ࡛ࠣᅱ") + str(id(self)) + bstack1l111l1_opy_ (u"ࠢ࡞ࠢࡰࡥ࡮ࡴ࠭ࡱࡴࡲࡧࡪࡹࡳ࠻ࠢࡦࡳࡳࡴࡥࡤࡶࡨࡨࠧᅲ"))
        except grpc.bstack1ll1ll11111_opy_ as bstack1lll11111l1_opy_:
            self.logger.error(bstack1l111l1_opy_ (u"ࠣ࡝ࡾ࡭ࡩ࠮ࡳࡦ࡮ࡩ࠭ࢂࡣࠠࡵ࡫ࡰࡩࡴ࡫ࡵࡵ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥᅳ") + str(bstack1lll11111l1_opy_) + bstack1l111l1_opy_ (u"ࠤࠥᅴ"))
            traceback.print_exc()
            raise bstack1lll11111l1_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack1l111l1_opy_ (u"ࠥ࡟ࢀ࡯ࡤࠩࡵࡨࡰ࡫࠯ࡽ࡞ࠢࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢᅵ") + str(e) + bstack1l111l1_opy_ (u"ࠦࠧᅶ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1lll11ll11l_opy_, stage=STAGE.bstack11l11l11l1_opy_)
    def __1lll1111l1l_opy_(self):
        if not self.bstack1llll11111_opy_() or not self.cli_bin_session_id or self.bstack1ll11lll11l_opy_:
            return
        bstack1ll11llll_opy_ = datetime.now()
        req = structs.ConnectBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.platform_index = int(os.environ.get(bstack1l111l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᅷ"), bstack1l111l1_opy_ (u"࠭࠰ࠨᅸ")))
        try:
            self.logger.debug(bstack1l111l1_opy_ (u"ࠢ࡜ࠤᅹ") + str(id(self)) + bstack1l111l1_opy_ (u"ࠣ࡟ࠣࡧ࡭࡯࡬ࡥ࠯ࡳࡶࡴࡩࡥࡴࡵ࠽ࠤࡨࡵ࡮࡯ࡧࡦࡸࡤࡨࡩ࡯ࡡࡶࡩࡸࡹࡩࡰࡰࠥᅺ"))
            r = self.bstack1lll11l1l1l_opy_.ConnectBinSession(req)
            self.bstack111lll11l_opy_(bstack1l111l1_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡤࡱࡱࡲࡪࡩࡴࡠࡤ࡬ࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࠨᅻ"), datetime.now() - bstack1ll11llll_opy_)
            self.__1ll11ll1l11_opy_(r)
            self.__1ll1llll1ll_opy_()
            self.bstack1llll1llll1_opy_.start()
            self.bstack1ll11lll11l_opy_ = True
            self.logger.debug(bstack1l111l1_opy_ (u"ࠥ࡟ࠧᅼ") + str(id(self)) + bstack1l111l1_opy_ (u"ࠦࡢࠦࡣࡩ࡫࡯ࡨ࠲ࡶࡲࡰࡥࡨࡷࡸࡀࠠࡤࡱࡱࡲࡪࡩࡴࡦࡦࠥᅽ"))
        except grpc.bstack1ll1ll11111_opy_ as bstack1lll11111l1_opy_:
            self.logger.error(bstack1l111l1_opy_ (u"ࠧࡡࡻࡪࡦࠫࡷࡪࡲࡦࠪࡿࡠࠤࡹ࡯࡭ࡦࡱࡨࡹࡹ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢᅾ") + str(bstack1lll11111l1_opy_) + bstack1l111l1_opy_ (u"ࠨࠢᅿ"))
            traceback.print_exc()
            raise bstack1lll11111l1_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack1l111l1_opy_ (u"ࠢ࡜ࡽ࡬ࡨ࠭ࡹࡥ࡭ࡨࠬࢁࡢࠦࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦᆀ") + str(e) + bstack1l111l1_opy_ (u"ࠣࠤᆁ"))
            traceback.print_exc()
            raise e
    def __1ll11ll1l11_opy_(self, r):
        self.bstack1ll1ll1llll_opy_(r)
        if not r.bin_session_id or not r.config or not isinstance(r.config, str):
            raise ValueError(bstack1l111l1_opy_ (u"ࠤࡸࡲࡪࡾࡰࡦࡥࡷࡩࡩࠦࡳࡦࡴࡹࡩࡷࠦࡲࡦࡵࡳࡳࡳࡹࡥࠣᆂ") + str(r))
        self.config = json.loads(r.config)
        if not self.config:
            raise ValueError(bstack1l111l1_opy_ (u"ࠥࡩࡲࡶࡴࡺࠢࡦࡳࡳ࡬ࡩࡨࠢࡩࡳࡺࡴࡤࠣᆃ"))
        self.session_framework = r.session_framework
        self.config_testhub = r.testhub
        self.config_observability = r.observability
        self.config_accessibility = r.accessibility
        bstack1l111l1_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡒࡨࡶࡨࡿࠠࡪࡵࠣࡷࡪࡴࡴࠡࡱࡱࡰࡾࠦࡡࡴࠢࡳࡥࡷࡺࠠࡰࡨࠣࡸ࡭࡫ࠠࠣࡅࡲࡲࡳ࡫ࡣࡵࡄ࡬ࡲࡘ࡫ࡳࡴ࡫ࡲࡲ࠱ࠨࠠࡢࡰࡧࠤࡹ࡮ࡩࡴࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤ࡮ࡹࠠࡢ࡮ࡶࡳࠥࡻࡳࡦࡦࠣࡦࡾࠦࡓࡵࡣࡵࡸࡇ࡯࡮ࡔࡧࡶࡷ࡮ࡵ࡮࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡘ࡭࡫ࡲࡦࡨࡲࡶࡪ࠲ࠠࡏࡱࡱࡩࠥ࡮ࡡ࡯ࡦ࡯࡭ࡳ࡭ࠠࡪࡵࠣ࡭ࡲࡶ࡬ࡦ࡯ࡨࡲࡹ࡫ࡤ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᆄ")
        self.bstack1ll1lll1lll_opy_ = getattr(r, bstack1l111l1_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫᆅ"), None)
        self.cli_bin_session_id = r.bin_session_id
        os.environ[bstack1l111l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪᆆ")] = self.config_testhub.jwt
        os.environ[bstack1l111l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬᆇ")] = self.config_testhub.build_hashed_id
    def bstack1lll1111111_opy_(event_name: EVENTS, stage: STAGE):
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                if self.bstack1ll1l1lllll_opy_:
                    return func(self, *args, **kwargs)
                @measure(event_name=event_name, stage=stage)
                def bstack1lll1l11111_opy_(*a, **kw):
                    return func(self, *a, **kw)
                return bstack1lll1l11111_opy_(*args, **kwargs)
            return wrapper
        return decorator
    @bstack1lll1111111_opy_(event_name=EVENTS.bstack1ll1lllllll_opy_, stage=STAGE.bstack11l11l11l1_opy_)
    def __1ll1ll11l11_opy_(self, bstack1ll1ll111ll_opy_=10):
        if self.bstack1ll1l1lllll_opy_:
            self.logger.debug(bstack1l111l1_opy_ (u"ࠣࡵࡷࡥࡷࡺ࠺ࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡵࡹࡳࡴࡩ࡯ࡩࠥᆈ"))
            return True
        self.logger.debug(bstack1l111l1_opy_ (u"ࠤࡶࡸࡦࡸࡴࠣᆉ"))
        if os.getenv(bstack1l111l1_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡐࡎࡥࡅࡏࡘࠥᆊ")) == bstack1ll11ll11l1_opy_:
            self.cli_bin_session_id = bstack1ll11ll11l1_opy_
            self.cli_listen_addr = bstack1l111l1_opy_ (u"ࠦࡺࡴࡩࡹ࠼࠲ࡸࡲࡶ࠯ࡴࡦ࡮࠱ࡵࡲࡡࡵࡨࡲࡶࡲ࠳ࠥࡴ࠰ࡶࡳࡨࡱࠢᆋ") % (self.cli_bin_session_id)
            self.bstack1ll1l1lllll_opy_ = True
            return True
        self.process = subprocess.Popen(
            [self.bstack1lll11l111l_opy_, bstack1l111l1_opy_ (u"ࠧࡹࡤ࡬ࠤᆌ")],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=dict(os.environ),
            text=True,
            universal_newlines=True, # bstack1lll1l1111l_opy_ compat for text=True in bstack1ll1l1l1ll1_opy_ python
            encoding=bstack1l111l1_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᆍ"),
            bufsize=1,
            close_fds=True,
        )
        bstack1ll11l1ll11_opy_ = threading.Thread(target=self.__1ll1ll1l11l_opy_, args=(bstack1ll1ll111ll_opy_,))
        bstack1ll11l1ll11_opy_.start()
        bstack1ll11l1ll11_opy_.join()
        if self.process.returncode is not None:
            self.logger.debug(bstack1l111l1_opy_ (u"ࠢ࡜ࡽ࡬ࡨ࠭ࡹࡥ࡭ࡨࠬࢁࡢࠦࡳࡱࡣࡺࡲ࠿ࠦࡲࡦࡶࡸࡶࡳࡩ࡯ࡥࡧࡀࡿࡸ࡫࡬ࡧ࠰ࡳࡶࡴࡩࡥࡴࡵ࠱ࡶࡪࡺࡵࡳࡰࡦࡳࡩ࡫ࡽࠡࡱࡸࡸࡂࢁࡳࡦ࡮ࡩ࠲ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡹࡴࡥࡱࡸࡸ࠳ࡸࡥࡢࡦࠫ࠭ࢂࠦࡥࡳࡴࡀࠦᆎ") + str(self.process.stderr.read()) + bstack1l111l1_opy_ (u"ࠣࠤᆏ"))
        if not self.bstack1ll1l1lllll_opy_:
            self.logger.debug(bstack1l111l1_opy_ (u"ࠤ࡞ࠦᆐ") + str(id(self)) + bstack1l111l1_opy_ (u"ࠥࡡࠥࡩ࡬ࡦࡣࡱࡹࡵࠨᆑ"))
            self.__1ll11l1l1l1_opy_()
        self.logger.debug(bstack1l111l1_opy_ (u"ࠦࡠࢁࡩࡥࠪࡶࡩࡱ࡬ࠩࡾ࡟ࠣࡴࡷࡵࡣࡦࡵࡶࡣࡷ࡫ࡡࡥࡻ࠽ࠤࠧᆒ") + str(self.bstack1ll1l1lllll_opy_) + bstack1l111l1_opy_ (u"ࠧࠨᆓ"))
        return self.bstack1ll1l1lllll_opy_
    def __1ll1ll1l11l_opy_(self, bstack1ll1l111111_opy_=10):
        bstack1lll11lllll_opy_ = time.time()
        while self.process and time.time() - bstack1lll11lllll_opy_ < bstack1ll1l111111_opy_:
            try:
                line = self.process.stdout.readline()
                if bstack1l111l1_opy_ (u"ࠨࡩࡥ࠿ࠥᆔ") in line:
                    self.cli_bin_session_id = line.split(bstack1l111l1_opy_ (u"ࠢࡪࡦࡀࠦᆕ"))[-1:][0].strip()
                    self.logger.debug(bstack1l111l1_opy_ (u"ࠣࡥ࡯࡭ࡤࡨࡩ࡯ࡡࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࡀࠢᆖ") + str(self.cli_bin_session_id) + bstack1l111l1_opy_ (u"ࠤࠥᆗ"))
                    continue
                if bstack1l111l1_opy_ (u"ࠥࡰ࡮ࡹࡴࡦࡰࡀࠦᆘ") in line:
                    self.cli_listen_addr = line.split(bstack1l111l1_opy_ (u"ࠦࡱ࡯ࡳࡵࡧࡱࡁࠧᆙ"))[-1:][0].strip()
                    self.logger.debug(bstack1l111l1_opy_ (u"ࠧࡩ࡬ࡪࡡ࡯࡭ࡸࡺࡥ࡯ࡡࡤࡨࡩࡸ࠺ࠣᆚ") + str(self.cli_listen_addr) + bstack1l111l1_opy_ (u"ࠨࠢᆛ"))
                    continue
                if bstack1l111l1_opy_ (u"ࠢࡱࡱࡵࡸࡂࠨᆜ") in line:
                    port = line.split(bstack1l111l1_opy_ (u"ࠣࡲࡲࡶࡹࡃࠢᆝ"))[-1:][0].strip()
                    self.logger.debug(bstack1l111l1_opy_ (u"ࠤࡳࡳࡷࡺ࠺ࠣᆞ") + str(port) + bstack1l111l1_opy_ (u"ࠥࠦᆟ"))
                    continue
                if line.strip() == bstack1ll1l111l1l_opy_ and self.cli_bin_session_id and self.cli_listen_addr:
                    if os.getenv(bstack1l111l1_opy_ (u"ࠦࡘࡊࡋࡠࡅࡏࡍࡤࡌࡌࡂࡉࡢࡍࡔࡥࡓࡕࡔࡈࡅࡒࠨᆠ"), bstack1l111l1_opy_ (u"ࠧ࠷ࠢᆡ")) == bstack1l111l1_opy_ (u"ࠨ࠱ࠣᆢ"):
                        if not self.process.stdout.closed:
                            self.process.stdout.close()
                        if not self.process.stderr.closed:
                            self.process.stderr.close()
                    self.bstack1ll1l1lllll_opy_ = True
                    return True
            except Exception as e:
                self.logger.debug(bstack1l111l1_opy_ (u"ࠢࡦࡴࡵࡳࡷࡀࠠࠣᆣ") + str(e) + bstack1l111l1_opy_ (u"ࠣࠤᆤ"))
        return False
    @measure(event_name=EVENTS.bstack1ll1l1lll1l_opy_, stage=STAGE.bstack11l11l11l1_opy_)
    def __1ll11l1l1l1_opy_(self):
        if self.bstack1ll1l11l11l_opy_:
            self.bstack1llll1llll1_opy_.stop()
            start = datetime.now()
            if self.bstack1ll1ll1l1ll_opy_():
                self.cli_bin_session_id = None
                if self.bstack1ll11lll11l_opy_:
                    self.bstack111lll11l_opy_(bstack1l111l1_opy_ (u"ࠤࡶࡸࡴࡶ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡶ࡬ࡱࡪࠨᆥ"), datetime.now() - start)
                else:
                    self.bstack111lll11l_opy_(bstack1l111l1_opy_ (u"ࠥࡷࡹࡵࡰࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡷ࡭ࡲ࡫ࠢᆦ"), datetime.now() - start)
            self.__1lll111l1l1_opy_()
            start = datetime.now()
            self.bstack1ll1l11l11l_opy_.close()
            self.bstack111lll11l_opy_(bstack1l111l1_opy_ (u"ࠦࡩ࡯ࡳࡤࡱࡱࡲࡪࡩࡴࡠࡶ࡬ࡱࡪࠨᆧ"), datetime.now() - start)
            self.bstack1ll1l11l11l_opy_ = None
        if self.process:
            self.logger.debug(bstack1l111l1_opy_ (u"ࠧࡹࡴࡰࡲࠥᆨ"))
            start = datetime.now()
            self.process.terminate()
            self.bstack111lll11l_opy_(bstack1l111l1_opy_ (u"ࠨ࡫ࡪ࡮࡯ࡣࡹ࡯࡭ࡦࠤᆩ"), datetime.now() - start)
            self.process = None
            if self.bstack1lll1111lll_opy_ and self.config_observability and self.config_testhub and self.config_testhub.testhub_events:
                self.bstack1l1l1l11l_opy_()
                self.logger.info(
                    bstack1l111l1_opy_ (u"ࠢࡗ࡫ࡶ࡭ࡹࠦࡨࡵࡶࡳࡷ࠿࠵࠯ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿࠣࡸࡴࠦࡶࡪࡧࡺࠤࡧࡻࡩ࡭ࡦࠣࡶࡪࡶ࡯ࡳࡶ࠯ࠤ࡮ࡴࡳࡪࡩ࡫ࡸࡸ࠲ࠠࡢࡰࡧࠤࡲࡧ࡮ࡺࠢࡰࡳࡷ࡫ࠠࡥࡧࡥࡹ࡬࡭ࡩ࡯ࡩࠣ࡭ࡳ࡬࡯ࡳ࡯ࡤࡸ࡮ࡵ࡮ࠡࡣ࡯ࡰࠥࡧࡴࠡࡱࡱࡩࠥࡶ࡬ࡢࡥࡨࠥࡡࡴࠢᆪ").format(
                        self.config_testhub.build_hashed_id
                    )
                )
                os.environ[bstack1l111l1_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠧᆫ")] = self.config_testhub.build_hashed_id
        self.bstack1ll1l1lllll_opy_ = False
    def __1ll1l111lll_opy_(self, data):
        try:
            import selenium
            data.framework_versions[bstack1l111l1_opy_ (u"ࠤࡶࡩࡱ࡫࡮ࡪࡷࡰࠦᆬ")] = selenium.__version__
            data.frameworks.append(bstack1l111l1_opy_ (u"ࠥࡷࡪࡲࡥ࡯࡫ࡸࡱࠧᆭ"))
        except:
            pass
        try:
            from playwright._repo_version import __version__
            data.framework_versions[bstack1l111l1_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣᆮ")] = __version__
            data.frameworks.append(bstack1l111l1_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤᆯ"))
        except:
            pass
    def bstack1lll11llll1_opy_(self, hub_url: str, platform_index: int, bstack111ll1l1_opy_: Any):
        if self.bstack1lll1ll1l11_opy_:
            self.logger.debug(bstack1l111l1_opy_ (u"ࠨࡳ࡬࡫ࡳࡴࡪࡪࠠࡴࡧࡷࡹࡵࠦࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࠻ࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡷࡪࡺࠠࡶࡲࠥᆰ"))
            return
        try:
            bstack1ll11llll_opy_ = datetime.now()
            import selenium
            from selenium.webdriver.remote.webdriver import WebDriver
            from selenium.webdriver.common.service import Service
            framework = bstack1l111l1_opy_ (u"ࠢࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠤᆱ")
            self.bstack1lll1ll1l11_opy_ = bstack1ll11llll11_opy_(
                cli.config.get(bstack1l111l1_opy_ (u"ࠣࡪࡸࡦ࡚ࡸ࡬ࠣᆲ"), hub_url),
                platform_index,
                framework_name=framework,
                framework_version=selenium.__version__,
                classes=[WebDriver],
                bstack1ll1ll111l1_opy_={bstack1l111l1_opy_ (u"ࠤࡦࡶࡪࡧࡴࡦࡡࡲࡴࡹ࡯࡯࡯ࡵࡢࡪࡷࡵ࡭ࡠࡥࡤࡴࡸࠨᆳ"): bstack111ll1l1_opy_}
            )
            def bstack1lll11l1l11_opy_(self):
                return
            if self.config.get(bstack1l111l1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠧᆴ"), True):
                Service.start = bstack1lll11l1l11_opy_
                Service.stop = bstack1lll11l1l11_opy_
            def get_accessibility_results(driver):
                if self.accessibility and self.accessibility.is_enabled():
                    return self.accessibility.get_accessibility_results(driver, framework_name=framework)
            def get_accessibility_results_summary(driver):
                if self.accessibility and self.accessibility.is_enabled():
                    return self.accessibility.get_accessibility_results_summary(driver, framework_name=framework)
            def perform_scan(driver):
                if self.accessibility and self.accessibility.is_enabled():
                    return self.accessibility.perform_scan(driver, method=None, framework_name=framework)
            WebDriver.getAccessibilityResults = get_accessibility_results
            WebDriver.get_accessibility_results = get_accessibility_results
            WebDriver.getAccessibilityResultsSummary = get_accessibility_results_summary
            WebDriver.get_accessibility_results_summary = get_accessibility_results_summary
            WebDriver.upload_attachment = staticmethod(bstack11l11l1l1_opy_.upload_attachment)
            WebDriver.set_custom_tag = staticmethod(bstack1lll111llll_opy_.set_custom_tag)
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
            self.bstack111lll11l_opy_(bstack1l111l1_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡷࡪࡲࡥ࡯࡫ࡸࡱࠧᆵ"), datetime.now() - bstack1ll11llll_opy_)
        except Exception as e:
            self.logger.error(bstack1l111l1_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࡺࡶࠠࡴࡧ࡯ࡩࡳ࡯ࡵ࡮࠼ࠣࠦᆶ") + str(e) + bstack1l111l1_opy_ (u"ࠨࠢᆷ"))
    def bstack1ll1ll11ll1_opy_(self, platform_index: int):
        try:
            from playwright.sync_api import BrowserType
            from playwright.sync_api import BrowserContext
            from playwright._impl._connection import Connection
            from playwright._repo_version import __version__
            from bstack_utils.helper import bstack1111l1lll_opy_
            self.bstack1lll1ll1l11_opy_ = bstack1ll1l1111l1_opy_(
                platform_index,
                framework_name=bstack1l111l1_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦᆸ"),
                framework_version=__version__,
                classes=[BrowserType, BrowserContext, Connection],
            )
        except Exception as e:
            self.logger.error(bstack1l111l1_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࡶࡲࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠺ࠡࠤᆹ") + str(e) + bstack1l111l1_opy_ (u"ࠤࠥᆺ"))
            pass
    def bstack1ll1l11lll1_opy_(self):
        if self.test_framework:
            self.logger.debug(bstack1l111l1_opy_ (u"ࠥࡷࡰ࡯ࡰࡱࡧࡧࠤࡸ࡫ࡴࡶࡲࠣࡴࡾࡺࡥࡴࡶ࠽ࠤࡦࡲࡲࡦࡣࡧࡽࠥࡹࡥࡵࠢࡸࡴࠧᆻ"))
            return
        if bstack1lllllll1_opy_():
            import pytest
            self.test_framework = PytestBDDFramework({ bstack1l111l1_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷࠦᆼ"): pytest.__version__ }, [bstack1l111l1_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠤᆽ")], self.bstack1llll1llll1_opy_, self.bstack1lll11l1l1l_opy_)
            return
        try:
            import pytest
            self.test_framework = bstack1lll11l11ll_opy_({ bstack1l111l1_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࠨᆾ"): pytest.__version__ }, [bstack1l111l1_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺࠢᆿ")], self.bstack1llll1llll1_opy_, self.bstack1lll11l1l1l_opy_)
        except Exception as e:
            self.logger.error(bstack1l111l1_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࡶࡲࠣࡴࡾࡺࡥࡴࡶ࠽ࠤࠧᇀ") + str(e) + bstack1l111l1_opy_ (u"ࠤࠥᇁ"))
        self.bstack1lll11l1111_opy_()
    def bstack1lll11l1111_opy_(self):
        if not self.bstack11lll1lll_opy_():
            return
        bstack1l1ll1lll1_opy_ = None
        def bstack11l1l1l1ll_opy_(config, startdir):
            return bstack1l111l1_opy_ (u"ࠥࡨࡷ࡯ࡶࡦࡴ࠽ࠤࢀ࠶ࡽࠣᇂ").format(bstack1l111l1_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥᇃ"))
        def bstack111ll11l11_opy_():
            return
        def bstack1l11ll111l_opy_(self, name: str, default=Notset(), skip: bool = False):
            if str(name).lower() == bstack1l111l1_opy_ (u"ࠬࡪࡲࡪࡸࡨࡶࠬᇄ"):
                return bstack1l111l1_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠧᇅ")
            else:
                return bstack1l1ll1lll1_opy_(self, name, default, skip)
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            bstack1l1ll1lll1_opy_ = Config.getoption
            pytest_selenium.pytest_report_header = bstack11l1l1l1ll_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack111ll11l11_opy_
            Config.getoption = bstack1l11ll111l_opy_
        except Exception as e:
            self.logger.error(bstack1l111l1_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡺࡣࡩࠢࡳࡽࡹ࡫ࡳࡵࠢࡶࡩࡱ࡫࡮ࡪࡷࡰࠤ࡫ࡵࡲࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠺ࠡࠤᇆ") + str(e) + bstack1l111l1_opy_ (u"ࠣࠤᇇ"))
    def bstack1lll11111ll_opy_(self):
        bstack11llll1l1_opy_ = MessageToDict(cli.config_testhub, preserving_proto_field_name=True)
        if isinstance(bstack11llll1l1_opy_, dict):
            if cli.config_observability:
                bstack11llll1l1_opy_.update(
                    {bstack1l111l1_opy_ (u"ࠤࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠤᇈ"): MessageToDict(cli.config_observability, preserving_proto_field_name=True)}
                )
            if cli.config_accessibility:
                accessibility = MessageToDict(cli.config_accessibility, preserving_proto_field_name=True)
                if isinstance(accessibility, dict) and bstack1l111l1_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡷࡤࡺ࡯ࡠࡹࡵࡥࡵࠨᇉ") in accessibility.get(bstack1l111l1_opy_ (u"ࠦࡴࡶࡴࡪࡱࡱࡷࠧᇊ"), {}):
                    bstack1ll1lll11ll_opy_ = accessibility.get(bstack1l111l1_opy_ (u"ࠧࡵࡰࡵ࡫ࡲࡲࡸࠨᇋ"))
                    bstack1ll1lll11ll_opy_.update({ bstack1l111l1_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࡳࡕࡱ࡚ࡶࡦࡶࠢᇌ"): bstack1ll1lll11ll_opy_.pop(bstack1l111l1_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡴࡡࡷࡳࡤࡽࡲࡢࡲࠥᇍ")) })
                bstack11llll1l1_opy_.update({bstack1l111l1_opy_ (u"ࠣࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠣᇎ"): accessibility })
        return bstack11llll1l1_opy_
    @measure(event_name=EVENTS.bstack1ll1llll1l1_opy_, stage=STAGE.bstack11l11l11l1_opy_)
    def bstack1ll1ll1l1ll_opy_(self, bstack1lll11lll11_opy_: str = None, bstack1ll11l1l1ll_opy_: str = None, exit_code: int = None):
        if not self.cli_bin_session_id or not self.bstack1lll11l1l1l_opy_:
            return
        bstack1ll11llll_opy_ = datetime.now()
        req = structs.StopBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        if exit_code:
            req.exit_code = exit_code
        if bstack1lll11lll11_opy_:
            req.bstack1lll11lll11_opy_ = bstack1lll11lll11_opy_
        if bstack1ll11l1l1ll_opy_:
            req.bstack1ll11l1l1ll_opy_ = bstack1ll11l1l1ll_opy_
        try:
            r = self.bstack1lll11l1l1l_opy_.StopBinSession(req)
            SDKCLI.automate_buildlink = r.automate_buildlink
            SDKCLI.hashed_id = r.hashed_id
            self.bstack111lll11l_opy_(bstack1l111l1_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡶࡲࡴࡤࡨࡩ࡯ࡡࡶࡩࡸࡹࡩࡰࡰࠥᇏ"), datetime.now() - bstack1ll11llll_opy_)
            return r.success
        except grpc.RpcError as e:
            traceback.print_exc()
            raise e
    def bstack111lll11l_opy_(self, key: str, value: timedelta):
        tag = bstack1l111l1_opy_ (u"ࠥࡧ࡭࡯࡬ࡥ࠯ࡳࡶࡴࡩࡥࡴࡵࠥᇐ") if self.bstack1llll11111_opy_() else bstack1l111l1_opy_ (u"ࠦࡲࡧࡩ࡯࠯ࡳࡶࡴࡩࡥࡴࡵࠥᇑ")
        self.bstack1ll11l1ll1l_opy_[bstack1l111l1_opy_ (u"ࠧࡀࠢᇒ").join([tag + bstack1l111l1_opy_ (u"ࠨ࠭ࠣᇓ") + str(id(self)), key])] += value
    def bstack1l1l1l11l_opy_(self):
        if not os.getenv(bstack1l111l1_opy_ (u"ࠢࡅࡇࡅ࡙ࡌࡥࡐࡆࡔࡉࠦᇔ"), bstack1l111l1_opy_ (u"ࠣ࠲ࠥᇕ")) == bstack1l111l1_opy_ (u"ࠤ࠴ࠦᇖ"):
            return
        bstack1ll1l111ll1_opy_ = dict()
        bstack1llll11llll_opy_ = []
        if self.test_framework:
            bstack1llll11llll_opy_.extend(list(self.test_framework.bstack1llll11llll_opy_.values()))
        if self.bstack1lll1ll1l11_opy_:
            bstack1llll11llll_opy_.extend(list(self.bstack1lll1ll1l11_opy_.bstack1llll11llll_opy_.values()))
        for instance in bstack1llll11llll_opy_:
            if not instance.platform_index in bstack1ll1l111ll1_opy_:
                bstack1ll1l111ll1_opy_[instance.platform_index] = defaultdict(lambda: timedelta(microseconds=0))
            report = bstack1ll1l111ll1_opy_[instance.platform_index]
            for k, v in instance.bstack1ll11l1lll1_opy_().items():
                report[k] += v
                report[k.split(bstack1l111l1_opy_ (u"ࠥ࠾ࠧᇗ"))[0]] += v
        bstack1ll11lll111_opy_ = sorted([(k, v) for k, v in self.bstack1ll11l1ll1l_opy_.items()], key=lambda o: o[1], reverse=True)
        bstack1ll1ll1lll1_opy_ = 0
        for r in bstack1ll11lll111_opy_:
            bstack1lll1l11ll1_opy_ = r[1].total_seconds()
            bstack1ll1ll1lll1_opy_ += bstack1lll1l11ll1_opy_
            self.logger.debug(bstack1l111l1_opy_ (u"ࠦࡠࡶࡥࡳࡨࡠࠤࡨࡲࡩ࠻ࡽࡵ࡟࠵ࡣࡽ࠾ࠤᇘ") + str(bstack1lll1l11ll1_opy_) + bstack1l111l1_opy_ (u"ࠧࠨᇙ"))
        self.logger.debug(bstack1l111l1_opy_ (u"ࠨ࠭࠮ࠤᇚ"))
        bstack1ll1l1l1l1l_opy_ = []
        for platform_index, report in bstack1ll1l111ll1_opy_.items():
            bstack1ll1l1l1l1l_opy_.extend([(platform_index, k, v) for k, v in report.items()])
        bstack1ll1l1l1l1l_opy_.sort(key=lambda o: o[2], reverse=True)
        bstack1l1l1lllll_opy_ = set()
        bstack1lll111l11l_opy_ = 0
        for r in bstack1ll1l1l1l1l_opy_:
            bstack1lll1l11ll1_opy_ = r[2].total_seconds()
            bstack1lll111l11l_opy_ += bstack1lll1l11ll1_opy_
            bstack1l1l1lllll_opy_.add(r[0])
            self.logger.debug(bstack1l111l1_opy_ (u"ࠢ࡜ࡲࡨࡶ࡫ࡣࠠࡵࡧࡶࡸ࠿ࡶ࡬ࡢࡶࡩࡳࡷࡳ࠭ࡼࡴ࡞࠴ࡢࢃ࠺ࡼࡴ࡞࠵ࡢࢃ࠽ࠣᇛ") + str(bstack1lll1l11ll1_opy_) + bstack1l111l1_opy_ (u"ࠣࠤᇜ"))
        if self.bstack1llll11111_opy_():
            self.logger.debug(bstack1l111l1_opy_ (u"ࠤ࠰࠱ࠧᇝ"))
            self.logger.debug(bstack1l111l1_opy_ (u"ࠥ࡟ࡵ࡫ࡲࡧ࡟ࠣࡧࡱ࡯࠺ࡤࡪ࡬ࡰࡩ࠳ࡰࡳࡱࡦࡩࡸࡹ࠽ࡼࡶࡲࡸࡦࡲ࡟ࡤ࡮࡬ࢁࠥࡺࡥࡴࡶ࠽ࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠳ࡻࡴࡶࡵࠬࡵࡲࡡࡵࡨࡲࡶࡲࡹࠩࡾ࠿ࠥᇞ") + str(bstack1lll111l11l_opy_) + bstack1l111l1_opy_ (u"ࠦࠧᇟ"))
        else:
            self.logger.debug(bstack1l111l1_opy_ (u"ࠧࡡࡰࡦࡴࡩࡡࠥࡩ࡬ࡪ࠼ࡰࡥ࡮ࡴ࠭ࡱࡴࡲࡧࡪࡹࡳ࠾ࠤᇠ") + str(bstack1ll1ll1lll1_opy_) + bstack1l111l1_opy_ (u"ࠨࠢᇡ"))
        self.logger.debug(bstack1l111l1_opy_ (u"ࠢ࠮࠯ࠥᇢ"))
    def test_orchestration_session(self, test_files: list, orchestration_strategy: str, orchestration_metadata: str):
        request = structs.TestOrchestrationRequest(
            bin_session_id=self.cli_bin_session_id,
            orchestration_strategy=orchestration_strategy,
            test_files=test_files,
            orchestration_metadata=orchestration_metadata
        )
        if not self.bstack1lll11l1l1l_opy_:
            self.logger.error(bstack1l111l1_opy_ (u"ࠣࡥ࡯࡭ࡤࡹࡥࡳࡸ࡬ࡧࡪࠦࡩࡴࠢࡱࡳࡹࠦࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡻࡧࡧ࠲ࠥࡉࡡ࡯ࡰࡲࡸࠥࡶࡥࡳࡨࡲࡶࡲࠦࡴࡦࡵࡷࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱ࠲ࠧᇣ"))
            return None
        response = self.bstack1lll11l1l1l_opy_.TestOrchestration(request)
        self.logger.debug(bstack1l111l1_opy_ (u"ࠤࡷࡩࡸࡺ࠭ࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴ࠭ࡴࡧࡶࡷ࡮ࡵ࡮࠾ࡽࢀࠦᇤ").format(response))
        if response.success:
            return list(response.ordered_test_files)
        return None
    def bstack1ll1ll1llll_opy_(self, r):
        if r is not None and getattr(r, bstack1l111l1_opy_ (u"ࠪࡸࡪࡹࡴࡩࡷࡥࠫᇥ"), None) and getattr(r.testhub, bstack1l111l1_opy_ (u"ࠫࡪࡸࡲࡰࡴࡶࠫᇦ"), None):
            errors = json.loads(r.testhub.errors.decode(bstack1l111l1_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦᇧ")))
            for bstack1lll1111l11_opy_, err in errors.items():
                if err[bstack1l111l1_opy_ (u"࠭ࡴࡺࡲࡨࠫᇨ")] == bstack1l111l1_opy_ (u"ࠧࡪࡰࡩࡳࠬᇩ"):
                    self.logger.info(err[bstack1l111l1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᇪ")])
                else:
                    self.logger.error(err[bstack1l111l1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᇫ")])
    def bstack1l1l1ll111_opy_(self):
        return SDKCLI.automate_buildlink, SDKCLI.hashed_id
cli = SDKCLI()