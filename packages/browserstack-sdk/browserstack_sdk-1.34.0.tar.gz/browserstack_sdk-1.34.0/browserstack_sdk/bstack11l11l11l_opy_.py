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
import threading
import os
import logging
from uuid import uuid4
from bstack_utils.bstack111l11l1l1_opy_ import bstack111l11ll11_opy_, bstack111l11l111_opy_
from bstack_utils.bstack111l1ll11l_opy_ import bstack11ll11l11_opy_
from bstack_utils.helper import bstack1l1l1l111_opy_, bstack11llll1111_opy_, Result
from bstack_utils.bstack111l11l11l_opy_ import bstack1llll1lll1_opy_
from bstack_utils.capture import bstack111l1lll11_opy_
from bstack_utils.constants import *
logger = logging.getLogger(__name__)
class bstack11l11l11l_opy_:
    def __init__(self):
        self.bstack111l11ll1l_opy_ = bstack111l1lll11_opy_(self.bstack111l1l11l1_opy_)
        self.tests = {}
    @staticmethod
    def bstack111l1l11l1_opy_(log):
        if not (log[bstack1l111l1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩས")] and log[bstack1l111l1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪཧ")].strip()):
            return
        active = bstack11ll11l11_opy_.bstack111l1l1ll1_opy_()
        log = {
            bstack1l111l1_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩཨ"): log[bstack1l111l1_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪཀྵ")],
            bstack1l111l1_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨཪ"): bstack11llll1111_opy_(),
            bstack1l111l1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧཫ"): log[bstack1l111l1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨཬ")],
        }
        if active:
            if active[bstack1l111l1_opy_ (u"ࠨࡶࡼࡴࡪ࠭཭")] == bstack1l111l1_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ཮"):
                log[bstack1l111l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ཯")] = active[bstack1l111l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ཰")]
            elif active[bstack1l111l1_opy_ (u"ࠬࡺࡹࡱࡧཱࠪ")] == bstack1l111l1_opy_ (u"࠭ࡴࡦࡵࡷིࠫ"):
                log[bstack1l111l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪཱིࠧ")] = active[bstack1l111l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨུ")]
        bstack1llll1lll1_opy_.bstack11l1l111_opy_([log])
    def start_test(self, attrs):
        test_uuid = uuid4().__str__()
        self.tests[test_uuid] = {}
        self.bstack111l11ll1l_opy_.start()
        driver = bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨཱུ"), None)
        bstack111l11l1l1_opy_ = bstack111l11l111_opy_(
            name=attrs.scenario.name,
            uuid=test_uuid,
            started_at=bstack11llll1111_opy_(),
            file_path=attrs.feature.filename,
            result=bstack1l111l1_opy_ (u"ࠥࡴࡪࡴࡤࡪࡰࡪࠦྲྀ"),
            framework=bstack1l111l1_opy_ (u"ࠫࡇ࡫ࡨࡢࡸࡨࠫཷ"),
            scope=[attrs.feature.name],
            bstack111l1llll1_opy_=bstack1llll1lll1_opy_.bstack111l1ll111_opy_(driver) if driver and driver.session_id else {},
            meta={},
            tags=attrs.scenario.tags
        )
        self.tests[test_uuid][bstack1l111l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨླྀ")] = bstack111l11l1l1_opy_
        threading.current_thread().current_test_uuid = test_uuid
        bstack1llll1lll1_opy_.bstack111l1l111l_opy_(bstack1l111l1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧཹ"), bstack111l11l1l1_opy_)
    def end_test(self, attrs):
        bstack111l1ll1l1_opy_ = {
            bstack1l111l1_opy_ (u"ࠢ࡯ࡣࡰࡩེࠧ"): attrs.feature.name,
            bstack1l111l1_opy_ (u"ࠣࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳࠨཻ"): attrs.feature.description
        }
        current_test_uuid = threading.current_thread().current_test_uuid
        bstack111l11l1l1_opy_ = self.tests[current_test_uuid][bstack1l111l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥོࠬ")]
        meta = {
            bstack1l111l1_opy_ (u"ࠥࡪࡪࡧࡴࡶࡴࡨཽࠦ"): bstack111l1ll1l1_opy_,
            bstack1l111l1_opy_ (u"ࠦࡸࡺࡥࡱࡵࠥཾ"): bstack111l11l1l1_opy_.meta.get(bstack1l111l1_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫཿ"), []),
            bstack1l111l1_opy_ (u"ࠨࡳࡤࡧࡱࡥࡷ࡯࡯ྀࠣ"): {
                bstack1l111l1_opy_ (u"ࠢ࡯ࡣࡰࡩཱྀࠧ"): attrs.feature.scenarios[0].name if len(attrs.feature.scenarios) else None
            }
        }
        bstack111l11l1l1_opy_.bstack111l1lll1l_opy_(meta)
        bstack111l11l1l1_opy_.bstack111l1l1111_opy_(bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ࠭ྂ"), []))
        bstack111l111l1l_opy_, exception = self._111l1ll1ll_opy_(attrs)
        status = bstack1l111l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩྃ") if attrs.status.name.lower() == bstack1l111l1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳ྄ࠩ") else attrs.status.name.lower()
        bstack111l11lll1_opy_ = Result(result=status, exception=exception, bstack111l111lll_opy_=[bstack111l111l1l_opy_])
        self.tests[threading.current_thread().current_test_uuid][bstack1l111l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ྅")].stop(time=bstack11llll1111_opy_(), duration=int(attrs.duration)*1000, result=bstack111l11lll1_opy_)
        bstack1llll1lll1_opy_.bstack111l1l111l_opy_(bstack1l111l1_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ྆"), self.tests[threading.current_thread().current_test_uuid][bstack1l111l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ྇")])
    def bstack1l1ll1l1l_opy_(self, attrs):
        bstack111l1l11ll_opy_ = {
            bstack1l111l1_opy_ (u"ࠧࡪࡦࠪྈ"): uuid4().__str__(),
            bstack1l111l1_opy_ (u"ࠨ࡭ࡨࡽࡼࡵࡲࡥࠩྉ"): attrs.keyword,
            bstack1l111l1_opy_ (u"ࠩࡶࡸࡪࡶ࡟ࡢࡴࡪࡹࡲ࡫࡮ࡵࠩྊ"): [],
            bstack1l111l1_opy_ (u"ࠪࡸࡪࡾࡴࠨྋ"): attrs.name,
            bstack1l111l1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨྌ"): bstack11llll1111_opy_(),
            bstack1l111l1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬྍ"): bstack1l111l1_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧྎ"),
            bstack1l111l1_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬྏ"): bstack1l111l1_opy_ (u"ࠨࠩྐ")
        }
        self.tests[threading.current_thread().current_test_uuid][bstack1l111l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬྑ")].add_step(bstack111l1l11ll_opy_)
        threading.current_thread().current_step_uuid = bstack111l1l11ll_opy_[bstack1l111l1_opy_ (u"ࠪ࡭ࡩ࠭ྒ")]
    def bstack1ll1llll11_opy_(self, attrs):
        current_test_id = bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨྒྷ"), None)
        current_step_uuid = bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡵࡧࡳࡣࡺࡻࡩࡥࠩྔ"), None)
        bstack111l111l1l_opy_, exception = self._111l1ll1ll_opy_(attrs)
        status = bstack1l111l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ྕ") if attrs.status.name.lower() == bstack1l111l1_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ྖ") else attrs.status.name.lower()
        bstack111l11lll1_opy_ = Result(result=status, exception=exception, bstack111l111lll_opy_=[bstack111l111l1l_opy_])
        self.tests[current_test_id][bstack1l111l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫྗ")].bstack111l11l1ll_opy_(current_step_uuid, duration=int(attrs.duration)*1000, result=bstack111l11lll1_opy_)
        threading.current_thread().current_step_uuid = None
    def bstack111lllll11_opy_(self, name, attrs):
        try:
            bstack111l11llll_opy_ = os.environ.get(bstack1l111l1_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡡࡖࡈࡐࡥࡄࡆࡈࡄ࡙ࡑ࡚࡟ࡉࡑࡒࡏࡘ࠭྘"), bstack1l111l1_opy_ (u"ࠪࠫྙ")).split(bstack1l111l1_opy_ (u"ࠫ࠱࠭ྚ"))
            if name in bstack111l11llll_opy_ and bstack111l11llll_opy_ != [bstack1l111l1_opy_ (u"ࠬ࠭ྛ")]:
                return
            bstack111l1l1lll_opy_ = uuid4().__str__()
            self.tests[bstack111l1l1lll_opy_] = {}
            self.bstack111l11ll1l_opy_.start()
            scopes = []
            driver = bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬྜ"), None)
            current_thread = threading.current_thread()
            if not hasattr(current_thread, bstack1l111l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࠬྜྷ")):
                current_thread.current_test_hooks = []
            current_thread.current_test_hooks.append(bstack111l1l1lll_opy_)
            if name in [bstack1l111l1_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠧྞ"), bstack1l111l1_opy_ (u"ࠤࡤࡪࡹ࡫ࡲࡠࡣ࡯ࡰࠧྟ")]:
                file_path = os.path.join(attrs.config.base_dir, attrs.config.environment_file)
                scopes = [attrs.config.environment_file]
            elif name in [bstack1l111l1_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡪࡪࡧࡴࡶࡴࡨࠦྠ"), bstack1l111l1_opy_ (u"ࠦࡦ࡬ࡴࡦࡴࡢࡪࡪࡧࡴࡶࡴࡨࠦྡ")]:
                file_path = attrs.filename
                scopes = [attrs.name]
            else:
                file_path = attrs.filename
                if hasattr(attrs, bstack1l111l1_opy_ (u"ࠬ࡬ࡥࡢࡶࡸࡶࡪ࠭ྡྷ")):
                    scopes =  [attrs.feature.name]
            hook_data = bstack111l11ll11_opy_(
                name=name,
                uuid=bstack111l1l1lll_opy_,
                started_at=bstack11llll1111_opy_(),
                file_path=file_path,
                framework=bstack1l111l1_opy_ (u"ࠨࡂࡦࡪࡤࡺࡪࠨྣ"),
                bstack111l1llll1_opy_=bstack1llll1lll1_opy_.bstack111l1ll111_opy_(driver) if driver and driver.session_id else {},
                scope=scopes,
                result=bstack1l111l1_opy_ (u"ࠢࡱࡧࡱࡨ࡮ࡴࡧࠣྤ"),
                hook_type=name
            )
            self.tests[bstack111l1l1lll_opy_][bstack1l111l1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡤࡢࡶࡤࠦྥ")] = hook_data
            current_test_id = bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"ࠤࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩࠨྦ"), None)
            if current_test_id:
                hook_data.bstack111l1lllll_opy_(current_test_id)
            if name == bstack1l111l1_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠢྦྷ"):
                threading.current_thread().before_all_hook_uuid = bstack111l1l1lll_opy_
            threading.current_thread().current_hook_uuid = bstack111l1l1lll_opy_
            bstack1llll1lll1_opy_.bstack111l1l111l_opy_(bstack1l111l1_opy_ (u"ࠦࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠧྨ"), hook_data)
        except Exception as e:
            logger.debug(bstack1l111l1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡴࡩࡣࡶࡴࡵࡩࡩࠦࡩ࡯ࠢࡶࡸࡦࡸࡴࠡࡪࡲࡳࡰࠦࡥࡷࡧࡱࡸࡸ࠲ࠠࡩࡱࡲ࡯ࠥࡴࡡ࡮ࡧ࠽ࠤࠪࡹࠬࠡࡧࡵࡶࡴࡸ࠺ࠡࠧࡶࠦྩ"), name, e)
    def bstack1llll1lll_opy_(self, attrs):
        hook_name = getattr(attrs, bstack1l111l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠩྪ"), None) or (hasattr(self, bstack1l111l1_opy_ (u"ࠧࡠࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬྫ")) and self._111l111ll1_opy_)
        bstack111l11llll_opy_ = os.environ.get(bstack1l111l1_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡕࡇࡏࡤࡊࡅࡇࡃࡘࡐ࡙ࡥࡈࡐࡑࡎࡗࠬྫྷ"), bstack1l111l1_opy_ (u"ࠩࠪྭ")).split(bstack1l111l1_opy_ (u"ࠪ࠰ࠬྮ"))
        if hook_name in bstack111l11llll_opy_ and bstack111l11llll_opy_ != [bstack1l111l1_opy_ (u"ࠫࠬྯ")]:
            return
        bstack111l1l1l1l_opy_ = bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩྰ"), None)
        hook_data = self.tests[bstack111l1l1l1l_opy_][bstack1l111l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩྱ")]
        status = bstack1l111l1_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢྲ")
        exception = None
        bstack111l111l1l_opy_ = None
        if hook_data.name == bstack1l111l1_opy_ (u"ࠣࡣࡩࡸࡪࡸ࡟ࡢ࡮࡯ࠦླ"):
            self.bstack111l11ll1l_opy_.reset()
            bstack111l1l1l11_opy_ = self.tests[bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩྴ"), None)][bstack1l111l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ྵ")].result.result
            if bstack111l1l1l11_opy_ == bstack1l111l1_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦྶ"):
                if attrs.hook_failures == 1:
                    status = bstack1l111l1_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧྷ")
                elif attrs.hook_failures == 2:
                    status = bstack1l111l1_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨྸ")
            elif attrs.aborted:
                status = bstack1l111l1_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢྐྵ")
            threading.current_thread().before_all_hook_uuid = None
        else:
            if hook_data.name == bstack1l111l1_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠬྺ") and attrs.hook_failures == 1:
                status = bstack1l111l1_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤྻ")
            elif hasattr(attrs, bstack1l111l1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡡࡰࡩࡸࡹࡡࡨࡧࠪྼ")) and attrs.error_message:
                status = bstack1l111l1_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ྽")
            bstack111l111l1l_opy_, exception = self._111l1ll1ll_opy_(attrs)
        bstack111l11lll1_opy_ = Result(result=status, exception=exception, bstack111l111lll_opy_=[bstack111l111l1l_opy_])
        hook_data.stop(time=bstack11llll1111_opy_(), duration=0, result=bstack111l11lll1_opy_)
        bstack1llll1lll1_opy_.bstack111l1l111l_opy_(bstack1l111l1_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ྾"), self.tests[bstack111l1l1l1l_opy_][bstack1l111l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ྿")])
        threading.current_thread().current_hook_uuid = None
    def _111l1ll1ll_opy_(self, attrs):
        try:
            import traceback
            bstack11l1ll111l_opy_ = traceback.format_tb(attrs.exc_traceback)
            bstack111l111l1l_opy_ = bstack11l1ll111l_opy_[-1] if bstack11l1ll111l_opy_ else None
            exception = attrs.exception
        except Exception:
            logger.debug(bstack1l111l1_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦ࡯ࡤࡥࡸࡶࡷ࡫ࡤࠡࡹ࡫࡭ࡱ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡥࡸࡷࡹࡵ࡭ࠡࡶࡵࡥࡨ࡫ࡢࡢࡥ࡮ࠦ࿀"))
            bstack111l111l1l_opy_ = None
            exception = None
        return bstack111l111l1l_opy_, exception