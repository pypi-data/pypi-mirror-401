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
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack11l111l1111_opy_
from browserstack_sdk.bstack11l11111l1_opy_ import bstack1lllllllll_opy_
def _111l111llll_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack111l11l1lll_opy_:
    def __init__(self, handler):
        self._111l111ll1l_opy_ = {}
        self._111l111l11l_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack1lllllllll_opy_.version()
        if bstack11l111l1111_opy_(pytest_version, bstack1l111l1_opy_ (u"ࠤ࠻࠲࠶࠴࠱ࠣṜ")) >= 0:
            self._111l111ll1l_opy_[bstack1l111l1_opy_ (u"ࠪࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ṝ")] = Module._register_setup_function_fixture
            self._111l111ll1l_opy_[bstack1l111l1_opy_ (u"ࠫࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬṞ")] = Module._register_setup_module_fixture
            self._111l111ll1l_opy_[bstack1l111l1_opy_ (u"ࠬࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࠬṟ")] = Class._register_setup_class_fixture
            self._111l111ll1l_opy_[bstack1l111l1_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠧṠ")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack111l111l1l1_opy_(bstack1l111l1_opy_ (u"ࠧࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪṡ"))
            Module._register_setup_module_fixture = self.bstack111l111l1l1_opy_(bstack1l111l1_opy_ (u"ࠨ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩṢ"))
            Class._register_setup_class_fixture = self.bstack111l111l1l1_opy_(bstack1l111l1_opy_ (u"ࠩࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠩṣ"))
            Class._register_setup_method_fixture = self.bstack111l111l1l1_opy_(bstack1l111l1_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࠫṤ"))
        else:
            self._111l111ll1l_opy_[bstack1l111l1_opy_ (u"ࠫ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧṥ")] = Module._inject_setup_function_fixture
            self._111l111ll1l_opy_[bstack1l111l1_opy_ (u"ࠬࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭Ṧ")] = Module._inject_setup_module_fixture
            self._111l111ll1l_opy_[bstack1l111l1_opy_ (u"࠭ࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ṧ")] = Class._inject_setup_class_fixture
            self._111l111ll1l_opy_[bstack1l111l1_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨṨ")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack111l111l1l1_opy_(bstack1l111l1_opy_ (u"ࠨࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫṩ"))
            Module._inject_setup_module_fixture = self.bstack111l111l1l1_opy_(bstack1l111l1_opy_ (u"ࠩࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪṪ"))
            Class._inject_setup_class_fixture = self.bstack111l111l1l1_opy_(bstack1l111l1_opy_ (u"ࠪࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠪṫ"))
            Class._inject_setup_method_fixture = self.bstack111l111l1l1_opy_(bstack1l111l1_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠬṬ"))
    def bstack111l11l11ll_opy_(self, bstack111l11l1111_opy_, hook_type):
        bstack111l111ll11_opy_ = id(bstack111l11l1111_opy_.__class__)
        if (bstack111l111ll11_opy_, hook_type) in self._111l111l11l_opy_:
            return
        meth = getattr(bstack111l11l1111_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._111l111l11l_opy_[(bstack111l111ll11_opy_, hook_type)] = meth
            setattr(bstack111l11l1111_opy_, hook_type, self.bstack111l111l1ll_opy_(hook_type, bstack111l111ll11_opy_))
    def bstack111l11l1ll1_opy_(self, instance, bstack111l11l1l11_opy_):
        if bstack111l11l1l11_opy_ == bstack1l111l1_opy_ (u"ࠧ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠣṭ"):
            self.bstack111l11l11ll_opy_(instance.obj, bstack1l111l1_opy_ (u"ࠨࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠢṮ"))
            self.bstack111l11l11ll_opy_(instance.obj, bstack1l111l1_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࠦṯ"))
        if bstack111l11l1l11_opy_ == bstack1l111l1_opy_ (u"ࠣ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠤṰ"):
            self.bstack111l11l11ll_opy_(instance.obj, bstack1l111l1_opy_ (u"ࠤࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠣṱ"))
            self.bstack111l11l11ll_opy_(instance.obj, bstack1l111l1_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࠧṲ"))
        if bstack111l11l1l11_opy_ == bstack1l111l1_opy_ (u"ࠦࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠦṳ"):
            self.bstack111l11l11ll_opy_(instance.obj, bstack1l111l1_opy_ (u"ࠧࡹࡥࡵࡷࡳࡣࡨࡲࡡࡴࡵࠥṴ"))
            self.bstack111l11l11ll_opy_(instance.obj, bstack1l111l1_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠢṵ"))
        if bstack111l11l1l11_opy_ == bstack1l111l1_opy_ (u"ࠢ࡮ࡧࡷ࡬ࡴࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠣṶ"):
            self.bstack111l11l11ll_opy_(instance.obj, bstack1l111l1_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠢṷ"))
            self.bstack111l11l11ll_opy_(instance.obj, bstack1l111l1_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠦṸ"))
    @staticmethod
    def bstack111l111lll1_opy_(hook_type, func, args):
        if hook_type in [bstack1l111l1_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠩṹ"), bstack1l111l1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩ࠭Ṻ")]:
            _111l111llll_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack111l111l1ll_opy_(self, hook_type, bstack111l111ll11_opy_):
        def bstack111l11l1l1l_opy_(arg=None):
            self.handler(hook_type, bstack1l111l1_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࠬṻ"))
            result = None
            try:
                bstack1llll1l11ll_opy_ = self._111l111l11l_opy_[(bstack111l111ll11_opy_, hook_type)]
                self.bstack111l111lll1_opy_(hook_type, bstack1llll1l11ll_opy_, (arg,))
                result = Result(result=bstack1l111l1_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭Ṽ"))
            except Exception as e:
                result = Result(result=bstack1l111l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧṽ"), exception=e)
                self.handler(hook_type, bstack1l111l1_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧṾ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1l111l1_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨṿ"), result)
        def bstack111l11l11l1_opy_(this, arg=None):
            self.handler(hook_type, bstack1l111l1_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪẀ"))
            result = None
            exception = None
            try:
                self.bstack111l111lll1_opy_(hook_type, self._111l111l11l_opy_[hook_type], (this, arg))
                result = Result(result=bstack1l111l1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫẁ"))
            except Exception as e:
                result = Result(result=bstack1l111l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬẂ"), exception=e)
                self.handler(hook_type, bstack1l111l1_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬẃ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1l111l1_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭Ẅ"), result)
        if hook_type in [bstack1l111l1_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠧẅ"), bstack1l111l1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫẆ")]:
            return bstack111l11l11l1_opy_
        return bstack111l11l1l1l_opy_
    def bstack111l111l1l1_opy_(self, bstack111l11l1l11_opy_):
        def bstack111l11l111l_opy_(this, *args, **kwargs):
            self.bstack111l11l1ll1_opy_(this, bstack111l11l1l11_opy_)
            self._111l111ll1l_opy_[bstack111l11l1l11_opy_](this, *args, **kwargs)
        return bstack111l11l111l_opy_