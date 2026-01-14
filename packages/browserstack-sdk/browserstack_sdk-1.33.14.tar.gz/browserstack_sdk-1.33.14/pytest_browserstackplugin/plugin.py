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
import atexit
import datetime
import inspect
import logging
import signal
import threading
from uuid import uuid4
from bstack_utils.measure import bstack1lll1l111_opy_
from bstack_utils.percy_sdk import PercySDK
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack1l1l11ll1l_opy_, bstack1ll11l11ll_opy_, update, bstack11ll11111_opy_,
                                       bstack1ll111l11l_opy_, bstack1llll1ll_opy_, bstack11ll1l1l1_opy_, bstack1l11l111l1_opy_,
                                       bstack11l1ll1111_opy_, bstack1lll111l1_opy_, bstack11lll1l111_opy_,
                                       bstack11l11lllll_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack1ll11ll1l1_opy_)
from browserstack_sdk.bstack11l1ll11ll_opy_ import bstack1lll1l11_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack11lllll1_opy_
from bstack_utils.capture import bstack111l1l1l11_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack1llll11ll_opy_, bstack1l11lll1ll_opy_, bstack1l11lll1l1_opy_, \
    bstack11ll1ll11_opy_
from bstack_utils.helper import bstack1ll1ll11ll_opy_, bstack111l1l1lll1_opy_, bstack1111l11111_opy_, bstack111l111l_opy_, bstack1l1l11ll1ll_opy_, bstack11ll11ll1l_opy_, \
    bstack111ll111l11_opy_, \
    bstack11l1111llll_opy_, bstack1ll1l1ll11_opy_, bstack1ll1111l1_opy_, bstack111l1ll1lll_opy_, bstack1111ll11_opy_, Notset, \
    bstack1lllll111l_opy_, bstack111lll11ll1_opy_, bstack111l1ll11ll_opy_, Result, bstack111ll1ll111_opy_, bstack111l1llllll_opy_, error_handler, \
    bstack1l11ll1111_opy_, bstack111llll11_opy_, bstack11lll1l1l_opy_, bstack111lll1111l_opy_
from bstack_utils.bstack111l1l1111l_opy_ import bstack111l11lllll_opy_
from bstack_utils.messages import bstack1ll1111l_opy_, bstack1llll11lll_opy_, bstack1ll1111l1l_opy_, bstack1l1ll1lll1_opy_, bstack1lll111111_opy_, \
    bstack1l1111l11l_opy_, bstack11lll1lll1_opy_, bstack1l1111l1l1_opy_, bstack11l1l1ll1_opy_, bstack11lll1l1l1_opy_, \
    bstack11lllll11_opy_, bstack11llll1lll_opy_, bstack1llll111l1_opy_
from bstack_utils.proxy import bstack111111l1l_opy_, bstack111l11l11_opy_
from bstack_utils.bstack1ll1lll11_opy_ import bstack1llll1lll1l1_opy_, bstack1lllll111111_opy_, bstack1llll1llll1l_opy_, bstack1lllll111l11_opy_, \
    bstack1llll1lllll1_opy_, bstack1lllll11111l_opy_, bstack1llll1lll1ll_opy_, bstack11ll111ll1_opy_, bstack1lllll1111l1_opy_
from bstack_utils.bstack11l11ll11_opy_ import bstack111lll1l_opy_
from bstack_utils.bstack1ll1111l11_opy_ import bstack1lll11l1ll_opy_, bstack111ll1l1ll_opy_, bstack1l1111ll11_opy_, \
    bstack1l11l11l_opy_, bstack1ll1ll11l_opy_
