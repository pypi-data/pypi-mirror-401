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
import logging
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.bstack1ll1lll11_opy_ import get_logger
from bstack_utils.bstack11lll1l1ll_opy_ import bstack1ll11ll1ll1_opy_
bstack11lll1l1ll_opy_ = bstack1ll11ll1ll1_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack111l1l11_opy_: Optional[str] = None):
    bstack1l111l1_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡈࡪࡩ࡯ࡳࡣࡷࡳࡷࠦࡴࡰࠢ࡯ࡳ࡬ࠦࡴࡩࡧࠣࡷࡹࡧࡲࡵࠢࡷ࡭ࡲ࡫ࠠࡰࡨࠣࡥࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡦࡺࡨࡧࡺࡺࡩࡰࡰࠍࠤࠥࠦࠠࡢ࡮ࡲࡲ࡬ࠦࡷࡪࡶ࡫ࠤࡪࡼࡥ࡯ࡶࠣࡲࡦࡳࡥࠡࡣࡱࡨࠥࡹࡴࡢࡩࡨ࠲ࠏࠦࠠࠡࠢࠥࠦࠧỔ")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack1ll111ll11l_opy_: str = bstack11lll1l1ll_opy_.bstack11ll1111l1l_opy_(label)
            start_mark: str = label + bstack1l111l1_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦổ")
            end_mark: str = label + bstack1l111l1_opy_ (u"ࠧࡀࡥ࡯ࡦࠥỖ")
            result = None
            try:
                if stage.value == STAGE.bstack1ll1l1llll_opy_.value:
                    bstack11lll1l1ll_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack11lll1l1ll_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack111l1l11_opy_)
                elif stage.value == STAGE.bstack11l11l11l1_opy_.value:
                    start_mark: str = bstack1ll111ll11l_opy_ + bstack1l111l1_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨỗ")
                    end_mark: str = bstack1ll111ll11l_opy_ + bstack1l111l1_opy_ (u"ࠢ࠻ࡧࡱࡨࠧỘ")
                    bstack11lll1l1ll_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack11lll1l1ll_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack111l1l11_opy_)
            except Exception as e:
                bstack11lll1l1ll_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack111l1l11_opy_)
            return result
        return wrapper
    return decorator