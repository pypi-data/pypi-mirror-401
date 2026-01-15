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
import json
from bstack_utils.bstack1ll1lll11_opy_ import get_logger
logger = get_logger(__name__)
class bstack11l1ll11l11_opy_(object):
  bstack1lll1l1l1_opy_ = os.path.join(os.path.expanduser(bstack1l111l1_opy_ (u"ࠧࡿࠩ᠐")), bstack1l111l1_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ᠑"))
  bstack11l1ll11ll1_opy_ = os.path.join(bstack1lll1l1l1_opy_, bstack1l111l1_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶ࠲࡯ࡹ࡯࡯ࠩ᠒"))
  commands_to_wrap = None
  perform_scan = None
  bstack1ll111ll1_opy_ = None
  bstack11l1111l11_opy_ = None
  bstack11ll11l11l1_opy_ = None
  bstack11l1lllll1l_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack1l111l1_opy_ (u"ࠪ࡭ࡳࡹࡴࡢࡰࡦࡩࠬ᠓")):
      cls.instance = super(bstack11l1ll11l11_opy_, cls).__new__(cls)
      cls.instance.bstack11l1ll1l111_opy_()
    return cls.instance
  def bstack11l1ll1l111_opy_(self):
    try:
      with open(self.bstack11l1ll11ll1_opy_, bstack1l111l1_opy_ (u"ࠫࡷ࠭᠔")) as bstack1l1111l1_opy_:
        bstack11l1ll11lll_opy_ = bstack1l1111l1_opy_.read()
        data = json.loads(bstack11l1ll11lll_opy_)
        if bstack1l111l1_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࠧ᠕") in data:
          self.bstack11l1lll1lll_opy_(data[bstack1l111l1_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳࠨ᠖")])
        if bstack1l111l1_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨ᠗") in data:
          self.bstack11l111ll11_opy_(data[bstack1l111l1_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࠩ᠘")])
        if bstack1l111l1_opy_ (u"ࠩࡱࡳࡳࡈࡓࡵࡣࡦ࡯ࡎࡴࡦࡳࡣࡄ࠵࠶ࡿࡃࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭᠙") in data:
          self.bstack11l1ll11l1l_opy_(data[bstack1l111l1_opy_ (u"ࠪࡲࡴࡴࡂࡔࡶࡤࡧࡰࡏ࡮ࡧࡴࡤࡅ࠶࠷ࡹࡄࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ᠚")])
    except:
      pass
  def bstack11l1ll11l1l_opy_(self, bstack11l1lllll1l_opy_):
    if bstack11l1lllll1l_opy_ != None:
      self.bstack11l1lllll1l_opy_ = bstack11l1lllll1l_opy_
  def bstack11l111ll11_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack1l111l1_opy_ (u"ࠫࡸࡩࡡ࡯ࠩ᠛"),bstack1l111l1_opy_ (u"ࠬ࠭᠜"))
      self.bstack1ll111ll1_opy_ = scripts.get(bstack1l111l1_opy_ (u"࠭ࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠪ᠝"),bstack1l111l1_opy_ (u"ࠧࠨ᠞"))
      self.bstack11l1111l11_opy_ = scripts.get(bstack1l111l1_opy_ (u"ࠨࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࡘࡻ࡭࡮ࡣࡵࡽࠬ᠟"),bstack1l111l1_opy_ (u"ࠩࠪᠠ"))
      self.bstack11ll11l11l1_opy_ = scripts.get(bstack1l111l1_opy_ (u"ࠪࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠨᠡ"),bstack1l111l1_opy_ (u"ࠫࠬᠢ"))
  def bstack11l1lll1lll_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def store(self):
    try:
      with open(self.bstack11l1ll11ll1_opy_, bstack1l111l1_opy_ (u"ࠬࡽࠧᠣ")) as file:
        json.dump({
          bstack1l111l1_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࡳࠣᠤ"): self.commands_to_wrap,
          bstack1l111l1_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࡳࠣᠥ"): {
            bstack1l111l1_opy_ (u"ࠣࡵࡦࡥࡳࠨᠦ"): self.perform_scan,
            bstack1l111l1_opy_ (u"ࠤࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸࠨᠧ"): self.bstack1ll111ll1_opy_,
            bstack1l111l1_opy_ (u"ࠥ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠢᠨ"): self.bstack11l1111l11_opy_,
            bstack1l111l1_opy_ (u"ࠦࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠤᠩ"): self.bstack11ll11l11l1_opy_
          },
          bstack1l111l1_opy_ (u"ࠧࡴ࡯࡯ࡄࡖࡸࡦࡩ࡫ࡊࡰࡩࡶࡦࡇ࠱࠲ࡻࡆ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠤᠪ"): self.bstack11l1lllll1l_opy_
        }, file)
    except Exception as e:
      logger.error(bstack1l111l1_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡸࡺ࡯ࡳ࡫ࡱ࡫ࠥࡩ࡯࡮࡯ࡤࡲࡩࡹ࠺ࠡࡽࢀࠦᠫ").format(e))
      pass
  def bstack111l11lll_opy_(self, command_name):
    try:
      return any(command.get(bstack1l111l1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᠬ")) == command_name for command in self.commands_to_wrap)
    except:
      return False
bstack1l111l1l_opy_ = bstack11l1ll11l11_opy_()