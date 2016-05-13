#!/usr/bin/env python3

import logging
import requests

# import http.client as http_client
# http_client.HTTPConnection.debuglevel = 1


_LOGGER = logging.getLogger(__name__)

BASE_URL = "https://beta.lds.org"
MLS_URL = "{}/mls/mbr".format(BASE_URL)
HT_URL = "{}/htvt/services/v1".format(BASE_URL)
USER_AGENT = ''.join(
    ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) ',
     'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80',
     'Safari/537.36'])


class API():
    def __init__(self, username, password, session=None):
        self.session = session
        if self.session is None:
            self.session = requests.Session()

        self._login(username, password)

    def _login(self, user, password):
        _LOGGER.info("Logging in")

        # Set up the session cookie
        _LOGGER.info("Setting up session cookie")
        self.session.get('https://www.lds.org/mls/mbr/')

        # Log in
        _LOGGER.info("Log in")
        self.session.post('https://ident.lds.org/sso/UI/Login',
                          data={'action': 'login',
                                'IDToken1': user,
                                'IDToken2': password,
                                'IDButton': 'Log In',
                                'goto': '',
                                'gotoOnFail': '',
                                'SunQueryParamsString': '',
                                'encoded': 'false',
                                'gx_charset': 'UTF-8'})

    def birthday_list(self, month, months=1):
        _LOGGER.info("Getting birthday list")

        result = self.session.get(
            url='{}/services/report/birthday-list'.format(MLS_URL),
            params={'lang': 'eng',
                    'month': month,
                    'months': months},
            cookies={'clerk-resources-beta-terms': 'true'})

        _LOGGER.debug("Birthday list result (as text): %s", result.text)
        return result.json()

    def members_moved_in(self):
        result = self.session.get(
            url='{}/report/members-moved-in'.format(MLS_URL),
            params={'lang': 'eng'},
            cookies={'clerk-resources-beta-terms': 'true'})

        result = self.session.get(
            url='{}/services/report/members-moved-in/unit/4022/1'.format(
                MLS_URL),
            params={'lang': 'eng'},
            cookies={'clerk-resources-beta-terms': 'true'},
            headers={'Accept': 'application/json, text/plain, */*',
                     'Accept-Encoding': 'gzip, deflate, sdch',
                     'Accept-Language': 'en-US,en;q=0.8',
                     'Connection': 'keep-alive',
                     'Host': 'beta.lds.org',
                     'Referer': '{}/report/members-moved-in?lang=eng'.format(
                         MLS_URL),
                     'User-Agent': USER_AGENT})

        return result.json()

    def members_moved_out(self):
        self.session.get(
            url='{}/report/members-moved-out'.format(MLS_URL),
            params={'lang': 'eng'},
            cookies={'clerk-resources-beta-terms': 'true'})

        result = self.session.get(
            url='{}/services/report/members-moved-out/unit/4022/1'.format(
                MLS_URL),
            params={'lang': 'eng'},
            cookies={'clerk-resources-beta-terms': 'true'},
            headers={'Accept': 'application/json, text/plain, */*',
                     'Accept-Encoding': 'gzip, deflate, sdch',
                     'Accept-Language': 'en-US,en;q=0.8',
                     'Connection': 'keep-alive',
                     'Host': 'beta.lds.org',
                     'Referer': '{}/report/members-moved-in?lang=eng'.format(
                         MLS_URL),
                     'User-Agent': USER_AGENT})

        return result.json()

    # TODO: Change this to three separate methods
    def custom_home_and_visiting_teaching(self):
        members = self.session.get(
            url='{}/4022/members'.format(HT_URL),
            cookies={'clerk-resources-beta-terms': 'true'})
        # open("members.json", 'w').write(members.text)
        members = members.json()

        hp_data = self.session.get(
            url='{}/4022/districts/472432'.format(HT_URL),
            cookies={'clerk-resources-beta-terms': 'true'})
        # open("hp_data.json", 'w').write(hp_data.text)
        hp_data = hp_data.json()

        eq_data = self.session.get(
            url='{}/4022/districts/472433'.format(HT_URL),
            cookies={'clerk-resources-beta-terms': 'true'})
        # open("eq_data.json", 'w').write(eq_data.text)
        eq_data = eq_data.json()

        rs_data = self.session.get(
            url='{}/4022/districts/472435'.format(HT_URL),
            cookies={'clerk-resources-beta-terms': 'true'})
        # open("rs_data.json", 'w').write(rs_data.text)
        rs_data = rs_data.json()

        return {"families": members['families'],
                "hp": hp_data,
                "eq": eq_data,
                "rs": rs_data}

    def member_list(self):
        result = self.session.get(
            url='{}/services/report/member-list?lang=eng&unitNumber=4022'.format(MLS_URL),
            cookies={'clerk-resources-beta-terms': 'true'})

        return result.json()

    def individual_picture(self, member_id):
        result = self.session.get(
            url='{}/individual-photo?lang=eng&id={}'.format(MLS_URL,
                                                            member_id),
            cookies={'clerk-resources-beta-terms': 'true'})

        return result.content
