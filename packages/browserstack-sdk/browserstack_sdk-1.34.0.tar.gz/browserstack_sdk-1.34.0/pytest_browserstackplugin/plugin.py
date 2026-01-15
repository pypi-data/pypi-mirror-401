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
import atexit
import datetime
import inspect
import logging
import signal
import threading
from uuid import uuid4
from bstack_utils.measure import bstack11lll1l1ll_opy_
from bstack_utils.percy_sdk import PercySDK
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack1l1ll111l_opy_, bstack11l1lll11_opy_, update, bstack111ll1l1_opy_,
                                       bstack11l1l1l1ll_opy_, bstack111ll11l11_opy_, bstack111ll1llll_opy_, bstack11lll11lll_opy_,
                                       bstack11l1ll1l1l_opy_, bstack11l1l1ll1l_opy_, bstack1ll11l1l1_opy_,
                                       bstack11lll111l_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack1llll11ll1_opy_)
from browserstack_sdk.bstack11l11111l1_opy_ import bstack1lllllllll_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack1ll1lll11_opy_
from bstack_utils.capture import bstack111l1lll11_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack1111l1l1l_opy_, bstack1ll11111ll_opy_, bstack1l11lll11l_opy_, \
    bstack1ll111l1l1_opy_
from bstack_utils.helper import bstack1l1l1l111_opy_, bstack111l1llllll_opy_, bstack1111l1l1ll_opy_, bstack11l111l11l_opy_, bstack1l1l1l11l1l_opy_, bstack11llll1111_opy_, \
    bstack111ll111ll1_opy_, \
    bstack111ll11111l_opy_, bstack111l1111l_opy_, bstack1lllllll11_opy_, bstack111ll11l1ll_opy_, bstack1lllllll1_opy_, Notset, \
    bstack1llllllll_opy_, bstack111llllllll_opy_, bstack111l1llll11_opy_, Result, bstack111lll1ll1l_opy_, bstack111lll11111_opy_, error_handler, \
    bstack111lll1111_opy_, bstack111l11l11_opy_, bstack11lll111_opy_, bstack111ll1l11l1_opy_
from bstack_utils.bstack111l11ll111_opy_ import bstack111l11l1lll_opy_
from bstack_utils.messages import bstack1ll11l1l1l_opy_, bstack1l111l1ll1_opy_, bstack1ll1l11l_opy_, bstack111ll111l1_opy_, bstack1ll1lll1_opy_, \
    bstack11l1lll111_opy_, bstack11l1l11l1l_opy_, bstack1111ll11_opy_, bstack111ll11ll1_opy_, bstack1l11l11l_opy_, \
    bstack111ll11lll_opy_, bstack11l1111l_opy_, bstack11l11lll11_opy_
from bstack_utils.proxy import bstack11ll11l1l_opy_, bstack1ll1ll11ll_opy_
from bstack_utils.bstack1ll11ll11_opy_ import bstack1llll1llll11_opy_, bstack1llll1lll111_opy_, bstack1llll1ll1ll1_opy_, bstack1llll1ll11l1_opy_, \
    bstack1llll1ll111l_opy_, bstack1llll1ll1l1l_opy_, bstack1llll1l1llll_opy_, bstack1lll1llll1_opy_, bstack1llll1ll1l11_opy_
from bstack_utils.bstack1ll11ll1l_opy_ import bstack1l1l1l1l1l_opy_
from bstack_utils.bstack1l1111ll_opy_ import bstack11l111llll_opy_, bstack111llllll1_opy_, bstack11l111l1ll_opy_, \
    bstack11llll1ll_opy_, bstack11ll1lll11_opy_
