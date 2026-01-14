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
bstack1l11l1l_opy_ (u"ࠢࠣࠤࠍࡔࡾࡺࡥࡴࡶࠣࡸࡪࡹࡴࠡࡥࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲࠥ࡮ࡥ࡭ࡲࡨࡶࠥࡻࡳࡪࡰࡪࠤࡩ࡯ࡲࡦࡥࡷࠤࡵࡿࡴࡦࡵࡷࠤ࡭ࡵ࡯࡬ࡵ࠱ࠎࠧࠨࠢၯ")
import pytest
import io
import os
from contextlib import redirect_stdout, redirect_stderr
import subprocess
import sys
def bstack11111lll11_opy_(bstack11111ll1l1_opy_=None, bstack11111l1ll1_opy_=None):
    bstack1l11l1l_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡅࡲࡰࡱ࡫ࡣࡵࠢࡳࡽࡹ࡫ࡳࡵࠢࡷࡩࡸࡺࡳࠡࡷࡶ࡭ࡳ࡭ࠠࡱࡻࡷࡩࡸࡺࠧࡴࠢ࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠤࡆࡖࡉࡴ࠰ࠍࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡵࡧࡶࡸࡤࡧࡲࡨࡵࠣࠬࡱ࡯ࡳࡵ࠮ࠣࡳࡵࡺࡩࡰࡰࡤࡰ࠮ࡀࠠࡄࡱࡰࡴࡱ࡫ࡴࡦࠢ࡯࡭ࡸࡺࠠࡰࡨࠣࡴࡾࡺࡥࡴࡶࠣࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠦࡩ࡯ࡥ࡯ࡹࡩ࡯࡮ࡨࠢࡳࡥࡹ࡮ࡳࠡࡣࡱࡨࠥ࡬࡬ࡢࡩࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡚ࠥࡡ࡬ࡧࡶࠤࡵࡸࡥࡤࡧࡧࡩࡳࡩࡥࠡࡱࡹࡩࡷࠦࡴࡦࡵࡷࡣࡵࡧࡴࡩࡵࠣ࡭࡫ࠦࡢࡰࡶ࡫ࠤࡦࡸࡥࠡࡲࡵࡳࡻ࡯ࡤࡦࡦ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡺࡥࡴࡶࡢࡴࡦࡺࡨࡴࠢࠫࡰ࡮ࡹࡴࠡࡱࡵࠤࡸࡺࡲ࠭ࠢࡲࡴࡹ࡯࡯࡯ࡣ࡯࠭࠿ࠦࡔࡦࡵࡷࠤ࡫࡯࡬ࡦࠪࡶ࠭࠴ࡪࡩࡳࡧࡦࡸࡴࡸࡹࠩ࡫ࡨࡷ࠮ࠦࡴࡰࠢࡦࡳࡱࡲࡥࡤࡶࠣࡪࡷࡵ࡭࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡇࡦࡴࠠࡣࡧࠣࡥࠥࡹࡩ࡯ࡩ࡯ࡩࠥࡶࡡࡵࡪࠣࡷࡹࡸࡩ࡯ࡩࠣࡳࡷࠦ࡬ࡪࡵࡷࠤࡴ࡬ࠠࡱࡣࡷ࡬ࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡋࡪࡲࡴࡸࡥࡥࠢ࡬ࡪࠥࡺࡥࡴࡶࡢࡥࡷ࡭ࡳࠡ࡫ࡶࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡩ࠴ࠊࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡥ࡫ࡦࡸ࠿ࠦࡃࡰ࡮࡯ࡩࡨࡺࡩࡰࡰࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡼ࡯ࡴࡩࠢ࡮ࡩࡾࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡵࡸࡧࡨ࡫ࡳࡴࠢࠫࡦࡴࡵ࡬ࠪࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡦࡳࡺࡴࡴࠡࠪ࡬ࡲࡹ࠯ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠ࡯ࡱࡧࡩ࡮ࡪࡳࠡࠪ࡯࡭ࡸࡺࠩࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡶࡨࡷࡹࡥࡦࡪ࡮ࡨࡷࠥ࠮࡬ࡪࡵࡷ࠭ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥ࡫ࡲࡳࡱࡵࠤ࠭ࡹࡴࡳࠫࠍࠤࠥࠦࠠࠣࠤࠥၰ")
    try:
        bstack11111l1l1l_opy_ = os.getenv(bstack1l11l1l_opy_ (u"ࠤࡓ࡝࡙ࡋࡓࡕࡡࡆ࡙ࡗࡘࡅࡏࡖࡢࡘࡊ࡙ࡔࠣၱ")) is not None
        if bstack11111ll1l1_opy_ is not None:
            args = list(bstack11111ll1l1_opy_)
        elif bstack11111l1ll1_opy_ is not None:
            if isinstance(bstack11111l1ll1_opy_, str):
                args = [bstack11111l1ll1_opy_]
            elif isinstance(bstack11111l1ll1_opy_, list):
                args = list(bstack11111l1ll1_opy_)
            else:
                args = [bstack1l11l1l_opy_ (u"ࠥ࠲ࠧၲ")]
        else:
            args = [bstack1l11l1l_opy_ (u"ࠦ࠳ࠨၳ")]
        if bstack11111l1l1l_opy_:
            return _11111llll1_opy_(args)
        bstack11111l1l11_opy_ = args + [
            bstack1l11l1l_opy_ (u"ࠧ࠳࠭ࡤࡱ࡯ࡰࡪࡩࡴ࠮ࡱࡱࡰࡾࠨၴ"),
            bstack1l11l1l_opy_ (u"ࠨ࠭࠮ࡳࡸ࡭ࡪࡺࠢၵ")
        ]
        class bstack11111l1lll_opy_:
            bstack1l11l1l_opy_ (u"ࠢࠣࠤࡓࡽࡹ࡫ࡳࡵࠢࡳࡰࡺ࡭ࡩ࡯ࠢࡷ࡬ࡦࡺࠠࡤࡣࡳࡸࡺࡸࡥࡴࠢࡦࡳࡱࡲࡥࡤࡶࡨࡨࠥࡺࡥࡴࡶࠣ࡭ࡹ࡫࡭ࡴ࠰ࠥࠦࠧၶ")
            def __init__(self):
                self.bstack11111lll1l_opy_ = []
                self.test_files = set()
                self.bstack11111ll111_opy_ = None
            def pytest_collection_finish(self, session):
                bstack1l11l1l_opy_ (u"ࠣࠤࠥࡌࡴࡵ࡫ࠡࡥࡤࡰࡱ࡫ࡤࠡࡣࡩࡸࡪࡸࠠࡤࡱ࡯ࡰࡪࡩࡴࡪࡱࡱࠤ࡮ࡹࠠࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥ࠰ࠥࠦࠧၷ")
                try:
                    for item in session.items:
                        nodeid = item.nodeid
                        self.bstack11111lll1l_opy_.append(nodeid)
                        if bstack1l11l1l_opy_ (u"ࠤ࠽࠾ࠧၸ") in nodeid:
                            file_path = nodeid.split(bstack1l11l1l_opy_ (u"ࠥ࠾࠿ࠨၹ"), 1)[0]
                            if file_path.endswith(bstack1l11l1l_opy_ (u"ࠫ࠳ࡶࡹࠨၺ")):
                                self.test_files.add(file_path)
                except Exception as e:
                    self.bstack11111ll111_opy_ = str(e)
        collector = bstack11111l1lll_opy_()
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            exit_code = pytest.main(bstack11111l1l11_opy_, plugins=[collector])
        if collector.bstack11111ll111_opy_:
            return {bstack1l11l1l_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸࠨၻ"): False, bstack1l11l1l_opy_ (u"ࠨࡣࡰࡷࡱࡸࠧၼ"): 0, bstack1l11l1l_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࡳࠣၽ"): [], bstack1l11l1l_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡪ࡮ࡨࡷࠧၾ"): [], bstack1l11l1l_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣၿ"): bstack1l11l1l_opy_ (u"ࠥࡇࡴࡲ࡬ࡦࡥࡷ࡭ࡴࡴࠠࡦࡴࡵࡳࡷࡀࠠࡼࡿࠥႀ").format(collector.bstack11111ll111_opy_)}
        return {
            bstack1l11l1l_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷࠧႁ"): True,
            bstack1l11l1l_opy_ (u"ࠧࡩ࡯ࡶࡰࡷࠦႂ"): len(collector.bstack11111lll1l_opy_),
            bstack1l11l1l_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࡹࠢႃ"): collector.bstack11111lll1l_opy_,
            bstack1l11l1l_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡩ࡭ࡧࡶࠦႄ"): sorted(collector.test_files),
            bstack1l11l1l_opy_ (u"ࠣࡧࡻ࡭ࡹࡥࡣࡰࡦࡨࠦႅ"): exit_code
        }
    except Exception as e:
        return {bstack1l11l1l_opy_ (u"ࠤࡶࡹࡨࡩࡥࡴࡵࠥႆ"): False, bstack1l11l1l_opy_ (u"ࠥࡧࡴࡻ࡮ࡵࠤႇ"): 0, bstack1l11l1l_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࡷࠧႈ"): [], bstack1l11l1l_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪ࡮ࡲࡥࡴࠤႉ"): [], bstack1l11l1l_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧႊ"): bstack1l11l1l_opy_ (u"ࠢࡖࡰࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࡪࡸࡲࡰࡴࠣ࡭ࡳࠦࡴࡦࡵࡷࠤࡨࡵ࡬࡭ࡧࡦࡸ࡮ࡵ࡮࠻ࠢࡾࢁࠧႋ").format(e)}
