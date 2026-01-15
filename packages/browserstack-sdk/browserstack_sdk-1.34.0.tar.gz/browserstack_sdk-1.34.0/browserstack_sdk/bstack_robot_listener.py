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
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack11111lll11_opy_ import RobotHandler
from bstack_utils.capture import bstack111l1lll11_opy_
from bstack_utils.bstack111l11l1l1_opy_ import bstack111l1111ll_opy_, bstack111l11ll11_opy_, bstack111l11l111_opy_
from bstack_utils.bstack111l1ll11l_opy_ import bstack11ll11l11_opy_
from bstack_utils.bstack111l11l11l_opy_ import bstack1llll1lll1_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack1l1l1l111_opy_, bstack11llll1111_opy_, Result, \
    error_handler, bstack1111l1l1ll_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    _lock = threading.Lock()
    store = {
        bstack1l111l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ࿁"): [],
        bstack1l111l1_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭ࡡ࡫ࡳࡴࡱࡳࠨ࿂"): [],
        bstack1l111l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹࠧ࿃"): []
    }
    bstack11111ll1ll_opy_ = []
    bstack1111ll1l11_opy_ = []
    @staticmethod
    def bstack111l1l11l1_opy_(log):
        if not ((isinstance(log[bstack1l111l1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ࿄")], list) or (isinstance(log[bstack1l111l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭࿅")], dict)) and len(log[bstack1l111l1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫࿆ࠧ")])>0) or (isinstance(log[bstack1l111l1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ࿇")], str) and log[bstack1l111l1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ࿈")].strip())):
            return
        active = bstack11ll11l11_opy_.bstack111l1l1ll1_opy_()
        log = {
            bstack1l111l1_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ࿉"): log[bstack1l111l1_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ࿊")],
            bstack1l111l1_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ࿋"): bstack1111l1l1ll_opy_().isoformat() + bstack1l111l1_opy_ (u"ࠬࡠࠧ࿌"),
            bstack1l111l1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ࿍"): log[bstack1l111l1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ࿎")],
        }
        if active:
            if active[bstack1l111l1_opy_ (u"ࠨࡶࡼࡴࡪ࠭࿏")] == bstack1l111l1_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ࿐"):
                log[bstack1l111l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ࿑")] = active[bstack1l111l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ࿒")]
            elif active[bstack1l111l1_opy_ (u"ࠬࡺࡹࡱࡧࠪ࿓")] == bstack1l111l1_opy_ (u"࠭ࡴࡦࡵࡷࠫ࿔"):
                log[bstack1l111l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ࿕")] = active[bstack1l111l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ࿖")]
        bstack1llll1lll1_opy_.bstack11l1l111_opy_([log])
    def __init__(self):
        self.messages = bstack1111l11lll_opy_()
        self._1111llll1l_opy_ = None
        self._11111l1lll_opy_ = None
        self._1111l1l11l_opy_ = OrderedDict()
        self.bstack111l11ll1l_opy_ = bstack111l1lll11_opy_(self.bstack111l1l11l1_opy_)
    @error_handler(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack1111l1ll11_opy_()
        if not self._1111l1l11l_opy_.get(attrs.get(bstack1l111l1_opy_ (u"ࠩ࡬ࡨࠬ࿗")), None):
            self._1111l1l11l_opy_[attrs.get(bstack1l111l1_opy_ (u"ࠪ࡭ࡩ࠭࿘"))] = {}
        bstack11111lllll_opy_ = bstack111l11l111_opy_(
                bstack1111l1111l_opy_=attrs.get(bstack1l111l1_opy_ (u"ࠫ࡮ࡪࠧ࿙")),
                name=name,
                started_at=bstack11llll1111_opy_(),
                file_path=os.path.relpath(attrs[bstack1l111l1_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬ࿚")], start=os.getcwd()) if attrs.get(bstack1l111l1_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭࿛")) != bstack1l111l1_opy_ (u"ࠧࠨ࿜") else bstack1l111l1_opy_ (u"ࠨࠩ࿝"),
                framework=bstack1l111l1_opy_ (u"ࠩࡕࡳࡧࡵࡴࠨ࿞")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack1l111l1_opy_ (u"ࠪ࡭ࡩ࠭࿟"), None)
        self._1111l1l11l_opy_[attrs.get(bstack1l111l1_opy_ (u"ࠫ࡮ࡪࠧ࿠"))][bstack1l111l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ࿡")] = bstack11111lllll_opy_
    @error_handler(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack1111l11ll1_opy_()
        self._111l111111_opy_(messages)
        with self._lock:
            for bstack1111l111l1_opy_ in self.bstack11111ll1ll_opy_:
                bstack1111l111l1_opy_[bstack1l111l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨ࿢")][bstack1l111l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭࿣")].extend(self.store[bstack1l111l1_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧ࿤")])
                bstack1llll1lll1_opy_.bstack1ll111llll_opy_(bstack1111l111l1_opy_)
            self.bstack11111ll1ll_opy_ = []
            self.store[bstack1l111l1_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭ࡡ࡫ࡳࡴࡱࡳࠨ࿥")] = []
    @error_handler(class_method=True)
    def start_test(self, name, attrs):
        self.bstack111l11ll1l_opy_.start()
        if not self._1111l1l11l_opy_.get(attrs.get(bstack1l111l1_opy_ (u"ࠪ࡭ࡩ࠭࿦")), None):
            self._1111l1l11l_opy_[attrs.get(bstack1l111l1_opy_ (u"ࠫ࡮ࡪࠧ࿧"))] = {}
        driver = bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ࿨"), None)
        bstack111l11l1l1_opy_ = bstack111l11l111_opy_(
            bstack1111l1111l_opy_=attrs.get(bstack1l111l1_opy_ (u"࠭ࡩࡥࠩ࿩")),
            name=name,
            started_at=bstack11llll1111_opy_(),
            file_path=os.path.relpath(attrs[bstack1l111l1_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ࿪")], start=os.getcwd()),
            scope=RobotHandler.bstack1111ll11l1_opy_(attrs.get(bstack1l111l1_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨ࿫"), None)),
            framework=bstack1l111l1_opy_ (u"ࠩࡕࡳࡧࡵࡴࠨ࿬"),
            tags=attrs[bstack1l111l1_opy_ (u"ࠪࡸࡦ࡭ࡳࠨ࿭")],
            hooks=self.store[bstack1l111l1_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡣ࡭ࡵ࡯࡬ࡵࠪ࿮")],
            bstack111l1llll1_opy_=bstack1llll1lll1_opy_.bstack111l1ll111_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack1l111l1_opy_ (u"ࠧࢁࡽࠡ࡞ࡱࠤࢀࢃࠢ࿯").format(bstack1l111l1_opy_ (u"ࠨࠠࠣ࿰").join(attrs[bstack1l111l1_opy_ (u"ࠧࡵࡣࡪࡷࠬ࿱")]), name) if attrs[bstack1l111l1_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭࿲")] else name
        )
        self._1111l1l11l_opy_[attrs.get(bstack1l111l1_opy_ (u"ࠩ࡬ࡨࠬ࿳"))][bstack1l111l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭࿴")] = bstack111l11l1l1_opy_
        threading.current_thread().current_test_uuid = bstack111l11l1l1_opy_.bstack1111lll1l1_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack1l111l1_opy_ (u"ࠫ࡮ࡪࠧ࿵"), None)
        self.bstack111l1l111l_opy_(bstack1l111l1_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭࿶"), bstack111l11l1l1_opy_)
    @error_handler(class_method=True)
    def end_test(self, name, attrs):
        self.bstack111l11ll1l_opy_.reset()
        bstack11111ll111_opy_ = bstack111l111l11_opy_.get(attrs.get(bstack1l111l1_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭࿷")), bstack1l111l1_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ࿸"))
        self._1111l1l11l_opy_[attrs.get(bstack1l111l1_opy_ (u"ࠨ࡫ࡧࠫ࿹"))][bstack1l111l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ࿺")].stop(time=bstack11llll1111_opy_(), duration=int(attrs.get(bstack1l111l1_opy_ (u"ࠪࡩࡱࡧࡰࡴࡧࡧࡸ࡮ࡳࡥࠨ࿻"), bstack1l111l1_opy_ (u"ࠫ࠵࠭࿼"))), result=Result(result=bstack11111ll111_opy_, exception=attrs.get(bstack1l111l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭࿽")), bstack111l111lll_opy_=[attrs.get(bstack1l111l1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ࿾"))]))
        self.bstack111l1l111l_opy_(bstack1l111l1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ࿿"), self._1111l1l11l_opy_[attrs.get(bstack1l111l1_opy_ (u"ࠨ࡫ࡧࠫက"))][bstack1l111l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬခ")], True)
        with self._lock:
            self.store[bstack1l111l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹࠧဂ")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @error_handler(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack1111l1ll11_opy_()
        current_test_id = bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡩ࠭ဃ"), None)
        bstack1111lll111_opy_ = current_test_id if bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡪࠧင"), None) else bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡴࡷ࡬ࡸࡪࡥࡩࡥࠩစ"), None)
        if attrs.get(bstack1l111l1_opy_ (u"ࠧࡵࡻࡳࡩࠬဆ"), bstack1l111l1_opy_ (u"ࠨࠩဇ")).lower() in [bstack1l111l1_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨဈ"), bstack1l111l1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬဉ")]:
            hook_type = bstack1111l1l111_opy_(attrs.get(bstack1l111l1_opy_ (u"ࠫࡹࡿࡰࡦࠩည")), bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩဋ"), None))
            hook_name = bstack1l111l1_opy_ (u"࠭ࡻࡾࠩဌ").format(attrs.get(bstack1l111l1_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧဍ"), bstack1l111l1_opy_ (u"ࠨࠩဎ")))
            if hook_type in [bstack1l111l1_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭ဏ"), bstack1l111l1_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡄࡐࡑ࠭တ")]:
                hook_name = bstack1l111l1_opy_ (u"ࠫࡠࢁࡽ࡞ࠢࡾࢁࠬထ").format(bstack1111l1lll1_opy_.get(hook_type), attrs.get(bstack1l111l1_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬဒ"), bstack1l111l1_opy_ (u"࠭ࠧဓ")))
            bstack1111l11l1l_opy_ = bstack111l11ll11_opy_(
                bstack1111l1111l_opy_=bstack1111lll111_opy_ + bstack1l111l1_opy_ (u"ࠧ࠮ࠩန") + attrs.get(bstack1l111l1_opy_ (u"ࠨࡶࡼࡴࡪ࠭ပ"), bstack1l111l1_opy_ (u"ࠩࠪဖ")).lower(),
                name=hook_name,
                started_at=bstack11llll1111_opy_(),
                file_path=os.path.relpath(attrs.get(bstack1l111l1_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪဗ")), start=os.getcwd()),
                framework=bstack1l111l1_opy_ (u"ࠫࡗࡵࡢࡰࡶࠪဘ"),
                tags=attrs[bstack1l111l1_opy_ (u"ࠬࡺࡡࡨࡵࠪမ")],
                scope=RobotHandler.bstack1111ll11l1_opy_(attrs.get(bstack1l111l1_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ယ"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack1111l11l1l_opy_.bstack1111lll1l1_opy_()
            threading.current_thread().current_hook_id = bstack1111lll111_opy_ + bstack1l111l1_opy_ (u"ࠧ࠮ࠩရ") + attrs.get(bstack1l111l1_opy_ (u"ࠨࡶࡼࡴࡪ࠭လ"), bstack1l111l1_opy_ (u"ࠩࠪဝ")).lower()
            with self._lock:
                self.store[bstack1l111l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧသ")] = [bstack1111l11l1l_opy_.bstack1111lll1l1_opy_()]
                if bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨဟ"), None):
                    self.store[bstack1l111l1_opy_ (u"ࠬࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࠩဠ")].append(bstack1111l11l1l_opy_.bstack1111lll1l1_opy_())
                else:
                    self.store[bstack1l111l1_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬအ")].append(bstack1111l11l1l_opy_.bstack1111lll1l1_opy_())
            if bstack1111lll111_opy_:
                self._1111l1l11l_opy_[bstack1111lll111_opy_ + bstack1l111l1_opy_ (u"ࠧ࠮ࠩဢ") + attrs.get(bstack1l111l1_opy_ (u"ࠨࡶࡼࡴࡪ࠭ဣ"), bstack1l111l1_opy_ (u"ࠩࠪဤ")).lower()] = { bstack1l111l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ဥ"): bstack1111l11l1l_opy_ }
            bstack1llll1lll1_opy_.bstack111l1l111l_opy_(bstack1l111l1_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬဦ"), bstack1111l11l1l_opy_)
        else:
            bstack111l1l11ll_opy_ = {
                bstack1l111l1_opy_ (u"ࠬ࡯ࡤࠨဧ"): uuid4().__str__(),
                bstack1l111l1_opy_ (u"࠭ࡴࡦࡺࡷࠫဨ"): bstack1l111l1_opy_ (u"ࠧࡼࡿࠣࡿࢂ࠭ဩ").format(attrs.get(bstack1l111l1_opy_ (u"ࠨ࡭ࡺࡲࡦࡳࡥࠨဪ")), attrs.get(bstack1l111l1_opy_ (u"ࠩࡤࡶ࡬ࡹࠧါ"), bstack1l111l1_opy_ (u"ࠪࠫာ"))) if attrs.get(bstack1l111l1_opy_ (u"ࠫࡦࡸࡧࡴࠩိ"), []) else attrs.get(bstack1l111l1_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬီ")),
                bstack1l111l1_opy_ (u"࠭ࡳࡵࡧࡳࡣࡦࡸࡧࡶ࡯ࡨࡲࡹ࠭ု"): attrs.get(bstack1l111l1_opy_ (u"ࠧࡢࡴࡪࡷࠬူ"), []),
                bstack1l111l1_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬေ"): bstack11llll1111_opy_(),
                bstack1l111l1_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩဲ"): bstack1l111l1_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫဳ"),
                bstack1l111l1_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩဴ"): attrs.get(bstack1l111l1_opy_ (u"ࠬࡪ࡯ࡤࠩဵ"), bstack1l111l1_opy_ (u"࠭ࠧံ"))
            }
            if attrs.get(bstack1l111l1_opy_ (u"ࠧ࡭࡫ࡥࡲࡦࡳࡥࠨ့"), bstack1l111l1_opy_ (u"ࠨࠩး")) != bstack1l111l1_opy_ (u"္ࠩࠪ"):
                bstack111l1l11ll_opy_[bstack1l111l1_opy_ (u"ࠪ࡯ࡪࡿࡷࡰࡴࡧ်ࠫ")] = attrs.get(bstack1l111l1_opy_ (u"ࠫࡱ࡯ࡢ࡯ࡣࡰࡩࠬျ"))
            if not self.bstack1111ll1l11_opy_:
                self._1111l1l11l_opy_[self._1111ll1111_opy_()][bstack1l111l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨြ")].add_step(bstack111l1l11ll_opy_)
                threading.current_thread().current_step_uuid = bstack111l1l11ll_opy_[bstack1l111l1_opy_ (u"࠭ࡩࡥࠩွ")]
            self.bstack1111ll1l11_opy_.append(bstack111l1l11ll_opy_)
    @error_handler(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack1111l11ll1_opy_()
        self._111l111111_opy_(messages)
        current_test_id = bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡥࠩှ"), None)
        bstack1111lll111_opy_ = current_test_id if current_test_id else bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡹ࡮ࡺࡥࡠ࡫ࡧࠫဿ"), None)
        bstack11111lll1l_opy_ = bstack111l111l11_opy_.get(attrs.get(bstack1l111l1_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ၀")), bstack1l111l1_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ၁"))
        bstack1111ll1l1l_opy_ = attrs.get(bstack1l111l1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ၂"))
        if bstack11111lll1l_opy_ != bstack1l111l1_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭၃") and not attrs.get(bstack1l111l1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ၄")) and self._1111llll1l_opy_:
            bstack1111ll1l1l_opy_ = self._1111llll1l_opy_
        bstack111l11lll1_opy_ = Result(result=bstack11111lll1l_opy_, exception=bstack1111ll1l1l_opy_, bstack111l111lll_opy_=[bstack1111ll1l1l_opy_])
        if attrs.get(bstack1l111l1_opy_ (u"ࠧࡵࡻࡳࡩࠬ၅"), bstack1l111l1_opy_ (u"ࠨࠩ၆")).lower() in [bstack1l111l1_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ၇"), bstack1l111l1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬ၈")]:
            bstack1111lll111_opy_ = current_test_id if current_test_id else bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡹࡵࡪࡶࡨࡣ࡮ࡪࠧ၉"), None)
            if bstack1111lll111_opy_:
                bstack111l1l1l1l_opy_ = bstack1111lll111_opy_ + bstack1l111l1_opy_ (u"ࠧ࠳ࠢ၊") + attrs.get(bstack1l111l1_opy_ (u"࠭ࡴࡺࡲࡨࠫ။"), bstack1l111l1_opy_ (u"ࠧࠨ၌")).lower()
                self._1111l1l11l_opy_[bstack111l1l1l1l_opy_][bstack1l111l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ၍")].stop(time=bstack11llll1111_opy_(), duration=int(attrs.get(bstack1l111l1_opy_ (u"ࠩࡨࡰࡦࡶࡳࡦࡦࡷ࡭ࡲ࡫ࠧ၎"), bstack1l111l1_opy_ (u"ࠪ࠴ࠬ၏"))), result=bstack111l11lll1_opy_)
                bstack1llll1lll1_opy_.bstack111l1l111l_opy_(bstack1l111l1_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ၐ"), self._1111l1l11l_opy_[bstack111l1l1l1l_opy_][bstack1l111l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨၑ")])
        else:
            bstack1111lll111_opy_ = current_test_id if current_test_id else bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤ࡯ࡤࠨၒ"), None)
            if bstack1111lll111_opy_ and len(self.bstack1111ll1l11_opy_) == 1:
                current_step_uuid = bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡵࡷࡩࡵࡥࡵࡶ࡫ࡧࠫၓ"), None)
                self._1111l1l11l_opy_[bstack1111lll111_opy_][bstack1l111l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫၔ")].bstack111l11l1ll_opy_(current_step_uuid, duration=int(attrs.get(bstack1l111l1_opy_ (u"ࠩࡨࡰࡦࡶࡳࡦࡦࡷ࡭ࡲ࡫ࠧၕ"), bstack1l111l1_opy_ (u"ࠪ࠴ࠬၖ"))), result=bstack111l11lll1_opy_)
            else:
                self.bstack1111ll1ll1_opy_(attrs)
            self.bstack1111ll1l11_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack1l111l1_opy_ (u"ࠫ࡭ࡺ࡭࡭ࠩၗ"), bstack1l111l1_opy_ (u"ࠬࡴ࡯ࠨၘ")) == bstack1l111l1_opy_ (u"࠭ࡹࡦࡵࠪၙ"):
                return
            self.messages.push(message)
            logs = []
            if bstack11ll11l11_opy_.bstack111l1l1ll1_opy_():
                logs.append({
                    bstack1l111l1_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪၚ"): bstack11llll1111_opy_(),
                    bstack1l111l1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩၛ"): message.get(bstack1l111l1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪၜ")),
                    bstack1l111l1_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩၝ"): message.get(bstack1l111l1_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪၞ")),
                    **bstack11ll11l11_opy_.bstack111l1l1ll1_opy_()
                })
                if len(logs) > 0:
                    bstack1llll1lll1_opy_.bstack11l1l111_opy_(logs)
        except Exception as err:
            pass
    def close(self):
        bstack1llll1lll1_opy_.bstack111l1111l1_opy_()
    def bstack1111ll1ll1_opy_(self, bstack1111lll11l_opy_):
        if not bstack11ll11l11_opy_.bstack111l1l1ll1_opy_():
            return
        kwname = bstack1l111l1_opy_ (u"ࠬࢁࡽࠡࡽࢀࠫၟ").format(bstack1111lll11l_opy_.get(bstack1l111l1_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭ၠ")), bstack1111lll11l_opy_.get(bstack1l111l1_opy_ (u"ࠧࡢࡴࡪࡷࠬၡ"), bstack1l111l1_opy_ (u"ࠨࠩၢ"))) if bstack1111lll11l_opy_.get(bstack1l111l1_opy_ (u"ࠩࡤࡶ࡬ࡹࠧၣ"), []) else bstack1111lll11l_opy_.get(bstack1l111l1_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪၤ"))
        error_message = bstack1l111l1_opy_ (u"ࠦࡰࡽ࡮ࡢ࡯ࡨ࠾ࠥࡢࠢࡼ࠲ࢀࡠࠧࠦࡼࠡࡵࡷࡥࡹࡻࡳ࠻ࠢ࡟ࠦࢀ࠷ࡽ࡝ࠤࠣࢀࠥ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮࠻ࠢ࡟ࠦࢀ࠸ࡽ࡝ࠤࠥၥ").format(kwname, bstack1111lll11l_opy_.get(bstack1l111l1_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬၦ")), str(bstack1111lll11l_opy_.get(bstack1l111l1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧၧ"))))
        bstack1111llllll_opy_ = bstack1l111l1_opy_ (u"ࠢ࡬ࡹࡱࡥࡲ࡫࠺ࠡ࡞ࠥࡿ࠵ࢃ࡜ࠣࠢࡿࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࡢࠢࡼ࠳ࢀࡠࠧࠨၨ").format(kwname, bstack1111lll11l_opy_.get(bstack1l111l1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨၩ")))
        bstack1111l111ll_opy_ = error_message if bstack1111lll11l_opy_.get(bstack1l111l1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪၪ")) else bstack1111llllll_opy_
        bstack11111ll1l1_opy_ = {
            bstack1l111l1_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ၫ"): self.bstack1111ll1l11_opy_[-1].get(bstack1l111l1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨၬ"), bstack11llll1111_opy_()),
            bstack1l111l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ၭ"): bstack1111l111ll_opy_,
            bstack1l111l1_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬၮ"): bstack1l111l1_opy_ (u"ࠧࡆࡔࡕࡓࡗ࠭ၯ") if bstack1111lll11l_opy_.get(bstack1l111l1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨၰ")) == bstack1l111l1_opy_ (u"ࠩࡉࡅࡎࡒࠧၱ") else bstack1l111l1_opy_ (u"ࠪࡍࡓࡌࡏࠨၲ"),
            **bstack11ll11l11_opy_.bstack111l1l1ll1_opy_()
        }
        bstack1llll1lll1_opy_.bstack11l1l111_opy_([bstack11111ll1l1_opy_])
    def _1111ll1111_opy_(self):
        for bstack1111l1111l_opy_ in reversed(self._1111l1l11l_opy_):
            bstack1111ll111l_opy_ = bstack1111l1111l_opy_
            data = self._1111l1l11l_opy_[bstack1111l1111l_opy_][bstack1l111l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧၳ")]
            if isinstance(data, bstack111l11ll11_opy_):
                if not bstack1l111l1_opy_ (u"ࠬࡋࡁࡄࡊࠪၴ") in data.bstack1111l11111_opy_():
                    return bstack1111ll111l_opy_
            else:
                return bstack1111ll111l_opy_
    def _111l111111_opy_(self, messages):
        try:
            bstack1111lllll1_opy_ = BuiltIn().get_variable_value(bstack1l111l1_opy_ (u"ࠨࠤࡼࡎࡒࡋࠥࡒࡅࡗࡇࡏࢁࠧၵ")) in (bstack111l11111l_opy_.DEBUG, bstack111l11111l_opy_.TRACE)
            for message, bstack1111ll11ll_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack1l111l1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨၶ"))
                level = message.get(bstack1l111l1_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧၷ"))
                if level == bstack111l11111l_opy_.FAIL:
                    self._1111llll1l_opy_ = name or self._1111llll1l_opy_
                    self._11111l1lll_opy_ = bstack1111ll11ll_opy_.get(bstack1l111l1_opy_ (u"ࠤࡰࡩࡸࡹࡡࡨࡧࠥၸ")) if bstack1111lllll1_opy_ and bstack1111ll11ll_opy_ else self._11111l1lll_opy_
        except:
            pass
    @classmethod
    def bstack111l1l111l_opy_(self, event: str, bstack1111l1ll1l_opy_: bstack111l1111ll_opy_, bstack1111l1l1l1_opy_=False):
        if event == bstack1l111l1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬၹ"):
            bstack1111l1ll1l_opy_.set(hooks=self.store[bstack1l111l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࠨၺ")])
        if event == bstack1l111l1_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ࠭ၻ"):
            event = bstack1l111l1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨၼ")
        if bstack1111l1l1l1_opy_:
            bstack1111l11l11_opy_ = {
                bstack1l111l1_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫၽ"): event,
                bstack1111l1ll1l_opy_.bstack1111ll1lll_opy_(): bstack1111l1ll1l_opy_.bstack11111ll11l_opy_(event)
            }
            with self._lock:
                self.bstack11111ll1ll_opy_.append(bstack1111l11l11_opy_)
        else:
            bstack1llll1lll1_opy_.bstack111l1l111l_opy_(event, bstack1111l1ll1l_opy_)
class bstack1111l11lll_opy_:
    def __init__(self):
        self._1111l1llll_opy_ = []
    def bstack1111l1ll11_opy_(self):
        self._1111l1llll_opy_.append([])
    def bstack1111l11ll1_opy_(self):
        return self._1111l1llll_opy_.pop() if self._1111l1llll_opy_ else list()
    def push(self, message):
        self._1111l1llll_opy_[-1].append(message) if self._1111l1llll_opy_ else self._1111l1llll_opy_.append([message])
class bstack111l11111l_opy_:
    FAIL = bstack1l111l1_opy_ (u"ࠨࡈࡄࡍࡑ࠭ၾ")
    ERROR = bstack1l111l1_opy_ (u"ࠩࡈࡖࡗࡕࡒࠨၿ")
    WARNING = bstack1l111l1_opy_ (u"࡛ࠪࡆࡘࡎࠨႀ")
    bstack1111llll11_opy_ = bstack1l111l1_opy_ (u"ࠫࡎࡔࡆࡐࠩႁ")
    DEBUG = bstack1l111l1_opy_ (u"ࠬࡊࡅࡃࡗࡊࠫႂ")
    TRACE = bstack1l111l1_opy_ (u"࠭ࡔࡓࡃࡆࡉࠬႃ")
    bstack11111l1ll1_opy_ = [FAIL, ERROR]
def bstack1111lll1ll_opy_(bstack11111llll1_opy_):
    if not bstack11111llll1_opy_:
        return None
    if bstack11111llll1_opy_.get(bstack1l111l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪႄ"), None):
        return getattr(bstack11111llll1_opy_[bstack1l111l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫႅ")], bstack1l111l1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧႆ"), None)
    return bstack11111llll1_opy_.get(bstack1l111l1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨႇ"), None)
def bstack1111l1l111_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack1l111l1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪႈ"), bstack1l111l1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧႉ")]:
        return
    if hook_type.lower() == bstack1l111l1_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬႊ"):
        if current_test_uuid is None:
            return bstack1l111l1_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫႋ")
        else:
            return bstack1l111l1_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭ႌ")
    elif hook_type.lower() == bstack1l111l1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱႍࠫ"):
        if current_test_uuid is None:
            return bstack1l111l1_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡄࡐࡑ࠭ႎ")
        else:
            return bstack1l111l1_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨႏ")