import re
from subprocess import PIPE
from subprocess import Popen

import pytest

from dkist_dev_tools.git import git_commit_files
from dkist_dev_tools.git import git_get_v_version
from dkist_dev_tools.git import git_tag
from dkist_dev_tools.git import run_git_command
from dkist_dev_tools.version_type import Version


def test_run_git_command(tmp_path_factory):
    """
    Given: Two dirs, one with git initialized and one without
    When: Running `git status` in the two dirs through the `run_git_command` function
    Then: The initialized dir correctly runs and the un-initialized dir fails correctly depending on the value of
          the `exit_on_fail` kwarg.
    """

    good_dir = tmp_path_factory.mktemp("with_git")
    bad_dir = tmp_path_factory.mktemp("no_git")

    Popen(["git", "init"], cwd=good_dir).wait()

    args = ["status"]

    # 128 is the git exit code when running in a dir that hasn't been initialized
    with pytest.raises(SystemExit, match="128"):
        run_git_command(git_args=args, exit_on_fail=True, cmd_path=bad_dir)

    return_code, _, std_err = run_git_command(git_args=args, exit_on_fail=False, cmd_path=bad_dir)
    assert return_code == 128
    assert "fatal: not a git repository " in std_err.replace("\n", " ")

    return_code, std_out, _ = run_git_command(git_args=args, cmd_path=good_dir)
    assert return_code == 0
    assert "No commits yet" in std_out.replace("\n", " ")


def test_git_get_v_version(tmp_path_factory):
    """
    Given: Two git dirs, one with a version tag and one without
    When: Trying to get the version via `git_get_v_version`
    Then: The dir with a version tag is correctly parsed and the un-tagged dir either fails or returns None depending on
          the value of the `fail_on_no_version` kwarg
    """
    good_dir = tmp_path_factory.mktemp("with_version")
    bad_dir = tmp_path_factory.mktemp("no_version")

    v_version = "v6.6.6"

    for d in [good_dir, bad_dir]:
        first_file = d / "stuff.txt"
        first_file.write_text("I love git")
        Popen(["git", "init"], cwd=d).wait()
        Popen(["git", "add", "."], cwd=d).wait()
        Popen(["git", "commit", "-m", "first commit!"], cwd=d).wait()

    Popen(["git", "tag", v_version], cwd=good_dir).wait()

    good_version = git_get_v_version(cmd_path=good_dir)
    assert isinstance(good_version, Version)
    assert good_version.v_version == v_version

    assert git_get_v_version(cmd_path=bad_dir, fail_on_no_version=False) is None
    with pytest.raises(SystemExit, match="128"):
        git_get_v_version(cmd_path=bad_dir, fail_on_no_version=True)


def test_git_commit_files(tmp_path_factory):
    """
    Given: An initialized git directory
    When: Committing files via the `git_commit_files` function
    Then: Trying with no files fails, but valid calls succeed in making a git commit
    """
    git_dir = tmp_path_factory.mktemp("git_repo")
    Popen(["git", "init"], cwd=git_dir).wait()

    with pytest.raises(SystemExit, match="1"):
        git_commit_files(files=[], commit_message="fail", cmd_path=git_dir)

    first_file = git_dir / "stuff.txt"
    first_file.write_text("I love git")
    Popen(["git", "add", "stuff.txt"], cwd=git_dir).wait()
    git_commit_files(files=first_file, commit_message="Add stuff", cmd_path=git_dir)

    p = Popen(["git", "log", "--grep", "Add stuff"], cwd=git_dir, stdout=PIPE)
    p.wait()
    output = p.communicate()[0].decode().replace("\n", " ")

    assert p.returncode == 0
    assert "Add stuff" in output
    assert "Auto commit from `dkist-dev-tools`" in output

    # Make sure the commit actually committed the file
    p = Popen(["git", "status"], cwd=git_dir, stdout=PIPE)
    p.wait()
    output = p.communicate()[0].decode().replace("\n", " ").strip()

    assert p.returncode == 0
    assert output == "On branch main nothing to commit, working tree clean"

    # Now try with a list of files. We'll explicitly modify but not commit the first file
    first_file.write_text("I love git A LOT!!")
    second_file = git_dir / "more_stuff.txt"
    second_file.write_text("Other stuff")
    third_file = git_dir / "more_stuff_pt2.txt"
    third_file.write_text("Even more")
    Popen(["git", "add", "more_stuff.txt", "more_stuff_pt2.txt"], cwd=git_dir).wait()

    git_commit_files(
        files=[second_file, third_file], commit_message="Add two new files", cmd_path=git_dir
    )

    p = Popen(["git", "log", "--grep", "Add two new files"], cwd=git_dir, stdout=PIPE)
    p.wait()
    output = p.communicate()[0].decode().replace("\n", " ")

    assert p.returncode == 0
    assert "Add two new files" in output
    assert "Auto commit from `dkist-dev-tools`" in output

    # Make sure the modified-but-not-committed file wasn't committed
    p = Popen(["git", "status"], cwd=git_dir, stdout=PIPE)
    p.wait()
    output = p.communicate()[0].decode().replace("\n", " ")

    assert p.returncode == 0
    assert "modified:   stuff.txt" in output


def test_git_tag(tmp_path_factory):
    """
    Given: A git dir with a commit
    When: Tagging the commit with `git_tag`
    Then: The tag is correctly applied to the most recent commit
    """
    git_dir = tmp_path_factory.mktemp("git_repo_for_tags")
    Popen(["git", "init"], cwd=git_dir).wait()

    first_file = git_dir / "stuff.txt"
    first_file.write_text("I love git")
    Popen(["git", "add", "stuff.txt"], cwd=git_dir).wait()
    Popen(["git", "commit", "-m", "first commit"], cwd=git_dir).wait()

    tag = "A_Tag"

    git_tag(tag=tag, cmd_path=git_dir)

    # For some reason the git doesn't always display the tag in the output of `git log` so we'll ensure the tag was
    # applied to the correct commit by looking at the hash of the most recent commit (`-n 1`)...
    p = Popen(["git", "log", "-n", "1"], cwd=git_dir, stdout=PIPE)
    p.wait()
    log_output = p.communicate()[0].decode().replace("\n", " ")
    commit_hash = re.findall("commit (.*) Author:", log_output)[0]

    # ...and comparing it to the hash of the commit associated with the tag
    p = Popen(["git", "rev-list", "-1", tag], cwd=git_dir, stdout=PIPE)
    p.wait()
    rev_output = p.communicate()[0].decode().replace("\n", " ")

    assert commit_hash in rev_output
