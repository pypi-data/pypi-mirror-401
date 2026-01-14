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
import logging
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.bstack11lllll1_opy_ import get_logger
from bstack_utils.bstack1lll1l111_opy_ import bstack1ll1llll11l_opy_
bstack1lll1l111_opy_ = bstack1ll1llll11l_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack1l1l111lll_opy_: Optional[str] = None):
    bstack1l11l1l_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡊࡥࡤࡱࡵࡥࡹࡵࡲࠡࡶࡲࠤࡱࡵࡧࠡࡶ࡫ࡩࠥࡹࡴࡢࡴࡷࠤࡹ࡯࡭ࡦࠢࡲࡪࠥࡧࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࡨࡼࡪࡩࡵࡵ࡫ࡲࡲࠏࠦࠠࠡࠢࡤࡰࡴࡴࡧࠡࡹ࡬ࡸ࡭ࠦࡥࡷࡧࡱࡸࠥࡴࡡ࡮ࡧࠣࡥࡳࡪࠠࡴࡶࡤ࡫ࡪ࠴ࠊࠡࠢࠣࠤࠧࠨࠢẳ")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack1l1lll11lll_opy_: str = bstack1lll1l111_opy_.bstack11ll11l1l11_opy_(label)
            start_mark: str = label + bstack1l11l1l_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨẴ")
            end_mark: str = label + bstack1l11l1l_opy_ (u"ࠢ࠻ࡧࡱࡨࠧẵ")
            result = None
            try:
                if stage.value == STAGE.bstack11l1l1lll1_opy_.value:
                    bstack1lll1l111_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack1lll1l111_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack1l1l111lll_opy_)
                elif stage.value == STAGE.bstack11l1llllll_opy_.value:
                    start_mark: str = bstack1l1lll11lll_opy_ + bstack1l11l1l_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣẶ")
                    end_mark: str = bstack1l1lll11lll_opy_ + bstack1l11l1l_opy_ (u"ࠤ࠽ࡩࡳࡪࠢặ")
                    bstack1lll1l111_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack1lll1l111_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack1l1l111lll_opy_)
            except Exception as e:
                bstack1lll1l111_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack1l1l111lll_opy_)
            return result
        return wrapper
    return decorator