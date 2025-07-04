from pytest import mark
from .identity import url_identity


@mark.parametrize('identity, url', [
    # bare domain is untouched
    ('fivethirtyeight.com', 'https://fivethirtyeight.com/features/lionel-messi-is-impossible/'),

    # less than three domain parts is unchanged
    ('www.com', 'https://www.com'),


    # -- standard top level domains are removed

    # `blog` is removed
    ('lastpass.com', 'https://blog.lastpass.com/2022/12/notice-of-recent-security-incident/'),

    # `web` is removed
    ('archive.org', 'https://web.archive.org'),
    ('lrb.co.uk', 'https://www.lrb.co.uk/the-paper/v45/n11/neal-ascherson/kings-grew-pale'),

    # `www` is removed
    ('nature.com', 'https://www.nature.com/articles/srep00487'),

    # `www2` domain is removed
    ('lib.uchicago.edu', 'https://www2.lib.uchicago.edu/keith/emacs'),


    # -- `/<user>/<...>` paths

    ('gitlab.com/cznic', 'https://gitlab.com/cznic/sqlite'),
    ('sites.google.com/site/misterzeropage', 'https://sites.google.com/site/misterzeropage/'),
    ('people.kernel.org/monsieuricon', 'https://people.kernel.org/monsieuricon/fix-your-mutt'),
    ('kickstarter.com/projects/robwalling', 'https://www.kickstarter.com/projects/robwalling/the-saas-playbook-by-rob-walling'),
    ('devblogs.microsoft.com/oldnewthing', 'https://devblogs.microsoft.com/oldnewthing/20221216-00/?p=107598'),
    ('codeberg.org/loke', 'https://codeberg.org/loke/array'),


    # == `/~<user>/<...>` paths

    ('sr.ht/~icefox', 'https://sr.ht/~icefox/oorandom/'),
    ('git.sr.ht/~akkartik', 'https://git.sr.ht/~akkartik/snap.love'),


    # -- `/@<user>/<...>` paths

    ('flipboard.social/@mike', 'https://flipboard.social/@mike/110137461654913391'),
    ('floss.social/@ademalsasa', 'https://floss.social/@ademalsasa/109597861116785251'),
    ('mastodon.social/@mastodonusercount', 'https://mastodon.social/@mastodonusercount/110051957865629817'),
    ('social.network.europa.eu/@EU_Commission', 'https://social.network.europa.eu/@EU_Commission/110140022257601348'),
    ('social.treehouse.systems/@marcan', 'https://social.treehouse.systems/@marcan/109917995005981968'),
    ('mastodon.nl/@vickyvdtogt', 'https://mastodon.nl/@vickyvdtogt/110196805189572082'),
    ('masto.ai/@mg', 'https://masto.ai/@mg/110212843144499061'),


    # -- package repositories

    ('crates.io/crates/fundsp', 'https://crates.io/crates/fundsp/0.13.0'),
    ('npmjs.com/package/express', 'https://www.npmjs.com/package/express'),
    ('pypi.org/project/pytest', 'https://pypi.org/project/pytest/'),

    # -- bluesky

    ('bsky.app/profile/duetosymmetry.com', 'https://bsky.app/profile/duetosymmetry.com/post/3knzeem5w362r'),
    ('bsky.app/profile/makai.chaotic.ninja', 'https://bsky.app/profile/makai.chaotic.ninja/post/3kofrm3pcvc2p'),

    # -- github

    ('github.com', 'https://github.com'),
    ('github.com/electronicarts', 'https://github.com/electronicarts/EAStdC/blob/master/include/EAStdC/EABitTricks.h'),
    ('github.com/Immediate-Mode-UI', 'https://github.com/Immediate-Mode-UI'),
    ('github.com/Immediate-Mode-UI', 'https://github.com/Immediate-Mode-UI/Nuklear'),
    ('github.com/microsoft', 'https://github.com/microsoft/WSA/discussions/167'),
    ('github.com/readme', 'https://github.com/readme/featured/nuclear-fusion-open-source'),
    ('github.com/timvisee', 'https://gist.github.com/timvisee/fcda9bbdff88d45cc9061606b4b923ca'),


    # -- medium

    ('felipepepe.medium.com', 'https://felipepepe.medium.com/before-genshin-impact-a-brief-history-of-chinese-rpgs-bc962fc29908'),
    ('medium.com/@ElizAyer', 'https://medium.com/@ElizAyer/meetings-are-the-work-9e429dde6aa3'),


    # -- reddit

    ('reddit.com/r/printSF', 'https://www.reddit.com/r/printSF'),
    ('reddit.com/r/printSF', 'https://www.reddit.com/r/printSF/comments/zuit3f/best_place_to_start_reading_isaac_asimov/'),
    ('reddit.com', 'https://www.reddit.com'),
    ('reddit.com', 'https://www.reddit.com/rules/'),
    ('reddit.com', 'https://www.reddit.com/wiki/reddiquette/'),

    # `old.reddit.com`
    ('reddit.com/r/YouShouldKnow', 'https://old.reddit.com/r/YouShouldKnow/comments/zl8ko3/ysk_apple_music_deletes_your_original_songs_and/'),


    # -- special cases

    # `lite.cnn.com`
    ('cnn.com', 'https://lite.cnn.com/2025/06/16/science/fast-radio-bursts-missing-matter'),

    # `text.npr.org'
    ('npr.org', 'https://text.npr.org/1144331954'),
])
def test_url_identity(identity, url):
    assert url_identity(url) == identity
