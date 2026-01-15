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
bstack1l111l1_opy_ (u"ࠧࠨࠢࠋࡒࡼࡸࡪࡹࡴࠡࡶࡨࡷࡹࠦࡣࡰ࡮࡯ࡩࡨࡺࡩࡰࡰࠣ࡬ࡪࡲࡰࡦࡴࠣࡹࡸ࡯࡮ࡨࠢࡧ࡭ࡷ࡫ࡣࡵࠢࡳࡽࡹ࡫ࡳࡵࠢ࡫ࡳࡴࡱࡳ࠯ࠌࠥࠦࠧ႐")
import pytest
import io
import os
from contextlib import redirect_stdout, redirect_stderr
import subprocess
import sys
def bstack111111llll_opy_(bstack111111l1l1_opy_=None, bstack111111ll11_opy_=None):
    bstack1l111l1_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡃࡰ࡮࡯ࡩࡨࡺࠠࡱࡻࡷࡩࡸࡺࠠࡵࡧࡶࡸࡸࠦࡵࡴ࡫ࡱ࡫ࠥࡶࡹࡵࡧࡶࡸࠬࡹࠠࡪࡰࡷࡩࡷࡴࡡ࡭ࠢࡄࡔࡎࡹ࠮ࠋࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡺࡥࡴࡶࡢࡥࡷ࡭ࡳࠡࠪ࡯࡭ࡸࡺࠬࠡࡱࡳࡸ࡮ࡵ࡮ࡢ࡮ࠬ࠾ࠥࡉ࡯࡮ࡲ࡯ࡩࡹ࡫ࠠ࡭࡫ࡶࡸࠥࡵࡦࠡࡲࡼࡸࡪࡹࡴࠡࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠤ࡮ࡴࡣ࡭ࡷࡧ࡭ࡳ࡭ࠠࡱࡣࡷ࡬ࡸࠦࡡ࡯ࡦࠣࡪࡱࡧࡧࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡘࡦࡱࡥࡴࠢࡳࡶࡪࡩࡥࡥࡧࡱࡧࡪࠦ࡯ࡷࡧࡵࠤࡹ࡫ࡳࡵࡡࡳࡥࡹ࡮ࡳࠡ࡫ࡩࠤࡧࡵࡴࡩࠢࡤࡶࡪࠦࡰࡳࡱࡹ࡭ࡩ࡫ࡤ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡸࡪࡹࡴࡠࡲࡤࡸ࡭ࡹࠠࠩ࡮࡬ࡷࡹࠦ࡯ࡳࠢࡶࡸࡷ࠲ࠠࡰࡲࡷ࡭ࡴࡴࡡ࡭ࠫ࠽ࠤ࡙࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࠨࡴࠫ࠲ࡨ࡮ࡸࡥࡤࡶࡲࡶࡾ࠮ࡩࡦࡵࠬࠤࡹࡵࠠࡤࡱ࡯ࡰࡪࡩࡴࠡࡨࡵࡳࡲ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡅࡤࡲࠥࡨࡥࠡࡣࠣࡷ࡮ࡴࡧ࡭ࡧࠣࡴࡦࡺࡨࠡࡵࡷࡶ࡮ࡴࡧࠡࡱࡵࠤࡱ࡯ࡳࡵࠢࡲࡪࠥࡶࡡࡵࡪࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡉࡨࡰࡲࡶࡪࡪࠠࡪࡨࠣࡸࡪࡹࡴࡠࡣࡵ࡫ࡸࠦࡩࡴࠢࡳࡶࡴࡼࡩࡥࡧࡧ࠲ࠏࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡪࡩࡤࡶ࠽ࠤࡈࡵ࡬࡭ࡧࡦࡸ࡮ࡵ࡮ࠡࡴࡨࡷࡺࡲࡴࡴࠢࡺ࡭ࡹ࡮ࠠ࡬ࡧࡼࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡳࡶࡥࡦࡩࡸࡹࠠࠩࡤࡲࡳࡱ࠯ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡤࡱࡸࡲࡹࠦࠨࡪࡰࡷ࠭ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡴ࡯ࡥࡧ࡬ࡨࡸࠦࠨ࡭࡫ࡶࡸ࠮ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡴࡦࡵࡷࡣ࡫࡯࡬ࡦࡵࠣࠬࡱ࡯ࡳࡵࠫࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡩࡷࡸ࡯ࡳࠢࠫࡷࡹࡸࠩࠋࠢࠣࠤࠥࠨࠢࠣ႑")
    try:
        bstack111111l1ll_opy_ = os.getenv(bstack1l111l1_opy_ (u"ࠢࡑ࡛ࡗࡉࡘ࡚࡟ࡄࡗࡕࡖࡊࡔࡔࡠࡖࡈࡗ࡙ࠨ႒")) is not None
        if bstack111111l1l1_opy_ is not None:
            args = list(bstack111111l1l1_opy_)
        elif bstack111111ll11_opy_ is not None:
            if isinstance(bstack111111ll11_opy_, str):
                args = [bstack111111ll11_opy_]
            elif isinstance(bstack111111ll11_opy_, list):
                args = list(bstack111111ll11_opy_)
            else:
                args = [bstack1l111l1_opy_ (u"ࠣ࠰ࠥ႓")]
        else:
            args = [bstack1l111l1_opy_ (u"ࠤ࠱ࠦ႔")]
        if bstack111111l1ll_opy_:
            return _11111l1l1l_opy_(args)
        bstack11111l11l1_opy_ = args + [
            bstack1l111l1_opy_ (u"ࠥ࠱࠲ࡩ࡯࡭࡮ࡨࡧࡹ࠳࡯࡯࡮ࡼࠦ႕"),
            bstack1l111l1_opy_ (u"ࠦ࠲࠳ࡱࡶ࡫ࡨࡸࠧ႖")
        ]
        class bstack11111l11ll_opy_:
            bstack1l111l1_opy_ (u"ࠧࠨࠢࡑࡻࡷࡩࡸࡺࠠࡱ࡮ࡸ࡫࡮ࡴࠠࡵࡪࡤࡸࠥࡩࡡࡱࡶࡸࡶࡪࡹࠠࡤࡱ࡯ࡰࡪࡩࡴࡦࡦࠣࡸࡪࡹࡴࠡ࡫ࡷࡩࡲࡹ࠮ࠣࠤࠥ႗")
            def __init__(self):
                self.bstack111111lll1_opy_ = []
                self.test_files = set()
                self.bstack11111l111l_opy_ = None
            def pytest_collection_finish(self, session):
                bstack1l111l1_opy_ (u"ࠨࠢࠣࡊࡲࡳࡰࠦࡣࡢ࡮࡯ࡩࡩࠦࡡࡧࡶࡨࡶࠥࡩ࡯࡭࡮ࡨࡧࡹ࡯࡯࡯ࠢ࡬ࡷࠥ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࠮ࠣࠤࠥ႘")
                try:
                    for item in session.items:
                        nodeid = item.nodeid
                        self.bstack111111lll1_opy_.append(nodeid)
                        if bstack1l111l1_opy_ (u"ࠢ࠻࠼ࠥ႙") in nodeid:
                            file_path = nodeid.split(bstack1l111l1_opy_ (u"ࠣ࠼࠽ࠦႚ"), 1)[0]
                            if file_path.endswith(bstack1l111l1_opy_ (u"ࠩ࠱ࡴࡾ࠭ႛ")):
                                self.test_files.add(file_path)
                except Exception as e:
                    self.bstack11111l111l_opy_ = str(e)
        collector = bstack11111l11ll_opy_()
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            exit_code = pytest.main(bstack11111l11l1_opy_, plugins=[collector])
        if collector.bstack11111l111l_opy_:
            return {bstack1l111l1_opy_ (u"ࠥࡷࡺࡩࡣࡦࡵࡶࠦႜ"): False, bstack1l111l1_opy_ (u"ࠦࡨࡵࡵ࡯ࡶࠥႝ"): 0, bstack1l111l1_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࡸࠨ႞"): [], bstack1l111l1_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫࡯࡬ࡦࡵࠥ႟"): [], bstack1l111l1_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨႠ"): bstack1l111l1_opy_ (u"ࠣࡅࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠣႡ").format(collector.bstack11111l111l_opy_)}
        return {
            bstack1l111l1_opy_ (u"ࠤࡶࡹࡨࡩࡥࡴࡵࠥႢ"): True,
            bstack1l111l1_opy_ (u"ࠥࡧࡴࡻ࡮ࡵࠤႣ"): len(collector.bstack111111lll1_opy_),
            bstack1l111l1_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࡷࠧႤ"): collector.bstack111111lll1_opy_,
            bstack1l111l1_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪ࡮ࡲࡥࡴࠤႥ"): sorted(collector.test_files),
            bstack1l111l1_opy_ (u"ࠨࡥࡹ࡫ࡷࡣࡨࡵࡤࡦࠤႦ"): exit_code
        }
    except Exception as e:
        return {bstack1l111l1_opy_ (u"ࠢࡴࡷࡦࡧࡪࡹࡳࠣႧ"): False, bstack1l111l1_opy_ (u"ࠣࡥࡲࡹࡳࡺࠢႨ"): 0, bstack1l111l1_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࡵࠥႩ"): [], bstack1l111l1_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨ࡬ࡰࡪࡹࠢႪ"): [], bstack1l111l1_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥႫ"): bstack1l111l1_opy_ (u"࡛ࠧ࡮ࡦࡺࡳࡩࡨࡺࡥࡥࠢࡨࡶࡷࡵࡲࠡ࡫ࡱࠤࡹ࡫ࡳࡵࠢࡦࡳࡱࡲࡥࡤࡶ࡬ࡳࡳࡀࠠࡼࡿࠥႬ").format(e)}
