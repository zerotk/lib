import contextlib
import os


def find_all(name, path):
    result = []
    for root, dirs, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
    return result


def find_up(name, path):
    directory = os.path.abspath(path)
    while directory:
        filename = os.path.join(directory, name)
        if os.path.isfile(filename):
            return filename
        directory = os.path.dirname(directory)
    return None


@contextlib.contextmanager
def popd(dir):
    curdir= os.getcwd()
    try:
        os.chdir(dir)
        yield  os.getcwd()
    finally:
        os.chdir(curdir)


class GitIgnored(object):
    """
    Helper class to find out if a filename is being ignored by .gitignore files.
    """

    GITIGNORE_FILENAME = '.gitignore'
    GIT_ROOT_DIRECTORY = '.git'

    def __init__(self):
        pass

    @classmethod
    def filter(cls, filenames):
        return [i for i in filenames if not cls.git_ignores_path(i)]

    @classmethod
    def is_ignored(cls, filename):
        return False

    # @classmethod
    # def list(cls, filename):
    #     """
    #     Lists all gitignore files that have influence to the given filename.
    #
    #     Stops when it finds the repository root directory, in other words, when it finds the directory with a .git directory
    #     in it.
    #
    #     :param Path filename:
    #     :return list(Path):
    #     """
    #     from pathlib import Path
    #
    #     result = []
    #
    #     curdir = Path(filename)
    #     while curdir:
    #         gitignore = curdir / cls.GITIGNORE_FILENAME
    #         if gitignore.exists():
    #             result.append(gitignore)
    #
    #         if cls._is_git_root(curdir):
    #             break
    #
    #         curdir = curdir.parent
    #
    #     return result
    #
    # @classmethod
    # def _is_git_root(cls, directory):
    #     git_filename = directory / cls.GIT_ROOT_DIRECTORY
    #     return git_filename.exists()

    @classmethod
    def git_ignores_path(cls, path):
        import subprocess
        import pathlib

        path = pathlib.Path(path)

        if path.parts[-1] == '.git':  # Ignore .git directory
            return True

        child = subprocess.Popen(
            ['git', 'check-ignore', str(path)],
            cwd=str(path.parent),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        output = child.communicate()
        status = child.wait()
        # Possible return values: (via git help check-ignore)
        #    0: Yes, the file is ignored
        #    1: No, the file isn't ignored
        #  128: Fatal error, git can't tell us whether to ignore
        #
        # The latter happens a lot with python virtualenvs, since they have
        # symlinks and git gives up when you try to follow one.  But maybe you have
        # a test directory that you include with a symlink, who knows?  So we treat
        # the file as not-ignored.
        return status == 0