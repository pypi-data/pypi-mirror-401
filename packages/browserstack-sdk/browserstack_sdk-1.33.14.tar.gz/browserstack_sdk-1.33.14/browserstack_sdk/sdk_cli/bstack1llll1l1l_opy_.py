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
from collections import defaultdict
from threading import Lock
from dataclasses import dataclass
import logging
import traceback
from typing import List, Dict, Any
import os
@dataclass
class bstack1ll11llll1_opy_:
    sdk_version: str
    path_config: str
    path_project: str
    test_framework: str
    frameworks: List[str]
    framework_versions: Dict[str, str]
    bs_config: Dict[str, Any]
@dataclass
class bstack11l1l111_opy_:
    pass
class bstack1l11ll1l1_opy_:
    bstack11l1ll111_opy_ = bstack1l11l1l_opy_ (u"ࠧࡨ࡯ࡰࡶࡶࡸࡷࡧࡰࠣᇋ")
    CONNECT = bstack1l11l1l_opy_ (u"ࠨࡣࡰࡰࡱࡩࡨࡺࠢᇌ")
    bstack1111l1l1l_opy_ = bstack1l11l1l_opy_ (u"ࠢࡴࡪࡸࡸࡩࡵࡷ࡯ࠤᇍ")
    CONFIG = bstack1l11l1l_opy_ (u"ࠣࡥࡲࡲ࡫࡯ࡧࠣᇎ")
    bstack1ll11l1l1ll_opy_ = bstack1l11l1l_opy_ (u"ࠤࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡸࠨᇏ")
    bstack1l1111llll_opy_ = bstack1l11l1l_opy_ (u"ࠥࡩࡽ࡯ࡴࠣᇐ")
class bstack1ll11l1ll11_opy_:
    bstack1ll11l1llll_opy_ = bstack1l11l1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡷࡹࡧࡲࡵࡧࡧࠦᇑ")
    FINISHED = bstack1l11l1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࠨᇒ")
class bstack1ll11l1lll1_opy_:
    bstack1ll11l1llll_opy_ = bstack1l11l1l_opy_ (u"ࠨࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡵࡷࡥࡷࡺࡥࡥࠤᇓ")
    FINISHED = bstack1l11l1l_opy_ (u"ࠢࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࠦᇔ")
class bstack1ll11ll1111_opy_:
    bstack1ll11l1llll_opy_ = bstack1l11l1l_opy_ (u"ࠣࡪࡲࡳࡰࡥࡲࡶࡰࡢࡷࡹࡧࡲࡵࡧࡧࠦᇕ")
    FINISHED = bstack1l11l1l_opy_ (u"ࠤ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࠨᇖ")
class bstack1ll11l1ll1l_opy_:
    bstack1ll11ll111l_opy_ = bstack1l11l1l_opy_ (u"ࠥࡧࡧࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡥࡵࡩࡦࡺࡥࡥࠤᇗ")
class bstack1ll11ll11l1_opy_:
    _1lll1l1l111_opy_ = None
    def __new__(cls):
        if not cls._1lll1l1l111_opy_:
            cls._1lll1l1l111_opy_ = super(bstack1ll11ll11l1_opy_, cls).__new__(cls)
        return cls._1lll1l1l111_opy_
    def __init__(self):
        self._hooks = defaultdict(lambda: defaultdict(list))
        self._lock = Lock()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def clear(self):
        with self._lock:
            self._hooks = defaultdict(list)
    def register(self, event_name, callback):
        with self._lock:
            if not callable(callback):
                raise ValueError(bstack1l11l1l_opy_ (u"ࠦࡈࡧ࡬࡭ࡤࡤࡧࡰࠦ࡭ࡶࡵࡷࠤࡧ࡫ࠠࡤࡣ࡯ࡰࡦࡨ࡬ࡦࠢࡩࡳࡷࠦࠢᇘ") + event_name)
            pid = os.getpid()
            self.logger.debug(bstack1l11l1l_opy_ (u"ࠧࡘࡥࡨ࡫ࡶࡸࡪࡸࡩ࡯ࡩࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯ࠥ࡬࡯ࡳࠢࡨࡺࡪࡴࡴࠡࠩࡾࡩࡻ࡫࡮ࡵࡡࡱࡥࡲ࡫ࡽࠨࠢࡺ࡭ࡹ࡮ࠠࡱ࡫ࡧࠤࠧᇙ") + str(pid) + bstack1l11l1l_opy_ (u"ࠨࠢᇚ"))
            self._hooks[event_name][pid].append(callback)
    def invoke(self, event_name, *args, **kwargs):
        with self._lock:
            pid = os.getpid()
            callbacks = self._hooks.get(event_name, {}).get(pid, [])
            if not callbacks:
                self.logger.warning(bstack1l11l1l_opy_ (u"ࠢࡏࡱࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯ࡸࠦࡦࡰࡴࠣࡩࡻ࡫࡮ࡵࠢࠪࡿࡪࡼࡥ࡯ࡶࡢࡲࡦࡳࡥࡾࠩࠣࡻ࡮ࡺࡨࠡࡲ࡬ࡨࠥࠨᇛ") + str(pid) + bstack1l11l1l_opy_ (u"ࠣࠤᇜ"))
                return
            self.logger.debug(bstack1l11l1l_opy_ (u"ࠤࡌࡲࡻࡵ࡫ࡪࡰࡪࠤࢀࡲࡥ࡯ࠪࡦࡥࡱࡲࡢࡢࡥ࡮ࡷ࠮ࢃࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬ࡵࠣࡪࡴࡸࠠࡦࡸࡨࡲࡹࠦࠧࡼࡧࡹࡩࡳࡺ࡟࡯ࡣࡰࡩࢂ࠭ࠠࡸ࡫ࡷ࡬ࠥࡶࡩࡥࠢࠥᇝ") + str(pid) + bstack1l11l1l_opy_ (u"ࠥࠦᇞ"))
            for callback in callbacks:
                try:
                    self.logger.debug(bstack1l11l1l_opy_ (u"ࠦࡎࡴࡶࡰ࡭ࡨࡨࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࠠࡧࡱࡵࠤࡪࡼࡥ࡯ࡶࠣࠫࢀ࡫ࡶࡦࡰࡷࡣࡳࡧ࡭ࡦࡿࠪࠤࡼ࡯ࡴࡩࠢࡳ࡭ࡩࠦࠢᇟ") + str(pid) + bstack1l11l1l_opy_ (u"ࠧࠨᇠ"))
                    callback(event_name, *args, **kwargs)
                except Exception as e:
                    self.logger.error(bstack1l11l1l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡯࡮ࡷࡱ࡮࡭ࡳ࡭ࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬ࠢࡩࡳࡷࠦࡥࡷࡧࡱࡸࠥ࠭ࡻࡦࡸࡨࡲࡹࡥ࡮ࡢ࡯ࡨࢁࠬࠦࡷࡪࡶ࡫ࠤࡵ࡯ࡤࠡࡽࡳ࡭ࡩࢃ࠺ࠡࠤᇡ") + str(e) + bstack1l11l1l_opy_ (u"ࠢࠣᇢ"))
                    traceback.print_exc()
bstack1llll1l1l_opy_ = bstack1ll11ll11l1_opy_()