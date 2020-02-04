#!/usr/bin/env python3

import unittest
import doctest

from za_business_time_delta import za_business_time_delta


def load_tests(loader, suite, ignore):
    suite.addTests(doctest.DocTestSuite(za_business_time_delta))
    suite.addTest(doctest.DocFileSuite('test_za_business_time_delta.txt'))
    return suite


def test():
    unittest.main(verbosity=2)


if __name__ == '__main__':
    test()
