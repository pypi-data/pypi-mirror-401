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
from collections import deque
from bstack_utils.constants import *
class bstack111llll1ll_opy_:
    def __init__(self):
        self._1lllll1l1lll_opy_ = deque()
        self._1lllll1l1l11_opy_ = {}
        self._1lllll1ll11l_opy_ = False
        self._lock = threading.RLock()
    def bstack1lllll11lll1_opy_(self, test_name, bstack1lllll1ll1l1_opy_):
        with self._lock:
            bstack1lllll1l11ll_opy_ = self._1lllll1l1l11_opy_.get(test_name, {})
            return bstack1lllll1l11ll_opy_.get(bstack1lllll1ll1l1_opy_, 0)
    def bstack1lllll1l1111_opy_(self, test_name, bstack1lllll1ll1l1_opy_):
        with self._lock:
            bstack1lllll1ll111_opy_ = self.bstack1lllll11lll1_opy_(test_name, bstack1lllll1ll1l1_opy_)
            self.bstack1lllll1l11l1_opy_(test_name, bstack1lllll1ll1l1_opy_)
            return bstack1lllll1ll111_opy_
    def bstack1lllll1l11l1_opy_(self, test_name, bstack1lllll1ll1l1_opy_):
        with self._lock:
            if test_name not in self._1lllll1l1l11_opy_:
                self._1lllll1l1l11_opy_[test_name] = {}
            bstack1lllll1l11ll_opy_ = self._1lllll1l1l11_opy_[test_name]
            bstack1lllll1ll111_opy_ = bstack1lllll1l11ll_opy_.get(bstack1lllll1ll1l1_opy_, 0)
            bstack1lllll1l11ll_opy_[bstack1lllll1ll1l1_opy_] = bstack1lllll1ll111_opy_ + 1
    def bstack11lll1ll11_opy_(self, bstack1lllll11llll_opy_, bstack1lllll1l1ll1_opy_):
        bstack1lllll1l1l1l_opy_ = self.bstack1lllll1l1111_opy_(bstack1lllll11llll_opy_, bstack1lllll1l1ll1_opy_)
        event_name = bstack11l1l111l11_opy_[bstack1lllll1l1ll1_opy_]
        bstack1l11lll11ll_opy_ = bstack1l111l1_opy_ (u"ࠧࢁࡽ࠮ࡽࢀ࠱ࢀࢃࠢ⁂").format(bstack1lllll11llll_opy_, event_name, bstack1lllll1l1l1l_opy_)
        with self._lock:
            self._1lllll1l1lll_opy_.append(bstack1l11lll11ll_opy_)
    def bstack1ll1111l1l_opy_(self):
        with self._lock:
            return len(self._1lllll1l1lll_opy_) == 0
    def bstack1ll1111l11_opy_(self):
        with self._lock:
            if self._1lllll1l1lll_opy_:
                bstack1lllll1l111l_opy_ = self._1lllll1l1lll_opy_.popleft()
                return bstack1lllll1l111l_opy_
            return None
    def capturing(self):
        with self._lock:
            return self._1lllll1ll11l_opy_
    def bstack11l1l1l11_opy_(self):
        with self._lock:
            self._1lllll1ll11l_opy_ = True
    def bstack1ll1111l1_opy_(self):
        with self._lock:
            self._1lllll1ll11l_opy_ = False