# -*- coding: utf-8 -*-

###################
# Actions on user #
###################

class User(object):

    def __init__(self, user_id: int) -> None:
        self.user = user_id

    def move_to(self, channel_id: int) -> None:
        """
        Moves the user to the specified voice channel

        :param channel_id: discord id of voice channel
        """
        pass
