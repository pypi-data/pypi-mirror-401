import mcpath
import pytest


@pytest.mark.xfail(
    raises=NotImplementedError, reason="Feature not supported on this platform"
)
def test_java():
    resultA = mcpath.java.get_runtime("1.21.3")
    resultB = mcpath.java.get_game_dir()
    resultC = mcpath.java.get_launcher()
    resultD = mcpath.java.get_versions_dir()
    resultE = mcpath.java.get_saves_dir()
    resultF = mcpath.java.get_resource_packs_dir()
    resultG = mcpath.java.get_screenshots_dir()
    resultH = mcpath.java.get_logs_dir()
    resultI = mcpath.java.get_versions()
    resultJ = mcpath.java.get_saves()
    resultK = mcpath.java.get_resource_packs()
    resultL = mcpath.java.get_screenshots()
    resultM = mcpath.java.get_logs()
    resultN = mcpath.java.get_launcher_logs()

    assert not resultA or isinstance(resultA, str)
    assert not resultB or isinstance(resultB, str)
    assert not resultC or isinstance(resultC, str)
    assert not resultD or isinstance(resultD, str)
    assert not resultE or isinstance(resultE, str)
    assert not resultF or isinstance(resultF, str)
    assert not resultG or isinstance(resultG, str)
    assert not resultH or isinstance(resultH, str)
    assert not resultN or isinstance(resultN, str)
    assert isinstance(resultI, list)
    assert isinstance(resultJ, list)
    assert isinstance(resultK, list)
    assert isinstance(resultL, list)
    assert isinstance(resultM, list)
