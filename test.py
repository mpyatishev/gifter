import random
import unittest

from collections import defaultdict
from datetime import date, timedelta
from pprint import pprint
from unittest import mock

from gifter import Gift, select_gift


random.seed(232)


class GifterTestCase(unittest.TestCase):
    def setUp(self):
        self.finite_gifts = (
            Gift(name='finite gift #1',
                 quantity=10,
                 drawing_start=date(2016, 12, 8),
                 drawing_end=date(2016, 12, 10)),
            Gift(name='finite gift #2',
                 quantity=1,
                 drawing_start=date(2016, 12, 8),
                 drawing_end=date(2016, 12, 10)),
            Gift(name='finite gift #3',
                 quantity=100,
                 drawing_start=date(2016, 12, 10),
                 drawing_end=date(2016, 12, 31)),
            Gift(name='finite gift #4',
                 quantity=10,
                 drawing_start=date(2016, 12, 9),
                 drawing_end=date(2016, 12, 18)),
        )
        self.infinite_gifts = (Gift(name='infinite gift #1',),
                               Gift(name='infinite gift #2',))

    @mock.patch('gifter.datetime')
    def test_distribution(self, m_datetime):
        today = date(2016, 12, 7)
        m_today = m_datetime.date.today
        gifts = self.finite_gifts + self.infinite_gifts
        selected_gifts = {}
        for d in range(7, 32):
            m_today.return_value = today
            today_gifts = defaultdict(int)
            for user in range(1000):
                gift = select_gift(gifts)
                gift.winners += 1
                if gift in self.finite_gifts:
                    gift.quantity -= 1
                    today_gifts[gift] += 1
            selected_gifts[today] = today_gifts
            today = today + timedelta(days=1)

        pprint(selected_gifts)

        for gift in self.finite_gifts:
            print(gift, gift.quantity)
            self.assertEqual(gift.quantity, 0)


if __name__ == '__main__':
    unittest.main()
