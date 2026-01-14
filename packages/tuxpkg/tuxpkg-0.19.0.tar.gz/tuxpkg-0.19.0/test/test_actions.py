import os
import subprocess

import pytest
from pathlib import Path
from tuxpkg import actions
from tuxpkg.actions import Action
from tuxpkg.actions import PointToFile
from tuxpkg.actions import RunScript
from tuxpkg.actions import CopyDirectory
from tuxpkg.actions import CompositeAction
from tuxpkg.actions import detect_platform


@pytest.fixture
def set_platform():
    """Fixture to safely set and reset platform preference"""
    original = actions.init_platform

    def _set_platform(platform: str):
        actions.init_platform = platform

    yield _set_platform

    # Cleanup - always restore original value
    actions.init_platform = original


@pytest.fixture
def temp_cwd(tmp_path):
    """Fixture to temporarily change to tmp_path and restore cwd"""
    original_cwd = os.getcwd()
    os.chdir(tmp_path)
    yield tmp_path
    os.chdir(original_cwd)


class TestAction:
    def test_is_callable(self):
        action = Action()
        action()


class TestPointToFile:
    def test_shows_content(self, capsys):
        action = PointToFile("tuxpkg.mk")
        action()
        out, _ = capsys.readouterr()
        file = Path(out.strip())
        assert file.exists


class TestRunScript:
    def test_runs_script(self, mocker):
        execv = mocker.patch("os.execv")
        run_script = RunScript("create-repository")
        run_script()
        execv.assert_called()
        script_path = Path(execv.call_args[0][0])
        assert script_path.name == "create-repository"
        assert script_path.exists()
        assert type(execv.call_args[0][1]) in [list, tuple]


class TestCopyDirectory:
    def test_copies_files(self, temp_cwd, set_platform):
        set_platform("gitlab")
        action = CopyDirectory("init")
        action()

        # copies files
        assert (temp_cwd / "Dockerfile.ci-fedora").exists()
        assert (temp_cwd / "Dockerfile.ci-archlinux").exists()
        # subdirectories
        assert (temp_cwd / "debian" / "rules").exists()
        # template expansion
        assert temp_cwd.name in (temp_cwd / "Makefile").read_text()
        # template expansion in directory names
        name = temp_cwd.name
        assert (temp_cwd / name / "__init__.py").exists()
        # template expansion in template names
        assert (temp_cwd / name).with_suffix(".spec").exists()
        assert (temp_cwd / name).with_suffix(".PKGBUILD").exists()
        # file mode
        assert os.access(str(temp_cwd / "debian" / "rules"), os.X_OK)

    def test_wont_override_existing_files(self, temp_cwd, set_platform):
        set_platform("gitlab")
        Path("Makefile").write_text("")  # template
        Path("Dockerfile.ci-fedora").write_text("")  # regular file
        action = CopyDirectory("init")
        action()

        assert (temp_cwd / "Makefile").read_text() == ""
        assert (temp_cwd / "Dockerfile.ci-fedora").read_text() == ""

    def test_force_overrides_existing_files(self, tmp_path):
        cwd = os.getcwd()
        actions.init_platform = "gitlab"
        actions.init_force = True
        try:
            os.chdir(tmp_path)
            Path("Makefile").write_text("")  # template
            Path("Dockerfile.ci-fedora").write_text("")  # regular file
            action = CopyDirectory("init")
            action()
        finally:
            os.chdir(cwd)
            actions.init_platform = "auto"
            actions.init_force = False

        # Files should be overwritten when --force is used
        assert (tmp_path / "Makefile").read_text() != ""
        assert (tmp_path / "Dockerfile.ci-fedora").read_text() != ""


class TestCopyDirectoryPlatform:
    def test_copies_gitlab_ci_for_gitlab_platform(self, temp_cwd, set_platform):
        set_platform("gitlab")
        action = CopyDirectory("init")
        action()

        # GitLab CI file should exist
        assert (temp_cwd / ".gitlab-ci.yml").exists()
        # GitHub Actions should NOT exist
        assert not (temp_cwd / ".github").exists()

    def test_copies_github_actions_for_github_platform(self, temp_cwd, set_platform):
        set_platform("github")
        action = CopyDirectory("init")
        action()

        # GitHub Actions should exist
        assert (temp_cwd / ".github" / "workflows" / "ci.yml").exists()
        # GitLab CI file should NOT exist
        assert not (temp_cwd / ".gitlab-ci.yml").exists()

    def test_auto_detects_platform(self, temp_cwd, mocker):
        mocker.patch("tuxpkg.actions.detect_platform", return_value="github")
        # Ensure init_platform is "auto" to trigger detect_platform()
        assert actions.init_platform == "auto"
        action = CopyDirectory("init")
        action()

        # Verify detect_platform was used and returned github
        assert action.platform == "github"


class TestDetectPlatform:
    def test_detect_gitlab_by_default(self, mocker):
        # When git command fails or returns non-github URL
        mocker.patch(
            "subprocess.run",
            return_value=mocker.Mock(stdout="git@gitlab.com:Linaro/tuxpkg.git\n"),
        )
        assert detect_platform() == "gitlab"

    def test_detect_github_from_ssh_url(self, mocker):
        mocker.patch(
            "subprocess.run",
            return_value=mocker.Mock(stdout="git@github.com:user/repo.git\n"),
        )
        assert detect_platform() == "github"

    def test_detect_github_from_https_url(self, mocker):
        mocker.patch(
            "subprocess.run",
            return_value=mocker.Mock(stdout="https://github.com/user/repo.git\n"),
        )
        assert detect_platform() == "github"

    def test_raises_error_when_no_remote(self, mocker):
        mocker.patch(
            "subprocess.run",
            side_effect=subprocess.CalledProcessError(1, "git"),
        )
        with pytest.raises(RuntimeError, match="no git remote configured"):
            detect_platform()

    def test_raises_error_when_git_not_installed(self, mocker):
        mocker.patch("subprocess.run", side_effect=FileNotFoundError())
        with pytest.raises(RuntimeError, match="git is not installed"):
            detect_platform()


class TestCompositeAction:
    def test_runs_all_subactions(self):
        class TestAction(Action):
            called = False

            def __call__(self):
                self.called = True

        action1 = TestAction()
        action2 = TestAction()
        composite = CompositeAction(action1, action2)
        composite()
        assert action1.called
        assert action2.called
