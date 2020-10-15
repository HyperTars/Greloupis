from blinker import signal
import logging
from datetime import datetime
from flask import g
from mongoengine import QuerySet, Document
import source


# mongoengine pre_update and post_update
me_pre_update = signal('me_pre_update')
me_post_update = signal('me_post_update')

# call external api pre and post signals
pre_call_api = signal('pre_call_api')
post_call_api = signal('post_call_api')

logger = logging.getLogger(__name__)


class CustomQuerySet(QuerySet):

    def update(self, *args, **kwargs):
        current_datetime = datetime.now()
        kwargs['upsert'] = False  # upsert is set to false to make created_on and modified_on flag work properly
        kwargs['modified_on'] = current_datetime
        # Used full path for accessing User model to avoid circular imports
        kwargs['modified_by'] = source.models.base.User(username=g.user_info['username'], user_id=g.user_info['user_id']) if hasattr(g, 'user_info') else source.models.base.User(username="app", user_id="0")
        if 'is_active' in kwargs:
            kwargs['status_modified_on'] = current_datetime
            kwargs['status_modified_by'] = source.models.base.User(username=g.user_info['username'], user_id=g.user_info['user_id']) if hasattr(g, 'user_info') else source.models.base.User(username="app", user_id="0")
        return super().update(*args, **kwargs)

    def update_and_signal(self, multi=True, write_concern=None, full_result=False, **update):
        """
        {'n': 1,
         'nModified': 0,
         'ok': 1,
         'updatedExisting': False,
         'upserted': ObjectId('58a46040d6b24daca3382e68')}
        """
        signal_kwargs = {
            'multi': multi,
            'write_concern': write_concern,
            'full_result': full_result,
            'update': update
        }
        signal.me_pre_update.send(self.__class__, document=self, **signal_kwargs)
        result = self.update(multi=multi, write_concern=write_concern, full_result=full_result, **update)
        signal_kwargs['result'] = result
        signal.me_post_update.send(self.__class__, document=self, **signal_kwargs)
        return result

    def insert(self, doc_or_docs, *args, **kwargs):
        current_datetime = datetime.now()
        if isinstance(doc_or_docs, Document) or issubclass(doc_or_docs.__class__, Document):
            doc_or_docs.created_on = current_datetime
            doc_or_docs.created_by = source.models.base.User(username=g.user_info['username'], user_id=g.user_info['user_id']) if hasattr(g, 'user_info') else source.models.base.User(username="app", user_id="0")
            doc_or_docs.modified_on = current_datetime
            doc_or_docs.modified_by = source.models.base.User(username=g.user_info['username'], user_id=g.user_info['user_id']) if hasattr(g, 'user_info') else source.models.base.User(username="app", user_id="0")
        else:
            for doc in doc_or_docs:
                doc.created_on = current_datetime
                doc.created_by = source.models.base.User(username=g.user_info['username'], user_id=g.user_info['user_id']) if hasattr(g, 'user_info') else source.models.base.User(username="app", user_id="0")
                doc.modified_on = current_datetime
                doc.modified_by = source.models.base.User(username=g.user_info['username'], user_id=g.user_info['user_id']) if hasattr(g, 'user_info') else source.models.base.User(username="app", user_id="0")

        return super().insert(doc_or_docs, *args, **kwargs)
