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
import json
from bstack_utils.bstack11lllll1_opy_ import get_logger
logger = get_logger(__name__)
class bstack11l1ll1lll1_opy_(object):
  bstack1ll1lll1_opy_ = os.path.join(os.path.expanduser(bstack1l11l1l_opy_ (u"ࠩࢁࠫ៯")), bstack1l11l1l_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ៰"))
  bstack11l1lll11l1_opy_ = os.path.join(bstack1ll1lll1_opy_, bstack1l11l1l_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠴ࡪࡴࡱࡱࠫ៱"))
  commands_to_wrap = None
  perform_scan = None
  bstack1llll1ll1_opy_ = None
  bstack1ll1l1l11_opy_ = None
  bstack11l1llll111_opy_ = None
  bstack11ll11l1ll1_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack1l11l1l_opy_ (u"ࠬ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠧ៲")):
      cls.instance = super(bstack11l1ll1lll1_opy_, cls).__new__(cls)
      cls.instance.bstack11l1ll1llll_opy_()
    return cls.instance
  def bstack11l1ll1llll_opy_(self):
    try:
      with open(self.bstack11l1lll11l1_opy_, bstack1l11l1l_opy_ (u"࠭ࡲࠨ៳")) as bstack11l1lll11l_opy_:
        bstack11l1lll1111_opy_ = bstack11l1lll11l_opy_.read()
        data = json.loads(bstack11l1lll1111_opy_)
        if bstack1l11l1l_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࠩ៴") in data:
          self.bstack11ll111llll_opy_(data[bstack1l11l1l_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵࠪ៵")])
        if bstack1l11l1l_opy_ (u"ࠩࡶࡧࡷ࡯ࡰࡵࡵࠪ៶") in data:
          self.bstack11llll11_opy_(data[bstack1l11l1l_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࠫ៷")])
        if bstack1l11l1l_opy_ (u"ࠫࡳࡵ࡮ࡃࡕࡷࡥࡨࡱࡉ࡯ࡨࡵࡥࡆ࠷࠱ࡺࡅ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ៸") in data:
          self.bstack11l1lll111l_opy_(data[bstack1l11l1l_opy_ (u"ࠬࡴ࡯࡯ࡄࡖࡸࡦࡩ࡫ࡊࡰࡩࡶࡦࡇ࠱࠲ࡻࡆ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ៹")])
    except:
      pass
  def bstack11l1lll111l_opy_(self, bstack11ll11l1ll1_opy_):
    if bstack11ll11l1ll1_opy_ != None:
      self.bstack11ll11l1ll1_opy_ = bstack11ll11l1ll1_opy_
  def bstack11llll11_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack1l11l1l_opy_ (u"࠭ࡳࡤࡣࡱࠫ៺"),bstack1l11l1l_opy_ (u"ࠧࠨ៻"))
      self.bstack1llll1ll1_opy_ = scripts.get(bstack1l11l1l_opy_ (u"ࠨࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࠬ៼"),bstack1l11l1l_opy_ (u"ࠩࠪ៽"))
      self.bstack1ll1l1l11_opy_ = scripts.get(bstack1l11l1l_opy_ (u"ࠪ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠧ៾"),bstack1l11l1l_opy_ (u"ࠫࠬ៿"))
      self.bstack11l1llll111_opy_ = scripts.get(bstack1l11l1l_opy_ (u"ࠬࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠪ᠀"),bstack1l11l1l_opy_ (u"࠭ࠧ᠁"))
  def bstack11ll111llll_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def store(self):
    try:
      with open(self.bstack11l1lll11l1_opy_, bstack1l11l1l_opy_ (u"ࠧࡸࠩ᠂")) as file:
        json.dump({
          bstack1l11l1l_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡵࠥ᠃"): self.commands_to_wrap,
          bstack1l11l1l_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࡵࠥ᠄"): {
            bstack1l11l1l_opy_ (u"ࠥࡷࡨࡧ࡮ࠣ᠅"): self.perform_scan,
            bstack1l11l1l_opy_ (u"ࠦ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࠣ᠆"): self.bstack1llll1ll1_opy_,
            bstack1l11l1l_opy_ (u"ࠧ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࡕࡸࡱࡲࡧࡲࡺࠤ᠇"): self.bstack1ll1l1l11_opy_,
            bstack1l11l1l_opy_ (u"ࠨࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶࠦ᠈"): self.bstack11l1llll111_opy_
          },
          bstack1l11l1l_opy_ (u"ࠢ࡯ࡱࡱࡆࡘࡺࡡࡤ࡭ࡌࡲ࡫ࡸࡡࡂ࠳࠴ࡽࡈ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠦ᠉"): self.bstack11ll11l1ll1_opy_
        }, file)
    except Exception as e:
      logger.error(bstack1l11l1l_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡳࡵࡱࡵ࡭ࡳ࡭ࠠࡤࡱࡰࡱࡦࡴࡤࡴ࠼ࠣࡿࢂࠨ᠊").format(e))
      pass
  def bstack111lll11l_opy_(self, command_name):
    try:
      return any(command.get(bstack1l11l1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ᠋")) == command_name for command in self.commands_to_wrap)
    except:
      return False
bstack1l111lll_opy_ = bstack11l1ll1lll1_opy_()