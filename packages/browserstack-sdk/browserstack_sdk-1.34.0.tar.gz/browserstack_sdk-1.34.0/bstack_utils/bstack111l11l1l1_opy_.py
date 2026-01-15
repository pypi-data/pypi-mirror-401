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
from uuid import uuid4
from bstack_utils.helper import bstack11llll1111_opy_, bstack111llllllll_opy_
from bstack_utils.bstack1ll11ll11_opy_ import bstack1llll1lll1l1_opy_
class bstack111l1111ll_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack1llll111l1ll_opy_=None, bstack1llll11l111l_opy_=True, bstack11llll11l11_opy_=None, bstack1ll1l1ll11_opy_=None, result=None, duration=None, bstack1111l1111l_opy_=None, meta={}):
        self.bstack1111l1111l_opy_ = bstack1111l1111l_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1llll11l111l_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1llll111l1ll_opy_ = bstack1llll111l1ll_opy_
        self.bstack11llll11l11_opy_ = bstack11llll11l11_opy_
        self.bstack1ll1l1ll11_opy_ = bstack1ll1l1ll11_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack1111lll1l1_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack111l1lll1l_opy_(self, meta):
        self.meta = meta
    def bstack111l1l1111_opy_(self, hooks):
        self.hooks = hooks
    def bstack1llll111ll1l_opy_(self):
        bstack1llll11111l1_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1l111l1_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧℽ"): bstack1llll11111l1_opy_,
            bstack1l111l1_opy_ (u"ࠬࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠧℾ"): bstack1llll11111l1_opy_,
            bstack1l111l1_opy_ (u"࠭ࡶࡤࡡࡩ࡭ࡱ࡫ࡰࡢࡶ࡫ࠫℿ"): bstack1llll11111l1_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1l111l1_opy_ (u"ࠢࡖࡰࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࡦࡸࡧࡶ࡯ࡨࡲࡹࡀࠠࠣ⅀") + key)
            setattr(self, key, val)
    def bstack1llll11l1111_opy_(self):
        return {
            bstack1l111l1_opy_ (u"ࠨࡰࡤࡱࡪ࠭⅁"): self.name,
            bstack1l111l1_opy_ (u"ࠩࡥࡳࡩࡿࠧ⅂"): {
                bstack1l111l1_opy_ (u"ࠪࡰࡦࡴࡧࠨ⅃"): bstack1l111l1_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ⅄"),
                bstack1l111l1_opy_ (u"ࠬࡩ࡯ࡥࡧࠪⅅ"): self.code
            },
            bstack1l111l1_opy_ (u"࠭ࡳࡤࡱࡳࡩࡸ࠭ⅆ"): self.scope,
            bstack1l111l1_opy_ (u"ࠧࡵࡣࡪࡷࠬⅇ"): self.tags,
            bstack1l111l1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫⅈ"): self.framework,
            bstack1l111l1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ⅉ"): self.started_at
        }
    def bstack1llll1111l1l_opy_(self):
        return {
         bstack1l111l1_opy_ (u"ࠪࡱࡪࡺࡡࠨ⅊"): self.meta
        }
    def bstack1llll1111l11_opy_(self):
        return {
            bstack1l111l1_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡖࡪࡸࡵ࡯ࡒࡤࡶࡦࡳࠧ⅋"): {
                bstack1l111l1_opy_ (u"ࠬࡸࡥࡳࡷࡱࡣࡳࡧ࡭ࡦࠩ⅌"): self.bstack1llll111l1ll_opy_
            }
        }
    def bstack1llll111llll_opy_(self, bstack1llll11111ll_opy_, details):
        step = next(filter(lambda st: st[bstack1l111l1_opy_ (u"࠭ࡩࡥࠩ⅍")] == bstack1llll11111ll_opy_, self.meta[bstack1l111l1_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ⅎ")]), None)
        step.update(details)
    def bstack1l1ll1l1l_opy_(self, bstack1llll11111ll_opy_):
        step = next(filter(lambda st: st[bstack1l111l1_opy_ (u"ࠨ࡫ࡧࠫ⅏")] == bstack1llll11111ll_opy_, self.meta[bstack1l111l1_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨ⅐")]), None)
        step.update({
            bstack1l111l1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ⅑"): bstack11llll1111_opy_()
        })
    def bstack111l11l1ll_opy_(self, bstack1llll11111ll_opy_, result, duration=None):
        bstack11llll11l11_opy_ = bstack11llll1111_opy_()
        if bstack1llll11111ll_opy_ is not None and self.meta.get(bstack1l111l1_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪ⅒")):
            step = next(filter(lambda st: st[bstack1l111l1_opy_ (u"ࠬ࡯ࡤࠨ⅓")] == bstack1llll11111ll_opy_, self.meta[bstack1l111l1_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬ⅔")]), None)
            step.update({
                bstack1l111l1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⅕"): bstack11llll11l11_opy_,
                bstack1l111l1_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࠪ⅖"): duration if duration else bstack111llllllll_opy_(step[bstack1l111l1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭⅗")], bstack11llll11l11_opy_),
                bstack1l111l1_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ⅘"): result.result,
                bstack1l111l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬ⅙"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1llll111l1l1_opy_):
        if self.meta.get(bstack1l111l1_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫ⅚")):
            self.meta[bstack1l111l1_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬ⅛")].append(bstack1llll111l1l1_opy_)
        else:
            self.meta[bstack1l111l1_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭⅜")] = [ bstack1llll111l1l1_opy_ ]
    def bstack1llll1111lll_opy_(self):
        return {
            bstack1l111l1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⅝"): self.bstack1111lll1l1_opy_(),
            bstack1l111l1_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ⅞"): bstack1l111l1_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫ⅟"),
            **self.bstack1llll11l1111_opy_(),
            **self.bstack1llll111ll1l_opy_(),
            **self.bstack1llll1111l1l_opy_()
        }
    def bstack1llll111ll11_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack1l111l1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩⅠ"): self.bstack11llll11l11_opy_,
            bstack1l111l1_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭Ⅱ"): self.duration,
            bstack1l111l1_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭Ⅲ"): self.result.result
        }
        if data[bstack1l111l1_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧⅣ")] == bstack1l111l1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨⅤ"):
            data[bstack1l111l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨⅥ")] = self.result.bstack1lllll111ll_opy_()
            data[bstack1l111l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫⅦ")] = [{bstack1l111l1_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧⅧ"): self.result.bstack11l1111111l_opy_()}]
        return data
    def bstack1llll111lll1_opy_(self):
        return {
            bstack1l111l1_opy_ (u"ࠬࡻࡵࡪࡦࠪⅨ"): self.bstack1111lll1l1_opy_(),
            **self.bstack1llll11l1111_opy_(),
            **self.bstack1llll111ll1l_opy_(),
            **self.bstack1llll111ll11_opy_(),
            **self.bstack1llll1111l1l_opy_()
        }
    def bstack11111ll11l_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack1l111l1_opy_ (u"࠭ࡓࡵࡣࡵࡸࡪࡪࠧⅩ") in event:
            return self.bstack1llll1111lll_opy_()
        elif bstack1l111l1_opy_ (u"ࠧࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩⅪ") in event:
            return self.bstack1llll111lll1_opy_()
    def bstack1111ll1lll_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack11llll11l11_opy_ = time if time else bstack11llll1111_opy_()
        self.duration = duration if duration else bstack111llllllll_opy_(self.started_at, self.bstack11llll11l11_opy_)
        if result:
            self.result = result
class bstack111l11l111_opy_(bstack111l1111ll_opy_):
    def __init__(self, hooks=[], bstack111l1llll1_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack111l1llll1_opy_ = bstack111l1llll1_opy_
        super().__init__(*args, **kwargs, bstack1ll1l1ll11_opy_=bstack1l111l1_opy_ (u"ࠨࡶࡨࡷࡹ࠭Ⅻ"))
    @classmethod
    def bstack1llll1111ll1_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1l111l1_opy_ (u"ࠩ࡬ࡨࠬⅬ"): id(step),
                bstack1l111l1_opy_ (u"ࠪࡸࡪࡾࡴࠨⅭ"): step.name,
                bstack1l111l1_opy_ (u"ࠫࡰ࡫ࡹࡸࡱࡵࡨࠬⅮ"): step.keyword,
            })
        return bstack111l11l111_opy_(
            **kwargs,
            meta={
                bstack1l111l1_opy_ (u"ࠬ࡬ࡥࡢࡶࡸࡶࡪ࠭Ⅿ"): {
                    bstack1l111l1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫⅰ"): feature.name,
                    bstack1l111l1_opy_ (u"ࠧࡱࡣࡷ࡬ࠬⅱ"): feature.filename,
                    bstack1l111l1_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭ⅲ"): feature.description
                },
                bstack1l111l1_opy_ (u"ࠩࡶࡧࡪࡴࡡࡳ࡫ࡲࠫⅳ"): {
                    bstack1l111l1_opy_ (u"ࠪࡲࡦࡳࡥࠨⅴ"): scenario.name
                },
                bstack1l111l1_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪⅵ"): steps,
                bstack1l111l1_opy_ (u"ࠬ࡫ࡸࡢ࡯ࡳࡰࡪࡹࠧⅶ"): bstack1llll1lll1l1_opy_(test)
            }
        )
    def bstack1llll111l111_opy_(self):
        return {
            bstack1l111l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬⅷ"): self.hooks
        }
    def bstack1llll111111l_opy_(self):
        if self.bstack111l1llll1_opy_:
            return {
                bstack1l111l1_opy_ (u"ࠧࡪࡰࡷࡩ࡬ࡸࡡࡵ࡫ࡲࡲࡸ࠭ⅸ"): self.bstack111l1llll1_opy_
            }
        return {}
    def bstack1llll111lll1_opy_(self):
        return {
            **super().bstack1llll111lll1_opy_(),
            **self.bstack1llll111l111_opy_()
        }
    def bstack1llll1111lll_opy_(self):
        return {
            **super().bstack1llll1111lll_opy_(),
            **self.bstack1llll111111l_opy_()
        }
    def bstack1111ll1lll_opy_(self):
        return bstack1l111l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪⅹ")
class bstack111l11ll11_opy_(bstack111l1111ll_opy_):
    def __init__(self, hook_type, *args,bstack111l1llll1_opy_={}, **kwargs):
        self.hook_type = hook_type
        self.bstack1ll111lll1l_opy_ = None
        self.bstack111l1llll1_opy_ = bstack111l1llll1_opy_
        super().__init__(*args, **kwargs, bstack1ll1l1ll11_opy_=bstack1l111l1_opy_ (u"ࠩ࡫ࡳࡴࡱࠧⅺ"))
    def bstack1111l11111_opy_(self):
        return self.hook_type
    def bstack1llll111l11l_opy_(self):
        return {
            bstack1l111l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭ⅻ"): self.hook_type
        }
    def bstack1llll111lll1_opy_(self):
        return {
            **super().bstack1llll111lll1_opy_(),
            **self.bstack1llll111l11l_opy_()
        }
    def bstack1llll1111lll_opy_(self):
        return {
            **super().bstack1llll1111lll_opy_(),
            bstack1l111l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡩࡥࠩⅼ"): self.bstack1ll111lll1l_opy_,
            **self.bstack1llll111l11l_opy_()
        }
    def bstack1111ll1lll_opy_(self):
        return bstack1l111l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴࠧⅽ")
    def bstack111l1lllll_opy_(self, bstack1ll111lll1l_opy_):
        self.bstack1ll111lll1l_opy_ = bstack1ll111lll1l_opy_