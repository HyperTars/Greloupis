# -*- coding: utf-8 -*-

###
### DO NOT CHANGE THIS FILE
### 
### The code is auto generated, your change will be overwritten by 
### code generating.
###
from __future__ import absolute_import

from .api.user import User
from .api.user_login import UserLogin
from .api.user_logout import UserLogout
from .api.user_user_id import UserUserId
from .api.video import Video
from .api.video_video_id import VideoVideoId
from .api.search_video import SearchVideo
from .api.search_user import SearchUser
from .api.user_user_id_like import UserUserIdLike
from .api.video_video_id_like import VideoVideoIdLike
from .api.video_video_id_like_user_id import VideoVideoIdLikeUserId
from .api.user_user_id_dislike import UserUserIdDislike
from .api.video_video_id_dislike import VideoVideoIdDislike
from .api.video_video_id_dislike_user_id import VideoVideoIdDislikeUserId
from .api.user_user_id_star import UserUserIdStar
from .api.video_video_id_star import VideoVideoIdStar
from .api.video_video_id_star_user_id import VideoVideoIdStarUserId
from .api.video_video_id_view import VideoVideoIdView
from .api.user_user_id_comment import UserUserIdComment
from .api.video_video_id_comment import VideoVideoIdComment
from .api.video_video_id_comment_user_id import VideoVideoIdCommentUserId


routes = [
    dict(resource=User, urls=['/user'], endpoint='user'),
    dict(resource=UserLogin, urls=['/user/login'], endpoint='user_login'),
    dict(resource=UserLogout, urls=['/user/logout'], endpoint='user_logout'),
    dict(resource=UserUserId, urls=['/user/<user_id>'], endpoint='user_user_id'),
    dict(resource=Video, urls=['/video'], endpoint='video'),
    dict(resource=VideoVideoId, urls=['/video/<video_id>'], endpoint='video_video_id'),
    dict(resource=SearchVideo, urls=['/search/video'], endpoint='search_video'),
    dict(resource=SearchUser, urls=['/search/user'], endpoint='search_user'),
    dict(resource=UserUserIdLike, urls=['/user/<user_id>/like'], endpoint='user_user_id_like'),
    dict(resource=VideoVideoIdLike, urls=['/video/<video_id>/like'], endpoint='video_video_id_like'),
    dict(resource=VideoVideoIdLikeUserId, urls=['/video/<video_id>/like/<user_id>'], endpoint='video_video_id_like_user_id'),
    dict(resource=UserUserIdDislike, urls=['/user/<user_id>/dislike'], endpoint='user_user_id_dislike'),
    dict(resource=VideoVideoIdDislike, urls=['/video/<video_id>/dislike'], endpoint='video_video_id_dislike'),
    dict(resource=VideoVideoIdDislikeUserId, urls=['/video/<video_id>/dislike/<user_id>'], endpoint='video_video_id_dislike_user_id'),
    dict(resource=UserUserIdStar, urls=['/user/<user_id>/star'], endpoint='user_user_id_star'),
    dict(resource=VideoVideoIdStar, urls=['/video/<video_id>/star'], endpoint='video_video_id_star'),
    dict(resource=VideoVideoIdStarUserId, urls=['/video/<video_id>/star/<user_id>'], endpoint='video_video_id_star_user_id'),
    dict(resource=VideoVideoIdView, urls=['/video/<video_id>/view'], endpoint='video_video_id_view'),
    dict(resource=UserUserIdComment, urls=['/user/<user_id>/comment/'], endpoint='user_user_id_comment'),
    dict(resource=VideoVideoIdComment, urls=['/video/<video_id>/comment/'], endpoint='video_video_id_comment'),
    dict(resource=VideoVideoIdCommentUserId, urls=['/video/<video_id>/comment/<user_id>'], endpoint='video_video_id_comment_user_id'),
]