def _11111llll1_opy_(args):
    bstack1l11l1l_opy_ (u"ࠣࠤࠥࡍࡸࡵ࡬ࡢࡶࡨࡨࠥࡩ࡯࡭࡮ࡨࡧࡹ࡯࡯࡯ࠢࡨࡼࡪࡩࡵࡵࡧࡧࠤ࡮ࡴࠠࡢࠢࡶࡩࡵࡧࡲࡢࡶࡨࠤࡕࡿࡴࡩࡱࡱࠤࡵࡸ࡯ࡤࡧࡶࡷࠥࡺ࡯ࠡࡣࡹࡳ࡮ࡪࠠ࡯ࡧࡶࡸࡪࡪࠠࡱࡻࡷࡩࡸࡺࠠࡪࡵࡶࡹࡪࡹ࠮ࠣࠤࠥႌ")
    bstack11111lllll_opy_ = [sys.executable, bstack1l11l1l_opy_ (u"ࠤ࠰ࡱႍࠧ"), bstack1l11l1l_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࠥႎ"), bstack1l11l1l_opy_ (u"ࠦ࠲࠳ࡣࡰ࡮࡯ࡩࡨࡺ࠭ࡰࡰ࡯ࡽࠧႏ"), bstack1l11l1l_opy_ (u"ࠧ࠳࠭ࡲࡷ࡬ࡩࡹࠨ႐")]
    bstack11111ll11l_opy_ = [a for a in args if a not in (bstack1l11l1l_opy_ (u"ࠨ࠭࠮ࡥࡲࡰࡱ࡫ࡣࡵ࠯ࡲࡲࡱࡿࠢ႑"), bstack1l11l1l_opy_ (u"ࠢ࠮࠯ࡴࡹ࡮࡫ࡴࠣ႒"), bstack1l11l1l_opy_ (u"ࠣ࠯ࡴࠦ႓"))]
    cmd = bstack11111lllll_opy_ + bstack11111ll11l_opy_
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, env=os.environ.copy())
        stdout = proc.stdout.splitlines()
        bstack11111lll1l_opy_ = []
        test_files = set()
        for line in stdout:
            line = line.strip()
            if not line or bstack1l11l1l_opy_ (u"ࠤࠣࡧࡴࡲ࡬ࡦࡥࡷࡩࡩࠨ႔") in line.lower():
                continue
            if bstack1l11l1l_opy_ (u"ࠥ࠾࠿ࠨ႕") in line:
                bstack11111lll1l_opy_.append(line)
                file_path = line.split(bstack1l11l1l_opy_ (u"ࠦ࠿ࡀࠢ႖"), 1)[0]
                if file_path.endswith(bstack1l11l1l_opy_ (u"ࠬ࠴ࡰࡺࠩ႗")):
                    test_files.add(file_path)
        success = proc.returncode in (0, 5)
        return {
            bstack1l11l1l_opy_ (u"ࠨࡳࡶࡥࡦࡩࡸࡹࠢ႘"): success,
            bstack1l11l1l_opy_ (u"ࠢࡤࡱࡸࡲࡹࠨ႙"): len(bstack11111lll1l_opy_),
            bstack1l11l1l_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࡴࠤႚ"): bstack11111lll1l_opy_,
            bstack1l11l1l_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫࡯ࡩࡸࠨႛ"): sorted(test_files),
            bstack1l11l1l_opy_ (u"ࠥࡩࡽ࡯ࡴࡠࡥࡲࡨࡪࠨႜ"): proc.returncode,
            bstack1l11l1l_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥႝ"): None if success else bstack1l11l1l_opy_ (u"࡙ࠧࡵࡣࡲࡵࡳࡨ࡫ࡳࡴࠢࡦࡳࡱࡲࡥࡤࡶ࡬ࡳࡳࠦࡦࡢ࡫࡯ࡩࡩࠦࠨࡦࡺ࡬ࡸࠥࢁࡽࠪࠤ႞").format(proc.returncode)
        }
    except Exception as e:
        return {bstack1l11l1l_opy_ (u"ࠨࡳࡶࡥࡦࡩࡸࡹࠢ႟"): False, bstack1l11l1l_opy_ (u"ࠢࡤࡱࡸࡲࡹࠨႠ"): 0, bstack1l11l1l_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࡴࠤႡ"): [], bstack1l11l1l_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫࡯ࡩࡸࠨႢ"): [], bstack1l11l1l_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤႣ"): bstack1l11l1l_opy_ (u"ࠦࡘࡻࡢࡱࡴࡲࡧࡪࡹࡳࠡࡥࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠣႤ").format(e)}