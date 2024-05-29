# -*- coding: utf-8 -*-

###################
# Actions on user #
###################

class User(object):
    """
    Describes Discord user

    Attributes:
    - user (int): Discord id
    """

    def __init__(self, user_id: int) -> None:
        """
        Init Discord user object

        :param user_id: user discord id
        """
        self.user = user_id

    def move_to(self, channel_id: int) -> None:  # ToDo
        """
        Moves the user to the specified voice channel

        :param channel_id: discord id of voice channel
        """
        pass
