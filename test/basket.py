#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from unittest import TestCase
from unittest import main


class FixturesTest(TestCase):

    def setUp(self):
        print('In setUp()')
        self.fixture = range(1, 10)

    def tearDown(self):
        print('In tearDown()')
        del self.fixture

    def test(self):
        print('in test()')
        self.assertEqual(self.fixture, range(1, 10))

if __name__ == '__main__':
    main()
