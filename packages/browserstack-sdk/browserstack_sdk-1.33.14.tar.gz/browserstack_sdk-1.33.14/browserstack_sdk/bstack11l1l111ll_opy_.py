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
import threading
import os
import logging
from uuid import uuid4
from bstack_utils.bstack111l1l11l1_opy_ import bstack111ll11111_opy_, bstack111l1l11ll_opy_
from bstack_utils.bstack111l1l1111_opy_ import bstack1l1l1lllll_opy_
from bstack_utils.helper import bstack1ll1ll11ll_opy_, bstack11ll11ll1l_opy_, Result
from bstack_utils.bstack111l1l1l1l_opy_ import bstack111ll1lll1_opy_
from bstack_utils.capture import bstack111l1l1l11_opy_
from bstack_utils.constants import *
logger = logging.getLogger(__name__)
class bstack11l1l111ll_opy_:
    def __init__(self):
        self.bstack111l1l1lll_opy_ = bstack111l1l1l11_opy_(self.bstack111ll111l1_opy_)
        self.tests = {}
    @staticmethod
    def bstack111ll111l1_opy_(log):
        if not (log[bstack1l11l1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫན")] and log[bstack1l11l1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬཔ")].strip()):
            return
        active = bstack1l1l1lllll_opy_.bstack111ll1111l_opy_()
        log = {
            bstack1l11l1l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫཕ"): log[bstack1l11l1l_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬབ")],
            bstack1l11l1l_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪབྷ"): bstack11ll11ll1l_opy_(),
            bstack1l11l1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩམ"): log[bstack1l11l1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪཙ")],
        }
        if active:
            if active[bstack1l11l1l_opy_ (u"ࠪࡸࡾࡶࡥࠨཚ")] == bstack1l11l1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩཛ"):
                log[bstack1l11l1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬཛྷ")] = active[bstack1l11l1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ཝ")]
            elif active[bstack1l11l1l_opy_ (u"ࠧࡵࡻࡳࡩࠬཞ")] == bstack1l11l1l_opy_ (u"ࠨࡶࡨࡷࡹ࠭ཟ"):
                log[bstack1l11l1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩའ")] = active[bstack1l11l1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪཡ")]
        bstack111ll1lll1_opy_.bstack1l1111l11_opy_([log])
    def start_test(self, attrs):
        test_uuid = uuid4().__str__()
        self.tests[test_uuid] = {}
        self.bstack111l1l1lll_opy_.start()
        driver = bstack1ll1ll11ll_opy_(threading.current_thread(), bstack1l11l1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪར"), None)
        bstack111l1l11l1_opy_ = bstack111l1l11ll_opy_(
            name=attrs.scenario.name,
            uuid=test_uuid,
            started_at=bstack11ll11ll1l_opy_(),
            file_path=attrs.feature.filename,
            result=bstack1l11l1l_opy_ (u"ࠧࡶࡥ࡯ࡦ࡬ࡲ࡬ࠨལ"),
            framework=bstack1l11l1l_opy_ (u"࠭ࡂࡦࡪࡤࡺࡪ࠭ཤ"),
            scope=[attrs.feature.name],
            bstack111ll11lll_opy_=bstack111ll1lll1_opy_.bstack111l1ll1ll_opy_(driver) if driver and driver.session_id else {},
            meta={},
            tags=attrs.scenario.tags
        )
        self.tests[test_uuid][bstack1l11l1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪཥ")] = bstack111l1l11l1_opy_
        threading.current_thread().current_test_uuid = test_uuid
        bstack111ll1lll1_opy_.bstack111ll11l11_opy_(bstack1l11l1l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩས"), bstack111l1l11l1_opy_)
    def end_test(self, attrs):
        bstack111ll11ll1_opy_ = {
            bstack1l11l1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢཧ"): attrs.feature.name,
            bstack1l11l1l_opy_ (u"ࠥࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠣཨ"): attrs.feature.description
        }
        current_test_uuid = threading.current_thread().current_test_uuid
        bstack111l1l11l1_opy_ = self.tests[current_test_uuid][bstack1l11l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧཀྵ")]
        meta = {
            bstack1l11l1l_opy_ (u"ࠧ࡬ࡥࡢࡶࡸࡶࡪࠨཪ"): bstack111ll11ll1_opy_,
            bstack1l11l1l_opy_ (u"ࠨࡳࡵࡧࡳࡷࠧཫ"): bstack111l1l11l1_opy_.meta.get(bstack1l11l1l_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ཬ"), []),
            bstack1l11l1l_opy_ (u"ࠣࡵࡦࡩࡳࡧࡲࡪࡱࠥ཭"): {
                bstack1l11l1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ཮"): attrs.feature.scenarios[0].name if len(attrs.feature.scenarios) else None
            }
        }
        bstack111l1l11l1_opy_.bstack111l1lll1l_opy_(meta)
        bstack111l1l11l1_opy_.bstack111l1l1ll1_opy_(bstack1ll1ll11ll_opy_(threading.current_thread(), bstack1l11l1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࠨ཯"), []))
        bstack111l1llll1_opy_, exception = self._111l1lll11_opy_(attrs)
        bstack111ll111ll_opy_ = Result(result=attrs.status.name, exception=exception, bstack111l1ll11l_opy_=[bstack111l1llll1_opy_])
        self.tests[threading.current_thread().current_test_uuid][bstack1l11l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ཰")].stop(time=bstack11ll11ll1l_opy_(), duration=int(attrs.duration)*1000, result=bstack111ll111ll_opy_)
        bstack111ll1lll1_opy_.bstack111ll11l11_opy_(bstack1l11l1l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪཱࠧ"), self.tests[threading.current_thread().current_test_uuid][bstack1l11l1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢིࠩ")])
    def bstack1l1lll111_opy_(self, attrs):
        bstack111l1ll1l1_opy_ = {
            bstack1l11l1l_opy_ (u"ࠧࡪࡦཱིࠪ"): uuid4().__str__(),
            bstack1l11l1l_opy_ (u"ࠨ࡭ࡨࡽࡼࡵࡲࡥུࠩ"): attrs.keyword,
            bstack1l11l1l_opy_ (u"ࠩࡶࡸࡪࡶ࡟ࡢࡴࡪࡹࡲ࡫࡮ࡵཱུࠩ"): [],
            bstack1l11l1l_opy_ (u"ࠪࡸࡪࡾࡴࠨྲྀ"): attrs.name,
            bstack1l11l1l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨཷ"): bstack11ll11ll1l_opy_(),
            bstack1l11l1l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬླྀ"): bstack1l11l1l_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧཹ"),
            bstack1l11l1l_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲེࠬ"): bstack1l11l1l_opy_ (u"ࠨཻࠩ")
        }
        self.tests[threading.current_thread().current_test_uuid][bstack1l11l1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥོࠬ")].add_step(bstack111l1ll1l1_opy_)
        threading.current_thread().current_step_uuid = bstack111l1ll1l1_opy_[bstack1l11l1l_opy_ (u"ࠪ࡭ࡩཽ࠭")]
    def bstack1l11ll1lll_opy_(self, attrs):
        current_test_id = bstack1ll1ll11ll_opy_(threading.current_thread(), bstack1l11l1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨཾ"), None)
        current_step_uuid = bstack1ll1ll11ll_opy_(threading.current_thread(), bstack1l11l1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡵࡧࡳࡣࡺࡻࡩࡥࠩཿ"), None)
        bstack111l1llll1_opy_, exception = self._111l1lll11_opy_(attrs)
        bstack111ll111ll_opy_ = Result(result=attrs.status.name, exception=exception, bstack111l1ll11l_opy_=[bstack111l1llll1_opy_])
        self.tests[current_test_id][bstack1l11l1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢྀࠩ")].bstack111l1l111l_opy_(current_step_uuid, duration=int(attrs.duration)*1000, result=bstack111ll111ll_opy_)
        threading.current_thread().current_step_uuid = None
    def bstack1l11llll1l_opy_(self, name, attrs):
        try:
            bstack111l1ll111_opy_ = uuid4().__str__()
            self.tests[bstack111l1ll111_opy_] = {}
            self.bstack111l1l1lll_opy_.start()
            scopes = []
            driver = bstack1ll1ll11ll_opy_(threading.current_thread(), bstack1l11l1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷཱྀ࠭"), None)
            current_thread = threading.current_thread()
            if not hasattr(current_thread, bstack1l11l1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ࠭ྂ")):
                current_thread.current_test_hooks = []
            current_thread.current_test_hooks.append(bstack111l1ll111_opy_)
            if name in [bstack1l11l1l_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࠨྃ"), bstack1l11l1l_opy_ (u"ࠥࡥ࡫ࡺࡥࡳࡡࡤࡰࡱࠨ྄")]:
                file_path = os.path.join(attrs.config.base_dir, attrs.config.environment_file)
                scopes = [attrs.config.environment_file]
            elif name in [bstack1l11l1l_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩࠧ྅"), bstack1l11l1l_opy_ (u"ࠧࡧࡦࡵࡧࡵࡣ࡫࡫ࡡࡵࡷࡵࡩࠧ྆")]:
                file_path = attrs.filename
                scopes = [attrs.name]
            else:
                file_path = attrs.filename
                if hasattr(attrs, bstack1l11l1l_opy_ (u"࠭ࡦࡦࡣࡷࡹࡷ࡫ࠧ྇")):
                    scopes =  [attrs.feature.name]
            hook_data = bstack111ll11111_opy_(
                name=name,
                uuid=bstack111l1ll111_opy_,
                started_at=bstack11ll11ll1l_opy_(),
                file_path=file_path,
                framework=bstack1l11l1l_opy_ (u"ࠢࡃࡧ࡫ࡥࡻ࡫ࠢྈ"),
                bstack111ll11lll_opy_=bstack111ll1lll1_opy_.bstack111l1ll1ll_opy_(driver) if driver and driver.session_id else {},
                scope=scopes,
                result=bstack1l11l1l_opy_ (u"ࠣࡲࡨࡲࡩ࡯࡮ࡨࠤྉ"),
                hook_type=name
            )
            self.tests[bstack111l1ll111_opy_][bstack1l11l1l_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠧྊ")] = hook_data
            current_test_id = bstack1ll1ll11ll_opy_(threading.current_thread(), bstack1l11l1l_opy_ (u"ࠥࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠢྋ"), None)
            if current_test_id:
                hook_data.bstack111l11llll_opy_(current_test_id)
            if name == bstack1l11l1l_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠣྌ"):
                threading.current_thread().before_all_hook_uuid = bstack111l1ll111_opy_
            threading.current_thread().current_hook_uuid = bstack111l1ll111_opy_
            bstack111ll1lll1_opy_.bstack111ll11l11_opy_(bstack1l11l1l_opy_ (u"ࠧࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩࠨྍ"), hook_data)
        except Exception as e:
            logger.debug(bstack1l11l1l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡵࡣࡤࡷࡵࡶࡪࡪࠠࡪࡰࠣࡷࡹࡧࡲࡵࠢ࡫ࡳࡴࡱࠠࡦࡸࡨࡲࡹࡹࠬࠡࡪࡲࡳࡰࠦ࡮ࡢ࡯ࡨ࠾ࠥࠫࡳ࠭ࠢࡨࡶࡷࡵࡲ࠻ࠢࠨࡷࠧྎ"), name, e)
    def bstack1lll1l1l1_opy_(self, attrs):
        bstack111ll11l1l_opy_ = bstack1ll1ll11ll_opy_(threading.current_thread(), bstack1l11l1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫྏ"), None)
        hook_data = self.tests[bstack111ll11l1l_opy_][bstack1l11l1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫྐ")]
        status = bstack1l11l1l_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤྑ")
        exception = None
        bstack111l1llll1_opy_ = None
        if hook_data.name == bstack1l11l1l_opy_ (u"ࠥࡥ࡫ࡺࡥࡳࡡࡤࡰࡱࠨྒ"):
            self.bstack111l1l1lll_opy_.reset()
            bstack111l1lllll_opy_ = self.tests[bstack1ll1ll11ll_opy_(threading.current_thread(), bstack1l11l1l_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫྒྷ"), None)][bstack1l11l1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨྔ")].result.result
            if bstack111l1lllll_opy_ == bstack1l11l1l_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨྕ"):
                if attrs.hook_failures == 1:
                    status = bstack1l11l1l_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢྖ")
                elif attrs.hook_failures == 2:
                    status = bstack1l11l1l_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣྗ")
            elif attrs.aborted:
                status = bstack1l11l1l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ྘")
            threading.current_thread().before_all_hook_uuid = None
        else:
            if hook_data.name == bstack1l11l1l_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠧྙ") and attrs.hook_failures == 1:
                status = bstack1l11l1l_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦྚ")
            elif hasattr(attrs, bstack1l11l1l_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࡣࡲ࡫ࡳࡴࡣࡪࡩࠬྛ")) and attrs.error_message:
                status = bstack1l11l1l_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨྜ")
            bstack111l1llll1_opy_, exception = self._111l1lll11_opy_(attrs)
        bstack111ll111ll_opy_ = Result(result=status, exception=exception, bstack111l1ll11l_opy_=[bstack111l1llll1_opy_])
        hook_data.stop(time=bstack11ll11ll1l_opy_(), duration=0, result=bstack111ll111ll_opy_)
        bstack111ll1lll1_opy_.bstack111ll11l11_opy_(bstack1l11l1l_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩྜྷ"), self.tests[bstack111ll11l1l_opy_][bstack1l11l1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫྞ")])
        threading.current_thread().current_hook_uuid = None
    def _111l1lll11_opy_(self, attrs):
        try:
            import traceback
            bstack1l1l11111l_opy_ = traceback.format_tb(attrs.exc_traceback)
            bstack111l1llll1_opy_ = bstack1l1l11111l_opy_[-1] if bstack1l1l11111l_opy_ else None
            exception = attrs.exception
        except Exception:
            logger.debug(bstack1l11l1l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡱࡦࡧࡺࡸࡲࡦࡦࠣࡻ࡭࡯࡬ࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡧࡺࡹࡴࡰ࡯ࠣࡸࡷࡧࡣࡦࡤࡤࡧࡰࠨྟ"))
            bstack111l1llll1_opy_ = None
            exception = None
        return bstack111l1llll1_opy_, exception