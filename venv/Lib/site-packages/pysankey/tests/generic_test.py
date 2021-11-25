# -*- coding: utf-8 -*-

import unittest

import pandas as pd


class GenericTest(unittest.TestCase):

    """ Generic tests for sankey """

    @classmethod
    def setUpClass(cls):
        cls.data = ''
        cls.colorDict = ''


class TestFruit(GenericTest):

    """ Base test to test with the data in fruit.txt """

    def setUp(self):
        self.data = pd.read_csv(
            "pysankey/tests/fruits.txt", sep=" ",
            names=["true", "predicted"]
        )
        self.colorDict = {
            "apple": "#f71b1b",
            "blueberry": "#1b7ef7",
            "banana": "#f3f71b",
            "lime": "#12e23f",
            "orange": "#f78c1b",
            "kiwi": "#9BD937",
        }

class TestCustomerGood(GenericTest):

    """ Base test to test with the data in customers-goods.csv """

    def setUp(self):
        self.data = pd.read_csv(
            "pysankey/tests/customers-goods.csv",
            sep=",",
            names=["id", "customer", "good", "revenue"],
        )
