

def test_gitignored_filter(datadir):
    from zerotk.lib.path import GitIgnored

    filenames = [
        datadir / 'test_00/ignored/alpha.txt',
        datadir / 'test_00/included/alpha.txt',
    ]

    assert GitIgnored.filter(filenames) == [
        datadir / 'test_00/included/alpha.txt',
    ]


# def _test_gitignored_list(datadir, monkeypatch):
#     from zerotk.lib.path import GitIgnored
#
#     monkeypatch.setattr(GitIgnored, 'GIT_ROOT_DIRECTORY', 'git-root.txt')
#     assert GitIgnored.list(datadir / 'test_00/ignored/alpha.txt') == [
#         datadir / 'test_00/.gitignore'
#     ]
