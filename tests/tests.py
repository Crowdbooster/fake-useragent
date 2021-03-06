import os
from fake_useragent import UserAgent
from fake_useragent import settings
from fake_useragent import utils


def clear(path=settings.DB):
    try:
        os.unlink(path)
    except OSError:
        pass


def check_dict(data):
    assert data.get('randomize')
    assert data.get('browsers')
    assert data.get('browsers').get('chrome')
    assert data.get('browsers').get('firefox')
    assert data.get('browsers').get('opera')
    assert data.get('browsers').get('safari')
    assert data.get('browsers').get('internetexplorer')


def test_get_no_args():
    html = utils.get(settings.BROWSERS_STATS_PAGE)

    assert len(html) > 0


def test_get_args():
    html = utils.get(settings.BROWSER_BASE_PAGE.format(browser='Firefox'))

    assert len(html) > 0


def test_get_browsers():
    browsers = utils.get_browsers()

    browser_list = []

    for browser in browsers:
        # ie becomes popular !? xD
        if browser[0] == 'Internet Explorer':
            assert int(float(browser[1])) < 20
        browser_list.append(browser[0])

    assert len(browser_list) == 5

    assert 'Firefox' in browser_list
    assert 'Opera' in browser_list
    assert 'Chrome' in browser_list
    assert 'Internet Explorer' in browser_list
    assert 'Safari' in browser_list

    global browser_list


def test_get_browser_versions():
    for browser in browser_list:
        assert (
            len(utils.get_browser_versions(browser))
            ==
            settings.BROWSERS_COUNT_LIMIT
        )


def test_load():
    fake_useragent_dict = utils.load()

    check_dict(fake_useragent_dict)

    global fake_useragent_dict


def test_write():
    clear(settings.DB)

    assert not os.path.isfile(settings.DB)

    utils.write(settings.DB, fake_useragent_dict)

    assert os.path.isfile(settings.DB)


def test_read():
    data = utils.read(settings.DB)

    check_dict(data)

    assert os.path.isfile(settings.DB)


def test_exists():
    assert utils.exist(settings.DB)


def test_rm():
    assert utils.exist(settings.DB)
    utils.rm(settings.DB)
    assert not utils.exist(settings.DB)


def test_update():
    assert not utils.exist(settings.DB)
    utils.update(settings.DB)
    assert utils.exist(settings.DB)
    utils.update(settings.DB)
    assert utils.exist(settings.DB)


def test_load_cached():
    data = utils.load_cached(settings.DB)

    check_dict(data)

    clear(settings.DB)

    data = utils.load_cached(settings.DB)

    check_dict(data)


def test_user_agent():
    clear(settings.DB)
    assert not utils.exist(settings.DB)

    ua = UserAgent(cache=False)

    assert ua.ie is not None
    assert ua.msie is not None
    assert ua.internetexplorer is not None
    assert ua.internet_explorer is not None
    assert ua['internet explorer'] is not None
    assert ua.google is not None
    assert ua.chrome is not None
    assert ua.googlechrome is not None
    assert ua.google_chrome is not None
    assert ua['google chrome'] is not None
    assert ua.firefox is not None
    assert ua.ff is not None
    assert ua.ie is not None
    assert ua.safari is not None
    assert ua.random is not None
    assert ua['random'] is not None

    assert ua.non_existing is None
    assert ua['non_existing'] is None

    data1 = ua.data

    ua.update()

    data2 = ua.data

    assert data1 == data2
    assert data1 is not data2

    clear(settings.DB)
    del ua

    ua = UserAgent()

    assert utils.exist(settings.DB)

    data1 = ua.data

    clear(settings.DB)

    ua.update()

    assert utils.exist(settings.DB)

    data2 = ua.data

    assert data1 == data2
    assert data1 is not data2
