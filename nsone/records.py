#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#

from nsone.rest.records import Records
from nsone.rest.stats import Stats


class RecordException(Exception):
    pass


class Record(object):

    def __init__(self, parentZone, domain, type):
        self._rest = Records(parentZone.config)
        self.parentZone = parentZone
        if not domain.endswith(parentZone.zone):
            domain = domain + '.' + parentZone.zone
        self.domain = domain
        self.type = type
        self.data = None

    def _parseModel(self, data):
        self.data = data
        self.answers = data['answers']
        # XXX break out the rest? use getattr instead?

    def load(self, callback=None, errback=None):
        if self.data:
            raise RecordException('record already loaded')

        def success(result):
            self._parseModel(result)
            if callback:
                return callback(self)
            else:
                return self
        return self._rest.retrieve(self.parentZone.zone,
                                   self.domain, self.type,
                                   callback=success, errback=errback)

    def delete(self, callback=None, errback=None):
        if not self.data:
            raise RecordException('record not loaded')

        def success(result):
            if callback:
                return callback(result)
            else:
                return result

        return self._rest.delete(self.parentZone.zone,
                                 self.domain, self.type,
                                 callback=success, errback=errback)

    def update(self, callback=None, errback=None, **kwargs):
        if not self.data:
            raise RecordException('record not loaded')

        def success(result):
            self._parseModel(result)
            if callback:
                return callback(self)
            else:
                return self

        return self._rest.update(self.parentZone.zone, self.domain, self.type,
                                 callback=success, errback=errback, **kwargs)

    def create(self, callback=None, errback=None, **kwargs):
        if self.data:
            raise RecordException('record already loaded')

        def success(result):
            self._parseModel(result)
            if callback:
                return callback(self)
            else:
                return self

        return self._rest.create(self.parentZone.zone, self.domain, self.type,
                                 callback=success, errback=errback, **kwargs)

    def qps(self, callback=None, errback=None):
        if not self.data:
            raise RecordException('record not loaded')
        stats = Stats(self.parentZone.config)
        return stats.qps(zone=self.parentZone.zone,
                         domain=self.domain,
                         type=self.type,
                         callback=callback,
                         errback=errback)