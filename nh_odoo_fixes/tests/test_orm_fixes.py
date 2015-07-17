__author__ = 'wearp'
from datetime import datetime
import re
import pytz
from mock import MagicMock, patch

from openerp.osv import fields
from openerp.tests.common import TransactionCase


class TestORMFixes(TransactionCase):

    @classmethod
    def setUpClass(cls):
        cls.pattern = re.compile('\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')
        cls.date = datetime.now()

    def test_01_utc_timestamp(self):
        cr, uid = self.cr, self.uid

        timestamp = fields.datetime.utc_timestamp(cr, uid, self.date)
        result = re.match(self.pattern, timestamp)
        self.assertEquals(result.string, timestamp)

    @patch('pytz.timezone')
    def test_02_utc_timestamp_with_tz_in_context(self, timezone):
        cr, uid = self.cr, self.uid
        context = {'tz': 'GB'}
        date = datetime.now()

        fields.datetime.utc_timestamp(cr, uid, date, context=context)
        self.assertEquals(timezone.call_count, 2)
        timezone.assert_any_call('UTC')
        timezone.assert_any_call('GB')
        timezone.localize.called_with(date)


