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
import os
from uuid import uuid4
from bstack_utils.helper import bstack11ll11ll1l_opy_, bstack111lll11ll1_opy_
from bstack_utils.bstack1ll1lll11_opy_ import bstack1llll1lll11l_opy_
class bstack1111ll11ll_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack1llll11ll1l1_opy_=None, bstack1llll11l1l11_opy_=True, bstack11llll1lll1_opy_=None, bstack11l1111l_opy_=None, result=None, duration=None, bstack1111l1llll_opy_=None, meta={}):
        self.bstack1111l1llll_opy_ = bstack1111l1llll_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1llll11l1l11_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1llll11ll1l1_opy_ = bstack1llll11ll1l1_opy_
        self.bstack11llll1lll1_opy_ = bstack11llll1lll1_opy_
        self.bstack11l1111l_opy_ = bstack11l1111l_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack1111l1l1l1_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack111l1lll1l_opy_(self, meta):
        self.meta = meta
    def bstack111l1l1ll1_opy_(self, hooks):
        self.hooks = hooks
    def bstack1llll111l1l1_opy_(self):
        bstack1llll11l1ll1_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1l11l1l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩℜ"): bstack1llll11l1ll1_opy_,
            bstack1l11l1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠩℝ"): bstack1llll11l1ll1_opy_,
            bstack1l11l1l_opy_ (u"ࠨࡸࡦࡣ࡫࡯࡬ࡦࡲࡤࡸ࡭࠭℞"): bstack1llll11l1ll1_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1l11l1l_opy_ (u"ࠤࡘࡲࡪࡾࡰࡦࡥࡷࡩࡩࠦࡡࡳࡩࡸࡱࡪࡴࡴ࠻ࠢࠥ℟") + key)
            setattr(self, key, val)
    def bstack1llll111lll1_opy_(self):
        return {
            bstack1l11l1l_opy_ (u"ࠪࡲࡦࡳࡥࠨ℠"): self.name,
            bstack1l11l1l_opy_ (u"ࠫࡧࡵࡤࡺࠩ℡"): {
                bstack1l11l1l_opy_ (u"ࠬࡲࡡ࡯ࡩࠪ™"): bstack1l11l1l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭℣"),
                bstack1l11l1l_opy_ (u"ࠧࡤࡱࡧࡩࠬℤ"): self.code
            },
            bstack1l11l1l_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࡳࠨ℥"): self.scope,
            bstack1l11l1l_opy_ (u"ࠩࡷࡥ࡬ࡹࠧΩ"): self.tags,
            bstack1l11l1l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭℧"): self.framework,
            bstack1l11l1l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨℨ"): self.started_at
        }
    def bstack1llll11l11ll_opy_(self):
        return {
         bstack1l11l1l_opy_ (u"ࠬࡳࡥࡵࡣࠪ℩"): self.meta
        }
    def bstack1llll11l1lll_opy_(self):
        return {
            bstack1l11l1l_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡘࡥࡳࡷࡱࡔࡦࡸࡡ࡮ࠩK"): {
                bstack1l11l1l_opy_ (u"ࠧࡳࡧࡵࡹࡳࡥ࡮ࡢ࡯ࡨࠫÅ"): self.bstack1llll11ll1l1_opy_
            }
        }
    def bstack1llll11l1111_opy_(self, bstack1llll11ll111_opy_, details):
        step = next(filter(lambda st: st[bstack1l11l1l_opy_ (u"ࠨ࡫ࡧࠫℬ")] == bstack1llll11ll111_opy_, self.meta[bstack1l11l1l_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨℭ")]), None)
        step.update(details)
    def bstack1l1lll111_opy_(self, bstack1llll11ll111_opy_):
        step = next(filter(lambda st: st[bstack1l11l1l_opy_ (u"ࠪ࡭ࡩ࠭℮")] == bstack1llll11ll111_opy_, self.meta[bstack1l11l1l_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪℯ")]), None)
        step.update({
            bstack1l11l1l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩℰ"): bstack11ll11ll1l_opy_()
        })
    def bstack111l1l111l_opy_(self, bstack1llll11ll111_opy_, result, duration=None):
        bstack11llll1lll1_opy_ = bstack11ll11ll1l_opy_()
        if bstack1llll11ll111_opy_ is not None and self.meta.get(bstack1l11l1l_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬℱ")):
            step = next(filter(lambda st: st[bstack1l11l1l_opy_ (u"ࠧࡪࡦࠪℲ")] == bstack1llll11ll111_opy_, self.meta[bstack1l11l1l_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧℳ")]), None)
            step.update({
                bstack1l11l1l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧℴ"): bstack11llll1lll1_opy_,
                bstack1l11l1l_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬℵ"): duration if duration else bstack111lll11ll1_opy_(step[bstack1l11l1l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨℶ")], bstack11llll1lll1_opy_),
                bstack1l11l1l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬℷ"): result.result,
                bstack1l11l1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧℸ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1llll111llll_opy_):
        if self.meta.get(bstack1l11l1l_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ℹ")):
            self.meta[bstack1l11l1l_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ℺")].append(bstack1llll111llll_opy_)
        else:
            self.meta[bstack1l11l1l_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨ℻")] = [ bstack1llll111llll_opy_ ]
    def bstack1llll11l111l_opy_(self):
        return {
            bstack1l11l1l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨℼ"): self.bstack1111l1l1l1_opy_(),
            bstack1l11l1l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫℽ"): bstack1l11l1l_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭ℾ"),
            **self.bstack1llll111lll1_opy_(),
            **self.bstack1llll111l1l1_opy_(),
            **self.bstack1llll11l11ll_opy_()
        }
    def bstack1llll11l1l1l_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack1l11l1l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫℿ"): self.bstack11llll1lll1_opy_,
            bstack1l11l1l_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨ⅀"): self.duration,
            bstack1l11l1l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ⅁"): self.result.result
        }
        if data[bstack1l11l1l_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ⅂")] == bstack1l11l1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ⅃"):
            data[bstack1l11l1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪ⅄")] = self.result.bstack1lllll1ll11_opy_()
            data[bstack1l11l1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ⅅ")] = [{bstack1l11l1l_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩⅆ"): self.result.bstack111l1ll1l1l_opy_()}]
        return data
    def bstack1llll11ll11l_opy_(self):
        return {
            bstack1l11l1l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬⅇ"): self.bstack1111l1l1l1_opy_(),
            **self.bstack1llll111lll1_opy_(),
            **self.bstack1llll111l1l1_opy_(),
            **self.bstack1llll11l1l1l_opy_(),
            **self.bstack1llll11l11ll_opy_()
        }
    def bstack111l11ll1l_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack1l11l1l_opy_ (u"ࠨࡕࡷࡥࡷࡺࡥࡥࠩⅈ") in event:
            return self.bstack1llll11l111l_opy_()
        elif bstack1l11l1l_opy_ (u"ࠩࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫⅉ") in event:
            return self.bstack1llll11ll11l_opy_()
    def bstack1111l11l11_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack11llll1lll1_opy_ = time if time else bstack11ll11ll1l_opy_()
        self.duration = duration if duration else bstack111lll11ll1_opy_(self.started_at, self.bstack11llll1lll1_opy_)
        if result:
            self.result = result
class bstack111l1l11ll_opy_(bstack1111ll11ll_opy_):
    def __init__(self, hooks=[], bstack111ll11lll_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack111ll11lll_opy_ = bstack111ll11lll_opy_
        super().__init__(*args, **kwargs, bstack11l1111l_opy_=bstack1l11l1l_opy_ (u"ࠪࡸࡪࡹࡴࠨ⅊"))
    @classmethod
    def bstack1llll111ll1l_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1l11l1l_opy_ (u"ࠫ࡮ࡪࠧ⅋"): id(step),
                bstack1l11l1l_opy_ (u"ࠬࡺࡥࡹࡶࠪ⅌"): step.name,
                bstack1l11l1l_opy_ (u"࠭࡫ࡦࡻࡺࡳࡷࡪࠧ⅍"): step.keyword,
            })
        return bstack111l1l11ll_opy_(
            **kwargs,
            meta={
                bstack1l11l1l_opy_ (u"ࠧࡧࡧࡤࡸࡺࡸࡥࠨⅎ"): {
                    bstack1l11l1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭⅏"): feature.name,
                    bstack1l11l1l_opy_ (u"ࠩࡳࡥࡹ࡮ࠧ⅐"): feature.filename,
                    bstack1l11l1l_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨ⅑"): feature.description
                },
                bstack1l11l1l_opy_ (u"ࠫࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭⅒"): {
                    bstack1l11l1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ⅓"): scenario.name
                },
                bstack1l11l1l_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬ⅔"): steps,
                bstack1l11l1l_opy_ (u"ࠧࡦࡺࡤࡱࡵࡲࡥࡴࠩ⅕"): bstack1llll1lll11l_opy_(test)
            }
        )
    def bstack1llll11l11l1_opy_(self):
        return {
            bstack1l11l1l_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ⅖"): self.hooks
        }
    def bstack1llll111ll11_opy_(self):
        if self.bstack111ll11lll_opy_:
            return {
                bstack1l11l1l_opy_ (u"ࠩ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠨ⅗"): self.bstack111ll11lll_opy_
            }
        return {}
    def bstack1llll11ll11l_opy_(self):
        return {
            **super().bstack1llll11ll11l_opy_(),
            **self.bstack1llll11l11l1_opy_()
        }
    def bstack1llll11l111l_opy_(self):
        return {
            **super().bstack1llll11l111l_opy_(),
            **self.bstack1llll111ll11_opy_()
        }
    def bstack1111l11l11_opy_(self):
        return bstack1l11l1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬ⅘")
class bstack111ll11111_opy_(bstack1111ll11ll_opy_):
    def __init__(self, hook_type, *args,bstack111ll11lll_opy_={}, **kwargs):
        self.hook_type = hook_type
        self.bstack1l1llll1l1l_opy_ = None
        self.bstack111ll11lll_opy_ = bstack111ll11lll_opy_
        super().__init__(*args, **kwargs, bstack11l1111l_opy_=bstack1l11l1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩ⅙"))
    def bstack111l11lll1_opy_(self):
        return self.hook_type
    def bstack1llll111l1ll_opy_(self):
        return {
            bstack1l11l1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨ⅚"): self.hook_type
        }
    def bstack1llll11ll11l_opy_(self):
        return {
            **super().bstack1llll11ll11l_opy_(),
            **self.bstack1llll111l1ll_opy_()
        }
    def bstack1llll11l111l_opy_(self):
        return {
            **super().bstack1llll11l111l_opy_(),
            bstack1l11l1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠ࡫ࡧࠫ⅛"): self.bstack1l1llll1l1l_opy_,
            **self.bstack1llll111l1ll_opy_()
        }
    def bstack1111l11l11_opy_(self):
        return bstack1l11l1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࠩ⅜")
    def bstack111l11llll_opy_(self, bstack1l1llll1l1l_opy_):
        self.bstack1l1llll1l1l_opy_ = bstack1l1llll1l1l_opy_