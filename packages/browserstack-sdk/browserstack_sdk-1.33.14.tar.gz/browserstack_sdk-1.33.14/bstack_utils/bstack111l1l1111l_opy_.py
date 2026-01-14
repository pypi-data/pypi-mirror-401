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
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack111lllll1l1_opy_
from browserstack_sdk.bstack11l1ll11ll_opy_ import bstack1lll1l11_opy_
def _111l11ll11l_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack111l11lllll_opy_:
    def __init__(self, handler):
        self._111l11l1l1l_opy_ = {}
        self._111l11l1ll1_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack1lll1l11_opy_.version()
        if bstack111lllll1l1_opy_(pytest_version, bstack1l11l1l_opy_ (u"ࠦ࠽࠴࠱࠯࠳ࠥḻ")) >= 0:
            self._111l11l1l1l_opy_[bstack1l11l1l_opy_ (u"ࠬ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨḼ")] = Module._register_setup_function_fixture
            self._111l11l1l1l_opy_[bstack1l11l1l_opy_ (u"࠭࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧḽ")] = Module._register_setup_module_fixture
            self._111l11l1l1l_opy_[bstack1l11l1l_opy_ (u"ࠧࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫ࠧḾ")] = Class._register_setup_class_fixture
            self._111l11l1l1l_opy_[bstack1l11l1l_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠩḿ")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack111l11l1l11_opy_(bstack1l11l1l_opy_ (u"ࠩࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬṀ"))
            Module._register_setup_module_fixture = self.bstack111l11l1l11_opy_(bstack1l11l1l_opy_ (u"ࠪࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫṁ"))
            Class._register_setup_class_fixture = self.bstack111l11l1l11_opy_(bstack1l11l1l_opy_ (u"ࠫࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠫṂ"))
            Class._register_setup_method_fixture = self.bstack111l11l1l11_opy_(bstack1l11l1l_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ṃ"))
        else:
            self._111l11l1l1l_opy_[bstack1l11l1l_opy_ (u"࠭ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩṄ")] = Module._inject_setup_function_fixture
            self._111l11l1l1l_opy_[bstack1l11l1l_opy_ (u"ࠧ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨṅ")] = Module._inject_setup_module_fixture
            self._111l11l1l1l_opy_[bstack1l11l1l_opy_ (u"ࠨࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨṆ")] = Class._inject_setup_class_fixture
            self._111l11l1l1l_opy_[bstack1l11l1l_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠪṇ")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack111l11l1l11_opy_(bstack1l11l1l_opy_ (u"ࠪࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭Ṉ"))
            Module._inject_setup_module_fixture = self.bstack111l11l1l11_opy_(bstack1l11l1l_opy_ (u"ࠫࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬṉ"))
            Class._inject_setup_class_fixture = self.bstack111l11l1l11_opy_(bstack1l11l1l_opy_ (u"ࠬࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࠬṊ"))
            Class._inject_setup_method_fixture = self.bstack111l11l1l11_opy_(bstack1l11l1l_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠧṋ"))
    def bstack111l11l1lll_opy_(self, bstack111l11ll1l1_opy_, hook_type):
        bstack111l11llll1_opy_ = id(bstack111l11ll1l1_opy_.__class__)
        if (bstack111l11llll1_opy_, hook_type) in self._111l11l1ll1_opy_:
            return
        meth = getattr(bstack111l11ll1l1_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._111l11l1ll1_opy_[(bstack111l11llll1_opy_, hook_type)] = meth
            setattr(bstack111l11ll1l1_opy_, hook_type, self.bstack111l11lll1l_opy_(hook_type, bstack111l11llll1_opy_))
    def bstack111l1l111l1_opy_(self, instance, bstack111l1l11111_opy_):
        if bstack111l1l11111_opy_ == bstack1l11l1l_opy_ (u"ࠢࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠥṌ"):
            self.bstack111l11l1lll_opy_(instance.obj, bstack1l11l1l_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠤṍ"))
            self.bstack111l11l1lll_opy_(instance.obj, bstack1l11l1l_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠨṎ"))
        if bstack111l1l11111_opy_ == bstack1l11l1l_opy_ (u"ࠥࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠦṏ"):
            self.bstack111l11l1lll_opy_(instance.obj, bstack1l11l1l_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠥṐ"))
            self.bstack111l11l1lll_opy_(instance.obj, bstack1l11l1l_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠢṑ"))
        if bstack111l1l11111_opy_ == bstack1l11l1l_opy_ (u"ࠨࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪࠨṒ"):
            self.bstack111l11l1lll_opy_(instance.obj, bstack1l11l1l_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠧṓ"))
            self.bstack111l11l1lll_opy_(instance.obj, bstack1l11l1l_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠤṔ"))
        if bstack111l1l11111_opy_ == bstack1l11l1l_opy_ (u"ࠤࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠥṕ"):
            self.bstack111l11l1lll_opy_(instance.obj, bstack1l11l1l_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠤṖ"))
            self.bstack111l11l1lll_opy_(instance.obj, bstack1l11l1l_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩࠨṗ"))
    @staticmethod
    def bstack111l11l11ll_opy_(hook_type, func, args):
        if hook_type in [bstack1l11l1l_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠫṘ"), bstack1l11l1l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠨṙ")]:
            _111l11ll11l_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack111l11lll1l_opy_(self, hook_type, bstack111l11llll1_opy_):
        def bstack111l11ll111_opy_(arg=None):
            self.handler(hook_type, bstack1l11l1l_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫ࠧṚ"))
            result = None
            try:
                bstack1lll1lll1l1_opy_ = self._111l11l1ll1_opy_[(bstack111l11llll1_opy_, hook_type)]
                self.bstack111l11l11ll_opy_(hook_type, bstack1lll1lll1l1_opy_, (arg,))
                result = Result(result=bstack1l11l1l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨṛ"))
            except Exception as e:
                result = Result(result=bstack1l11l1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩṜ"), exception=e)
                self.handler(hook_type, bstack1l11l1l_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩṝ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1l11l1l_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪṞ"), result)
        def bstack111l11lll11_opy_(this, arg=None):
            self.handler(hook_type, bstack1l11l1l_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࠬṟ"))
            result = None
            exception = None
            try:
                self.bstack111l11l11ll_opy_(hook_type, self._111l11l1ll1_opy_[hook_type], (this, arg))
                result = Result(result=bstack1l11l1l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭Ṡ"))
            except Exception as e:
                result = Result(result=bstack1l11l1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧṡ"), exception=e)
                self.handler(hook_type, bstack1l11l1l_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧṢ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1l11l1l_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨṣ"), result)
        if hook_type in [bstack1l11l1l_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠩṤ"), bstack1l11l1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ṥ")]:
            return bstack111l11lll11_opy_
        return bstack111l11ll111_opy_
    def bstack111l11l1l11_opy_(self, bstack111l1l11111_opy_):
        def bstack111l11ll1ll_opy_(this, *args, **kwargs):
            self.bstack111l1l111l1_opy_(this, bstack111l1l11111_opy_)
            self._111l11l1l1l_opy_[bstack111l1l11111_opy_](this, *args, **kwargs)
        return bstack111l11ll1ll_opy_