def _11111l1l1l_opy_(args):
    bstack1l111l1_opy_ (u"ࠨࠢࠣࡋࡶࡳࡱࡧࡴࡦࡦࠣࡧࡴࡲ࡬ࡦࡥࡷ࡭ࡴࡴࠠࡦࡺࡨࡧࡺࡺࡥࡥࠢ࡬ࡲࠥࡧࠠࡴࡧࡳࡥࡷࡧࡴࡦࠢࡓࡽࡹ࡮࡯࡯ࠢࡳࡶࡴࡩࡥࡴࡵࠣࡸࡴࠦࡡࡷࡱ࡬ࡨࠥࡴࡥࡴࡶࡨࡨࠥࡶࡹࡵࡧࡶࡸࠥ࡯ࡳࡴࡷࡨࡷ࠳ࠨࠢࠣႭ")
    bstack11111l1111_opy_ = [sys.executable, bstack1l111l1_opy_ (u"ࠢ࠮࡯ࠥႮ"), bstack1l111l1_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴࠣႯ"), bstack1l111l1_opy_ (u"ࠤ࠰࠱ࡨࡵ࡬࡭ࡧࡦࡸ࠲ࡵ࡮࡭ࡻࠥႰ"), bstack1l111l1_opy_ (u"ࠥ࠱࠲ࡷࡵࡪࡧࡷࠦႱ")]
    bstack11111l1l11_opy_ = [a for a in args if a not in (bstack1l111l1_opy_ (u"ࠦ࠲࠳ࡣࡰ࡮࡯ࡩࡨࡺ࠭ࡰࡰ࡯ࡽࠧႲ"), bstack1l111l1_opy_ (u"ࠧ࠳࠭ࡲࡷ࡬ࡩࡹࠨႳ"), bstack1l111l1_opy_ (u"ࠨ࠭ࡲࠤႴ"))]
    cmd = bstack11111l1111_opy_ + bstack11111l1l11_opy_
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, env=os.environ.copy())
        stdout = proc.stdout.splitlines()
        bstack111111lll1_opy_ = []
        test_files = set()
        for line in stdout:
            line = line.strip()
            if not line or bstack1l111l1_opy_ (u"ࠢࠡࡥࡲࡰࡱ࡫ࡣࡵࡧࡧࠦႵ") in line.lower():
                continue
            if bstack1l111l1_opy_ (u"ࠣ࠼࠽ࠦႶ") in line:
                bstack111111lll1_opy_.append(line)
                file_path = line.split(bstack1l111l1_opy_ (u"ࠤ࠽࠾ࠧႷ"), 1)[0]
                if file_path.endswith(bstack1l111l1_opy_ (u"ࠪ࠲ࡵࡿࠧႸ")):
                    test_files.add(file_path)
        success = proc.returncode in (0, 5)
        return {
            bstack1l111l1_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷࠧႹ"): success,
            bstack1l111l1_opy_ (u"ࠧࡩ࡯ࡶࡰࡷࠦႺ"): len(bstack111111lll1_opy_),
            bstack1l111l1_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࡹࠢႻ"): bstack111111lll1_opy_,
            bstack1l111l1_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡩ࡭ࡧࡶࠦႼ"): sorted(test_files),
            bstack1l111l1_opy_ (u"ࠣࡧࡻ࡭ࡹࡥࡣࡰࡦࡨࠦႽ"): proc.returncode,
            bstack1l111l1_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣႾ"): None if success else bstack1l111l1_opy_ (u"ࠥࡗࡺࡨࡰࡳࡱࡦࡩࡸࡹࠠࡤࡱ࡯ࡰࡪࡩࡴࡪࡱࡱࠤ࡫ࡧࡩ࡭ࡧࡧࠤ࠭࡫ࡸࡪࡶࠣࡿࢂ࠯ࠢႿ").format(proc.returncode)
        }
    except Exception as e:
        return {bstack1l111l1_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷࠧჀ"): False, bstack1l111l1_opy_ (u"ࠧࡩ࡯ࡶࡰࡷࠦჁ"): 0, bstack1l111l1_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࡹࠢჂ"): [], bstack1l111l1_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡩ࡭ࡧࡶࠦჃ"): [], bstack1l111l1_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢჄ"): bstack1l111l1_opy_ (u"ࠤࡖࡹࡧࡶࡲࡰࡥࡨࡷࡸࠦࡣࡰ࡮࡯ࡩࡨࡺࡩࡰࡰࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨჅ").format(e)}