from bstack_utils.bstack111l11l1l1_opy_ import bstack111l11l111_opy_
from bstack_utils.bstack111l1ll11l_opy_ import bstack11ll11l11_opy_
import bstack_utils.accessibility as bstack11111l11l_opy_
from bstack_utils.bstack111l11l11l_opy_ import bstack1llll1lll1_opy_
from bstack_utils.bstack1l111l1l_opy_ import bstack1l111l1l_opy_
from bstack_utils.bstack1l111l1l1_opy_ import bstack1llll111l_opy_
from browserstack_sdk.__init__ import bstack1111ll1l_opy_
from browserstack_sdk.sdk_cli.bstack1lll111l1ll_opy_ import bstack1ll1l11llll_opy_
from browserstack_sdk.sdk_cli.bstack11ll111ll_opy_ import bstack11ll111ll_opy_, bstack1lll1ll1_opy_, bstack1ll1lll11l_opy_
from browserstack_sdk.sdk_cli.test_framework import bstack1l11111l1l1_opy_, bstack1ll1lll1111_opy_, bstack1lll11ll1l1_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack11ll111ll_opy_ import bstack11ll111ll_opy_, bstack1lll1ll1_opy_, bstack1ll1lll11l_opy_
bstack111lll1l1_opy_ = None
bstack1l11111l1l_opy_ = None
bstack1lll11ll11_opy_ = None
bstack1lll11lll_opy_ = None
bstack1l11lll1ll_opy_ = None
bstack1111l11l1_opy_ = None
bstack1l1l111lll_opy_ = None
bstack1l1l11l11_opy_ = None
bstack1ll1l1lll_opy_ = None
bstack1l111l111_opy_ = None
bstack1l1ll1lll1_opy_ = None
bstack1l1l11l111_opy_ = None
bstack111ll11ll_opy_ = None
bstack1lll11ll1l_opy_ = bstack1l111l1_opy_ (u"ࠪࠫ⌭")
CONFIG = {}
bstack11ll11l1_opy_ = False
bstack1l1l1l11l1_opy_ = bstack1l111l1_opy_ (u"ࠫࠬ⌮")
bstack1lll111l1_opy_ = bstack1l111l1_opy_ (u"ࠬ࠭⌯")
bstack1l1111l1l_opy_ = False
bstack1l11ll11_opy_ = []
bstack111l111l1_opy_ = bstack1111l1l1l_opy_
bstack1lll11l1l111_opy_ = bstack1l111l1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭⌰")
bstack11lll11l11_opy_ = {}
bstack1l1l1l1ll1_opy_ = None
bstack1l1l1llll1_opy_ = False
logger = bstack1ll1lll11_opy_.get_logger(__name__, bstack111l111l1_opy_)
store = {
    bstack1l111l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ⌱"): []
}
bstack1lll1l111111_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_1111l1l11l_opy_ = {}
current_test_uuid = None
cli_context = bstack1l11111l1l1_opy_(
    test_framework_name=bstack1l11l1ll11_opy_[bstack1l111l1_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔ࠮ࡄࡇࡈࠬ⌲")] if bstack1lllllll1_opy_() else bstack1l11l1ll11_opy_[bstack1l111l1_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࠩ⌳")],
    test_framework_version=pytest.__version__,
    platform_index=-1,
)
def bstack1lll1l111_opy_(page, bstack1lllllll1l_opy_):
    try:
        page.evaluate(bstack1l111l1_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦ⌴"),
                      bstack1l111l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠨ⌵") + json.dumps(
                          bstack1lllllll1l_opy_) + bstack1l111l1_opy_ (u"ࠧࢃࡽࠣ⌶"))
    except Exception as e:
        print(bstack1l111l1_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡࡽࢀࠦ⌷"), e)
def bstack1l1l1l1l11_opy_(page, message, level):
    try:
        page.evaluate(bstack1l111l1_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣ⌸"), bstack1l111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭⌹") + json.dumps(
            message) + bstack1l111l1_opy_ (u"ࠩ࠯ࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠬ⌺") + json.dumps(level) + bstack1l111l1_opy_ (u"ࠪࢁࢂ࠭⌻"))
    except Exception as e:
        print(bstack1l111l1_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡢࡰࡱࡳࡹࡧࡴࡪࡱࡱࠤࢀࢃࠢ⌼"), e)
def pytest_configure(config):
    global bstack1l1l1l11l1_opy_
    global CONFIG
    bstack1l1l1111_opy_ = Config.bstack1llll1ll11_opy_()
    config.args = bstack11ll11l11_opy_.bstack1lll1l1111ll_opy_(config.args)
    bstack1l1l1111_opy_.bstack1l1ll111_opy_(bstack11lll111_opy_(config.getoption(bstack1l111l1_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩ⌽"))))
    try:
        bstack1ll1lll11_opy_.bstack1111llll11l_opy_(config.inipath, config.rootpath)
    except:
        pass
    if cli.is_running():
        bstack11ll111ll_opy_.invoke(bstack1lll1ll1_opy_.CONNECT, bstack1ll1lll11l_opy_())
        cli_context.platform_index = int(os.environ.get(bstack1l111l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭⌾"), bstack1l111l1_opy_ (u"ࠧ࠱ࠩ⌿")))
        config = json.loads(os.environ.get(bstack1l111l1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍࠢ⍀"), bstack1l111l1_opy_ (u"ࠤࡾࢁࠧ⍁")))
        cli.bstack1lll11llll1_opy_(bstack1lllllll11_opy_(bstack1l1l1l11l1_opy_, CONFIG), cli_context.platform_index, bstack111ll1l1_opy_)
    if cli.bstack1ll1l1llll1_opy_(bstack1ll1l11llll_opy_):
        cli.bstack1ll1l11lll1_opy_()
        logger.debug(bstack1l111l1_opy_ (u"ࠥࡇࡑࡏࠠࡪࡵࠣࡥࡨࡺࡩࡷࡧࠣࡪࡴࡸࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸ࠾ࠤ⍂") + str(cli_context.platform_index) + bstack1l111l1_opy_ (u"ࠦࠧ⍃"))
        cli.test_framework.track_event(cli_context, bstack1ll1lll1111_opy_.BEFORE_ALL, bstack1lll11ll1l1_opy_.PRE, config)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    when = getattr(call, bstack1l111l1_opy_ (u"ࠧࡽࡨࡦࡰࠥ⍄"), None)
    if cli.is_running() and when == bstack1l111l1_opy_ (u"ࠨࡣࡢ࡮࡯ࠦ⍅"):
        cli.test_framework.track_event(cli_context, bstack1ll1lll1111_opy_.LOG_REPORT, bstack1lll11ll1l1_opy_.PRE, item, call)
    outcome = yield
    if when == bstack1l111l1_opy_ (u"ࠢࡤࡣ࡯ࡰࠧ⍆"):
        report = outcome.get_result()
        passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l111l1_opy_ (u"ࠣࡹࡤࡷࡽ࡬ࡡࡪ࡮ࠥ⍇")))
        if not passed:
            config = json.loads(os.environ.get(bstack1l111l1_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࠣ⍈"), bstack1l111l1_opy_ (u"ࠥࡿࢂࠨ⍉")))
            if bstack1llll111l_opy_.bstack1ll111l1ll_opy_(config):
                bstack1llllll11ll1_opy_ = bstack1llll111l_opy_.bstack1lll1111_opy_(config)
                if item.execution_count > bstack1llllll11ll1_opy_:
                    print(bstack1l111l1_opy_ (u"࡙ࠫ࡫ࡳࡵࠢࡩࡥ࡮ࡲࡥࡥࠢࡤࡪࡹ࡫ࡲࠡࡴࡨࡸࡷ࡯ࡥࡴ࠼ࠣࠫ⍊"), report.nodeid, os.environ.get(bstack1l111l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ⍋")))
                    bstack1llll111l_opy_.bstack11111lll111_opy_(report.nodeid)
            else:
                print(bstack1l111l1_opy_ (u"࠭ࡔࡦࡵࡷࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥ࠭⍌"), report.nodeid, os.environ.get(bstack1l111l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ⍍")))
                bstack1llll111l_opy_.bstack11111lll111_opy_(report.nodeid)
        else:
            print(bstack1l111l1_opy_ (u"ࠨࡖࡨࡷࡹࠦࡰࡢࡵࡶࡩࡩࡀࠠࠨ⍎"), report.nodeid, os.environ.get(bstack1l111l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ⍏")))
    if cli.is_running():
        if when == bstack1l111l1_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤ⍐"):
            cli.test_framework.track_event(cli_context, bstack1ll1lll1111_opy_.BEFORE_EACH, bstack1lll11ll1l1_opy_.POST, item, call, outcome)
        elif when == bstack1l111l1_opy_ (u"ࠦࡨࡧ࡬࡭ࠤ⍑"):
            cli.test_framework.track_event(cli_context, bstack1ll1lll1111_opy_.LOG_REPORT, bstack1lll11ll1l1_opy_.POST, item, call, outcome)
        elif when == bstack1l111l1_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢ⍒"):
            cli.test_framework.track_event(cli_context, bstack1ll1lll1111_opy_.AFTER_EACH, bstack1lll11ll1l1_opy_.POST, item, call, outcome)
        return # skip all existing operations
    skipSessionName = item.config.getoption(bstack1l111l1_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ⍓"))
    plugins = item.config.getoption(bstack1l111l1_opy_ (u"ࠢࡱ࡮ࡸ࡫࡮ࡴࡳࠣ⍔"))
    report = outcome.get_result()
    os.environ[bstack1l111l1_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࡠࡖࡈࡗ࡙ࡥࡎࡂࡏࡈࠫ⍕")] = report.nodeid
    bstack1lll11ll1ll1_opy_(item, call, report)
    if bstack1l111l1_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡱ࡮ࡸ࡫࡮ࡴࠢ⍖") not in plugins or bstack1lllllll1_opy_():
        return
    summary = []
    driver = getattr(item, bstack1l111l1_opy_ (u"ࠥࡣࡩࡸࡩࡷࡧࡵࠦ⍗"), None)
    page = getattr(item, bstack1l111l1_opy_ (u"ࠦࡤࡶࡡࡨࡧࠥ⍘"), None)
    try:
        if (driver == None or driver.session_id == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None or cli.is_running()):
        bstack1lll11l1l1ll_opy_(item, report, summary, skipSessionName)
    if (page is not None):
        bstack1lll11ll1111_opy_(item, report, summary, skipSessionName)
def bstack1lll11l1l1ll_opy_(item, report, summary, skipSessionName):
    if report.when == bstack1l111l1_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ⍙") and report.skipped:
        bstack1llll1ll1l11_opy_(report)
    if report.when in [bstack1l111l1_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧ⍚"), bstack1l111l1_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤ⍛")]:
        return
    if not bstack1l1l1l11l1l_opy_():
        return
    try:
        if ((str(skipSessionName).lower() != bstack1l111l1_opy_ (u"ࠨࡶࡵࡹࡪ࠭⍜")) and (not cli.is_running())) and item._driver.session_id:
            item._driver.execute_script(
                bstack1l111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿ࠦࠧ⍝") + json.dumps(
                    report.nodeid) + bstack1l111l1_opy_ (u"ࠪࢁࢂ࠭⍞"))
        os.environ[bstack1l111l1_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࡣ࡙ࡋࡓࡕࡡࡑࡅࡒࡋࠧ⍟")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack1l111l1_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫࠺ࠡࡽ࠳ࢁࠧ⍠").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l111l1_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣ⍡")))
    bstack11l1llll11_opy_ = bstack1l111l1_opy_ (u"ࠢࠣ⍢")
    bstack1llll1ll1l11_opy_(report)
    if not passed:
        try:
            bstack11l1llll11_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack1l111l1_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡩࡥ࡮ࡲࡵࡳࡧࠣࡶࡪࡧࡳࡰࡰ࠽ࠤࢀ࠶ࡽࠣ⍣").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack11l1llll11_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack1l111l1_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦ⍤")))
        bstack11l1llll11_opy_ = bstack1l111l1_opy_ (u"ࠥࠦ⍥")
        if not passed:
            try:
                bstack11l1llll11_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1l111l1_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥ࡬ࡡࡪ࡮ࡸࡶࡪࠦࡲࡦࡣࡶࡳࡳࡀࠠࡼ࠲ࢀࠦ⍦").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack11l1llll11_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack1l111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣ࡫ࡱࡪࡴࠨࠬࠡ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡦࡤࡸࡦࠨ࠺ࠡࠩ⍧")
                    + json.dumps(bstack1l111l1_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠧࠢ⍨"))
                    + bstack1l111l1_opy_ (u"ࠢ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿࠥ⍩")
                )
            else:
                item._driver.execute_script(
                    bstack1l111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦࡪࡸࡲࡰࡴࠥ࠰ࠥࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡪࡡࡵࡣࠥ࠾ࠥ࠭⍪")
                    + json.dumps(str(bstack11l1llll11_opy_))
                    + bstack1l111l1_opy_ (u"ࠤ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࠧ⍫")
                )
        except Exception as e:
            summary.append(bstack1l111l1_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡣࡱࡲࡴࡺࡡࡵࡧ࠽ࠤࢀ࠶ࡽࠣ⍬").format(e))
def bstack1lll11l11l1l_opy_(test_name, error_message):
    try:
        bstack1lll11l1ll11_opy_ = []
        bstack1l1l11111l_opy_ = os.environ.get(bstack1l111l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ⍭"), bstack1l111l1_opy_ (u"ࠬ࠶ࠧ⍮"))
        bstack11ll1ll1_opy_ = {bstack1l111l1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ⍯"): test_name, bstack1l111l1_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭⍰"): error_message, bstack1l111l1_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧ⍱"): bstack1l1l11111l_opy_}
        bstack1lll11ll111l_opy_ = os.path.join(tempfile.gettempdir(), bstack1l111l1_opy_ (u"ࠩࡳࡻࡤࡶࡹࡵࡧࡶࡸࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧ⍲"))
        if os.path.exists(bstack1lll11ll111l_opy_):
            with open(bstack1lll11ll111l_opy_) as f:
                bstack1lll11l1ll11_opy_ = json.load(f)
        bstack1lll11l1ll11_opy_.append(bstack11ll1ll1_opy_)
        with open(bstack1lll11ll111l_opy_, bstack1l111l1_opy_ (u"ࠪࡻࠬ⍳")) as f:
            json.dump(bstack1lll11l1ll11_opy_, f)
    except Exception as e:
        logger.debug(bstack1l111l1_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡰࡦࡴࡶ࡭ࡸࡺࡩ࡯ࡩࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡱࡻࡷࡩࡸࡺࠠࡦࡴࡵࡳࡷࡹ࠺ࠡࠩ⍴") + str(e))
def bstack1lll11ll1111_opy_(item, report, summary, skipSessionName):
    if report.when in [bstack1l111l1_opy_ (u"ࠧࡹࡥࡵࡷࡳࠦ⍵"), bstack1l111l1_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࠣ⍶")]:
        return
    if (str(skipSessionName).lower() != bstack1l111l1_opy_ (u"ࠧࡵࡴࡸࡩࠬ⍷")):
        bstack1lll1l111_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l111l1_opy_ (u"ࠣࡹࡤࡷࡽ࡬ࡡࡪ࡮ࠥ⍸")))
    bstack11l1llll11_opy_ = bstack1l111l1_opy_ (u"ࠤࠥ⍹")
    bstack1llll1ll1l11_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack11l1llll11_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1l111l1_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤ࡫ࡧࡩ࡭ࡷࡵࡩࠥࡸࡥࡢࡵࡲࡲ࠿ࠦࡻ࠱ࡿࠥ⍺").format(e)
                )
        try:
            if passed:
                bstack11ll1lll11_opy_(getattr(item, bstack1l111l1_opy_ (u"ࠫࡤࡶࡡࡨࡧࠪ⍻"), None), bstack1l111l1_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧ⍼"))
            else:
                error_message = bstack1l111l1_opy_ (u"࠭ࠧ⍽")
                if bstack11l1llll11_opy_:
                    bstack1l1l1l1l11_opy_(item._page, str(bstack11l1llll11_opy_), bstack1l111l1_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨ⍾"))
                    bstack11ll1lll11_opy_(getattr(item, bstack1l111l1_opy_ (u"ࠨࡡࡳࡥ࡬࡫ࠧ⍿"), None), bstack1l111l1_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ⎀"), str(bstack11l1llll11_opy_))
                    error_message = str(bstack11l1llll11_opy_)
                else:
                    bstack11ll1lll11_opy_(getattr(item, bstack1l111l1_opy_ (u"ࠪࡣࡵࡧࡧࡦࠩ⎁"), None), bstack1l111l1_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ⎂"))
                bstack1lll11l11l1l_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack1l111l1_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡹࡵࡪࡡࡵࡧࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࢁ࠰ࡾࠤ⎃").format(e))
def pytest_addoption(parser):
    parser.addoption(bstack1l111l1_opy_ (u"ࠨ࠭࠮ࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ⎄"), default=bstack1l111l1_opy_ (u"ࠢࡇࡣ࡯ࡷࡪࠨ⎅"), help=bstack1l111l1_opy_ (u"ࠣࡃࡸࡸࡴࡳࡡࡵ࡫ࡦࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠢ⎆"))
    parser.addoption(bstack1l111l1_opy_ (u"ࠤ࠰࠱ࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣ⎇"), default=bstack1l111l1_opy_ (u"ࠥࡊࡦࡲࡳࡦࠤ⎈"), help=bstack1l111l1_opy_ (u"ࠦࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡩࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠥ⎉"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack1l111l1_opy_ (u"ࠧ࠳࠭ࡥࡴ࡬ࡺࡪࡸࠢ⎊"), action=bstack1l111l1_opy_ (u"ࠨࡳࡵࡱࡵࡩࠧ⎋"), default=bstack1l111l1_opy_ (u"ࠢࡤࡪࡵࡳࡲ࡫ࠢ⎌"),
                         help=bstack1l111l1_opy_ (u"ࠣࡆࡵ࡭ࡻ࡫ࡲࠡࡶࡲࠤࡷࡻ࡮ࠡࡶࡨࡷࡹࡹࠢ⎍"))
def bstack111l1l11l1_opy_(log):
    if not (log[bstack1l111l1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ⎎")] and log[bstack1l111l1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ⎏")].strip()):
        return
    active = bstack111l1l1ll1_opy_()
    log = {
        bstack1l111l1_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ⎐"): log[bstack1l111l1_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ⎑")],
        bstack1l111l1_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ⎒"): bstack1111l1l1ll_opy_().isoformat() + bstack1l111l1_opy_ (u"࡛ࠧࠩ⎓"),
        bstack1l111l1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ⎔"): log[bstack1l111l1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ⎕")],
    }
    if active:
        if active[bstack1l111l1_opy_ (u"ࠪࡸࡾࡶࡥࠨ⎖")] == bstack1l111l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩ⎗"):
            log[bstack1l111l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⎘")] = active[bstack1l111l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⎙")]
        elif active[bstack1l111l1_opy_ (u"ࠧࡵࡻࡳࡩࠬ⎚")] == bstack1l111l1_opy_ (u"ࠨࡶࡨࡷࡹ࠭⎛"):
            log[bstack1l111l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⎜")] = active[bstack1l111l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⎝")]
    bstack1llll1lll1_opy_.bstack11l1l111_opy_([log])
def bstack111l1l1ll1_opy_():
    if len(store[bstack1l111l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ⎞")]) > 0 and store[bstack1l111l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ⎟")][-1]:
        return {
            bstack1l111l1_opy_ (u"࠭ࡴࡺࡲࡨࠫ⎠"): bstack1l111l1_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ⎡"),
            bstack1l111l1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⎢"): store[bstack1l111l1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭⎣")][-1]
        }
    if store.get(bstack1l111l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ⎤"), None):
        return {
            bstack1l111l1_opy_ (u"ࠫࡹࡿࡰࡦࠩ⎥"): bstack1l111l1_opy_ (u"ࠬࡺࡥࡴࡶࠪ⎦"),
            bstack1l111l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⎧"): store[bstack1l111l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ⎨")]
        }
    return None
def pytest_runtest_logstart(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1lll1111_opy_.INIT_TEST, bstack1lll11ll1l1_opy_.PRE, nodeid, location)
def pytest_runtest_logfinish(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1lll1111_opy_.INIT_TEST, bstack1lll11ll1l1_opy_.POST, nodeid, location)
def pytest_runtest_call(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1lll1111_opy_.TEST, bstack1lll11ll1l1_opy_.PRE, item)
        return
    try:
        global CONFIG
        item._1lll11llllll_opy_ = True
        bstack11lll1l11_opy_ = bstack11111l11l_opy_.bstack11l1l11111_opy_(bstack111ll11111l_opy_(item.own_markers))
        if not cli.bstack1ll1l1llll1_opy_(bstack1ll1l11llll_opy_):
            item._a11y_test_case = bstack11lll1l11_opy_
            if bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ⎩"), None):
                driver = getattr(item, bstack1l111l1_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪ⎪"), None)
                item._a11y_started = bstack11111l11l_opy_.bstack111l1ll1l_opy_(driver, bstack11lll1l11_opy_)
        if not bstack1llll1lll1_opy_.on() or bstack1lll11l1l111_opy_ != bstack1l111l1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ⎫"):
            return
        global current_test_uuid #, bstack111l11ll1l_opy_
        bstack11111llll1_opy_ = {
            bstack1l111l1_opy_ (u"ࠫࡺࡻࡩࡥࠩ⎬"): uuid4().__str__(),
            bstack1l111l1_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ⎭"): bstack1111l1l1ll_opy_().isoformat() + bstack1l111l1_opy_ (u"࡚࠭ࠨ⎮")
        }
        current_test_uuid = bstack11111llll1_opy_[bstack1l111l1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⎯")]
        store[bstack1l111l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ⎰")] = bstack11111llll1_opy_[bstack1l111l1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ⎱")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _1111l1l11l_opy_[item.nodeid] = {**_1111l1l11l_opy_[item.nodeid], **bstack11111llll1_opy_}
        bstack1lll11ll11l1_opy_(item, _1111l1l11l_opy_[item.nodeid], bstack1l111l1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ⎲"))
    except Exception as err:
        print(bstack1l111l1_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡶࡺࡴࡴࡦࡵࡷࡣࡨࡧ࡬࡭࠼ࠣࡿࢂ࠭⎳"), str(err))
def pytest_runtest_setup(item):
    store[bstack1l111l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩ⎴")] = item
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1lll1111_opy_.BEFORE_EACH, bstack1lll11ll1l1_opy_.PRE, item, bstack1l111l1_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ⎵"))
    if bstack1llll111l_opy_.bstack11111llll11_opy_():
            bstack1lll11l1llll_opy_ = bstack1l111l1_opy_ (u"ࠢࡔ࡭࡬ࡴࡵ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡢࡵࠣࡸ࡭࡫ࠠࡢࡤࡲࡶࡹࠦࡢࡶ࡫࡯ࡨࠥ࡬ࡩ࡭ࡧࠣࡩࡽ࡯ࡳࡵࡵ࠱ࠦ⎶")
            logger.error(bstack1lll11l1llll_opy_)
            bstack11111llll1_opy_ = {
                bstack1l111l1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⎷"): uuid4().__str__(),
                bstack1l111l1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭⎸"): bstack1111l1l1ll_opy_().isoformat() + bstack1l111l1_opy_ (u"ࠪ࡞ࠬ⎹"),
                bstack1l111l1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⎺"): bstack1111l1l1ll_opy_().isoformat() + bstack1l111l1_opy_ (u"ࠬࡠࠧ⎻"),
                bstack1l111l1_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭⎼"): bstack1l111l1_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ⎽"),
                bstack1l111l1_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨ⎾"): bstack1lll11l1llll_opy_,
                bstack1l111l1_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ⎿"): [],
                bstack1l111l1_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬ⏀"): []
            }
            bstack1lll11ll11l1_opy_(item, bstack11111llll1_opy_, bstack1l111l1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬ⏁"))
            pytest.skip(bstack1lll11l1llll_opy_)
            return # skip all existing operations
    global bstack1lll1l111111_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack111ll11l1ll_opy_():
        atexit.register(bstack111lllllll_opy_)
        if not bstack1lll1l111111_opy_:
            try:
                bstack1lll11l1lll1_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack111ll1l11l1_opy_():
                    bstack1lll11l1lll1_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1lll11l1lll1_opy_:
                    signal.signal(s, bstack1lll1l1111l1_opy_)
                bstack1lll1l111111_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack1l111l1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡳࡧࡪ࡭ࡸࡺࡥࡳࠢࡶ࡭࡬ࡴࡡ࡭ࠢ࡫ࡥࡳࡪ࡬ࡦࡴࡶ࠾ࠥࠨ⏂") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack1llll1llll11_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack1l111l1_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭⏃")
    try:
        if not bstack1llll1lll1_opy_.on():
            return
        uuid = uuid4().__str__()
        bstack11111llll1_opy_ = {
            bstack1l111l1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⏄"): uuid,
            bstack1l111l1_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ⏅"): bstack1111l1l1ll_opy_().isoformat() + bstack1l111l1_opy_ (u"ࠩ࡝ࠫ⏆"),
            bstack1l111l1_opy_ (u"ࠪࡸࡾࡶࡥࠨ⏇"): bstack1l111l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩ⏈"),
            bstack1l111l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨ⏉"): bstack1l111l1_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫ⏊"),
            bstack1l111l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪ⏋"): bstack1l111l1_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ⏌")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack1l111l1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭⏍")] = item
        store[bstack1l111l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ⏎")] = [uuid]
        if not _1111l1l11l_opy_.get(item.nodeid, None):
            _1111l1l11l_opy_[item.nodeid] = {bstack1l111l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ⏏"): [], bstack1l111l1_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧ⏐"): []}
        _1111l1l11l_opy_[item.nodeid][bstack1l111l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ⏑")].append(bstack11111llll1_opy_[bstack1l111l1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⏒")])
        _1111l1l11l_opy_[item.nodeid + bstack1l111l1_opy_ (u"ࠨ࠯ࡶࡩࡹࡻࡰࠨ⏓")] = bstack11111llll1_opy_
        bstack1lll11ll1l11_opy_(item, bstack11111llll1_opy_, bstack1l111l1_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ⏔"))
    except Exception as err:
        print(bstack1l111l1_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡵࡹࡳࡺࡥࡴࡶࡢࡷࡪࡺࡵࡱ࠼ࠣࡿࢂ࠭⏕"), str(err))
def pytest_runtest_teardown(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1lll1111_opy_.TEST, bstack1lll11ll1l1_opy_.POST, item)
        cli.test_framework.track_event(cli_context, bstack1ll1lll1111_opy_.AFTER_EACH, bstack1lll11ll1l1_opy_.PRE, item, bstack1l111l1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭⏖"))
        return # skip all existing operations
    try:
        global bstack11lll11l11_opy_
        bstack1l1l11111l_opy_ = 0
        if bstack1l1111l1l_opy_ is True:
            bstack1l1l11111l_opy_ = int(os.environ.get(bstack1l111l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ⏗")))
        if bstack11ll11111_opy_.bstack1111111l1_opy_() == bstack1l111l1_opy_ (u"ࠨࡴࡳࡷࡨࠦ⏘"):
            if bstack11ll11111_opy_.bstack1l1ll1ll1l_opy_() == bstack1l111l1_opy_ (u"ࠢࡵࡧࡶࡸࡨࡧࡳࡦࠤ⏙"):
                bstack1lll11l1l11l_opy_ = bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"ࠨࡲࡨࡶࡨࡿࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ⏚"), None)
                bstack111llll11l_opy_ = bstack1lll11l1l11l_opy_ + bstack1l111l1_opy_ (u"ࠤ࠰ࡸࡪࡹࡴࡤࡣࡶࡩࠧ⏛")
                driver = getattr(item, bstack1l111l1_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫ⏜"), None)
                bstack1111l11ll_opy_ = getattr(item, bstack1l111l1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ⏝"), None)
                bstack1lll1lll1l_opy_ = getattr(item, bstack1l111l1_opy_ (u"ࠬࡻࡵࡪࡦࠪ⏞"), None)
                PercySDK.screenshot(driver, bstack111llll11l_opy_, bstack1111l11ll_opy_=bstack1111l11ll_opy_, bstack1lll1lll1l_opy_=bstack1lll1lll1l_opy_, bstack11lllllll_opy_=bstack1l1l11111l_opy_)
        if not cli.bstack1ll1l1llll1_opy_(bstack1ll1l11llll_opy_):
            if getattr(item, bstack1l111l1_opy_ (u"࠭࡟ࡢ࠳࠴ࡽࡤࡹࡴࡢࡴࡷࡩࡩ࠭⏟"), False):
                bstack1lllllllll_opy_.bstack1ll1l111ll_opy_(getattr(item, bstack1l111l1_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨ⏠"), None), bstack11lll11l11_opy_, logger, item)
        if not bstack1llll1lll1_opy_.on():
            return
        bstack11111llll1_opy_ = {
            bstack1l111l1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⏡"): uuid4().__str__(),
            bstack1l111l1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭⏢"): bstack1111l1l1ll_opy_().isoformat() + bstack1l111l1_opy_ (u"ࠪ࡞ࠬ⏣"),
            bstack1l111l1_opy_ (u"ࠫࡹࡿࡰࡦࠩ⏤"): bstack1l111l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪ⏥"),
            bstack1l111l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩ⏦"): bstack1l111l1_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫ⏧"),
            bstack1l111l1_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫ⏨"): bstack1l111l1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫ⏩")
        }
        _1111l1l11l_opy_[item.nodeid + bstack1l111l1_opy_ (u"ࠪ࠱ࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭⏪")] = bstack11111llll1_opy_
        bstack1lll11ll1l11_opy_(item, bstack11111llll1_opy_, bstack1l111l1_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ⏫"))
    except Exception as err:
        print(bstack1l111l1_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡷࡻ࡮ࡵࡧࡶࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࠺ࠡࡽࢀࠫ⏬"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if bstack1llll1ll11l1_opy_(fixturedef.argname):
        store[bstack1l111l1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡪࡶࡨࡱࠬ⏭")] = request.node
    elif bstack1llll1ll111l_opy_(fixturedef.argname):
        store[bstack1l111l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡥ࡯ࡥࡸࡹ࡟ࡪࡶࡨࡱࠬ⏮")] = request.node
    if not bstack1llll1lll1_opy_.on():
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll1lll1111_opy_.SETUP_FIXTURE, bstack1lll11ll1l1_opy_.PRE, fixturedef, request)
        outcome = yield
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll1lll1111_opy_.SETUP_FIXTURE, bstack1lll11ll1l1_opy_.POST, fixturedef, request, outcome)
        return # skip all existing operations
    start_time = datetime.datetime.now()
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1lll1111_opy_.SETUP_FIXTURE, bstack1lll11ll1l1_opy_.PRE, fixturedef, request)
    outcome = yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1lll1111_opy_.SETUP_FIXTURE, bstack1lll11ll1l1_opy_.POST, fixturedef, request, outcome)
        return # skip all existing operations
    try:
        fixture = {
            bstack1l111l1_opy_ (u"ࠨࡰࡤࡱࡪ࠭⏯"): fixturedef.argname,
            bstack1l111l1_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ⏰"): bstack111ll111ll1_opy_(outcome),
            bstack1l111l1_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬ⏱"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack1l111l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨ⏲")]
        if not _1111l1l11l_opy_.get(current_test_item.nodeid, None):
            _1111l1l11l_opy_[current_test_item.nodeid] = {bstack1l111l1_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧ⏳"): []}
        _1111l1l11l_opy_[current_test_item.nodeid][bstack1l111l1_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨ⏴")].append(fixture)
    except Exception as err:
        logger.debug(bstack1l111l1_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡴࡧࡷࡹࡵࡀࠠࡼࡿࠪ⏵"), str(err))
if bstack1lllllll1_opy_() and bstack1llll1lll1_opy_.on():
    def pytest_bdd_before_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll1lll1111_opy_.STEP, bstack1lll11ll1l1_opy_.PRE, request, step)
            return
        try:
            _1111l1l11l_opy_[request.node.nodeid][bstack1l111l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ⏶")].bstack1l1ll1l1l_opy_(id(step))
        except Exception as err:
            print(bstack1l111l1_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲ࠽ࠤࢀࢃࠧ⏷"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll1lll1111_opy_.STEP, bstack1lll11ll1l1_opy_.POST, request, step, exception)
            return
        try:
            _1111l1l11l_opy_[request.node.nodeid][bstack1l111l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭⏸")].bstack111l11l1ll_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack1l111l1_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡴࡶࡨࡴࡤ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠨ⏹"), str(err))
    def pytest_bdd_after_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll1lll1111_opy_.STEP, bstack1lll11ll1l1_opy_.POST, request, step)
            return
        try:
            bstack111l11l1l1_opy_: bstack111l11l111_opy_ = _1111l1l11l_opy_[request.node.nodeid][bstack1l111l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ⏺")]
            bstack111l11l1l1_opy_.bstack111l11l1ll_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack1l111l1_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡶࡸࡪࡶ࡟ࡦࡴࡵࡳࡷࡀࠠࡼࡿࠪ⏻"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1lll11l1l111_opy_
        try:
            if not bstack1llll1lll1_opy_.on() or bstack1lll11l1l111_opy_ != bstack1l111l1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫ⏼"):
                return
            if cli.is_running():
                cli.test_framework.track_event(cli_context, bstack1ll1lll1111_opy_.TEST, bstack1lll11ll1l1_opy_.PRE, request, feature, scenario)
                return
            driver = bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧ⏽"), None)
            if not _1111l1l11l_opy_.get(request.node.nodeid, None):
                _1111l1l11l_opy_[request.node.nodeid] = {}
            bstack111l11l1l1_opy_ = bstack111l11l111_opy_.bstack1llll1111ll1_opy_(
                scenario, feature, request.node,
                name=bstack1llll1ll1l1l_opy_(request.node, scenario),
                started_at=bstack11llll1111_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack1l111l1_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵ࠯ࡦࡹࡨࡻ࡭ࡣࡧࡵࠫ⏾"),
                tags=bstack1llll1l1llll_opy_(feature, scenario),
                bstack111l1llll1_opy_=bstack1llll1lll1_opy_.bstack111l1ll111_opy_(driver) if driver and driver.session_id else {}
            )
            _1111l1l11l_opy_[request.node.nodeid][bstack1l111l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭⏿")] = bstack111l11l1l1_opy_
            bstack1lll11ll11ll_opy_(bstack111l11l1l1_opy_.uuid)
            bstack1llll1lll1_opy_.bstack111l1l111l_opy_(bstack1l111l1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ␀"), bstack111l11l1l1_opy_)
        except Exception as err:
            print(bstack1l111l1_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱ࠽ࠤࢀࢃࠧ␁"), str(err))
def bstack1lll11l1ll1l_opy_(bstack111l1l1lll_opy_):
    if bstack111l1l1lll_opy_ in store[bstack1l111l1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ␂")]:
        store[bstack1l111l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ␃")].remove(bstack111l1l1lll_opy_)
def bstack1lll11ll11ll_opy_(test_uuid):
    store[bstack1l111l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ␄")] = test_uuid
    threading.current_thread().current_test_uuid = test_uuid
@bstack1llll1lll1_opy_.bstack1lll1ll1111l_opy_
def bstack1lll11ll1ll1_opy_(item, call, report):
    logger.debug(bstack1l111l1_opy_ (u"ࠩ࡫ࡥࡳࡪ࡬ࡦࡡࡲ࠵࠶ࡿ࡟ࡵࡧࡶࡸࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡹࡴࡢࡴࡷࠫ␅"))
    global bstack1lll11l1l111_opy_
    bstack11l11ll11l_opy_ = bstack11llll1111_opy_()
    if hasattr(report, bstack1l111l1_opy_ (u"ࠪࡷࡹࡵࡰࠨ␆")):
        bstack11l11ll11l_opy_ = bstack111lll1ll1l_opy_(report.stop)
    elif hasattr(report, bstack1l111l1_opy_ (u"ࠫࡸࡺࡡࡳࡶࠪ␇")):
        bstack11l11ll11l_opy_ = bstack111lll1ll1l_opy_(report.start)
    try:
        if getattr(report, bstack1l111l1_opy_ (u"ࠬࡽࡨࡦࡰࠪ␈"), bstack1l111l1_opy_ (u"࠭ࠧ␉")) == bstack1l111l1_opy_ (u"ࠧࡤࡣ࡯ࡰࠬ␊"):
            logger.debug(bstack1l111l1_opy_ (u"ࠨࡪࡤࡲࡩࡲࡥࡠࡱ࠴࠵ࡾࡥࡴࡦࡵࡷࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡸࡺࡡࡵࡧࠣ࠱ࠥࢁࡽ࠭ࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠥ࠳ࠠࡼࡿࠪ␋").format(getattr(report, bstack1l111l1_opy_ (u"ࠩࡺ࡬ࡪࡴࠧ␌"), bstack1l111l1_opy_ (u"ࠪࠫ␍")).__str__(), bstack1lll11l1l111_opy_))
            if bstack1lll11l1l111_opy_ == bstack1l111l1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ␎"):
                _1111l1l11l_opy_[item.nodeid][bstack1l111l1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ␏")] = bstack11l11ll11l_opy_
                bstack1lll11ll11l1_opy_(item, _1111l1l11l_opy_[item.nodeid], bstack1l111l1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ␐"), report, call)
                store[bstack1l111l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ␑")] = None
            elif bstack1lll11l1l111_opy_ == bstack1l111l1_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠧ␒"):
                bstack111l11l1l1_opy_ = _1111l1l11l_opy_[item.nodeid][bstack1l111l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ␓")]
                bstack111l11l1l1_opy_.set(hooks=_1111l1l11l_opy_[item.nodeid].get(bstack1l111l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ␔"), []))
                exception, bstack111l111lll_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack111l111lll_opy_ = [call.excinfo.exconly(), getattr(report, bstack1l111l1_opy_ (u"ࠫࡱࡵ࡮ࡨࡴࡨࡴࡷࡺࡥࡹࡶࠪ␕"), bstack1l111l1_opy_ (u"ࠬ࠭␖"))]
                bstack111l11l1l1_opy_.stop(time=bstack11l11ll11l_opy_, result=Result(result=getattr(report, bstack1l111l1_opy_ (u"࠭࡯ࡶࡶࡦࡳࡲ࡫ࠧ␗"), bstack1l111l1_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ␘")), exception=exception, bstack111l111lll_opy_=bstack111l111lll_opy_))
                bstack1llll1lll1_opy_.bstack111l1l111l_opy_(bstack1l111l1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ␙"), _1111l1l11l_opy_[item.nodeid][bstack1l111l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ␚")])
        elif getattr(report, bstack1l111l1_opy_ (u"ࠪࡻ࡭࡫࡮ࠨ␛"), bstack1l111l1_opy_ (u"ࠫࠬ␜")) in [bstack1l111l1_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ␝"), bstack1l111l1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨ␞")]:
            logger.debug(bstack1l111l1_opy_ (u"ࠧࡩࡣࡱࡨࡱ࡫࡟ࡰ࠳࠴ࡽࡤࡺࡥࡴࡶࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡷࡹࡧࡴࡦࠢ࠰ࠤࢀࢃࠬࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤ࠲ࠦࡻࡾࠩ␟").format(getattr(report, bstack1l111l1_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭␠"), bstack1l111l1_opy_ (u"ࠩࠪ␡")).__str__(), bstack1lll11l1l111_opy_))
            bstack111l1l1l1l_opy_ = item.nodeid + bstack1l111l1_opy_ (u"ࠪ࠱ࠬ␢") + getattr(report, bstack1l111l1_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩ␣"), bstack1l111l1_opy_ (u"ࠬ࠭␤"))
            if getattr(report, bstack1l111l1_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ␥"), False):
                hook_type = bstack1l111l1_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬ␦") if getattr(report, bstack1l111l1_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭␧"), bstack1l111l1_opy_ (u"ࠩࠪ␨")) == bstack1l111l1_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ␩") else bstack1l111l1_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨ␪")
                _1111l1l11l_opy_[bstack111l1l1l1l_opy_] = {
                    bstack1l111l1_opy_ (u"ࠬࡻࡵࡪࡦࠪ␫"): uuid4().__str__(),
                    bstack1l111l1_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ␬"): bstack11l11ll11l_opy_,
                    bstack1l111l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪ␭"): hook_type
                }
            _1111l1l11l_opy_[bstack111l1l1l1l_opy_][bstack1l111l1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭␮")] = bstack11l11ll11l_opy_
            bstack1lll11l1ll1l_opy_(_1111l1l11l_opy_[bstack111l1l1l1l_opy_][bstack1l111l1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ␯")])
            bstack1lll11ll1l11_opy_(item, _1111l1l11l_opy_[bstack111l1l1l1l_opy_], bstack1l111l1_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ␰"), report, call)
            if getattr(report, bstack1l111l1_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩ␱"), bstack1l111l1_opy_ (u"ࠬ࠭␲")) == bstack1l111l1_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ␳"):
                if getattr(report, bstack1l111l1_opy_ (u"ࠧࡰࡷࡷࡧࡴࡳࡥࠨ␴"), bstack1l111l1_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ␵")) == bstack1l111l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ␶"):
                    bstack11111llll1_opy_ = {
                        bstack1l111l1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ␷"): uuid4().__str__(),
                        bstack1l111l1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ␸"): bstack11llll1111_opy_(),
                        bstack1l111l1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ␹"): bstack11llll1111_opy_()
                    }
                    _1111l1l11l_opy_[item.nodeid] = {**_1111l1l11l_opy_[item.nodeid], **bstack11111llll1_opy_}
                    bstack1lll11ll11l1_opy_(item, _1111l1l11l_opy_[item.nodeid], bstack1l111l1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ␺"))
                    bstack1lll11ll11l1_opy_(item, _1111l1l11l_opy_[item.nodeid], bstack1l111l1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ␻"), report, call)
    except Exception as err:
        print(bstack1l111l1_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡩࡣࡱࡨࡱ࡫࡟ࡰ࠳࠴ࡽࡤࡺࡥࡴࡶࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡿࢂ࠭␼"), str(err))
def bstack1lll11lllll1_opy_(test, bstack11111llll1_opy_, result=None, call=None, bstack1ll1l1ll11_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack111l11l1l1_opy_ = {
        bstack1l111l1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ␽"): bstack11111llll1_opy_[bstack1l111l1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ␾")],
        bstack1l111l1_opy_ (u"ࠫࡹࡿࡰࡦࠩ␿"): bstack1l111l1_opy_ (u"ࠬࡺࡥࡴࡶࠪ⑀"),
        bstack1l111l1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ⑁"): test.name,
        bstack1l111l1_opy_ (u"ࠧࡣࡱࡧࡽࠬ⑂"): {
            bstack1l111l1_opy_ (u"ࠨ࡮ࡤࡲ࡬࠭⑃"): bstack1l111l1_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ⑄"),
            bstack1l111l1_opy_ (u"ࠪࡧࡴࡪࡥࠨ⑅"): inspect.getsource(test.obj)
        },
        bstack1l111l1_opy_ (u"ࠫ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ⑆"): test.name,
        bstack1l111l1_opy_ (u"ࠬࡹࡣࡰࡲࡨࠫ⑇"): test.name,
        bstack1l111l1_opy_ (u"࠭ࡳࡤࡱࡳࡩࡸ࠭⑈"): bstack11ll11l11_opy_.bstack1111ll11l1_opy_(test),
        bstack1l111l1_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ⑉"): file_path,
        bstack1l111l1_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࠪ⑊"): file_path,
        bstack1l111l1_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ⑋"): bstack1l111l1_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫ⑌"),
        bstack1l111l1_opy_ (u"ࠫࡻࡩ࡟ࡧ࡫࡯ࡩࡵࡧࡴࡩࠩ⑍"): file_path,
        bstack1l111l1_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ⑎"): bstack11111llll1_opy_[bstack1l111l1_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ⑏")],
        bstack1l111l1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ⑐"): bstack1l111l1_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴࠨ⑑"),
        bstack1l111l1_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡔࡨࡶࡺࡴࡐࡢࡴࡤࡱࠬ⑒"): {
            bstack1l111l1_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࡡࡱࡥࡲ࡫ࠧ⑓"): test.nodeid
        },
        bstack1l111l1_opy_ (u"ࠫࡹࡧࡧࡴࠩ⑔"): bstack111ll11111l_opy_(test.own_markers)
    }
    if bstack1ll1l1ll11_opy_ in [bstack1l111l1_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ࠭⑕"), bstack1l111l1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ⑖")]:
        bstack111l11l1l1_opy_[bstack1l111l1_opy_ (u"ࠧ࡮ࡧࡷࡥࠬ⑗")] = {
            bstack1l111l1_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪ⑘"): bstack11111llll1_opy_.get(bstack1l111l1_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫ⑙"), [])
        }
    if bstack1ll1l1ll11_opy_ == bstack1l111l1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫ⑚"):
        bstack111l11l1l1_opy_[bstack1l111l1_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ⑛")] = bstack1l111l1_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭⑜")
        bstack111l11l1l1_opy_[bstack1l111l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ⑝")] = bstack11111llll1_opy_[bstack1l111l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭⑞")]
        bstack111l11l1l1_opy_[bstack1l111l1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⑟")] = bstack11111llll1_opy_[bstack1l111l1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ①")]
    if result:
        bstack111l11l1l1_opy_[bstack1l111l1_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ②")] = result.outcome
        bstack111l11l1l1_opy_[bstack1l111l1_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬ③")] = result.duration * 1000
        bstack111l11l1l1_opy_[bstack1l111l1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ④")] = bstack11111llll1_opy_[bstack1l111l1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⑤")]
        if result.failed:
            bstack111l11l1l1_opy_[bstack1l111l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭⑥")] = bstack1llll1lll1_opy_.bstack1lllll111ll_opy_(call.excinfo.typename)
            bstack111l11l1l1_opy_[bstack1l111l1_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩ⑦")] = bstack1llll1lll1_opy_.bstack1lll1l1lll1l_opy_(call.excinfo, result)
        bstack111l11l1l1_opy_[bstack1l111l1_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ⑧")] = bstack11111llll1_opy_[bstack1l111l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ⑨")]
    if outcome:
        bstack111l11l1l1_opy_[bstack1l111l1_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ⑩")] = bstack111ll111ll1_opy_(outcome)
        bstack111l11l1l1_opy_[bstack1l111l1_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭⑪")] = 0
        bstack111l11l1l1_opy_[bstack1l111l1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⑫")] = bstack11111llll1_opy_[bstack1l111l1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⑬")]
        if bstack111l11l1l1_opy_[bstack1l111l1_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ⑭")] == bstack1l111l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ⑮"):
            bstack111l11l1l1_opy_[bstack1l111l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩ⑯")] = bstack1l111l1_opy_ (u"࡚ࠫࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠬ⑰")  # bstack1lll11l1l1l1_opy_
            bstack111l11l1l1_opy_[bstack1l111l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭⑱")] = [{bstack1l111l1_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩ⑲"): [bstack1l111l1_opy_ (u"ࠧࡴࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠫ⑳")]}]
        bstack111l11l1l1_opy_[bstack1l111l1_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ⑴")] = bstack11111llll1_opy_[bstack1l111l1_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ⑵")]
    return bstack111l11l1l1_opy_
def bstack1lll11ll1l1l_opy_(test, bstack1111l11l1l_opy_, bstack1ll1l1ll11_opy_, result, call, outcome, bstack1lll1l11111l_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack1111l11l1l_opy_[bstack1l111l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭⑶")]
    hook_name = bstack1111l11l1l_opy_[bstack1l111l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠧ⑷")]
    hook_data = {
        bstack1l111l1_opy_ (u"ࠬࡻࡵࡪࡦࠪ⑸"): bstack1111l11l1l_opy_[bstack1l111l1_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⑹")],
        bstack1l111l1_opy_ (u"ࠧࡵࡻࡳࡩࠬ⑺"): bstack1l111l1_opy_ (u"ࠨࡪࡲࡳࡰ࠭⑻"),
        bstack1l111l1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ⑼"): bstack1l111l1_opy_ (u"ࠪࡿࢂ࠭⑽").format(bstack1llll1lll111_opy_(hook_name)),
        bstack1l111l1_opy_ (u"ࠫࡧࡵࡤࡺࠩ⑾"): {
            bstack1l111l1_opy_ (u"ࠬࡲࡡ࡯ࡩࠪ⑿"): bstack1l111l1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭⒀"),
            bstack1l111l1_opy_ (u"ࠧࡤࡱࡧࡩࠬ⒁"): None
        },
        bstack1l111l1_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࠧ⒂"): test.name,
        bstack1l111l1_opy_ (u"ࠩࡶࡧࡴࡶࡥࡴࠩ⒃"): bstack11ll11l11_opy_.bstack1111ll11l1_opy_(test, hook_name),
        bstack1l111l1_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭⒄"): file_path,
        bstack1l111l1_opy_ (u"ࠫࡱࡵࡣࡢࡶ࡬ࡳࡳ࠭⒅"): file_path,
        bstack1l111l1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ⒆"): bstack1l111l1_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧ⒇"),
        bstack1l111l1_opy_ (u"ࠧࡷࡥࡢࡪ࡮ࡲࡥࡱࡣࡷ࡬ࠬ⒈"): file_path,
        bstack1l111l1_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ⒉"): bstack1111l11l1l_opy_[bstack1l111l1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭⒊")],
        bstack1l111l1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭⒋"): bstack1l111l1_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷ࠱ࡨࡻࡣࡶ࡯ࡥࡩࡷ࠭⒌") if bstack1lll11l1l111_opy_ == bstack1l111l1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠩ⒍") else bstack1l111l1_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠭⒎"),
        bstack1l111l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪ⒏"): hook_type
    }
    bstack1ll111lll1l_opy_ = bstack1111lll1ll_opy_(_1111l1l11l_opy_.get(test.nodeid, None))
    if bstack1ll111lll1l_opy_:
        hook_data[bstack1l111l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢ࡭ࡩ࠭⒐")] = bstack1ll111lll1l_opy_
    if result:
        hook_data[bstack1l111l1_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ⒑")] = result.outcome
        hook_data[bstack1l111l1_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫ⒒")] = result.duration * 1000
        hook_data[bstack1l111l1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⒓")] = bstack1111l11l1l_opy_[bstack1l111l1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⒔")]
        if result.failed:
            hook_data[bstack1l111l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬ⒕")] = bstack1llll1lll1_opy_.bstack1lllll111ll_opy_(call.excinfo.typename)
            hook_data[bstack1l111l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨ⒖")] = bstack1llll1lll1_opy_.bstack1lll1l1lll1l_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack1l111l1_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ⒗")] = bstack111ll111ll1_opy_(outcome)
        hook_data[bstack1l111l1_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪ⒘")] = 100
        hook_data[bstack1l111l1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⒙")] = bstack1111l11l1l_opy_[bstack1l111l1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⒚")]
        if hook_data[bstack1l111l1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ⒛")] == bstack1l111l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭⒜"):
            hook_data[bstack1l111l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭⒝")] = bstack1l111l1_opy_ (u"ࠨࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠩ⒞")  # bstack1lll11l1l1l1_opy_
            hook_data[bstack1l111l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪ⒟")] = [{bstack1l111l1_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭⒠"): [bstack1l111l1_opy_ (u"ࠫࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠨ⒡")]}]
    if bstack1lll1l11111l_opy_:
        hook_data[bstack1l111l1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ⒢")] = bstack1lll1l11111l_opy_.result
        hook_data[bstack1l111l1_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧ⒣")] = bstack111llllllll_opy_(bstack1111l11l1l_opy_[bstack1l111l1_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ⒤")], bstack1111l11l1l_opy_[bstack1l111l1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⒥")])
        hook_data[bstack1l111l1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⒦")] = bstack1111l11l1l_opy_[bstack1l111l1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⒧")]
        if hook_data[bstack1l111l1_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ⒨")] == bstack1l111l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ⒩"):
            hook_data[bstack1l111l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬ⒪")] = bstack1llll1lll1_opy_.bstack1lllll111ll_opy_(bstack1lll1l11111l_opy_.exception_type)
            hook_data[bstack1l111l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨ⒫")] = [{bstack1l111l1_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫ⒬"): bstack111l1llll11_opy_(bstack1lll1l11111l_opy_.exception)}]
    return hook_data
def bstack1lll11ll11l1_opy_(test, bstack11111llll1_opy_, bstack1ll1l1ll11_opy_, result=None, call=None, outcome=None):
    logger.debug(bstack1l111l1_opy_ (u"ࠩࡶࡩࡳࡪ࡟ࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡨࡺࡪࡴࡴ࠻ࠢࡄࡸࡹ࡫࡭ࡱࡶ࡬ࡲ࡬ࠦࡴࡰࠢࡪࡩࡳ࡫ࡲࡢࡶࡨࠤࡹ࡫ࡳࡵࠢࡧࡥࡹࡧࠠࡧࡱࡵࠤࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠡ࠯ࠣࡿࢂ࠭⒭").format(bstack1ll1l1ll11_opy_))
    bstack111l11l1l1_opy_ = bstack1lll11lllll1_opy_(test, bstack11111llll1_opy_, result, call, bstack1ll1l1ll11_opy_, outcome)
    driver = getattr(test, bstack1l111l1_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫ⒮"), None)
    if bstack1ll1l1ll11_opy_ == bstack1l111l1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ⒯") and driver:
        bstack111l11l1l1_opy_[bstack1l111l1_opy_ (u"ࠬ࡯࡮ࡵࡧࡪࡶࡦࡺࡩࡰࡰࡶࠫ⒰")] = bstack1llll1lll1_opy_.bstack111l1ll111_opy_(driver)
    if bstack1ll1l1ll11_opy_ == bstack1l111l1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧ⒱"):
        bstack1ll1l1ll11_opy_ = bstack1l111l1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ⒲")
    bstack1111l11l11_opy_ = {
        bstack1l111l1_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ⒳"): bstack1ll1l1ll11_opy_,
        bstack1l111l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫ⒴"): bstack111l11l1l1_opy_
    }
    bstack1llll1lll1_opy_.bstack1ll111llll_opy_(bstack1111l11l11_opy_)
    if bstack1ll1l1ll11_opy_ == bstack1l111l1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ⒵"):
        threading.current_thread().bstackTestMeta = {bstack1l111l1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫⒶ"): bstack1l111l1_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭Ⓑ")}
    elif bstack1ll1l1ll11_opy_ == bstack1l111l1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨⒸ"):
        threading.current_thread().bstackTestMeta = {bstack1l111l1_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧⒹ"): getattr(result, bstack1l111l1_opy_ (u"ࠨࡱࡸࡸࡨࡵ࡭ࡦࠩⒺ"), bstack1l111l1_opy_ (u"ࠩࠪⒻ"))}
def bstack1lll11ll1l11_opy_(test, bstack11111llll1_opy_, bstack1ll1l1ll11_opy_, result=None, call=None, outcome=None, bstack1lll1l11111l_opy_=None):
    logger.debug(bstack1l111l1_opy_ (u"ࠪࡷࡪࡴࡤࡠࡪࡲࡳࡰࡥࡲࡶࡰࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡅࡹࡺࡥ࡮ࡲࡷ࡭ࡳ࡭ࠠࡵࡱࠣ࡫ࡪࡴࡥࡳࡣࡷࡩࠥ࡮࡯ࡰ࡭ࠣࡨࡦࡺࡡ࠭ࠢࡨࡺࡪࡴࡴࡕࡻࡳࡩࠥ࠳ࠠࡼࡿࠪⒼ").format(bstack1ll1l1ll11_opy_))
    hook_data = bstack1lll11ll1l1l_opy_(test, bstack11111llll1_opy_, bstack1ll1l1ll11_opy_, result, call, outcome, bstack1lll1l11111l_opy_)
    bstack1111l11l11_opy_ = {
        bstack1l111l1_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨⒽ"): bstack1ll1l1ll11_opy_,
        bstack1l111l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴࠧⒾ"): hook_data
    }
    bstack1llll1lll1_opy_.bstack1ll111llll_opy_(bstack1111l11l11_opy_)
def bstack1111lll1ll_opy_(bstack11111llll1_opy_):
    if not bstack11111llll1_opy_:
        return None
    if bstack11111llll1_opy_.get(bstack1l111l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩⒿ"), None):
        return getattr(bstack11111llll1_opy_[bstack1l111l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪⓀ")], bstack1l111l1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭Ⓛ"), None)
    return bstack11111llll1_opy_.get(bstack1l111l1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧⓂ"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1lll1111_opy_.LOG, bstack1lll11ll1l1_opy_.PRE, request, caplog)
    yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1lll1111_opy_.LOG, bstack1lll11ll1l1_opy_.POST, request, caplog)
        return # skip all existing operations
    try:
        if not bstack1llll1lll1_opy_.on():
            return
        places = [bstack1l111l1_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩⓃ"), bstack1l111l1_opy_ (u"ࠫࡨࡧ࡬࡭ࠩⓄ"), bstack1l111l1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧⓅ")]
        logs = []
        for bstack1lll11l11ll1_opy_ in places:
            records = caplog.get_records(bstack1lll11l11ll1_opy_)
            bstack1lll11lll1ll_opy_ = bstack1l111l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭Ⓠ") if bstack1lll11l11ll1_opy_ == bstack1l111l1_opy_ (u"ࠧࡤࡣ࡯ࡰࠬⓇ") else bstack1l111l1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨⓈ")
            bstack1lll11l11lll_opy_ = request.node.nodeid + (bstack1l111l1_opy_ (u"ࠩࠪⓉ") if bstack1lll11l11ll1_opy_ == bstack1l111l1_opy_ (u"ࠪࡧࡦࡲ࡬ࠨⓊ") else bstack1l111l1_opy_ (u"ࠫ࠲࠭Ⓥ") + bstack1lll11l11ll1_opy_)
            test_uuid = bstack1111lll1ll_opy_(_1111l1l11l_opy_.get(bstack1lll11l11lll_opy_, None))
            if not test_uuid:
                continue
            for record in records:
                if bstack111lll11111_opy_(record.message):
                    continue
                logs.append({
                    bstack1l111l1_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨⓌ"): bstack111l1llllll_opy_(record.created).isoformat() + bstack1l111l1_opy_ (u"࡚࠭ࠨⓍ"),
                    bstack1l111l1_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭Ⓨ"): record.levelname,
                    bstack1l111l1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩⓏ"): record.message,
                    bstack1lll11lll1ll_opy_: test_uuid
                })
        if len(logs) > 0:
            bstack1llll1lll1_opy_.bstack11l1l111_opy_(logs)
    except Exception as err:
        print(bstack1l111l1_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡨࡧࡴࡴࡤࡠࡨ࡬ࡼࡹࡻࡲࡦ࠼ࠣࡿࢂ࠭ⓐ"), str(err))
def bstack11llll111_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack1l1l1llll1_opy_
    bstack1ll1llll1_opy_ = bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧⓑ"), None) and bstack1l1l1l111_opy_(
            threading.current_thread(), bstack1l111l1_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪⓒ"), None)
    bstack1l111l1lll_opy_ = getattr(driver, bstack1l111l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬⓓ"), None) != None and getattr(driver, bstack1l111l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭ⓔ"), None) == True
    if sequence == bstack1l111l1_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫ࠧⓕ") and driver != None:
      if not bstack1l1l1llll1_opy_ and bstack1l1l1l11l1l_opy_() and bstack1l111l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨⓖ") in CONFIG and CONFIG[bstack1l111l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩⓗ")] == True and bstack1l111l1l_opy_.bstack111l11lll_opy_(driver_command) and (bstack1l111l1lll_opy_ or bstack1ll1llll1_opy_) and not bstack1llll11ll1_opy_(args):
        try:
          bstack1l1l1llll1_opy_ = True
          logger.debug(bstack1l111l1_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥ࡬࡯ࡳࠢࡾࢁࠬⓘ").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack1l111l1_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡧࡵࡪࡴࡸ࡭ࠡࡵࡦࡥࡳࠦࡻࡾࠩⓙ").format(str(err)))
        bstack1l1l1llll1_opy_ = False
    if sequence == bstack1l111l1_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫⓚ"):
        if driver_command == bstack1l111l1_opy_ (u"࠭ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠪⓛ"):
            bstack1llll1lll1_opy_.bstack1l111111l1_opy_({
                bstack1l111l1_opy_ (u"ࠧࡪ࡯ࡤ࡫ࡪ࠭ⓜ"): response[bstack1l111l1_opy_ (u"ࠨࡸࡤࡰࡺ࡫ࠧⓝ")],
                bstack1l111l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩⓞ"): store[bstack1l111l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧⓟ")]
            })
def bstack111lllllll_opy_():
    global bstack1l11ll11_opy_
    bstack1ll1lll11_opy_.bstack1lll111l11_opy_()
    logging.shutdown()
    bstack1llll1lll1_opy_.bstack111l1111l1_opy_()
    for driver in bstack1l11ll11_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1lll1l1111l1_opy_(*args):
    global bstack1l11ll11_opy_
    bstack1llll1lll1_opy_.bstack111l1111l1_opy_()
    for driver in bstack1l11ll11_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack11111ll11_opy_, stage=STAGE.bstack11l11l11l1_opy_, bstack111l1l11_opy_=bstack1l1l1l1ll1_opy_)
def bstack11l11lll_opy_(self, *args, **kwargs):
    bstack1l1l1ll1l1_opy_ = bstack111lll1l1_opy_(self, *args, **kwargs)
    bstack11ll1l1l1l_opy_ = getattr(threading.current_thread(), bstack1l111l1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡘࡪࡹࡴࡎࡧࡷࡥࠬⓠ"), None)
    if bstack11ll1l1l1l_opy_ and bstack11ll1l1l1l_opy_.get(bstack1l111l1_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬⓡ"), bstack1l111l1_opy_ (u"࠭ࠧⓢ")) == bstack1l111l1_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨⓣ"):
        bstack1llll1lll1_opy_.bstack111ll1lll1_opy_(self)
    return bstack1l1l1ll1l1_opy_
@measure(event_name=EVENTS.bstack1l1l11ll1_opy_, stage=STAGE.bstack1ll1l1llll_opy_, bstack111l1l11_opy_=bstack1l1l1l1ll1_opy_)
def bstack1111l1111_opy_(framework_name):
    from bstack_utils.config import Config
    bstack1l1l1111_opy_ = Config.bstack1llll1ll11_opy_()
    if bstack1l1l1111_opy_.get_property(bstack1l111l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠ࡯ࡲࡨࡤࡩࡡ࡭࡮ࡨࡨࠬⓤ")):
        return
    bstack1l1l1111_opy_.bstack11ll11l11l_opy_(bstack1l111l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡰࡳࡩࡥࡣࡢ࡮࡯ࡩࡩ࠭ⓥ"), True)
    global bstack1lll11ll1l_opy_
    global bstack11l1111111_opy_
    bstack1lll11ll1l_opy_ = framework_name
    logger.info(bstack11l1111l_opy_.format(bstack1lll11ll1l_opy_.split(bstack1l111l1_opy_ (u"ࠪ࠱ࠬⓦ"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1l1l1l11l1l_opy_():
            Service.start = bstack111ll1llll_opy_
            Service.stop = bstack11lll11lll_opy_
            webdriver.Remote.get = bstack1l11ll1ll_opy_
            webdriver.Remote.__init__ = bstack1ll11lll1_opy_
            if not isinstance(os.getenv(bstack1l111l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔ࡞࡚ࡅࡔࡖࡢࡔࡆࡘࡁࡍࡎࡈࡐࠬⓧ")), str):
                return
            WebDriver.quit = bstack1ll11lll_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        elif bstack1llll1lll1_opy_.on():
            webdriver.Remote.__init__ = bstack11l11lll_opy_
        bstack11l1111111_opy_ = True
    except Exception as e:
        pass
    if os.environ.get(bstack1l111l1_opy_ (u"࡙ࠬࡅࡍࡇࡑࡍ࡚ࡓ࡟ࡐࡔࡢࡔࡑࡇ࡙ࡘࡔࡌࡋࡍ࡚࡟ࡊࡐࡖࡘࡆࡒࡌࡆࡆࠪⓨ")):
        bstack11l1111111_opy_ = eval(os.environ.get(bstack1l111l1_opy_ (u"࠭ࡓࡆࡎࡈࡒࡎ࡛ࡍࡠࡑࡕࡣࡕࡒࡁ࡚࡙ࡕࡍࡌࡎࡔࡠࡋࡑࡗ࡙ࡇࡌࡍࡇࡇࠫⓩ")))
    if not bstack11l1111111_opy_:
        bstack11l1l1ll1l_opy_(bstack1l111l1_opy_ (u"ࠢࡑࡣࡦ࡯ࡦ࡭ࡥࡴࠢࡱࡳࡹࠦࡩ࡯ࡵࡷࡥࡱࡲࡥࡥࠤ⓪"), bstack111ll11lll_opy_)
    if bstack111llllll_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            if hasattr(RemoteConnection, bstack1l111l1_opy_ (u"ࠨࡡࡪࡩࡹࡥࡰࡳࡱࡻࡽࡤࡻࡲ࡭ࠩ⓫")) and callable(getattr(RemoteConnection, bstack1l111l1_opy_ (u"ࠩࡢ࡫ࡪࡺ࡟ࡱࡴࡲࡼࡾࡥࡵࡳ࡮ࠪ⓬"))):
                RemoteConnection._get_proxy_url = bstack1l1ll1llll_opy_
            else:
                from selenium.webdriver.remote.client_config import ClientConfig
                ClientConfig.get_proxy_url = bstack1l1ll1llll_opy_
        except Exception as e:
            logger.error(bstack11l1lll111_opy_.format(str(e)))
    if bstack1l111l1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ⓭") in str(framework_name).lower():
        if not bstack1l1l1l11l1l_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack11l1l1l1ll_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack111ll11l11_opy_
            Config.getoption = bstack1l11ll111l_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack1llll111ll_opy_
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1ll1l1l11l_opy_, stage=STAGE.bstack11l11l11l1_opy_, bstack111l1l11_opy_=bstack1l1l1l1ll1_opy_)
def bstack1ll11lll_opy_(self):
    global bstack1lll11ll1l_opy_
    global bstack1llll1ll1l_opy_
    global bstack1l11111l1l_opy_
    try:
        if bstack1l111l1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ⓮") in bstack1lll11ll1l_opy_ and self.session_id != None and bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"ࠬࡺࡥࡴࡶࡖࡸࡦࡺࡵࡴࠩ⓯"), bstack1l111l1_opy_ (u"࠭ࠧ⓰")) != bstack1l111l1_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ⓱"):
            bstack1l1ll11l11_opy_ = bstack1l111l1_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ⓲") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1l111l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ⓳")
            bstack111l11l11_opy_(logger, True)
            if os.environ.get(bstack1l111l1_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖࡢࡘࡊ࡙ࡔࡠࡐࡄࡑࡊ࠭⓴"), None):
                self.execute_script(
                    bstack1l111l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩ⓵") + json.dumps(
                        os.environ.get(bstack1l111l1_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࡤ࡚ࡅࡔࡖࡢࡒࡆࡓࡅࠨ⓶"))) + bstack1l111l1_opy_ (u"࠭ࡽࡾࠩ⓷"))
            if self != None:
                bstack11llll1ll_opy_(self, bstack1l1ll11l11_opy_, bstack1l111l1_opy_ (u"ࠧ࠭ࠢࠪ⓸").join(threading.current_thread().bstackTestErrorMessages))
        if not cli.bstack1ll1l1llll1_opy_(bstack1ll1l11llll_opy_):
            item = store.get(bstack1l111l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬ⓹"), None)
            if item is not None and bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ⓺"), None):
                bstack1lllllllll_opy_.bstack1ll1l111ll_opy_(self, bstack11lll11l11_opy_, logger, item)
        threading.current_thread().testStatus = bstack1l111l1_opy_ (u"ࠪࠫ⓻")
    except Exception as e:
        logger.debug(bstack1l111l1_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡰࡥࡷࡱࡩ࡯ࡩࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࠧ⓼") + str(e))
    bstack1l11111l1l_opy_(self)
    self.session_id = None
@measure(event_name=EVENTS.bstack1llll1l111_opy_, stage=STAGE.bstack11l11l11l1_opy_, bstack111l1l11_opy_=bstack1l1l1l1ll1_opy_)
def bstack1ll11lll1_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1llll1ll1l_opy_
    global bstack1l1l1l1ll1_opy_
    global bstack1l1111l1l_opy_
    global bstack1lll11ll1l_opy_
    global bstack111lll1l1_opy_
    global bstack1l11ll11_opy_
    global bstack1l1l1l11l1_opy_
    global bstack1lll111l1_opy_
    global bstack11lll11l11_opy_
    CONFIG[bstack1l111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ⓽")] = str(bstack1lll11ll1l_opy_) + str(__version__)
    command_executor = bstack1lllllll11_opy_(bstack1l1l1l11l1_opy_, CONFIG)
    logger.debug(bstack111ll111l1_opy_.format(command_executor))
    proxy = bstack11lll111l_opy_(CONFIG, proxy)
    bstack1l1l11111l_opy_ = 0
    try:
        if bstack1l1111l1l_opy_ is True:
            bstack1l1l11111l_opy_ = int(os.environ.get(bstack1l111l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭⓾")))
    except:
        bstack1l1l11111l_opy_ = 0
    bstack1l11ll1l_opy_ = bstack1l1ll111l_opy_(CONFIG, bstack1l1l11111l_opy_)
    logger.debug(bstack1111ll11_opy_.format(str(bstack1l11ll1l_opy_)))
    bstack11lll11l11_opy_ = CONFIG.get(bstack1l111l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ⓿"))[bstack1l1l11111l_opy_]
    if bstack1l111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ─") in CONFIG and CONFIG[bstack1l111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭━")]:
        bstack11l111l1ll_opy_(bstack1l11ll1l_opy_, bstack1lll111l1_opy_)
    if bstack11111l11l_opy_.bstack1l1llllll1_opy_(CONFIG, bstack1l1l11111l_opy_) and bstack11111l11l_opy_.bstack11l11llll_opy_(bstack1l11ll1l_opy_, options, desired_capabilities):
        threading.current_thread().a11yPlatform = True
        if not cli.bstack1ll1l1llll1_opy_(bstack1ll1l11llll_opy_):
            bstack11111l11l_opy_.set_capabilities(bstack1l11ll1l_opy_, CONFIG)
    if desired_capabilities:
        bstack1l1ll1ll_opy_ = bstack11l1lll11_opy_(desired_capabilities)
        bstack1l1ll1ll_opy_[bstack1l111l1_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪ│")] = bstack1llllllll_opy_(CONFIG)
        bstack111ll1lll_opy_ = bstack1l1ll111l_opy_(bstack1l1ll1ll_opy_)
        if bstack111ll1lll_opy_:
            bstack1l11ll1l_opy_ = update(bstack111ll1lll_opy_, bstack1l11ll1l_opy_)
        desired_capabilities = None
    if options:
        bstack11l1ll1l1l_opy_(options, bstack1l11ll1l_opy_)
    if not options:
        options = bstack111ll1l1_opy_(bstack1l11ll1l_opy_)
    if proxy and bstack111l1111l_opy_() >= version.parse(bstack1l111l1_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫ┃")):
        options.proxy(proxy)
    if options and bstack111l1111l_opy_() >= version.parse(bstack1l111l1_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫ┄")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack111l1111l_opy_() < version.parse(bstack1l111l1_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬ┅")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1l11ll1l_opy_)
    logger.info(bstack1ll1l11l_opy_)
    bstack11lll1l1ll_opy_.end(EVENTS.bstack1l1l11ll1_opy_.value, EVENTS.bstack1l1l11ll1_opy_.value + bstack1l111l1_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢ┆"),
                               EVENTS.bstack1l1l11ll1_opy_.value + bstack1l111l1_opy_ (u"ࠣ࠼ࡨࡲࡩࠨ┇"), True, None)
    try:
        if bstack111l1111l_opy_() >= version.parse(bstack1l111l1_opy_ (u"ࠩ࠷࠲࠶࠶࠮࠱ࠩ┈")):
            bstack111lll1l1_opy_(self, command_executor=command_executor,
                      options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
        elif bstack111l1111l_opy_() >= version.parse(bstack1l111l1_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩ┉")):
            bstack111lll1l1_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities, options=options,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive, file_detector=file_detector)
        elif bstack111l1111l_opy_() >= version.parse(bstack1l111l1_opy_ (u"ࠫ࠷࠴࠵࠴࠰࠳ࠫ┊")):
            bstack111lll1l1_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive, file_detector=file_detector)
        else:
            bstack111lll1l1_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive)
    except Exception as bstack1l1ll1ll11_opy_:
        logger.error(bstack11l11lll11_opy_.format(bstack1l111l1_opy_ (u"ࠬࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠫ┋"), str(bstack1l1ll1ll11_opy_)))
        raise bstack1l1ll1ll11_opy_
    try:
        bstack11lll1l111_opy_ = bstack1l111l1_opy_ (u"࠭ࠧ┌")
        if bstack111l1111l_opy_() >= version.parse(bstack1l111l1_opy_ (u"ࠧ࠵࠰࠳࠲࠵ࡨ࠱ࠨ┍")):
            bstack11lll1l111_opy_ = self.caps.get(bstack1l111l1_opy_ (u"ࠣࡱࡳࡸ࡮ࡳࡡ࡭ࡊࡸࡦ࡚ࡸ࡬ࠣ┎"))
        else:
            bstack11lll1l111_opy_ = self.capabilities.get(bstack1l111l1_opy_ (u"ࠤࡲࡴࡹ࡯࡭ࡢ࡮ࡋࡹࡧ࡛ࡲ࡭ࠤ┏"))
        if bstack11lll1l111_opy_:
            bstack111lll1111_opy_(bstack11lll1l111_opy_)
            if bstack111l1111l_opy_() <= version.parse(bstack1l111l1_opy_ (u"ࠪ࠷࠳࠷࠳࠯࠲ࠪ┐")):
                self.command_executor._url = bstack1l111l1_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧ┑") + bstack1l1l1l11l1_opy_ + bstack1l111l1_opy_ (u"ࠧࡀ࠸࠱࠱ࡺࡨ࠴࡮ࡵࡣࠤ┒")
            else:
                self.command_executor._url = bstack1l111l1_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࠣ┓") + bstack11lll1l111_opy_ + bstack1l111l1_opy_ (u"ࠢ࠰ࡹࡧ࠳࡭ࡻࡢࠣ└")
            logger.debug(bstack1l111l1ll1_opy_.format(bstack11lll1l111_opy_))
        else:
            logger.debug(bstack1ll11l1l1l_opy_.format(bstack1l111l1_opy_ (u"ࠣࡑࡳࡸ࡮ࡳࡡ࡭ࠢࡋࡹࡧࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥࠤ┕")))
    except Exception as e:
        logger.debug(bstack1ll11l1l1l_opy_.format(e))
    bstack1llll1ll1l_opy_ = self.session_id
    if bstack1l111l1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ┖") in bstack1lll11ll1l_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack1l111l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧ┗"), None)
        if item:
            bstack1lll11lll11l_opy_ = getattr(item, bstack1l111l1_opy_ (u"ࠫࡤࡺࡥࡴࡶࡢࡧࡦࡹࡥࡠࡵࡷࡥࡷࡺࡥࡥࠩ┘"), False)
            if not getattr(item, bstack1l111l1_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭┙"), None) and bstack1lll11lll11l_opy_:
                setattr(store[bstack1l111l1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪ┚")], bstack1l111l1_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨ┛"), self)
        bstack11ll1l1l1l_opy_ = getattr(threading.current_thread(), bstack1l111l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡕࡧࡶࡸࡒ࡫ࡴࡢࠩ├"), None)
        if bstack11ll1l1l1l_opy_ and bstack11ll1l1l1l_opy_.get(bstack1l111l1_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ┝"), bstack1l111l1_opy_ (u"ࠪࠫ┞")) == bstack1l111l1_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬ┟"):
            bstack1llll1lll1_opy_.bstack111ll1lll1_opy_(self)
    bstack1l11ll11_opy_.append(self)
    if bstack1l111l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ┠") in CONFIG and bstack1l111l1_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ┡") in CONFIG[bstack1l111l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ┢")][bstack1l1l11111l_opy_]:
        bstack1l1l1l1ll1_opy_ = CONFIG[bstack1l111l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ┣")][bstack1l1l11111l_opy_][bstack1l111l1_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ┤")]
    logger.debug(bstack1l11l11l_opy_.format(bstack1llll1ll1l_opy_))
@measure(event_name=EVENTS.bstack1l1ll11l_opy_, stage=STAGE.bstack11l11l11l1_opy_, bstack111l1l11_opy_=bstack1l1l1l1ll1_opy_)
def bstack1l11ll1ll_opy_(self, url):
    global bstack1ll1l1lll_opy_
    global CONFIG
    try:
        bstack111llllll1_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack111ll11ll1_opy_.format(str(err)))
    try:
        bstack1ll1l1lll_opy_(self, url)
    except Exception as e:
        try:
            bstack1llllll11l_opy_ = str(e)
            if any(err_msg in bstack1llllll11l_opy_ for err_msg in bstack1l11lll11l_opy_):
                bstack111llllll1_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack111ll11ll1_opy_.format(str(err)))
        raise e
def bstack11llll1l1l_opy_(item, when):
    global bstack1l1l11l111_opy_
    try:
        bstack1l1l11l111_opy_(item, when)
    except Exception as e:
        pass
def bstack1llll111ll_opy_(item, call, rep):
    global bstack111ll11ll_opy_
    global bstack1l11ll11_opy_
    name = bstack1l111l1_opy_ (u"ࠪࠫ┥")
    try:
        if rep.when == bstack1l111l1_opy_ (u"ࠫࡨࡧ࡬࡭ࠩ┦"):
            bstack1llll1ll1l_opy_ = threading.current_thread().bstackSessionId
            skipSessionName = item.config.getoption(bstack1l111l1_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ┧"))
            try:
                if (str(skipSessionName).lower() != bstack1l111l1_opy_ (u"࠭ࡴࡳࡷࡨࠫ┨")):
                    name = str(rep.nodeid)
                    bstack111ll1l11_opy_ = bstack11l111llll_opy_(bstack1l111l1_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ┩"), name, bstack1l111l1_opy_ (u"ࠨࠩ┪"), bstack1l111l1_opy_ (u"ࠩࠪ┫"), bstack1l111l1_opy_ (u"ࠪࠫ┬"), bstack1l111l1_opy_ (u"ࠫࠬ┭"))
                    os.environ[bstack1l111l1_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࡤ࡚ࡅࡔࡖࡢࡒࡆࡓࡅࠨ┮")] = name
                    for driver in bstack1l11ll11_opy_:
                        if bstack1llll1ll1l_opy_ == driver.session_id:
                            driver.execute_script(bstack111ll1l11_opy_)
            except Exception as e:
                logger.debug(bstack1l111l1_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠠࡧࡱࡵࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡵࡨࡷࡸ࡯࡯࡯࠼ࠣࡿࢂ࠭┯").format(str(e)))
            try:
                bstack1lll1llll1_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack1l111l1_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ┰"):
                    status = bstack1l111l1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ┱") if rep.outcome.lower() == bstack1l111l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ┲") else bstack1l111l1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ┳")
                    reason = bstack1l111l1_opy_ (u"ࠫࠬ┴")
                    if status == bstack1l111l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ┵"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack1l111l1_opy_ (u"࠭ࡩ࡯ࡨࡲࠫ┶") if status == bstack1l111l1_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ┷") else bstack1l111l1_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ┸")
                    data = name + bstack1l111l1_opy_ (u"ࠩࠣࡴࡦࡹࡳࡦࡦࠤࠫ┹") if status == bstack1l111l1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ┺") else name + bstack1l111l1_opy_ (u"ࠫࠥ࡬ࡡࡪ࡮ࡨࡨࠦࠦࠧ┻") + reason
                    bstack1lllll111l_opy_ = bstack11l111llll_opy_(bstack1l111l1_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧ┼"), bstack1l111l1_opy_ (u"࠭ࠧ┽"), bstack1l111l1_opy_ (u"ࠧࠨ┾"), bstack1l111l1_opy_ (u"ࠨࠩ┿"), level, data)
                    for driver in bstack1l11ll11_opy_:
                        if bstack1llll1ll1l_opy_ == driver.session_id:
                            driver.execute_script(bstack1lllll111l_opy_)
            except Exception as e:
                logger.debug(bstack1l111l1_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡣࡰࡰࡷࡩࡽࡺࠠࡧࡱࡵࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡵࡨࡷࡸ࡯࡯࡯࠼ࠣࡿࢂ࠭╀").format(str(e)))
    except Exception as e:
        logger.debug(bstack1l111l1_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡵࡣࡷࡩࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺࡥࡴࡶࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࢀࢃࠧ╁").format(str(e)))
    bstack111ll11ll_opy_(item, call, rep)
notset = Notset()
def bstack1l11ll111l_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1l1ll1lll1_opy_
    if str(name).lower() == bstack1l111l1_opy_ (u"ࠫࡩࡸࡩࡷࡧࡵࠫ╂"):
        return bstack1l111l1_opy_ (u"ࠧࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠦ╃")
    else:
        return bstack1l1ll1lll1_opy_(self, name, default, skip)
def bstack1l1ll1llll_opy_(self):
    global CONFIG
    global bstack1l1l111lll_opy_
    try:
        proxy = bstack11ll11l1l_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack1l111l1_opy_ (u"࠭࠮ࡱࡣࡦࠫ╄")):
                proxies = bstack1ll1ll11ll_opy_(proxy, bstack1lllllll11_opy_())
                if len(proxies) > 0:
                    protocol, bstack111l1l11l_opy_ = proxies.popitem()
                    if bstack1l111l1_opy_ (u"ࠢ࠻࠱࠲ࠦ╅") in bstack111l1l11l_opy_:
                        return bstack111l1l11l_opy_
                    else:
                        return bstack1l111l1_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤ╆") + bstack111l1l11l_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack1l111l1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡶࡲࡰࡺࡼࠤࡺࡸ࡬ࠡ࠼ࠣࡿࢂࠨ╇").format(str(e)))
    return bstack1l1l111lll_opy_(self)
def bstack111llllll_opy_():
    return (bstack1l111l1_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭╈") in CONFIG or bstack1l111l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ╉") in CONFIG) and bstack11l111l11l_opy_() and bstack111l1111l_opy_() >= version.parse(
        bstack1ll11111ll_opy_)
def bstack111ll1l1l1_opy_(self,
               executablePath=None,
               channel=None,
               args=None,
               ignoreDefaultArgs=None,
               handleSIGINT=None,
               handleSIGTERM=None,
               handleSIGHUP=None,
               timeout=None,
               env=None,
               headless=None,
               devtools=None,
               proxy=None,
               downloadsPath=None,
               slowMo=None,
               tracesDir=None,
               chromiumSandbox=None,
               firefoxUserPrefs=None
               ):
    global CONFIG
    global bstack1l1l1l1ll1_opy_
    global bstack1l1111l1l_opy_
    global bstack1lll11ll1l_opy_
    CONFIG[bstack1l111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ╊")] = str(bstack1lll11ll1l_opy_) + str(__version__)
    bstack1l1l11111l_opy_ = 0
    try:
        if bstack1l1111l1l_opy_ is True:
            bstack1l1l11111l_opy_ = int(os.environ.get(bstack1l111l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭╋")))
    except:
        bstack1l1l11111l_opy_ = 0
    CONFIG[bstack1l111l1_opy_ (u"ࠢࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨ╌")] = True
    bstack1l11ll1l_opy_ = bstack1l1ll111l_opy_(CONFIG, bstack1l1l11111l_opy_)
    logger.debug(bstack1111ll11_opy_.format(str(bstack1l11ll1l_opy_)))
    if CONFIG.get(bstack1l111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ╍")):
        bstack11l111l1ll_opy_(bstack1l11ll1l_opy_, bstack1lll111l1_opy_)
    if bstack1l111l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ╎") in CONFIG and bstack1l111l1_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ╏") in CONFIG[bstack1l111l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ═")][bstack1l1l11111l_opy_]:
        bstack1l1l1l1ll1_opy_ = CONFIG[bstack1l111l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ║")][bstack1l1l11111l_opy_][bstack1l111l1_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ╒")]
    import urllib
    import json
    if bstack1l111l1_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ╓") in CONFIG and str(CONFIG[bstack1l111l1_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ╔")]).lower() != bstack1l111l1_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨ╕"):
        bstack1l111l111l_opy_ = bstack1111ll1l_opy_()
        bstack1l11l111ll_opy_ = bstack1l111l111l_opy_ + urllib.parse.quote(json.dumps(bstack1l11ll1l_opy_))
    else:
        bstack1l11l111ll_opy_ = bstack1l111l1_opy_ (u"ࠪࡻࡸࡹ࠺࠰࠱ࡦࡨࡵ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡅࡣࡢࡲࡶࡁࠬ╖") + urllib.parse.quote(json.dumps(bstack1l11ll1l_opy_))
    browser = self.connect(bstack1l11l111ll_opy_)
    return browser
def bstack1l1ll1lll_opy_():
    global bstack11l1111111_opy_
    global bstack1lll11ll1l_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1111l1lll_opy_
        if not bstack1l1l1l11l1l_opy_():
            global bstack11ll11lll_opy_
            if not bstack11ll11lll_opy_:
                from bstack_utils.helper import bstack1111l1l11_opy_, bstack111ll1l111_opy_
                bstack11ll11lll_opy_ = bstack1111l1l11_opy_()
                bstack111ll1l111_opy_(bstack1lll11ll1l_opy_)
            BrowserType.connect = bstack1111l1lll_opy_
            return
        BrowserType.launch = bstack111ll1l1l1_opy_
        bstack11l1111111_opy_ = True
    except Exception as e:
        pass
def bstack1lll11lll1l1_opy_():
    global CONFIG
    global bstack11ll11l1_opy_
    global bstack1l1l1l11l1_opy_
    global bstack1lll111l1_opy_
    global bstack1l1111l1l_opy_
    global bstack111l111l1_opy_
    CONFIG = json.loads(os.environ.get(bstack1l111l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࠪ╗")))
    bstack11ll11l1_opy_ = eval(os.environ.get(bstack1l111l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭╘")))
    bstack1l1l1l11l1_opy_ = os.environ.get(bstack1l111l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡎࡕࡃࡡࡘࡖࡑ࠭╙"))
    bstack1ll11l1l1_opy_(CONFIG, bstack11ll11l1_opy_)
    bstack111l111l1_opy_ = bstack1ll1lll11_opy_.configure_logger(CONFIG, bstack111l111l1_opy_)
    if cli.bstack1llll11111_opy_():
        bstack11ll111ll_opy_.invoke(bstack1lll1ll1_opy_.CONNECT, bstack1ll1lll11l_opy_())
        cli_context.platform_index = int(os.environ.get(bstack1l111l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧ╚"), bstack1l111l1_opy_ (u"ࠨ࠲ࠪ╛")))
        cli.bstack1ll1ll11ll1_opy_(cli_context.platform_index)
        cli.bstack1lll11llll1_opy_(bstack1lllllll11_opy_(bstack1l1l1l11l1_opy_, CONFIG), cli_context.platform_index, bstack111ll1l1_opy_)
        cli.bstack1ll1l11lll1_opy_()
        logger.debug(bstack1l111l1_opy_ (u"ࠤࡆࡐࡎࠦࡩࡴࠢࡤࡧࡹ࡯ࡶࡦࠢࡩࡳࡷࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾ࠽ࠣ╜") + str(cli_context.platform_index) + bstack1l111l1_opy_ (u"ࠥࠦ╝"))
        return # skip all existing operations
    global bstack111lll1l1_opy_
    global bstack1l11111l1l_opy_
    global bstack1lll11ll11_opy_
    global bstack1lll11lll_opy_
    global bstack1l11lll1ll_opy_
    global bstack1111l11l1_opy_
    global bstack1l1l11l11_opy_
    global bstack1ll1l1lll_opy_
    global bstack1l1l111lll_opy_
    global bstack1l1ll1lll1_opy_
    global bstack1l1l11l111_opy_
    global bstack111ll11ll_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack111lll1l1_opy_ = webdriver.Remote.__init__
        bstack1l11111l1l_opy_ = WebDriver.quit
        bstack1l1l11l11_opy_ = WebDriver.close
        bstack1ll1l1lll_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack1l111l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧ╞") in CONFIG or bstack1l111l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ╟") in CONFIG) and bstack11l111l11l_opy_():
        if bstack111l1111l_opy_() < version.parse(bstack1ll11111ll_opy_):
            logger.error(bstack11l1l11l1l_opy_.format(bstack111l1111l_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                if hasattr(RemoteConnection, bstack1l111l1_opy_ (u"࠭࡟ࡨࡧࡷࡣࡵࡸ࡯ࡹࡻࡢࡹࡷࡲࠧ╠")) and callable(getattr(RemoteConnection, bstack1l111l1_opy_ (u"ࠧࡠࡩࡨࡸࡤࡶࡲࡰࡺࡼࡣࡺࡸ࡬ࠨ╡"))):
                    bstack1l1l111lll_opy_ = RemoteConnection._get_proxy_url
                else:
                    from selenium.webdriver.remote.client_config import ClientConfig
                    bstack1l1l111lll_opy_ = ClientConfig.get_proxy_url
            except Exception as e:
                logger.error(bstack11l1lll111_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack1l1ll1lll1_opy_ = Config.getoption
        from _pytest import runner
        bstack1l1l11l111_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warning(bstack1l111l1_opy_ (u"ࠣࠧࡶ࠾ࠥࠫࡳࠣ╢"), bstack1ll1lll1_opy_, str(e))
    try:
        from pytest_bdd import reporting
        bstack111ll11ll_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack1l111l1_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡱࠣࡶࡺࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࡵࠪ╣"))
    bstack1lll111l1_opy_ = CONFIG.get(bstack1l111l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ╤"), {}).get(bstack1l111l1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭╥"))
    bstack1l1111l1l_opy_ = True
    bstack1111l1111_opy_(bstack1ll111l1l1_opy_)
if (bstack111ll11l1ll_opy_()):
    bstack1lll11lll1l1_opy_()
@error_handler(class_method=False)
def bstack1lll11lll111_opy_(hook_name, event, bstack11lllllll1l_opy_=None):
    if hook_name not in [bstack1l111l1_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭╦"), bstack1l111l1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪ╧"), bstack1l111l1_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭╨"), bstack1l111l1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪ╩"), bstack1l111l1_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧ╪"), bstack1l111l1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫ╫"), bstack1l111l1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠪ╬"), bstack1l111l1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠧ╭")]:
        return
    node = store[bstack1l111l1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪ╮")]
    if hook_name in [bstack1l111l1_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭╯"), bstack1l111l1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪ╰")]:
        node = store[bstack1l111l1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡱࡴࡪࡵ࡭ࡧࡢ࡭ࡹ࡫࡭ࠨ╱")]
    elif hook_name in [bstack1l111l1_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠨ╲"), bstack1l111l1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠬ╳")]:
        node = store[bstack1l111l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡣ࡭ࡣࡶࡷࡤ࡯ࡴࡦ࡯ࠪ╴")]
    hook_type = bstack1llll1ll1ll1_opy_(hook_name)
    if event == bstack1l111l1_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ࠭╵"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll1lll1111_opy_[hook_type], bstack1lll11ll1l1_opy_.PRE, node, hook_name)
            return
        uuid = uuid4().__str__()
        bstack1111l11l1l_opy_ = {
            bstack1l111l1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ╶"): uuid,
            bstack1l111l1_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ╷"): bstack11llll1111_opy_(),
            bstack1l111l1_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ╸"): bstack1l111l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨ╹"),
            bstack1l111l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧ╺"): hook_type,
            bstack1l111l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠨ╻"): hook_name
        }
        store[bstack1l111l1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ╼")].append(uuid)
        bstack1lll11llll11_opy_ = node.nodeid
        if hook_type == bstack1l111l1_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬ╽"):
            if not _1111l1l11l_opy_.get(bstack1lll11llll11_opy_, None):
                _1111l1l11l_opy_[bstack1lll11llll11_opy_] = {bstack1l111l1_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ╾"): []}
            _1111l1l11l_opy_[bstack1lll11llll11_opy_][bstack1l111l1_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ╿")].append(bstack1111l11l1l_opy_[bstack1l111l1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ▀")])
        _1111l1l11l_opy_[bstack1lll11llll11_opy_ + bstack1l111l1_opy_ (u"ࠫ࠲࠭▁") + hook_name] = bstack1111l11l1l_opy_
        bstack1lll11ll1l11_opy_(node, bstack1111l11l1l_opy_, bstack1l111l1_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭▂"))
    elif event == bstack1l111l1_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬ▃"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll1lll1111_opy_[hook_type], bstack1lll11ll1l1_opy_.POST, node, None, bstack11lllllll1l_opy_)
            return
        bstack111l1l1l1l_opy_ = node.nodeid + bstack1l111l1_opy_ (u"ࠧ࠮ࠩ▄") + hook_name
        _1111l1l11l_opy_[bstack111l1l1l1l_opy_][bstack1l111l1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭▅")] = bstack11llll1111_opy_()
        bstack1lll11l1ll1l_opy_(_1111l1l11l_opy_[bstack111l1l1l1l_opy_][bstack1l111l1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ▆")])
        bstack1lll11ll1l11_opy_(node, _1111l1l11l_opy_[bstack111l1l1l1l_opy_], bstack1l111l1_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ▇"), bstack1lll1l11111l_opy_=bstack11lllllll1l_opy_)
def bstack1lll11ll1lll_opy_():
    global bstack1lll11l1l111_opy_
    if bstack1lllllll1_opy_():
        bstack1lll11l1l111_opy_ = bstack1l111l1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨ█")
    else:
        bstack1lll11l1l111_opy_ = bstack1l111l1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ▉")
@bstack1llll1lll1_opy_.bstack1lll1ll1111l_opy_
def bstack1lll11llll1l_opy_():
    bstack1lll11ll1lll_opy_()
    if cli.is_running():
        try:
            bstack111l11l1lll_opy_(bstack1lll11lll111_opy_)
        except Exception as e:
            logger.debug(bstack1l111l1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࡶࠤࡵࡧࡴࡤࡪ࠽ࠤࢀࢃࠢ▊").format(e))
        return
    if bstack11l111l11l_opy_():
        bstack1l1l1111_opy_ = Config.bstack1llll1ll11_opy_()
        bstack1l111l1_opy_ (u"ࠧࠨࠩࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡈࡲࡶࠥࡶࡰࡱࠢࡀࠤ࠶࠲ࠠ࡮ࡱࡧࡣࡪࡾࡥࡤࡷࡷࡩࠥ࡭ࡥࡵࡵࠣࡹࡸ࡫ࡤࠡࡨࡲࡶࠥࡧ࠱࠲ࡻࠣࡧࡴࡳ࡭ࡢࡰࡧࡷ࠲ࡽࡲࡢࡲࡳ࡭ࡳ࡭ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡌ࡯ࡳࠢࡳࡴࡵࠦ࠾ࠡ࠳࠯ࠤࡲࡵࡤࡠࡧࡻࡩࡨࡻࡴࡦࠢࡧࡳࡪࡹࠠ࡯ࡱࡷࠤࡷࡻ࡮ࠡࡤࡨࡧࡦࡻࡳࡦࠢ࡬ࡸࠥ࡯ࡳࠡࡲࡤࡸࡨ࡮ࡥࡥࠢ࡬ࡲࠥࡧࠠࡥ࡫ࡩࡪࡪࡸࡥ࡯ࡶࠣࡴࡷࡵࡣࡦࡵࡶࠤ࡮ࡪࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡚ࠥࡨࡶࡵࠣࡻࡪࠦ࡮ࡦࡧࡧࠤࡹࡵࠠࡶࡵࡨࠤࡘ࡫࡬ࡦࡰ࡬ࡹࡲࡖࡡࡵࡥ࡫ࠬࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡥࡨࡢࡰࡧࡰࡪࡸࠩࠡࡨࡲࡶࠥࡶࡰࡱࠢࡁࠤ࠶ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠨࠩࠪ▋")
        if bstack1l1l1111_opy_.get_property(bstack1l111l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠ࡯ࡲࡨࡤࡩࡡ࡭࡮ࡨࡨࠬ▌")):
            if CONFIG.get(bstack1l111l1_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ▍")) is not None and int(CONFIG[bstack1l111l1_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ▎")]) > 1:
                bstack1l1l1l1l1l_opy_(bstack11llll111_opy_)
            return
        bstack1l1l1l1l1l_opy_(bstack11llll111_opy_)
    try:
        bstack111l11l1lll_opy_(bstack1lll11lll111_opy_)
    except Exception as e:
        logger.debug(bstack1l111l1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡴࡵ࡫ࡴࠢࡳࡥࡹࡩࡨ࠻ࠢࡾࢁࠧ▏").format(e))
bstack1lll11llll1l_opy_()