from bstack_utils.bstack111l1l11l1_opy_ import bstack111l1l11ll_opy_
from bstack_utils.bstack111l1l1111_opy_ import bstack1l1l1lllll_opy_
import bstack_utils.accessibility as bstack1ll1l11lll_opy_
from bstack_utils.bstack111l1l1l1l_opy_ import bstack111ll1lll1_opy_
from bstack_utils.bstack1l111lll_opy_ import bstack1l111lll_opy_
from bstack_utils.bstack1lll11lll1_opy_ import bstack111lll111l_opy_
from browserstack_sdk.__init__ import bstack11l11ll11l_opy_
from browserstack_sdk.sdk_cli.bstack1lll11lllll_opy_ import bstack1ll11lll1ll_opy_
from browserstack_sdk.sdk_cli.bstack1llll1l1l_opy_ import bstack1llll1l1l_opy_, bstack1l11ll1l1_opy_, bstack11l1l111_opy_
from browserstack_sdk.sdk_cli.test_framework import bstack11llll1l111_opy_, bstack1ll11ll1lll_opy_, bstack1ll1l1l1ll1_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack1llll1l1l_opy_ import bstack1llll1l1l_opy_, bstack1l11ll1l1_opy_, bstack11l1l111_opy_
bstack11lllll111_opy_ = None
bstack111l1111_opy_ = None
bstack11ll1ll1ll_opy_ = None
bstack11ll11ll1_opy_ = None
bstack1ll1ll1l1l_opy_ = None
bstack111l111l1_opy_ = None
bstack1l1lllll1_opy_ = None
bstack1l1ll1111_opy_ = None
bstack1llll1l11_opy_ = None
bstack1ll1ll1l_opy_ = None
bstack1ll11ll1l_opy_ = None
bstack11l1l1llll_opy_ = None
bstack1lll1111_opy_ = None
bstack1ll1ll1l1_opy_ = bstack1l11l1l_opy_ (u"ࠬ࠭⌌")
CONFIG = {}
bstack1l11l1l111_opy_ = False
bstack1l1llll111_opy_ = bstack1l11l1l_opy_ (u"࠭ࠧ⌍")
bstack1llllll11_opy_ = bstack1l11l1l_opy_ (u"ࠧࠨ⌎")
bstack11ll1ll1l1_opy_ = False
bstack1ll1l11111_opy_ = []
bstack11ll1l1lll_opy_ = bstack1llll11ll_opy_
bstack1lll11l1lll1_opy_ = bstack1l11l1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ⌏")
bstack11l1l1ll1l_opy_ = {}
bstack1lll1l11l_opy_ = None
bstack1l111111_opy_ = False
logger = bstack11lllll1_opy_.get_logger(__name__, bstack11ll1l1lll_opy_)
store = {
    bstack1l11l1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭⌐"): []
}
bstack1lll1l1111ll_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_1111ll1111_opy_ = {}
current_test_uuid = None
cli_context = bstack11llll1l111_opy_(
    test_framework_name=bstack11l111111_opy_[bstack1l11l1l_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖ࠰ࡆࡉࡊࠧ⌑")] if bstack1111ll11_opy_() else bstack11l111111_opy_[bstack1l11l1l_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࠫ⌒")],
    test_framework_version=pytest.__version__,
    platform_index=-1,
)
def bstack11llllll1l_opy_(page, bstack1ll11lll1_opy_):
    try:
        page.evaluate(bstack1l11l1l_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨ⌓"),
                      bstack1l11l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠪ⌔") + json.dumps(
                          bstack1ll11lll1_opy_) + bstack1l11l1l_opy_ (u"ࠢࡾࡿࠥ⌕"))
    except Exception as e:
        print(bstack1l11l1l_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣࡿࢂࠨ⌖"), e)
def bstack11llll11l1_opy_(page, message, level):
    try:
        page.evaluate(bstack1l11l1l_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥ⌗"), bstack1l11l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨ⌘") + json.dumps(
            message) + bstack1l11l1l_opy_ (u"ࠫ࠱ࠨ࡬ࡦࡸࡨࡰࠧࡀࠧ⌙") + json.dumps(level) + bstack1l11l1l_opy_ (u"ࠬࢃࡽࠨ⌚"))
    except Exception as e:
        print(bstack1l11l1l_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡤࡲࡳࡵࡴࡢࡶ࡬ࡳࡳࠦࡻࡾࠤ⌛"), e)
def pytest_configure(config):
    global bstack1l1llll111_opy_
    global CONFIG
    bstack11llllll_opy_ = Config.bstack1llll1111_opy_()
    config.args = bstack1l1l1lllll_opy_.bstack1lll1l11llll_opy_(config.args)
    bstack11llllll_opy_.bstack1ll111ll1l_opy_(bstack11lll1l1l_opy_(config.getoption(bstack1l11l1l_opy_ (u"ࠧࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫ⌜"))))
    try:
        bstack11lllll1_opy_.bstack1111llll1ll_opy_(config.inipath, config.rootpath)
    except:
        pass
    if cli.is_running():
        bstack1llll1l1l_opy_.invoke(bstack1l11ll1l1_opy_.CONNECT, bstack11l1l111_opy_())
        cli_context.platform_index = int(os.environ.get(bstack1l11l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ⌝"), bstack1l11l1l_opy_ (u"ࠩ࠳ࠫ⌞")))
        config = json.loads(os.environ.get(bstack1l11l1l_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࠤ⌟"), bstack1l11l1l_opy_ (u"ࠦࢀࢃࠢ⌠")))
        cli.bstack1ll11lll111_opy_(bstack1ll1111l1_opy_(bstack1l1llll111_opy_, CONFIG), cli_context.platform_index, bstack11ll11111_opy_)
    if cli.bstack1lll11l111l_opy_(bstack1ll11lll1ll_opy_):
        cli.bstack1ll11ll1l11_opy_()
        logger.debug(bstack1l11l1l_opy_ (u"ࠧࡉࡌࡊࠢ࡬ࡷࠥࡧࡣࡵ࡫ࡹࡩࠥ࡬࡯ࡳࠢࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࡀࠦ⌡") + str(cli_context.platform_index) + bstack1l11l1l_opy_ (u"ࠨࠢ⌢"))
        cli.test_framework.track_event(cli_context, bstack1ll11ll1lll_opy_.BEFORE_ALL, bstack1ll1l1l1ll1_opy_.PRE, config)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    when = getattr(call, bstack1l11l1l_opy_ (u"ࠢࡸࡪࡨࡲࠧ⌣"), None)
    if cli.is_running() and when == bstack1l11l1l_opy_ (u"ࠣࡥࡤࡰࡱࠨ⌤"):
        cli.test_framework.track_event(cli_context, bstack1ll11ll1lll_opy_.LOG_REPORT, bstack1ll1l1l1ll1_opy_.PRE, item, call)
    outcome = yield
    if when == bstack1l11l1l_opy_ (u"ࠤࡦࡥࡱࡲࠢ⌥"):
        report = outcome.get_result()
        passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l11l1l_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧ⌦")))
        if not passed:
            config = json.loads(os.environ.get(bstack1l11l1l_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࠥ⌧"), bstack1l11l1l_opy_ (u"ࠧࢁࡽࠣ⌨")))
            if bstack111lll111l_opy_.bstack1l11lll11l_opy_(config):
                bstack111111l111l_opy_ = bstack111lll111l_opy_.bstack1l1l1ll1ll_opy_(config)
                if item.execution_count > bstack111111l111l_opy_:
                    print(bstack1l11l1l_opy_ (u"࠭ࡔࡦࡵࡷࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡦ࡬ࡴࡦࡴࠣࡶࡪࡺࡲࡪࡧࡶ࠾ࠥ࠭〈"), report.nodeid, os.environ.get(bstack1l11l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ〉")))
                    bstack111lll111l_opy_.bstack1111l11l111_opy_(report.nodeid)
            else:
                print(bstack1l11l1l_opy_ (u"ࠨࡖࡨࡷࡹࠦࡦࡢ࡫࡯ࡩࡩࡀࠠࠨ⌫"), report.nodeid, os.environ.get(bstack1l11l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ⌬")))
                bstack111lll111l_opy_.bstack1111l11l111_opy_(report.nodeid)
        else:
            print(bstack1l11l1l_opy_ (u"ࠪࡘࡪࡹࡴࠡࡲࡤࡷࡸ࡫ࡤ࠻ࠢࠪ⌭"), report.nodeid, os.environ.get(bstack1l11l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ⌮")))
    if cli.is_running():
        if when == bstack1l11l1l_opy_ (u"ࠧࡹࡥࡵࡷࡳࠦ⌯"):
            cli.test_framework.track_event(cli_context, bstack1ll11ll1lll_opy_.BEFORE_EACH, bstack1ll1l1l1ll1_opy_.POST, item, call, outcome)
        elif when == bstack1l11l1l_opy_ (u"ࠨࡣࡢ࡮࡯ࠦ⌰"):
            cli.test_framework.track_event(cli_context, bstack1ll11ll1lll_opy_.LOG_REPORT, bstack1ll1l1l1ll1_opy_.POST, item, call, outcome)
        elif when == bstack1l11l1l_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤ⌱"):
            cli.test_framework.track_event(cli_context, bstack1ll11ll1lll_opy_.AFTER_EACH, bstack1ll1l1l1ll1_opy_.POST, item, call, outcome)
        return # skip all existing operations
    skipSessionName = item.config.getoption(bstack1l11l1l_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ⌲"))
    plugins = item.config.getoption(bstack1l11l1l_opy_ (u"ࠤࡳࡰࡺ࡭ࡩ࡯ࡵࠥ⌳"))
    report = outcome.get_result()
    os.environ[bstack1l11l1l_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖࡢࡘࡊ࡙ࡔࡠࡐࡄࡑࡊ࠭⌴")] = report.nodeid
    bstack1lll1l11111l_opy_(item, call, report)
    if bstack1l11l1l_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡳࡰࡺ࡭ࡩ࡯ࠤ⌵") not in plugins or bstack1111ll11_opy_():
        return
    summary = []
    driver = getattr(item, bstack1l11l1l_opy_ (u"ࠧࡥࡤࡳ࡫ࡹࡩࡷࠨ⌶"), None)
    page = getattr(item, bstack1l11l1l_opy_ (u"ࠨ࡟ࡱࡣࡪࡩࠧ⌷"), None)
    try:
        if (driver == None or driver.session_id == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None or cli.is_running()):
        bstack1lll11lll11l_opy_(item, report, summary, skipSessionName)
    if (page is not None):
        bstack1lll1l111lll_opy_(item, report, summary, skipSessionName)
def bstack1lll11lll11l_opy_(item, report, summary, skipSessionName):
    if report.when == bstack1l11l1l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭⌸") and report.skipped:
        bstack1lllll1111l1_opy_(report)
    if report.when in [bstack1l11l1l_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢ⌹"), bstack1l11l1l_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦ⌺")]:
        return
    if not bstack1l1l11ll1ll_opy_():
        return
    try:
        if ((str(skipSessionName).lower() != bstack1l11l1l_opy_ (u"ࠪࡸࡷࡻࡥࠨ⌻")) and (not cli.is_running())) and item._driver.session_id:
            item._driver.execute_script(
                bstack1l11l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩ⌼") + json.dumps(
                    report.nodeid) + bstack1l11l1l_opy_ (u"ࠬࢃࡽࠨ⌽"))
        os.environ[bstack1l11l1l_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙ࡥࡔࡆࡕࡗࡣࡓࡇࡍࡆࠩ⌾")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack1l11l1l_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦ࠼ࠣࡿ࠵ࢃࠢ⌿").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l11l1l_opy_ (u"ࠣࡹࡤࡷࡽ࡬ࡡࡪ࡮ࠥ⍀")))
    bstack1llll1ll11_opy_ = bstack1l11l1l_opy_ (u"ࠤࠥ⍁")
    bstack1lllll1111l1_opy_(report)
    if not passed:
        try:
            bstack1llll1ll11_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack1l11l1l_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤ࡫ࡧࡩ࡭ࡷࡵࡩࠥࡸࡥࡢࡵࡲࡲ࠿ࠦࡻ࠱ࡿࠥ⍂").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1llll1ll11_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack1l11l1l_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨ⍃")))
        bstack1llll1ll11_opy_ = bstack1l11l1l_opy_ (u"ࠧࠨ⍄")
        if not passed:
            try:
                bstack1llll1ll11_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1l11l1l_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡧࡣ࡬ࡰࡺࡸࡥࠡࡴࡨࡥࡸࡵ࡮࠻ࠢࡾ࠴ࢂࠨ⍅").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1llll1ll11_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack1l11l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣ࠮ࠣࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡨࡦࡺࡡࠣ࠼ࠣࠫ⍆")
                    + json.dumps(bstack1l11l1l_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠢࠤ⍇"))
                    + bstack1l11l1l_opy_ (u"ࠤ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࠧ⍈")
                )
            else:
                item._driver.execute_script(
                    bstack1l11l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧ࠲ࠠ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡥࡣࡷࡥࠧࡀࠠࠨ⍉")
                    + json.dumps(str(bstack1llll1ll11_opy_))
                    + bstack1l11l1l_opy_ (u"ࠦࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࠢ⍊")
                )
        except Exception as e:
            summary.append(bstack1l11l1l_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡥࡳࡴ࡯ࡵࡣࡷࡩ࠿ࠦࡻ࠱ࡿࠥ⍋").format(e))
def bstack1lll11llllll_opy_(test_name, error_message):
    try:
        bstack1lll1l111ll1_opy_ = []
        bstack1l11l1111_opy_ = os.environ.get(bstack1l11l1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭⍌"), bstack1l11l1l_opy_ (u"ࠧ࠱ࠩ⍍"))
        bstack1lll1ll1l_opy_ = {bstack1l11l1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭⍎"): test_name, bstack1l11l1l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ⍏"): error_message, bstack1l11l1l_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩ⍐"): bstack1l11l1111_opy_}
        bstack1lll11l1llll_opy_ = os.path.join(tempfile.gettempdir(), bstack1l11l1l_opy_ (u"ࠫࡵࡽ࡟ࡱࡻࡷࡩࡸࡺ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩ⍑"))
        if os.path.exists(bstack1lll11l1llll_opy_):
            with open(bstack1lll11l1llll_opy_) as f:
                bstack1lll1l111ll1_opy_ = json.load(f)
        bstack1lll1l111ll1_opy_.append(bstack1lll1ll1l_opy_)
        with open(bstack1lll11l1llll_opy_, bstack1l11l1l_opy_ (u"ࠬࡽࠧ⍒")) as f:
            json.dump(bstack1lll1l111ll1_opy_, f)
    except Exception as e:
        logger.debug(bstack1l11l1l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡨࡶࡸ࡯ࡳࡵ࡫ࡱ࡫ࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡳࡽࡹ࡫ࡳࡵࠢࡨࡶࡷࡵࡲࡴ࠼ࠣࠫ⍓") + str(e))
def bstack1lll1l111lll_opy_(item, report, summary, skipSessionName):
    if report.when in [bstack1l11l1l_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨ⍔"), bstack1l11l1l_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥ⍕")]:
        return
    if (str(skipSessionName).lower() != bstack1l11l1l_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ⍖")):
        bstack11llllll1l_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l11l1l_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧ⍗")))
    bstack1llll1ll11_opy_ = bstack1l11l1l_opy_ (u"ࠦࠧ⍘")
    bstack1lllll1111l1_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1llll1ll11_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1l11l1l_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫ࠠࡳࡧࡤࡷࡴࡴ࠺ࠡࡽ࠳ࢁࠧ⍙").format(e)
                )
        try:
            if passed:
                bstack1ll1ll11l_opy_(getattr(item, bstack1l11l1l_opy_ (u"࠭࡟ࡱࡣࡪࡩࠬ⍚"), None), bstack1l11l1l_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢ⍛"))
            else:
                error_message = bstack1l11l1l_opy_ (u"ࠨࠩ⍜")
                if bstack1llll1ll11_opy_:
                    bstack11llll11l1_opy_(item._page, str(bstack1llll1ll11_opy_), bstack1l11l1l_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣ⍝"))
                    bstack1ll1ll11l_opy_(getattr(item, bstack1l11l1l_opy_ (u"ࠪࡣࡵࡧࡧࡦࠩ⍞"), None), bstack1l11l1l_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ⍟"), str(bstack1llll1ll11_opy_))
                    error_message = str(bstack1llll1ll11_opy_)
                else:
                    bstack1ll1ll11l_opy_(getattr(item, bstack1l11l1l_opy_ (u"ࠬࡥࡰࡢࡩࡨࠫ⍠"), None), bstack1l11l1l_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ⍡"))
                bstack1lll11llllll_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack1l11l1l_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡻࡰࡥࡣࡷࡩࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࡀࠠࡼ࠲ࢀࠦ⍢").format(e))
def pytest_addoption(parser):
    parser.addoption(bstack1l11l1l_opy_ (u"ࠣ࠯࠰ࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ⍣"), default=bstack1l11l1l_opy_ (u"ࠤࡉࡥࡱࡹࡥࠣ⍤"), help=bstack1l11l1l_opy_ (u"ࠥࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡨࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠤ⍥"))
    parser.addoption(bstack1l11l1l_opy_ (u"ࠦ࠲࠳ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥ⍦"), default=bstack1l11l1l_opy_ (u"ࠧࡌࡡ࡭ࡵࡨࠦ⍧"), help=bstack1l11l1l_opy_ (u"ࠨࡁࡶࡶࡲࡱࡦࡺࡩࡤࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠧ⍨"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack1l11l1l_opy_ (u"ࠢ࠮࠯ࡧࡶ࡮ࡼࡥࡳࠤ⍩"), action=bstack1l11l1l_opy_ (u"ࠣࡵࡷࡳࡷ࡫ࠢ⍪"), default=bstack1l11l1l_opy_ (u"ࠤࡦ࡬ࡷࡵ࡭ࡦࠤ⍫"),
                         help=bstack1l11l1l_opy_ (u"ࠥࡈࡷ࡯ࡶࡦࡴࠣࡸࡴࠦࡲࡶࡰࠣࡸࡪࡹࡴࡴࠤ⍬"))
def bstack111ll111l1_opy_(log):
    if not (log[bstack1l11l1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ⍭")] and log[bstack1l11l1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭⍮")].strip()):
        return
    active = bstack111ll1111l_opy_()
    log = {
        bstack1l11l1l_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ⍯"): log[bstack1l11l1l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭⍰")],
        bstack1l11l1l_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ⍱"): bstack1111l11111_opy_().isoformat() + bstack1l11l1l_opy_ (u"ࠩ࡝ࠫ⍲"),
        bstack1l11l1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ⍳"): log[bstack1l11l1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ⍴")],
    }
    if active:
        if active[bstack1l11l1l_opy_ (u"ࠬࡺࡹࡱࡧࠪ⍵")] == bstack1l11l1l_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ⍶"):
            log[bstack1l11l1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⍷")] = active[bstack1l11l1l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⍸")]
        elif active[bstack1l11l1l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ⍹")] == bstack1l11l1l_opy_ (u"ࠪࡸࡪࡹࡴࠨ⍺"):
            log[bstack1l11l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⍻")] = active[bstack1l11l1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⍼")]
    bstack111ll1lll1_opy_.bstack1l1111l11_opy_([log])
def bstack111ll1111l_opy_():
    if len(store[bstack1l11l1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ⍽")]) > 0 and store[bstack1l11l1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ⍾")][-1]:
        return {
            bstack1l11l1l_opy_ (u"ࠨࡶࡼࡴࡪ࠭⍿"): bstack1l11l1l_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ⎀"),
            bstack1l11l1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⎁"): store[bstack1l11l1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ⎂")][-1]
        }
    if store.get(bstack1l11l1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ⎃"), None):
        return {
            bstack1l11l1l_opy_ (u"࠭ࡴࡺࡲࡨࠫ⎄"): bstack1l11l1l_opy_ (u"ࠧࡵࡧࡶࡸࠬ⎅"),
            bstack1l11l1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⎆"): store[bstack1l11l1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭⎇")]
        }
    return None
def pytest_runtest_logstart(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll11ll1lll_opy_.INIT_TEST, bstack1ll1l1l1ll1_opy_.PRE, nodeid, location)
def pytest_runtest_logfinish(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll11ll1lll_opy_.INIT_TEST, bstack1ll1l1l1ll1_opy_.POST, nodeid, location)
def pytest_runtest_call(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll11ll1lll_opy_.TEST, bstack1ll1l1l1ll1_opy_.PRE, item)
        return
    try:
        global CONFIG
        item._1lll11ll1l11_opy_ = True
        bstack1111l11l_opy_ = bstack1ll1l11lll_opy_.bstack1l1l11llll_opy_(bstack11l1111llll_opy_(item.own_markers))
        if not cli.bstack1lll11l111l_opy_(bstack1ll11lll1ll_opy_):
            item._a11y_test_case = bstack1111l11l_opy_
            if bstack1ll1ll11ll_opy_(threading.current_thread(), bstack1l11l1l_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ⎈"), None):
                driver = getattr(item, bstack1l11l1l_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬ⎉"), None)
                item._a11y_started = bstack1ll1l11lll_opy_.bstack1lllll1ll_opy_(driver, bstack1111l11l_opy_)
        if not bstack111ll1lll1_opy_.on() or bstack1lll11l1lll1_opy_ != bstack1l11l1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ⎊"):
            return
        global current_test_uuid #, bstack111l1l1lll_opy_
        bstack1111l1ll11_opy_ = {
            bstack1l11l1l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⎋"): uuid4().__str__(),
            bstack1l11l1l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ⎌"): bstack1111l11111_opy_().isoformat() + bstack1l11l1l_opy_ (u"ࠨ࡜ࠪ⎍")
        }
        current_test_uuid = bstack1111l1ll11_opy_[bstack1l11l1l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ⎎")]
        store[bstack1l11l1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ⎏")] = bstack1111l1ll11_opy_[bstack1l11l1l_opy_ (u"ࠫࡺࡻࡩࡥࠩ⎐")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _1111ll1111_opy_[item.nodeid] = {**_1111ll1111_opy_[item.nodeid], **bstack1111l1ll11_opy_}
        bstack1lll11ll1l1l_opy_(item, _1111ll1111_opy_[item.nodeid], bstack1l11l1l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭⎑"))
    except Exception as err:
        print(bstack1l11l1l_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡸࡵ࡯ࡶࡨࡷࡹࡥࡣࡢ࡮࡯࠾ࠥࢁࡽࠨ⎒"), str(err))
def pytest_runtest_setup(item):
    store[bstack1l11l1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫ⎓")] = item
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll11ll1lll_opy_.BEFORE_EACH, bstack1ll1l1l1ll1_opy_.PRE, item, bstack1l11l1l_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ⎔"))
    if bstack111lll111l_opy_.bstack11111lll1ll_opy_():
            bstack1lll11llll11_opy_ = bstack1l11l1l_opy_ (u"ࠤࡖ࡯࡮ࡶࡰࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡤࡷࠥࡺࡨࡦࠢࡤࡦࡴࡸࡴࠡࡤࡸ࡭ࡱࡪࠠࡧ࡫࡯ࡩࠥ࡫ࡸࡪࡵࡷࡷ࠳ࠨ⎕")
            logger.error(bstack1lll11llll11_opy_)
            bstack1111l1ll11_opy_ = {
                bstack1l11l1l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ⎖"): uuid4().__str__(),
                bstack1l11l1l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ⎗"): bstack1111l11111_opy_().isoformat() + bstack1l11l1l_opy_ (u"ࠬࡠࠧ⎘"),
                bstack1l11l1l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⎙"): bstack1111l11111_opy_().isoformat() + bstack1l11l1l_opy_ (u"࡛ࠧࠩ⎚"),
                bstack1l11l1l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ⎛"): bstack1l11l1l_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ⎜"),
                bstack1l11l1l_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪ⎝"): bstack1lll11llll11_opy_,
                bstack1l11l1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ⎞"): [],
                bstack1l11l1l_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧ⎟"): []
            }
            bstack1lll11ll1l1l_opy_(item, bstack1111l1ll11_opy_, bstack1l11l1l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧ⎠"))
            pytest.skip(bstack1lll11llll11_opy_)
            return # skip all existing operations
    global bstack1lll1l1111ll_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack111l1ll1lll_opy_():
        atexit.register(bstack1lllll111_opy_)
        if not bstack1lll1l1111ll_opy_:
            try:
                bstack1lll11ll1lll_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack111lll1111l_opy_():
                    bstack1lll11ll1lll_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1lll11ll1lll_opy_:
                    signal.signal(s, bstack1lll1l111l11_opy_)
                bstack1lll1l1111ll_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack1l11l1l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡵࡩ࡬࡯ࡳࡵࡧࡵࠤࡸ࡯ࡧ࡯ࡣ࡯ࠤ࡭ࡧ࡮ࡥ࡮ࡨࡶࡸࡀࠠࠣ⎡") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack1llll1lll1l1_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack1l11l1l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ⎢")
    try:
        if not bstack111ll1lll1_opy_.on():
            return
        uuid = uuid4().__str__()
        bstack1111l1ll11_opy_ = {
            bstack1l11l1l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ⎣"): uuid,
            bstack1l11l1l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ⎤"): bstack1111l11111_opy_().isoformat() + bstack1l11l1l_opy_ (u"ࠫ࡟࠭⎥"),
            bstack1l11l1l_opy_ (u"ࠬࡺࡹࡱࡧࠪ⎦"): bstack1l11l1l_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ⎧"),
            bstack1l11l1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪ⎨"): bstack1l11l1l_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭⎩"),
            bstack1l11l1l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬ⎪"): bstack1l11l1l_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ⎫")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack1l11l1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨ⎬")] = item
        store[bstack1l11l1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ⎭")] = [uuid]
        if not _1111ll1111_opy_.get(item.nodeid, None):
            _1111ll1111_opy_[item.nodeid] = {bstack1l11l1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ⎮"): [], bstack1l11l1l_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩ⎯"): []}
        _1111ll1111_opy_[item.nodeid][bstack1l11l1l_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ⎰")].append(bstack1111l1ll11_opy_[bstack1l11l1l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ⎱")])
        _1111ll1111_opy_[item.nodeid + bstack1l11l1l_opy_ (u"ࠪ࠱ࡸ࡫ࡴࡶࡲࠪ⎲")] = bstack1111l1ll11_opy_
        bstack1lll11lll1l1_opy_(item, bstack1111l1ll11_opy_, bstack1l11l1l_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ⎳"))
    except Exception as err:
        print(bstack1l11l1l_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡷࡻ࡮ࡵࡧࡶࡸࡤࡹࡥࡵࡷࡳ࠾ࠥࢁࡽࠨ⎴"), str(err))
def pytest_runtest_teardown(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll11ll1lll_opy_.TEST, bstack1ll1l1l1ll1_opy_.POST, item)
        cli.test_framework.track_event(cli_context, bstack1ll11ll1lll_opy_.AFTER_EACH, bstack1ll1l1l1ll1_opy_.PRE, item, bstack1l11l1l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨ⎵"))
        return # skip all existing operations
    try:
        global bstack11l1l1ll1l_opy_
        bstack1l11l1111_opy_ = 0
        if bstack11ll1ll1l1_opy_ is True:
            bstack1l11l1111_opy_ = int(os.environ.get(bstack1l11l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧ⎶")))
        if bstack1l1l11lll_opy_.bstack111ll11ll_opy_() == bstack1l11l1l_opy_ (u"ࠣࡶࡵࡹࡪࠨ⎷"):
            if bstack1l1l11lll_opy_.bstack1ll111l1l_opy_() == bstack1l11l1l_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦ⎸"):
                bstack1lll1l11l111_opy_ = bstack1ll1ll11ll_opy_(threading.current_thread(), bstack1l11l1l_opy_ (u"ࠪࡴࡪࡸࡣࡺࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭⎹"), None)
                bstack1ll1111ll1_opy_ = bstack1lll1l11l111_opy_ + bstack1l11l1l_opy_ (u"ࠦ࠲ࡺࡥࡴࡶࡦࡥࡸ࡫ࠢ⎺")
                driver = getattr(item, bstack1l11l1l_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭⎻"), None)
                bstack111lll1ll_opy_ = getattr(item, bstack1l11l1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ⎼"), None)
                bstack11l11lll11_opy_ = getattr(item, bstack1l11l1l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⎽"), None)
                PercySDK.screenshot(driver, bstack1ll1111ll1_opy_, bstack111lll1ll_opy_=bstack111lll1ll_opy_, bstack11l11lll11_opy_=bstack11l11lll11_opy_, bstack11l1lllll1_opy_=bstack1l11l1111_opy_)
        if not cli.bstack1lll11l111l_opy_(bstack1ll11lll1ll_opy_):
            if getattr(item, bstack1l11l1l_opy_ (u"ࠨࡡࡤ࠵࠶ࡿ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠨ⎾"), False):
                bstack1lll1l11_opy_.bstack1ll1l11ll1_opy_(getattr(item, bstack1l11l1l_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪ⎿"), None), bstack11l1l1ll1l_opy_, logger, item)
        if not bstack111ll1lll1_opy_.on():
            return
        bstack1111l1ll11_opy_ = {
            bstack1l11l1l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ⏀"): uuid4().__str__(),
            bstack1l11l1l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ⏁"): bstack1111l11111_opy_().isoformat() + bstack1l11l1l_opy_ (u"ࠬࡠࠧ⏂"),
            bstack1l11l1l_opy_ (u"࠭ࡴࡺࡲࡨࠫ⏃"): bstack1l11l1l_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ⏄"),
            bstack1l11l1l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫ⏅"): bstack1l11l1l_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍ࠭⏆"),
            bstack1l11l1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭⏇"): bstack1l11l1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭⏈")
        }
        _1111ll1111_opy_[item.nodeid + bstack1l11l1l_opy_ (u"ࠬ࠳ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨ⏉")] = bstack1111l1ll11_opy_
        bstack1lll11lll1l1_opy_(item, bstack1111l1ll11_opy_, bstack1l11l1l_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ⏊"))
    except Exception as err:
        print(bstack1l11l1l_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡲࡶࡰࡷࡩࡸࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯࠼ࠣࡿࢂ࠭⏋"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if bstack1lllll111l11_opy_(fixturedef.argname):
        store[bstack1l11l1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡰࡳࡩࡻ࡬ࡦࡡ࡬ࡸࡪࡳࠧ⏌")] = request.node
    elif bstack1llll1lllll1_opy_(fixturedef.argname):
        store[bstack1l11l1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡧࡱࡧࡳࡴࡡ࡬ࡸࡪࡳࠧ⏍")] = request.node
    if not bstack111ll1lll1_opy_.on():
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll11ll1lll_opy_.SETUP_FIXTURE, bstack1ll1l1l1ll1_opy_.PRE, fixturedef, request)
        outcome = yield
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll11ll1lll_opy_.SETUP_FIXTURE, bstack1ll1l1l1ll1_opy_.POST, fixturedef, request, outcome)
        return # skip all existing operations
    start_time = datetime.datetime.now()
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll11ll1lll_opy_.SETUP_FIXTURE, bstack1ll1l1l1ll1_opy_.PRE, fixturedef, request)
    outcome = yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll11ll1lll_opy_.SETUP_FIXTURE, bstack1ll1l1l1ll1_opy_.POST, fixturedef, request, outcome)
        return # skip all existing operations
    try:
        fixture = {
            bstack1l11l1l_opy_ (u"ࠪࡲࡦࡳࡥࠨ⏎"): fixturedef.argname,
            bstack1l11l1l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ⏏"): bstack111ll111l11_opy_(outcome),
            bstack1l11l1l_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧ⏐"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack1l11l1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪ⏑")]
        if not _1111ll1111_opy_.get(current_test_item.nodeid, None):
            _1111ll1111_opy_[current_test_item.nodeid] = {bstack1l11l1l_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩ⏒"): []}
        _1111ll1111_opy_[current_test_item.nodeid][bstack1l11l1l_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪ⏓")].append(fixture)
    except Exception as err:
        logger.debug(bstack1l11l1l_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡡࡶࡩࡹࡻࡰ࠻ࠢࡾࢁࠬ⏔"), str(err))
if bstack1111ll11_opy_() and bstack111ll1lll1_opy_.on():
    def pytest_bdd_before_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll11ll1lll_opy_.STEP, bstack1ll1l1l1ll1_opy_.PRE, request, step)
            return
        try:
            _1111ll1111_opy_[request.node.nodeid][bstack1l11l1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭⏕")].bstack1l1lll111_opy_(id(step))
        except Exception as err:
            print(bstack1l11l1l_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴ࠿ࠦࡻࡾࠩ⏖"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll11ll1lll_opy_.STEP, bstack1ll1l1l1ll1_opy_.POST, request, step, exception)
            return
        try:
            _1111ll1111_opy_[request.node.nodeid][bstack1l11l1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ⏗")].bstack111l1l111l_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack1l11l1l_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡶࡸࡪࡶ࡟ࡦࡴࡵࡳࡷࡀࠠࡼࡿࠪ⏘"), str(err))
    def pytest_bdd_after_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll11ll1lll_opy_.STEP, bstack1ll1l1l1ll1_opy_.POST, request, step)
            return
        try:
            bstack111l1l11l1_opy_: bstack111l1l11ll_opy_ = _1111ll1111_opy_[request.node.nodeid][bstack1l11l1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ⏙")]
            bstack111l1l11l1_opy_.bstack111l1l111l_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack1l11l1l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡸࡺࡥࡱࡡࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠬ⏚"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1lll11l1lll1_opy_
        try:
            if not bstack111ll1lll1_opy_.on() or bstack1lll11l1lll1_opy_ != bstack1l11l1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭⏛"):
                return
            if cli.is_running():
                cli.test_framework.track_event(cli_context, bstack1ll11ll1lll_opy_.TEST, bstack1ll1l1l1ll1_opy_.PRE, request, feature, scenario)
                return
            driver = bstack1ll1ll11ll_opy_(threading.current_thread(), bstack1l11l1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩ⏜"), None)
            if not _1111ll1111_opy_.get(request.node.nodeid, None):
                _1111ll1111_opy_[request.node.nodeid] = {}
            bstack111l1l11l1_opy_ = bstack111l1l11ll_opy_.bstack1llll111ll1l_opy_(
                scenario, feature, request.node,
                name=bstack1lllll11111l_opy_(request.node, scenario),
                started_at=bstack11ll11ll1l_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack1l11l1l_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷ࠱ࡨࡻࡣࡶ࡯ࡥࡩࡷ࠭⏝"),
                tags=bstack1llll1lll1ll_opy_(feature, scenario),
                bstack111ll11lll_opy_=bstack111ll1lll1_opy_.bstack111l1ll1ll_opy_(driver) if driver and driver.session_id else {}
            )
            _1111ll1111_opy_[request.node.nodeid][bstack1l11l1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ⏞")] = bstack111l1l11l1_opy_
            bstack1lll1l11l11l_opy_(bstack111l1l11l1_opy_.uuid)
            bstack111ll1lll1_opy_.bstack111ll11l11_opy_(bstack1l11l1l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ⏟"), bstack111l1l11l1_opy_)
        except Exception as err:
            print(bstack1l11l1l_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳ࠿ࠦࡻࡾࠩ⏠"), str(err))
def bstack1lll11lll1ll_opy_(bstack111l1ll111_opy_):
    if bstack111l1ll111_opy_ in store[bstack1l11l1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ⏡")]:
        store[bstack1l11l1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭⏢")].remove(bstack111l1ll111_opy_)
def bstack1lll1l11l11l_opy_(test_uuid):
    store[bstack1l11l1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ⏣")] = test_uuid
    threading.current_thread().current_test_uuid = test_uuid
@bstack111ll1lll1_opy_.bstack1lll1lll1lll_opy_
def bstack1lll1l11111l_opy_(item, call, report):
    logger.debug(bstack1l11l1l_opy_ (u"ࠫ࡭ࡧ࡮ࡥ࡮ࡨࡣࡴ࠷࠱ࡺࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡀࠠࡴࡶࡤࡶࡹ࠭⏤"))
    global bstack1lll11l1lll1_opy_
    bstack11111lll1_opy_ = bstack11ll11ll1l_opy_()
    if hasattr(report, bstack1l11l1l_opy_ (u"ࠬࡹࡴࡰࡲࠪ⏥")):
        bstack11111lll1_opy_ = bstack111ll1ll111_opy_(report.stop)
    elif hasattr(report, bstack1l11l1l_opy_ (u"࠭ࡳࡵࡣࡵࡸࠬ⏦")):
        bstack11111lll1_opy_ = bstack111ll1ll111_opy_(report.start)
    try:
        if getattr(report, bstack1l11l1l_opy_ (u"ࠧࡸࡪࡨࡲࠬ⏧"), bstack1l11l1l_opy_ (u"ࠨࠩ⏨")) == bstack1l11l1l_opy_ (u"ࠩࡦࡥࡱࡲࠧ⏩"):
            logger.debug(bstack1l11l1l_opy_ (u"ࠪ࡬ࡦࡴࡤ࡭ࡧࡢࡳ࠶࠷ࡹࡠࡶࡨࡷࡹࡥࡥࡷࡧࡱࡸ࠿ࠦࡳࡵࡣࡷࡩࠥ࠳ࠠࡼࡿ࠯ࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠠ࠮ࠢࡾࢁࠬ⏪").format(getattr(report, bstack1l11l1l_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩ⏫"), bstack1l11l1l_opy_ (u"ࠬ࠭⏬")).__str__(), bstack1lll11l1lll1_opy_))
            if bstack1lll11l1lll1_opy_ == bstack1l11l1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭⏭"):
                _1111ll1111_opy_[item.nodeid][bstack1l11l1l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⏮")] = bstack11111lll1_opy_
                bstack1lll11ll1l1l_opy_(item, _1111ll1111_opy_[item.nodeid], bstack1l11l1l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ⏯"), report, call)
                store[bstack1l11l1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭⏰")] = None
            elif bstack1lll11l1lll1_opy_ == bstack1l11l1l_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠢ⏱"):
                bstack111l1l11l1_opy_ = _1111ll1111_opy_[item.nodeid][bstack1l11l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ⏲")]
                bstack111l1l11l1_opy_.set(hooks=_1111ll1111_opy_[item.nodeid].get(bstack1l11l1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ⏳"), []))
                exception, bstack111l1ll11l_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack111l1ll11l_opy_ = [call.excinfo.exconly(), getattr(report, bstack1l11l1l_opy_ (u"࠭࡬ࡰࡰࡪࡶࡪࡶࡲࡵࡧࡻࡸࠬ⏴"), bstack1l11l1l_opy_ (u"ࠧࠨ⏵"))]
                bstack111l1l11l1_opy_.stop(time=bstack11111lll1_opy_, result=Result(result=getattr(report, bstack1l11l1l_opy_ (u"ࠨࡱࡸࡸࡨࡵ࡭ࡦࠩ⏶"), bstack1l11l1l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ⏷")), exception=exception, bstack111l1ll11l_opy_=bstack111l1ll11l_opy_))
                bstack111ll1lll1_opy_.bstack111ll11l11_opy_(bstack1l11l1l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ⏸"), _1111ll1111_opy_[item.nodeid][bstack1l11l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ⏹")])
        elif getattr(report, bstack1l11l1l_opy_ (u"ࠬࡽࡨࡦࡰࠪ⏺"), bstack1l11l1l_opy_ (u"࠭ࠧ⏻")) in [bstack1l11l1l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭⏼"), bstack1l11l1l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪ⏽")]:
            logger.debug(bstack1l11l1l_opy_ (u"ࠩ࡫ࡥࡳࡪ࡬ࡦࡡࡲ࠵࠶ࡿ࡟ࡵࡧࡶࡸࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡹࡴࡢࡶࡨࠤ࠲ࠦࡻࡾ࠮ࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠦ࠭ࠡࡽࢀࠫ⏾").format(getattr(report, bstack1l11l1l_opy_ (u"ࠪࡻ࡭࡫࡮ࠨ⏿"), bstack1l11l1l_opy_ (u"ࠫࠬ␀")).__str__(), bstack1lll11l1lll1_opy_))
            bstack111ll11l1l_opy_ = item.nodeid + bstack1l11l1l_opy_ (u"ࠬ࠳ࠧ␁") + getattr(report, bstack1l11l1l_opy_ (u"࠭ࡷࡩࡧࡱࠫ␂"), bstack1l11l1l_opy_ (u"ࠧࠨ␃"))
            if getattr(report, bstack1l11l1l_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ␄"), False):
                hook_type = bstack1l11l1l_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧ␅") if getattr(report, bstack1l11l1l_opy_ (u"ࠪࡻ࡭࡫࡮ࠨ␆"), bstack1l11l1l_opy_ (u"ࠫࠬ␇")) == bstack1l11l1l_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ␈") else bstack1l11l1l_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪ␉")
                _1111ll1111_opy_[bstack111ll11l1l_opy_] = {
                    bstack1l11l1l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ␊"): uuid4().__str__(),
                    bstack1l11l1l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ␋"): bstack11111lll1_opy_,
                    bstack1l11l1l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬ␌"): hook_type
                }
            _1111ll1111_opy_[bstack111ll11l1l_opy_][bstack1l11l1l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ␍")] = bstack11111lll1_opy_
            bstack1lll11lll1ll_opy_(_1111ll1111_opy_[bstack111ll11l1l_opy_][bstack1l11l1l_opy_ (u"ࠫࡺࡻࡩࡥࠩ␎")])
            bstack1lll11lll1l1_opy_(item, _1111ll1111_opy_[bstack111ll11l1l_opy_], bstack1l11l1l_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ␏"), report, call)
            if getattr(report, bstack1l11l1l_opy_ (u"࠭ࡷࡩࡧࡱࠫ␐"), bstack1l11l1l_opy_ (u"ࠧࠨ␑")) == bstack1l11l1l_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ␒"):
                if getattr(report, bstack1l11l1l_opy_ (u"ࠩࡲࡹࡹࡩ࡯࡮ࡧࠪ␓"), bstack1l11l1l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ␔")) == bstack1l11l1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ␕"):
                    bstack1111l1ll11_opy_ = {
                        bstack1l11l1l_opy_ (u"ࠬࡻࡵࡪࡦࠪ␖"): uuid4().__str__(),
                        bstack1l11l1l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ␗"): bstack11ll11ll1l_opy_(),
                        bstack1l11l1l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ␘"): bstack11ll11ll1l_opy_()
                    }
                    _1111ll1111_opy_[item.nodeid] = {**_1111ll1111_opy_[item.nodeid], **bstack1111l1ll11_opy_}
                    bstack1lll11ll1l1l_opy_(item, _1111ll1111_opy_[item.nodeid], bstack1l11l1l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ␙"))
                    bstack1lll11ll1l1l_opy_(item, _1111ll1111_opy_[item.nodeid], bstack1l11l1l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ␚"), report, call)
    except Exception as err:
        print(bstack1l11l1l_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡥࡳࡪ࡬ࡦࡡࡲ࠵࠶ࡿ࡟ࡵࡧࡶࡸࡤ࡫ࡶࡦࡰࡷ࠾ࠥࢁࡽࠨ␛"), str(err))
def bstack1lll11ll1111_opy_(test, bstack1111l1ll11_opy_, result=None, call=None, bstack11l1111l_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack111l1l11l1_opy_ = {
        bstack1l11l1l_opy_ (u"ࠫࡺࡻࡩࡥࠩ␜"): bstack1111l1ll11_opy_[bstack1l11l1l_opy_ (u"ࠬࡻࡵࡪࡦࠪ␝")],
        bstack1l11l1l_opy_ (u"࠭ࡴࡺࡲࡨࠫ␞"): bstack1l11l1l_opy_ (u"ࠧࡵࡧࡶࡸࠬ␟"),
        bstack1l11l1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭␠"): test.name,
        bstack1l11l1l_opy_ (u"ࠩࡥࡳࡩࡿࠧ␡"): {
            bstack1l11l1l_opy_ (u"ࠪࡰࡦࡴࡧࠨ␢"): bstack1l11l1l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ␣"),
            bstack1l11l1l_opy_ (u"ࠬࡩ࡯ࡥࡧࠪ␤"): inspect.getsource(test.obj)
        },
        bstack1l11l1l_opy_ (u"࠭ࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ␥"): test.name,
        bstack1l11l1l_opy_ (u"ࠧࡴࡥࡲࡴࡪ࠭␦"): test.name,
        bstack1l11l1l_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࡳࠨ␧"): bstack1l1l1lllll_opy_.bstack1111lll1l1_opy_(test),
        bstack1l11l1l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ␨"): file_path,
        bstack1l11l1l_opy_ (u"ࠪࡰࡴࡩࡡࡵ࡫ࡲࡲࠬ␩"): file_path,
        bstack1l11l1l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ␪"): bstack1l11l1l_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭␫"),
        bstack1l11l1l_opy_ (u"࠭ࡶࡤࡡࡩ࡭ࡱ࡫ࡰࡢࡶ࡫ࠫ␬"): file_path,
        bstack1l11l1l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ␭"): bstack1111l1ll11_opy_[bstack1l11l1l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ␮")],
        bstack1l11l1l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ␯"): bstack1l11l1l_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶࠪ␰"),
        bstack1l11l1l_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡖࡪࡸࡵ࡯ࡒࡤࡶࡦࡳࠧ␱"): {
            bstack1l11l1l_opy_ (u"ࠬࡸࡥࡳࡷࡱࡣࡳࡧ࡭ࡦࠩ␲"): test.nodeid
        },
        bstack1l11l1l_opy_ (u"࠭ࡴࡢࡩࡶࠫ␳"): bstack11l1111llll_opy_(test.own_markers)
    }
    if bstack11l1111l_opy_ in [bstack1l11l1l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨ␴"), bstack1l11l1l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ␵")]:
        bstack111l1l11l1_opy_[bstack1l11l1l_opy_ (u"ࠩࡰࡩࡹࡧࠧ␶")] = {
            bstack1l11l1l_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬ␷"): bstack1111l1ll11_opy_.get(bstack1l11l1l_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭␸"), [])
        }
    if bstack11l1111l_opy_ == bstack1l11l1l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ࠭␹"):
        bstack111l1l11l1_opy_[bstack1l11l1l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭␺")] = bstack1l11l1l_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ␻")
        bstack111l1l11l1_opy_[bstack1l11l1l_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ␼")] = bstack1111l1ll11_opy_[bstack1l11l1l_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ␽")]
        bstack111l1l11l1_opy_[bstack1l11l1l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ␾")] = bstack1111l1ll11_opy_[bstack1l11l1l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ␿")]
    if result:
        bstack111l1l11l1_opy_[bstack1l11l1l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ⑀")] = result.outcome
        bstack111l1l11l1_opy_[bstack1l11l1l_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧ⑁")] = result.duration * 1000
        bstack111l1l11l1_opy_[bstack1l11l1l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⑂")] = bstack1111l1ll11_opy_[bstack1l11l1l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⑃")]
        if result.failed:
            bstack111l1l11l1_opy_[bstack1l11l1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨ⑄")] = bstack111ll1lll1_opy_.bstack1lllll1ll11_opy_(call.excinfo.typename)
            bstack111l1l11l1_opy_[bstack1l11l1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫ⑅")] = bstack111ll1lll1_opy_.bstack1lll1lll1ll1_opy_(call.excinfo, result)
        bstack111l1l11l1_opy_[bstack1l11l1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ⑆")] = bstack1111l1ll11_opy_[bstack1l11l1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ⑇")]
    if outcome:
        bstack111l1l11l1_opy_[bstack1l11l1l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭⑈")] = bstack111ll111l11_opy_(outcome)
        bstack111l1l11l1_opy_[bstack1l11l1l_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨ⑉")] = 0
        bstack111l1l11l1_opy_[bstack1l11l1l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⑊")] = bstack1111l1ll11_opy_[bstack1l11l1l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⑋")]
        if bstack111l1l11l1_opy_[bstack1l11l1l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ⑌")] == bstack1l11l1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ⑍"):
            bstack111l1l11l1_opy_[bstack1l11l1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫ⑎")] = bstack1l11l1l_opy_ (u"࠭ࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠧ⑏")  # bstack1lll11ll11l1_opy_
            bstack111l1l11l1_opy_[bstack1l11l1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨ⑐")] = [{bstack1l11l1l_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫ⑑"): [bstack1l11l1l_opy_ (u"ࠩࡶࡳࡲ࡫ࠠࡦࡴࡵࡳࡷ࠭⑒")]}]
        bstack111l1l11l1_opy_[bstack1l11l1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ⑓")] = bstack1111l1ll11_opy_[bstack1l11l1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ⑔")]
    return bstack111l1l11l1_opy_
def bstack1lll1l111111_opy_(test, bstack1111llll11_opy_, bstack11l1111l_opy_, result, call, outcome, bstack1lll11ll1ll1_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack1111llll11_opy_[bstack1l11l1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨ⑕")]
    hook_name = bstack1111llll11_opy_[bstack1l11l1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠩ⑖")]
    hook_data = {
        bstack1l11l1l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⑗"): bstack1111llll11_opy_[bstack1l11l1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⑘")],
        bstack1l11l1l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ⑙"): bstack1l11l1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨ⑚"),
        bstack1l11l1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ⑛"): bstack1l11l1l_opy_ (u"ࠬࢁࡽࠨ⑜").format(bstack1lllll111111_opy_(hook_name)),
        bstack1l11l1l_opy_ (u"࠭ࡢࡰࡦࡼࠫ⑝"): {
            bstack1l11l1l_opy_ (u"ࠧ࡭ࡣࡱ࡫ࠬ⑞"): bstack1l11l1l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ⑟"),
            bstack1l11l1l_opy_ (u"ࠩࡦࡳࡩ࡫ࠧ①"): None
        },
        bstack1l11l1l_opy_ (u"ࠪࡷࡨࡵࡰࡦࠩ②"): test.name,
        bstack1l11l1l_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࡶࠫ③"): bstack1l1l1lllll_opy_.bstack1111lll1l1_opy_(test, hook_name),
        bstack1l11l1l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ④"): file_path,
        bstack1l11l1l_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠨ⑤"): file_path,
        bstack1l11l1l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ⑥"): bstack1l11l1l_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩ⑦"),
        bstack1l11l1l_opy_ (u"ࠩࡹࡧࡤ࡬ࡩ࡭ࡧࡳࡥࡹ࡮ࠧ⑧"): file_path,
        bstack1l11l1l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ⑨"): bstack1111llll11_opy_[bstack1l11l1l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ⑩")],
        bstack1l11l1l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ⑪"): bstack1l11l1l_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠳ࡣࡶࡥࡸࡱࡧ࡫ࡲࠨ⑫") if bstack1lll11l1lll1_opy_ == bstack1l11l1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫ⑬") else bstack1l11l1l_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴࠨ⑭"),
        bstack1l11l1l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬ⑮"): hook_type
    }
    bstack1l1llll1l1l_opy_ = bstack1111l11l1l_opy_(_1111ll1111_opy_.get(test.nodeid, None))
    if bstack1l1llll1l1l_opy_:
        hook_data[bstack1l11l1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤ࡯ࡤࠨ⑯")] = bstack1l1llll1l1l_opy_
    if result:
        hook_data[bstack1l11l1l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ⑰")] = result.outcome
        hook_data[bstack1l11l1l_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭⑱")] = result.duration * 1000
        hook_data[bstack1l11l1l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⑲")] = bstack1111llll11_opy_[bstack1l11l1l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⑳")]
        if result.failed:
            hook_data[bstack1l11l1l_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧ⑴")] = bstack111ll1lll1_opy_.bstack1lllll1ll11_opy_(call.excinfo.typename)
            hook_data[bstack1l11l1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪ⑵")] = bstack111ll1lll1_opy_.bstack1lll1lll1ll1_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack1l11l1l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ⑶")] = bstack111ll111l11_opy_(outcome)
        hook_data[bstack1l11l1l_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬ⑷")] = 100
        hook_data[bstack1l11l1l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⑸")] = bstack1111llll11_opy_[bstack1l11l1l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⑹")]
        if hook_data[bstack1l11l1l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ⑺")] == bstack1l11l1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ⑻"):
            hook_data[bstack1l11l1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨ⑼")] = bstack1l11l1l_opy_ (u"࡙ࠪࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠫ⑽")  # bstack1lll11ll11l1_opy_
            hook_data[bstack1l11l1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬ⑾")] = [{bstack1l11l1l_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨ⑿"): [bstack1l11l1l_opy_ (u"࠭ࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠪ⒀")]}]
    if bstack1lll11ll1ll1_opy_:
        hook_data[bstack1l11l1l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ⒁")] = bstack1lll11ll1ll1_opy_.result
        hook_data[bstack1l11l1l_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩ⒂")] = bstack111lll11ll1_opy_(bstack1111llll11_opy_[bstack1l11l1l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭⒃")], bstack1111llll11_opy_[bstack1l11l1l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⒄")])
        hook_data[bstack1l11l1l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⒅")] = bstack1111llll11_opy_[bstack1l11l1l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⒆")]
        if hook_data[bstack1l11l1l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭⒇")] == bstack1l11l1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ⒈"):
            hook_data[bstack1l11l1l_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧ⒉")] = bstack111ll1lll1_opy_.bstack1lllll1ll11_opy_(bstack1lll11ll1ll1_opy_.exception_type)
            hook_data[bstack1l11l1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪ⒊")] = [{bstack1l11l1l_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭⒋"): bstack111l1ll11ll_opy_(bstack1lll11ll1ll1_opy_.exception)}]
    return hook_data
def bstack1lll11ll1l1l_opy_(test, bstack1111l1ll11_opy_, bstack11l1111l_opy_, result=None, call=None, outcome=None):
    logger.debug(bstack1l11l1l_opy_ (u"ࠫࡸ࡫࡮ࡥࡡࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡆࡺࡴࡦ࡯ࡳࡸ࡮ࡴࡧࠡࡶࡲࠤ࡬࡫࡮ࡦࡴࡤࡸࡪࠦࡴࡦࡵࡷࠤࡩࡧࡴࡢࠢࡩࡳࡷࠦࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠣ࠱ࠥࢁࡽࠨ⒌").format(bstack11l1111l_opy_))
    bstack111l1l11l1_opy_ = bstack1lll11ll1111_opy_(test, bstack1111l1ll11_opy_, result, call, bstack11l1111l_opy_, outcome)
    driver = getattr(test, bstack1l11l1l_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭⒍"), None)
    if bstack11l1111l_opy_ == bstack1l11l1l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ⒎") and driver:
        bstack111l1l11l1_opy_[bstack1l11l1l_opy_ (u"ࠧࡪࡰࡷࡩ࡬ࡸࡡࡵ࡫ࡲࡲࡸ࠭⒏")] = bstack111ll1lll1_opy_.bstack111l1ll1ll_opy_(driver)
    if bstack11l1111l_opy_ == bstack1l11l1l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩ⒐"):
        bstack11l1111l_opy_ = bstack1l11l1l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ⒑")
    bstack1111l1111l_opy_ = {
        bstack1l11l1l_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ⒒"): bstack11l1111l_opy_,
        bstack1l11l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭⒓"): bstack111l1l11l1_opy_
    }
    bstack111ll1lll1_opy_.bstack11llll1l11_opy_(bstack1111l1111l_opy_)
    if bstack11l1111l_opy_ == bstack1l11l1l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭⒔"):
        threading.current_thread().bstackTestMeta = {bstack1l11l1l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭⒕"): bstack1l11l1l_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨ⒖")}
    elif bstack11l1111l_opy_ == bstack1l11l1l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ⒗"):
        threading.current_thread().bstackTestMeta = {bstack1l11l1l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ⒘"): getattr(result, bstack1l11l1l_opy_ (u"ࠪࡳࡺࡺࡣࡰ࡯ࡨࠫ⒙"), bstack1l11l1l_opy_ (u"ࠫࠬ⒚"))}
def bstack1lll11lll1l1_opy_(test, bstack1111l1ll11_opy_, bstack11l1111l_opy_, result=None, call=None, outcome=None, bstack1lll11ll1ll1_opy_=None):
    logger.debug(bstack1l11l1l_opy_ (u"ࠬࡹࡥ࡯ࡦࡢ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡇࡴࡵࡧࡰࡴࡹ࡯࡮ࡨࠢࡷࡳࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡫ࠠࡩࡱࡲ࡯ࠥࡪࡡࡵࡣ࠯ࠤࡪࡼࡥ࡯ࡶࡗࡽࡵ࡫ࠠ࠮ࠢࡾࢁࠬ⒛").format(bstack11l1111l_opy_))
    hook_data = bstack1lll1l111111_opy_(test, bstack1111l1ll11_opy_, bstack11l1111l_opy_, result, call, outcome, bstack1lll11ll1ll1_opy_)
    bstack1111l1111l_opy_ = {
        bstack1l11l1l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ⒜"): bstack11l1111l_opy_,
        bstack1l11l1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࠩ⒝"): hook_data
    }
    bstack111ll1lll1_opy_.bstack11llll1l11_opy_(bstack1111l1111l_opy_)
def bstack1111l11l1l_opy_(bstack1111l1ll11_opy_):
    if not bstack1111l1ll11_opy_:
        return None
    if bstack1111l1ll11_opy_.get(bstack1l11l1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ⒞"), None):
        return getattr(bstack1111l1ll11_opy_[bstack1l11l1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ⒟")], bstack1l11l1l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ⒠"), None)
    return bstack1111l1ll11_opy_.get(bstack1l11l1l_opy_ (u"ࠫࡺࡻࡩࡥࠩ⒡"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll11ll1lll_opy_.LOG, bstack1ll1l1l1ll1_opy_.PRE, request, caplog)
    yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll11ll1lll_opy_.LOG, bstack1ll1l1l1ll1_opy_.POST, request, caplog)
        return # skip all existing operations
    try:
        if not bstack111ll1lll1_opy_.on():
            return
        places = [bstack1l11l1l_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ⒢"), bstack1l11l1l_opy_ (u"࠭ࡣࡢ࡮࡯ࠫ⒣"), bstack1l11l1l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩ⒤")]
        logs = []
        for bstack1lll1l1111l1_opy_ in places:
            records = caplog.get_records(bstack1lll1l1111l1_opy_)
            bstack1lll11lll111_opy_ = bstack1l11l1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⒥") if bstack1lll1l1111l1_opy_ == bstack1l11l1l_opy_ (u"ࠩࡦࡥࡱࡲࠧ⒦") else bstack1l11l1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⒧")
            bstack1lll1l11l1ll_opy_ = request.node.nodeid + (bstack1l11l1l_opy_ (u"ࠫࠬ⒨") if bstack1lll1l1111l1_opy_ == bstack1l11l1l_opy_ (u"ࠬࡩࡡ࡭࡮ࠪ⒩") else bstack1l11l1l_opy_ (u"࠭࠭ࠨ⒪") + bstack1lll1l1111l1_opy_)
            test_uuid = bstack1111l11l1l_opy_(_1111ll1111_opy_.get(bstack1lll1l11l1ll_opy_, None))
            if not test_uuid:
                continue
            for record in records:
                if bstack111l1llllll_opy_(record.message):
                    continue
                logs.append({
                    bstack1l11l1l_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ⒫"): bstack111l1l1lll1_opy_(record.created).isoformat() + bstack1l11l1l_opy_ (u"ࠨ࡜ࠪ⒬"),
                    bstack1l11l1l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ⒭"): record.levelname,
                    bstack1l11l1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ⒮"): record.message,
                    bstack1lll11lll111_opy_: test_uuid
                })
        if len(logs) > 0:
            bstack111ll1lll1_opy_.bstack1l1111l11_opy_(logs)
    except Exception as err:
        print(bstack1l11l1l_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡪࡩ࡯࡯ࡦࡢࡪ࡮ࡾࡴࡶࡴࡨ࠾ࠥࢁࡽࠨ⒯"), str(err))
def bstack111ll1ll1_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack1l111111_opy_
    bstack1llll11l1_opy_ = bstack1ll1ll11ll_opy_(threading.current_thread(), bstack1l11l1l_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩ⒰"), None) and bstack1ll1ll11ll_opy_(
            threading.current_thread(), bstack1l11l1l_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ⒱"), None)
    bstack11l11111l1_opy_ = getattr(driver, bstack1l11l1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧ⒲"), None) != None and getattr(driver, bstack1l11l1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨ⒳"), None) == True
    if sequence == bstack1l11l1l_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࠩ⒴") and driver != None:
      if not bstack1l111111_opy_ and bstack1l1l11ll1ll_opy_() and bstack1l11l1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ⒵") in CONFIG and CONFIG[bstack1l11l1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫⒶ")] == True and bstack1l111lll_opy_.bstack111lll11l_opy_(driver_command) and (bstack11l11111l1_opy_ or bstack1llll11l1_opy_) and not bstack1ll11ll1l1_opy_(args):
        try:
          bstack1l111111_opy_ = True
          logger.debug(bstack1l11l1l_opy_ (u"ࠬࡖࡥࡳࡨࡲࡶࡲ࡯࡮ࡨࠢࡶࡧࡦࡴࠠࡧࡱࡵࠤࢀࢃࠧⒷ").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack1l11l1l_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡩࡷ࡬࡯ࡳ࡯ࠣࡷࡨࡧ࡮ࠡࡽࢀࠫⒸ").format(str(err)))
        bstack1l111111_opy_ = False
    if sequence == bstack1l11l1l_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭Ⓓ"):
        if driver_command == bstack1l11l1l_opy_ (u"ࠨࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠬⒺ"):
            bstack111ll1lll1_opy_.bstack11l1111lll_opy_({
                bstack1l11l1l_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨⒻ"): response[bstack1l11l1l_opy_ (u"ࠪࡺࡦࡲࡵࡦࠩⒼ")],
                bstack1l11l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫⒽ"): store[bstack1l11l1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩⒾ")]
            })
def bstack1lllll111_opy_():
    global bstack1ll1l11111_opy_
    bstack11lllll1_opy_.bstack1l111l1l1l_opy_()
    logging.shutdown()
    bstack111ll1lll1_opy_.bstack111l111ll1_opy_()
    for driver in bstack1ll1l11111_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1lll1l111l11_opy_(*args):
    global bstack1ll1l11111_opy_
    bstack111ll1lll1_opy_.bstack111l111ll1_opy_()
    for driver in bstack1ll1l11111_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1l11l11111_opy_, stage=STAGE.bstack11l1llllll_opy_, bstack1l1l111lll_opy_=bstack1lll1l11l_opy_)
def bstack1ll111ll1_opy_(self, *args, **kwargs):
    bstack1llllll111_opy_ = bstack11lllll111_opy_(self, *args, **kwargs)
    bstack1ll11111l_opy_ = getattr(threading.current_thread(), bstack1l11l1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡚ࡥࡴࡶࡐࡩࡹࡧࠧⒿ"), None)
    if bstack1ll11111l_opy_ and bstack1ll11111l_opy_.get(bstack1l11l1l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧⓀ"), bstack1l11l1l_opy_ (u"ࠨࠩⓁ")) == bstack1l11l1l_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪⓂ"):
        bstack111ll1lll1_opy_.bstack1ll1lll1l_opy_(self)
    return bstack1llllll111_opy_
@measure(event_name=EVENTS.bstack1111111ll_opy_, stage=STAGE.bstack11l1l1lll1_opy_, bstack1l1l111lll_opy_=bstack1lll1l11l_opy_)
def bstack1ll1111111_opy_(framework_name):
    from bstack_utils.config import Config
    bstack11llllll_opy_ = Config.bstack1llll1111_opy_()
    if bstack11llllll_opy_.get_property(bstack1l11l1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡱࡴࡪ࡟ࡤࡣ࡯ࡰࡪࡪࠧⓃ")):
        return
    bstack11llllll_opy_.bstack11ll1l111l_opy_(bstack1l11l1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡲࡵࡤࡠࡥࡤࡰࡱ࡫ࡤࠨⓄ"), True)
    global bstack1ll1ll1l1_opy_
    global bstack11l111l1ll_opy_
    bstack1ll1ll1l1_opy_ = framework_name
    logger.info(bstack11llll1lll_opy_.format(bstack1ll1ll1l1_opy_.split(bstack1l11l1l_opy_ (u"ࠬ࠳ࠧⓅ"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1l1l11ll1ll_opy_():
            Service.start = bstack11ll1l1l1_opy_
            Service.stop = bstack1l11l111l1_opy_
            webdriver.Remote.get = bstack111lllll11_opy_
            webdriver.Remote.__init__ = bstack1ll11l11_opy_
            if not isinstance(os.getenv(bstack1l11l1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖ࡙ࡕࡇࡖࡘࡤࡖࡁࡓࡃࡏࡐࡊࡒࠧⓆ")), str):
                return
            WebDriver.quit = bstack1l11l1lll1_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        elif bstack111ll1lll1_opy_.on():
            webdriver.Remote.__init__ = bstack1ll111ll1_opy_
        bstack11l111l1ll_opy_ = True
    except Exception as e:
        pass
    if os.environ.get(bstack1l11l1l_opy_ (u"ࠧࡔࡇࡏࡉࡓࡏࡕࡎࡡࡒࡖࡤࡖࡌࡂ࡛࡚ࡖࡎࡍࡈࡕࡡࡌࡒࡘ࡚ࡁࡍࡎࡈࡈࠬⓇ")):
        bstack11l111l1ll_opy_ = eval(os.environ.get(bstack1l11l1l_opy_ (u"ࠨࡕࡈࡐࡊࡔࡉࡖࡏࡢࡓࡗࡥࡐࡍࡃ࡜࡛ࡗࡏࡇࡉࡖࡢࡍࡓ࡙ࡔࡂࡎࡏࡉࡉ࠭Ⓢ")))
    if not bstack11l111l1ll_opy_:
        bstack1lll111l1_opy_(bstack1l11l1l_opy_ (u"ࠤࡓࡥࡨࡱࡡࡨࡧࡶࠤࡳࡵࡴࠡ࡫ࡱࡷࡹࡧ࡬࡭ࡧࡧࠦⓉ"), bstack11lllll11_opy_)
    if bstack111ll1lll_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            if hasattr(RemoteConnection, bstack1l11l1l_opy_ (u"ࠪࡣ࡬࡫ࡴࡠࡲࡵࡳࡽࡿ࡟ࡶࡴ࡯ࠫⓊ")) and callable(getattr(RemoteConnection, bstack1l11l1l_opy_ (u"ࠫࡤ࡭ࡥࡵࡡࡳࡶࡴࡾࡹࡠࡷࡵࡰࠬⓋ"))):
                RemoteConnection._get_proxy_url = bstack11l111l1l1_opy_
            else:
                from selenium.webdriver.remote.client_config import ClientConfig
                ClientConfig.get_proxy_url = bstack11l111l1l1_opy_
        except Exception as e:
            logger.error(bstack1l1111l11l_opy_.format(str(e)))
    if bstack1l11l1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬⓌ") in str(framework_name).lower():
        if not bstack1l1l11ll1ll_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack1ll111l11l_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1llll1ll_opy_
            Config.getoption = bstack1l11ll111l_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack111ll111l_opy_
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1llllll1l1_opy_, stage=STAGE.bstack11l1llllll_opy_, bstack1l1l111lll_opy_=bstack1lll1l11l_opy_)
def bstack1l11l1lll1_opy_(self):
    global bstack1ll1ll1l1_opy_
    global bstack11l11ll1ll_opy_
    global bstack111l1111_opy_
    try:
        if bstack1l11l1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭Ⓧ") in bstack1ll1ll1l1_opy_ and self.session_id != None and bstack1ll1ll11ll_opy_(threading.current_thread(), bstack1l11l1l_opy_ (u"ࠧࡵࡧࡶࡸࡘࡺࡡࡵࡷࡶࠫⓎ"), bstack1l11l1l_opy_ (u"ࠨࠩⓏ")) != bstack1l11l1l_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪⓐ"):
            bstack1l11llll11_opy_ = bstack1l11l1l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪⓑ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1l11l1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫⓒ")
            bstack111llll11_opy_(logger, True)
            if os.environ.get(bstack1l11l1l_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࡤ࡚ࡅࡔࡖࡢࡒࡆࡓࡅࠨⓓ"), None):
                self.execute_script(
                    bstack1l11l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫⓔ") + json.dumps(
                        os.environ.get(bstack1l11l1l_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࡟ࡕࡇࡖࡘࡤࡔࡁࡎࡇࠪⓕ"))) + bstack1l11l1l_opy_ (u"ࠨࡿࢀࠫⓖ"))
            if self != None:
                bstack1l11l11l_opy_(self, bstack1l11llll11_opy_, bstack1l11l1l_opy_ (u"ࠩ࠯ࠤࠬⓗ").join(threading.current_thread().bstackTestErrorMessages))
        if not cli.bstack1lll11l111l_opy_(bstack1ll11lll1ll_opy_):
            item = store.get(bstack1l11l1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧⓘ"), None)
            if item is not None and bstack1ll1ll11ll_opy_(threading.current_thread(), bstack1l11l1l_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪⓙ"), None):
                bstack1lll1l11_opy_.bstack1ll1l11ll1_opy_(self, bstack11l1l1ll1l_opy_, logger, item)
        threading.current_thread().testStatus = bstack1l11l1l_opy_ (u"ࠬ࠭ⓚ")
    except Exception as e:
        logger.debug(bstack1l11l1l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡲࡧࡲ࡬࡫ࡱ࡫ࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࠢⓛ") + str(e))
    bstack111l1111_opy_(self)
    self.session_id = None
@measure(event_name=EVENTS.bstack11l1l11l1_opy_, stage=STAGE.bstack11l1llllll_opy_, bstack1l1l111lll_opy_=bstack1lll1l11l_opy_)
def bstack1ll11l11_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack11l11ll1ll_opy_
    global bstack1lll1l11l_opy_
    global bstack11ll1ll1l1_opy_
    global bstack1ll1ll1l1_opy_
    global bstack11lllll111_opy_
    global bstack1ll1l11111_opy_
    global bstack1l1llll111_opy_
    global bstack1llllll11_opy_
    global bstack11l1l1ll1l_opy_
    CONFIG[bstack1l11l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩⓜ")] = str(bstack1ll1ll1l1_opy_) + str(__version__)
    command_executor = bstack1ll1111l1_opy_(bstack1l1llll111_opy_, CONFIG)
    logger.debug(bstack1l1ll1lll1_opy_.format(command_executor))
    proxy = bstack11l11lllll_opy_(CONFIG, proxy)
    bstack1l11l1111_opy_ = 0
    try:
        if bstack11ll1ll1l1_opy_ is True:
            bstack1l11l1111_opy_ = int(os.environ.get(bstack1l11l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨⓝ")))
    except:
        bstack1l11l1111_opy_ = 0
    bstack1lll11111_opy_ = bstack1l1l11ll1l_opy_(CONFIG, bstack1l11l1111_opy_)
    logger.debug(bstack1l1111l1l1_opy_.format(str(bstack1lll11111_opy_)))
    bstack11l1l1ll1l_opy_ = CONFIG.get(bstack1l11l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬⓞ"))[bstack1l11l1111_opy_]
    if bstack1l11l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧⓟ") in CONFIG and CONFIG[bstack1l11l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨⓠ")]:
        bstack1l1111ll11_opy_(bstack1lll11111_opy_, bstack1llllll11_opy_)
    if bstack1ll1l11lll_opy_.bstack1ll111l1_opy_(CONFIG, bstack1l11l1111_opy_) and bstack1ll1l11lll_opy_.bstack1ll11ll111_opy_(bstack1lll11111_opy_, options, desired_capabilities):
        threading.current_thread().a11yPlatform = True
        if not cli.bstack1lll11l111l_opy_(bstack1ll11lll1ll_opy_):
            bstack1ll1l11lll_opy_.set_capabilities(bstack1lll11111_opy_, CONFIG)
    if desired_capabilities:
        bstack1lll1lllll_opy_ = bstack1ll11l11ll_opy_(desired_capabilities)
        bstack1lll1lllll_opy_[bstack1l11l1l_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬⓡ")] = bstack1lllll111l_opy_(CONFIG)
        bstack1ll11ll1ll_opy_ = bstack1l1l11ll1l_opy_(bstack1lll1lllll_opy_)
        if bstack1ll11ll1ll_opy_:
            bstack1lll11111_opy_ = update(bstack1ll11ll1ll_opy_, bstack1lll11111_opy_)
        desired_capabilities = None
    if options:
        bstack11l1ll1111_opy_(options, bstack1lll11111_opy_)
    if not options:
        options = bstack11ll11111_opy_(bstack1lll11111_opy_)
    if proxy and bstack1ll1l1ll11_opy_() >= version.parse(bstack1l11l1l_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭ⓢ")):
        options.proxy(proxy)
    if options and bstack1ll1l1ll11_opy_() >= version.parse(bstack1l11l1l_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ⓣ")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1ll1l1ll11_opy_() < version.parse(bstack1l11l1l_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧⓤ")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1lll11111_opy_)
    logger.info(bstack1ll1111l1l_opy_)
    bstack1lll1l111_opy_.end(EVENTS.bstack1111111ll_opy_.value, EVENTS.bstack1111111ll_opy_.value + bstack1l11l1l_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤⓥ"),
                               EVENTS.bstack1111111ll_opy_.value + bstack1l11l1l_opy_ (u"ࠥ࠾ࡪࡴࡤࠣⓦ"), True, None)
    try:
        if bstack1ll1l1ll11_opy_() >= version.parse(bstack1l11l1l_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫⓧ")):
            bstack11lllll111_opy_(self, command_executor=command_executor,
                      options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
        elif bstack1ll1l1ll11_opy_() >= version.parse(bstack1l11l1l_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫⓨ")):
            bstack11lllll111_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities, options=options,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive, file_detector=file_detector)
        elif bstack1ll1l1ll11_opy_() >= version.parse(bstack1l11l1l_opy_ (u"࠭࠲࠯࠷࠶࠲࠵࠭ⓩ")):
            bstack11lllll111_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive, file_detector=file_detector)
        else:
            bstack11lllll111_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive)
    except Exception as bstack1l111lll11_opy_:
        logger.error(bstack1llll111l1_opy_.format(bstack1l11l1l_opy_ (u"ࠧࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰ࠭⓪"), str(bstack1l111lll11_opy_)))
        raise bstack1l111lll11_opy_
    try:
        bstack1ll11lll11_opy_ = bstack1l11l1l_opy_ (u"ࠨࠩ⓫")
        if bstack1ll1l1ll11_opy_() >= version.parse(bstack1l11l1l_opy_ (u"ࠩ࠷࠲࠵࠴࠰ࡣ࠳ࠪ⓬")):
            bstack1ll11lll11_opy_ = self.caps.get(bstack1l11l1l_opy_ (u"ࠥࡳࡵࡺࡩ࡮ࡣ࡯ࡌࡺࡨࡕࡳ࡮ࠥ⓭"))
        else:
            bstack1ll11lll11_opy_ = self.capabilities.get(bstack1l11l1l_opy_ (u"ࠦࡴࡶࡴࡪ࡯ࡤࡰࡍࡻࡢࡖࡴ࡯ࠦ⓮"))
        if bstack1ll11lll11_opy_:
            bstack1l11ll1111_opy_(bstack1ll11lll11_opy_)
            if bstack1ll1l1ll11_opy_() <= version.parse(bstack1l11l1l_opy_ (u"ࠬ࠹࠮࠲࠵࠱࠴ࠬ⓯")):
                self.command_executor._url = bstack1l11l1l_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢ⓰") + bstack1l1llll111_opy_ + bstack1l11l1l_opy_ (u"ࠢ࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠦ⓱")
            else:
                self.command_executor._url = bstack1l11l1l_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥ⓲") + bstack1ll11lll11_opy_ + bstack1l11l1l_opy_ (u"ࠤ࠲ࡻࡩ࠵ࡨࡶࡤࠥ⓳")
            logger.debug(bstack1llll11lll_opy_.format(bstack1ll11lll11_opy_))
        else:
            logger.debug(bstack1ll1111l_opy_.format(bstack1l11l1l_opy_ (u"ࠥࡓࡵࡺࡩ࡮ࡣ࡯ࠤࡍࡻࡢࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧࠦ⓴")))
    except Exception as e:
        logger.debug(bstack1ll1111l_opy_.format(e))
    bstack11l11ll1ll_opy_ = self.session_id
    if bstack1l11l1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ⓵") in bstack1ll1ll1l1_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack1l11l1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩ⓶"), None)
        if item:
            bstack1lll11lllll1_opy_ = getattr(item, bstack1l11l1l_opy_ (u"࠭࡟ࡵࡧࡶࡸࡤࡩࡡࡴࡧࡢࡷࡹࡧࡲࡵࡧࡧࠫ⓷"), False)
            if not getattr(item, bstack1l11l1l_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨ⓸"), None) and bstack1lll11lllll1_opy_:
                setattr(store[bstack1l11l1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬ⓹")], bstack1l11l1l_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪ⓺"), self)
        bstack1ll11111l_opy_ = getattr(threading.current_thread(), bstack1l11l1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡗࡩࡸࡺࡍࡦࡶࡤࠫ⓻"), None)
        if bstack1ll11111l_opy_ and bstack1ll11111l_opy_.get(bstack1l11l1l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ⓼"), bstack1l11l1l_opy_ (u"ࠬ࠭⓽")) == bstack1l11l1l_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧ⓾"):
            bstack111ll1lll1_opy_.bstack1ll1lll1l_opy_(self)
    bstack1ll1l11111_opy_.append(self)
    if bstack1l11l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ⓿") in CONFIG and bstack1l11l1l_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭─") in CONFIG[bstack1l11l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ━")][bstack1l11l1111_opy_]:
        bstack1lll1l11l_opy_ = CONFIG[bstack1l11l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭│")][bstack1l11l1111_opy_][bstack1l11l1l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ┃")]
    logger.debug(bstack11lll1l1l1_opy_.format(bstack11l11ll1ll_opy_))
@measure(event_name=EVENTS.bstack1ll1l111l_opy_, stage=STAGE.bstack11l1llllll_opy_, bstack1l1l111lll_opy_=bstack1lll1l11l_opy_)
def bstack111lllll11_opy_(self, url):
    global bstack1llll1l11_opy_
    global CONFIG
    try:
        bstack111ll1l1ll_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack11l1l1ll1_opy_.format(str(err)))
    try:
        bstack1llll1l11_opy_(self, url)
    except Exception as e:
        try:
            bstack1l1lll1l1_opy_ = str(e)
            if any(err_msg in bstack1l1lll1l1_opy_ for err_msg in bstack1l11lll1l1_opy_):
                bstack111ll1l1ll_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack11l1l1ll1_opy_.format(str(err)))
        raise e
def bstack1lllll1l1_opy_(item, when):
    global bstack11l1l1llll_opy_
    try:
        bstack11l1l1llll_opy_(item, when)
    except Exception as e:
        pass
def bstack111ll111l_opy_(item, call, rep):
    global bstack1lll1111_opy_
    global bstack1ll1l11111_opy_
    name = bstack1l11l1l_opy_ (u"ࠬ࠭┄")
    try:
        if rep.when == bstack1l11l1l_opy_ (u"࠭ࡣࡢ࡮࡯ࠫ┅"):
            bstack11l11ll1ll_opy_ = threading.current_thread().bstackSessionId
            skipSessionName = item.config.getoption(bstack1l11l1l_opy_ (u"ࠧࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ┆"))
            try:
                if (str(skipSessionName).lower() != bstack1l11l1l_opy_ (u"ࠨࡶࡵࡹࡪ࠭┇")):
                    name = str(rep.nodeid)
                    bstack1lll1ll1l1_opy_ = bstack1lll11l1ll_opy_(bstack1l11l1l_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ┈"), name, bstack1l11l1l_opy_ (u"ࠪࠫ┉"), bstack1l11l1l_opy_ (u"ࠫࠬ┊"), bstack1l11l1l_opy_ (u"ࠬ࠭┋"), bstack1l11l1l_opy_ (u"࠭ࠧ┌"))
                    os.environ[bstack1l11l1l_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࡟ࡕࡇࡖࡘࡤࡔࡁࡎࡇࠪ┍")] = name
                    for driver in bstack1ll1l11111_opy_:
                        if bstack11l11ll1ll_opy_ == driver.session_id:
                            driver.execute_script(bstack1lll1ll1l1_opy_)
            except Exception as e:
                logger.debug(bstack1l11l1l_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠢࡩࡳࡷࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡽࠨ┎").format(str(e)))
            try:
                bstack11ll111ll1_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack1l11l1l_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ┏"):
                    status = bstack1l11l1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ┐") if rep.outcome.lower() == bstack1l11l1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ┑") else bstack1l11l1l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ┒")
                    reason = bstack1l11l1l_opy_ (u"࠭ࠧ┓")
                    if status == bstack1l11l1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ└"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack1l11l1l_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭┕") if status == bstack1l11l1l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ┖") else bstack1l11l1l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ┗")
                    data = name + bstack1l11l1l_opy_ (u"ࠫࠥࡶࡡࡴࡵࡨࡨࠦ࠭┘") if status == bstack1l11l1l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ┙") else name + bstack1l11l1l_opy_ (u"࠭ࠠࡧࡣ࡬ࡰࡪࡪࠡࠡࠩ┚") + reason
                    bstack11ll1l1l11_opy_ = bstack1lll11l1ll_opy_(bstack1l11l1l_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩ┛"), bstack1l11l1l_opy_ (u"ࠨࠩ├"), bstack1l11l1l_opy_ (u"ࠩࠪ┝"), bstack1l11l1l_opy_ (u"ࠪࠫ┞"), level, data)
                    for driver in bstack1ll1l11111_opy_:
                        if bstack11l11ll1ll_opy_ == driver.session_id:
                            driver.execute_script(bstack11ll1l1l11_opy_)
            except Exception as e:
                logger.debug(bstack1l11l1l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡥࡲࡲࡹ࡫ࡸࡵࠢࡩࡳࡷࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡽࠨ┟").format(str(e)))
    except Exception as e:
        logger.debug(bstack1l11l1l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡵࡷࡥࡹ࡫ࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡧࡶࡸࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࡻࡾࠩ┠").format(str(e)))
    bstack1lll1111_opy_(item, call, rep)
notset = Notset()
def bstack1l11ll111l_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1ll11ll1l_opy_
    if str(name).lower() == bstack1l11l1l_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷ࠭┡"):
        return bstack1l11l1l_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠨ┢")
    else:
        return bstack1ll11ll1l_opy_(self, name, default, skip)
def bstack11l111l1l1_opy_(self):
    global CONFIG
    global bstack1l1lllll1_opy_
    try:
        proxy = bstack111111l1l_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack1l11l1l_opy_ (u"ࠨ࠰ࡳࡥࡨ࠭┣")):
                proxies = bstack111l11l11_opy_(proxy, bstack1ll1111l1_opy_())
                if len(proxies) > 0:
                    protocol, bstack1ll1ll111l_opy_ = proxies.popitem()
                    if bstack1l11l1l_opy_ (u"ࠤ࠽࠳࠴ࠨ┤") in bstack1ll1ll111l_opy_:
                        return bstack1ll1ll111l_opy_
                    else:
                        return bstack1l11l1l_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦ┥") + bstack1ll1ll111l_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack1l11l1l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡱࡴࡲࡼࡾࠦࡵࡳ࡮ࠣ࠾ࠥࢁࡽࠣ┦").format(str(e)))
    return bstack1l1lllll1_opy_(self)
def bstack111ll1lll_opy_():
    return (bstack1l11l1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨ┧") in CONFIG or bstack1l11l1l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ┨") in CONFIG) and bstack111l111l_opy_() and bstack1ll1l1ll11_opy_() >= version.parse(
        bstack1l11lll1ll_opy_)
def bstack1lll1l1l11_opy_(self,
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
    global bstack1lll1l11l_opy_
    global bstack11ll1ll1l1_opy_
    global bstack1ll1ll1l1_opy_
    CONFIG[bstack1l11l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩ┩")] = str(bstack1ll1ll1l1_opy_) + str(__version__)
    bstack1l11l1111_opy_ = 0
    try:
        if bstack11ll1ll1l1_opy_ is True:
            bstack1l11l1111_opy_ = int(os.environ.get(bstack1l11l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ┪")))
    except:
        bstack1l11l1111_opy_ = 0
    CONFIG[bstack1l11l1l_opy_ (u"ࠤ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣ┫")] = True
    bstack1lll11111_opy_ = bstack1l1l11ll1l_opy_(CONFIG, bstack1l11l1111_opy_)
    logger.debug(bstack1l1111l1l1_opy_.format(str(bstack1lll11111_opy_)))
    if CONFIG.get(bstack1l11l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ┬")):
        bstack1l1111ll11_opy_(bstack1lll11111_opy_, bstack1llllll11_opy_)
    if bstack1l11l1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ┭") in CONFIG and bstack1l11l1l_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ┮") in CONFIG[bstack1l11l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ┯")][bstack1l11l1111_opy_]:
        bstack1lll1l11l_opy_ = CONFIG[bstack1l11l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ┰")][bstack1l11l1111_opy_][bstack1l11l1l_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭┱")]
    import urllib
    import json
    if bstack1l11l1l_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭┲") in CONFIG and str(CONFIG[bstack1l11l1l_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ┳")]).lower() != bstack1l11l1l_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪ┴"):
        bstack11llll1ll1_opy_ = bstack11l11ll11l_opy_()
        bstack11111l11l_opy_ = bstack11llll1ll1_opy_ + urllib.parse.quote(json.dumps(bstack1lll11111_opy_))
    else:
        bstack11111l11l_opy_ = bstack1l11l1l_opy_ (u"ࠬࡽࡳࡴ࠼࠲࠳ࡨࡪࡰ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡀࡥࡤࡴࡸࡃࠧ┵") + urllib.parse.quote(json.dumps(bstack1lll11111_opy_))
    browser = self.connect(bstack11111l11l_opy_)
    return browser
def bstack11l11111ll_opy_():
    global bstack11l111l1ll_opy_
    global bstack1ll1ll1l1_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack11ll1ll1_opy_
        if not bstack1l1l11ll1ll_opy_():
            global bstack1ll1lllll1_opy_
            if not bstack1ll1lllll1_opy_:
                from bstack_utils.helper import bstack1l1l111111_opy_, bstack111lllll_opy_
                bstack1ll1lllll1_opy_ = bstack1l1l111111_opy_()
                bstack111lllll_opy_(bstack1ll1ll1l1_opy_)
            BrowserType.connect = bstack11ll1ll1_opy_
            return
        BrowserType.launch = bstack1lll1l1l11_opy_
        bstack11l111l1ll_opy_ = True
    except Exception as e:
        pass
def bstack1lll11ll11ll_opy_():
    global CONFIG
    global bstack1l11l1l111_opy_
    global bstack1l1llll111_opy_
    global bstack1llllll11_opy_
    global bstack11ll1ll1l1_opy_
    global bstack11ll1l1lll_opy_
    CONFIG = json.loads(os.environ.get(bstack1l11l1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࠬ┶")))
    bstack1l11l1l111_opy_ = eval(os.environ.get(bstack1l11l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨ┷")))
    bstack1l1llll111_opy_ = os.environ.get(bstack1l11l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡉࡗࡅࡣ࡚ࡘࡌࠨ┸"))
    bstack11lll1l111_opy_(CONFIG, bstack1l11l1l111_opy_)
    bstack11ll1l1lll_opy_ = bstack11lllll1_opy_.configure_logger(CONFIG, bstack11ll1l1lll_opy_)
    if cli.bstack1ll1llll1_opy_():
        bstack1llll1l1l_opy_.invoke(bstack1l11ll1l1_opy_.CONNECT, bstack11l1l111_opy_())
        cli_context.platform_index = int(os.environ.get(bstack1l11l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ┹"), bstack1l11l1l_opy_ (u"ࠪ࠴ࠬ┺")))
        cli.bstack1ll1l1ll111_opy_(cli_context.platform_index)
        cli.bstack1ll11lll111_opy_(bstack1ll1111l1_opy_(bstack1l1llll111_opy_, CONFIG), cli_context.platform_index, bstack11ll11111_opy_)
        cli.bstack1ll11ll1l11_opy_()
        logger.debug(bstack1l11l1l_opy_ (u"ࠦࡈࡒࡉࠡ࡫ࡶࠤࡦࡩࡴࡪࡸࡨࠤ࡫ࡵࡲࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹ࠿ࠥ┻") + str(cli_context.platform_index) + bstack1l11l1l_opy_ (u"ࠧࠨ┼"))
        return # skip all existing operations
    global bstack11lllll111_opy_
    global bstack111l1111_opy_
    global bstack11ll1ll1ll_opy_
    global bstack11ll11ll1_opy_
    global bstack1ll1ll1l1l_opy_
    global bstack111l111l1_opy_
    global bstack1l1ll1111_opy_
    global bstack1llll1l11_opy_
    global bstack1l1lllll1_opy_
    global bstack1ll11ll1l_opy_
    global bstack11l1l1llll_opy_
    global bstack1lll1111_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack11lllll111_opy_ = webdriver.Remote.__init__
        bstack111l1111_opy_ = WebDriver.quit
        bstack1l1ll1111_opy_ = WebDriver.close
        bstack1llll1l11_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack1l11l1l_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩ┽") in CONFIG or bstack1l11l1l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ┾") in CONFIG) and bstack111l111l_opy_():
        if bstack1ll1l1ll11_opy_() < version.parse(bstack1l11lll1ll_opy_):
            logger.error(bstack11lll1lll1_opy_.format(bstack1ll1l1ll11_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                if hasattr(RemoteConnection, bstack1l11l1l_opy_ (u"ࠨࡡࡪࡩࡹࡥࡰࡳࡱࡻࡽࡤࡻࡲ࡭ࠩ┿")) and callable(getattr(RemoteConnection, bstack1l11l1l_opy_ (u"ࠩࡢ࡫ࡪࡺ࡟ࡱࡴࡲࡼࡾࡥࡵࡳ࡮ࠪ╀"))):
                    bstack1l1lllll1_opy_ = RemoteConnection._get_proxy_url
                else:
                    from selenium.webdriver.remote.client_config import ClientConfig
                    bstack1l1lllll1_opy_ = ClientConfig.get_proxy_url
            except Exception as e:
                logger.error(bstack1l1111l11l_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack1ll11ll1l_opy_ = Config.getoption
        from _pytest import runner
        bstack11l1l1llll_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warning(bstack1l11l1l_opy_ (u"ࠥࠩࡸࡀࠠࠦࡵࠥ╁"), bstack1lll111111_opy_, str(e))
    try:
        from pytest_bdd import reporting
        bstack1lll1111_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack1l11l1l_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡳࠥࡸࡵ࡯ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡦࡵࡷࡷࠬ╂"))
    bstack1llllll11_opy_ = CONFIG.get(bstack1l11l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ╃"), {}).get(bstack1l11l1l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ╄"))
    bstack11ll1ll1l1_opy_ = True
    bstack1ll1111111_opy_(bstack11ll1ll11_opy_)
if (bstack111l1ll1lll_opy_()):
    bstack1lll11ll11ll_opy_()
@error_handler(class_method=False)
def bstack1lll11llll1l_opy_(hook_name, event, bstack11lll1ll1l1_opy_=None):
    if hook_name not in [bstack1l11l1l_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨ╅"), bstack1l11l1l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬ╆"), bstack1l11l1l_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠨ╇"), bstack1l11l1l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࠬ╈"), bstack1l11l1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠩ╉"), bstack1l11l1l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸ࠭╊"), bstack1l11l1l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠬ╋"), bstack1l11l1l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠩ╌")]:
        return
    node = store[bstack1l11l1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬ╍")]
    if hook_name in [bstack1l11l1l_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠨ╎"), bstack1l11l1l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࠬ╏")]:
        node = store[bstack1l11l1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡯ࡴࡦ࡯ࠪ═")]
    elif hook_name in [bstack1l11l1l_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡨࡲࡡࡴࡵࠪ║"), bstack1l11l1l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠧ╒")]:
        node = store[bstack1l11l1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡥ࡯ࡥࡸࡹ࡟ࡪࡶࡨࡱࠬ╓")]
    hook_type = bstack1llll1llll1l_opy_(hook_name)
    if event == bstack1l11l1l_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࠨ╔"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll11ll1lll_opy_[hook_type], bstack1ll1l1l1ll1_opy_.PRE, node, hook_name)
            return
        uuid = uuid4().__str__()
        bstack1111llll11_opy_ = {
            bstack1l11l1l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ╕"): uuid,
            bstack1l11l1l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ╖"): bstack11ll11ll1l_opy_(),
            bstack1l11l1l_opy_ (u"ࠫࡹࡿࡰࡦࠩ╗"): bstack1l11l1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪ╘"),
            bstack1l11l1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩ╙"): hook_type,
            bstack1l11l1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪ╚"): hook_name
        }
        store[bstack1l11l1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ╛")].append(uuid)
        bstack1lll11ll111l_opy_ = node.nodeid
        if hook_type == bstack1l11l1l_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧ╜"):
            if not _1111ll1111_opy_.get(bstack1lll11ll111l_opy_, None):
                _1111ll1111_opy_[bstack1lll11ll111l_opy_] = {bstack1l11l1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ╝"): []}
            _1111ll1111_opy_[bstack1lll11ll111l_opy_][bstack1l11l1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ╞")].append(bstack1111llll11_opy_[bstack1l11l1l_opy_ (u"ࠬࡻࡵࡪࡦࠪ╟")])
        _1111ll1111_opy_[bstack1lll11ll111l_opy_ + bstack1l11l1l_opy_ (u"࠭࠭ࠨ╠") + hook_name] = bstack1111llll11_opy_
        bstack1lll11lll1l1_opy_(node, bstack1111llll11_opy_, bstack1l11l1l_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ╡"))
    elif event == bstack1l11l1l_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧ╢"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll11ll1lll_opy_[hook_type], bstack1ll1l1l1ll1_opy_.POST, node, None, bstack11lll1ll1l1_opy_)
            return
        bstack111ll11l1l_opy_ = node.nodeid + bstack1l11l1l_opy_ (u"ࠩ࠰ࠫ╣") + hook_name
        _1111ll1111_opy_[bstack111ll11l1l_opy_][bstack1l11l1l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ╤")] = bstack11ll11ll1l_opy_()
        bstack1lll11lll1ll_opy_(_1111ll1111_opy_[bstack111ll11l1l_opy_][bstack1l11l1l_opy_ (u"ࠫࡺࡻࡩࡥࠩ╥")])
        bstack1lll11lll1l1_opy_(node, _1111ll1111_opy_[bstack111ll11l1l_opy_], bstack1l11l1l_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ╦"), bstack1lll11ll1ll1_opy_=bstack11lll1ll1l1_opy_)
def bstack1lll1l11l1l1_opy_():
    global bstack1lll11l1lll1_opy_
    if bstack1111ll11_opy_():
        bstack1lll11l1lll1_opy_ = bstack1l11l1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠪ╧")
    else:
        bstack1lll11l1lll1_opy_ = bstack1l11l1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ╨")
@bstack111ll1lll1_opy_.bstack1lll1lll1lll_opy_
def bstack1lll1l111l1l_opy_():
    bstack1lll1l11l1l1_opy_()
    if cli.is_running():
        try:
            bstack111l11lllll_opy_(bstack1lll11llll1l_opy_)
        except Exception as e:
            logger.debug(bstack1l11l1l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡩࡱࡲ࡯ࡸࠦࡰࡢࡶࡦ࡬࠿ࠦࡻࡾࠤ╩").format(e))
        return
    if bstack111l111l_opy_():
        bstack11llllll_opy_ = Config.bstack1llll1111_opy_()
        bstack1l11l1l_opy_ (u"ࠩࠪࠫࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡊࡴࡸࠠࡱࡲࡳࠤࡂࠦ࠱࠭ࠢࡰࡳࡩࡥࡥࡹࡧࡦࡹࡹ࡫ࠠࡨࡧࡷࡷࠥࡻࡳࡦࡦࠣࡪࡴࡸࠠࡢ࠳࠴ࡽࠥࡩ࡯࡮࡯ࡤࡲࡩࡹ࠭ࡸࡴࡤࡴࡵ࡯࡮ࡨࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡇࡱࡵࠤࡵࡶࡰࠡࡀࠣ࠵࠱ࠦ࡭ࡰࡦࡢࡩࡽ࡫ࡣࡶࡶࡨࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡲࡶࡰࠣࡦࡪࡩࡡࡶࡵࡨࠤ࡮ࡺࠠࡪࡵࠣࡴࡦࡺࡣࡩࡧࡧࠤ࡮ࡴࠠࡢࠢࡧ࡭࡫࡬ࡥࡳࡧࡱࡸࠥࡶࡲࡰࡥࡨࡷࡸࠦࡩࡥࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡕࡪࡸࡷࠥࡽࡥࠡࡰࡨࡩࡩࠦࡴࡰࠢࡸࡷࡪࠦࡓࡦ࡮ࡨࡲ࡮ࡻ࡭ࡑࡣࡷࡧ࡭࠮ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡠࡪࡤࡲࡩࡲࡥࡳࠫࠣࡪࡴࡸࠠࡱࡲࡳࠤࡃࠦ࠱ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠪࠫࠬ╪")
        if bstack11llllll_opy_.get_property(bstack1l11l1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡱࡴࡪ࡟ࡤࡣ࡯ࡰࡪࡪࠧ╫")):
            if CONFIG.get(bstack1l11l1l_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ╬")) is not None and int(CONFIG[bstack1l11l1l_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ╭")]) > 1:
                bstack111lll1l_opy_(bstack111ll1ll1_opy_)
            return
        bstack111lll1l_opy_(bstack111ll1ll1_opy_)
    try:
        bstack111l11lllll_opy_(bstack1lll11llll1l_opy_)
    except Exception as e:
        logger.debug(bstack1l11l1l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࡶࠤࡵࡧࡴࡤࡪ࠽ࠤࢀࢃࠢ╮").format(e))
bstack1lll1l111l1l_opy_()