import config
from utils import Utils
import json
import time
import logging
logger = logging.getLogger(__name__)


class Mails:
    """Get and read mails."""
    ut = Utils()

    def __init__(self, player):
        """Mails class init.

        Args:
            player: contains player with username, password and uhash
        """
        self.username = player.username
        self.password = player.password
        self.uhash = player.uhash
        self.wait_load = config.wait_load

    def get_mails_list(self):
        """Get mails list.

        Input:
            {"action":"list","time":"1503384535","uhash":"75f1750fe5af53125a9331cf7783c55cd07548d55243e2eb53ec532bb384e342",
             "user":"username","pass":"password"}

        Return:
            {"elo":"2922","money":"12169318","data":[
            {"from":"vHack XT","id":"579218",
             "subject":"Mission Reward!","time":"1502967015","read":"0"},
            {"from":"vHack XT","id":"293963",
             "subject":"Special reward!","time":"1502564235","read":"1"},
            {"from":"vHack XT","id":"289849",
             "subject":"Tournament Reward","time":"1502528410","read":"1"}]}
        """
        response = self.ut.requestString(self.username,
                                         self.password,
                                         self.uhash,
                                         "vh_mails.php",
                                         action="list")

        try:
            return json.loads(response)
        except Exception as e:
            logger.error('get_mails_list: {}'.format(e))
            return ''

    def get_mail(self, mID):
        """Get mail content

        Args:
            mID (str): mails ID from `id` in `get_mails_list['data']`

        Input:
            {"action":"getmail","time":"1503061118","uhash":"c5f3eb2c071c7b74364398977717958cb0dab8e992ae422833e5538f83b7b3e2",
             "mID":"586681","user":"username","pass":"password"}

        Return:
            Mail content
        """
        return self.ut.requestString(self.username,
                                     self.password,
                                     self.uhash,
                                     "vh_mails.php",
                                     action="getmail",
                                     mID=mID)

    def read_mails(self):
        """Read all unread mail"""
        time.sleep(self.wait_load)
        response = self.get_mails_list()
        try:
            for unread in response['data']:
                time.sleep(self.wait_load)
                if unread['read'] == "0":
                    logger.info(self.get_mail(mID=unread['id']))
        except Exception as e:
            logger.error('read_mails: {}'.format(e))
        return
