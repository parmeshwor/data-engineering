import unittest
from amazon_store import Item, Address, User, Buyer, Seller


class TestItem(unittest.TestCase):

    def setUp(self):
        self._item = Item(id=1, name="s21 ultra", description="samsung phone")

    def test_review(self):
        self._item.review = " first review"
        expected = [" first review"]
        self.assertEqual(expected, self._item.review,)

        self._item.review = "second review "
        expected = [" first review", "second review "]
        self.assertEqual(expected, self._item.review)

    def test_review_2(self):
        self._item.review = " third review"
        expected = [" third review"]
        self.assertEqual(expected, self._item.review,)

    def tearDown(self):
        del self._item


class TestAddress(unittest.TestCase):

    def setUp(self):
        self.address = Address()

    def test_full_address(self):
        expected = '45 manhattan ave'
        self.address.full_address = '45 manhattan ave'
        self.assertEqual(expected, self.address.full_address)

    def test_full_address_blank(self):

        expected = 'MISSING ADDRESS'
        self.assertEqual(expected, self.address.full_address)


    def tearDown(self):
        del self.address

class TestUser(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

class TestBuyer(unittest.TestCase):

    def setUp(self):
        pass


    def tearDown(self):
        pass


class TestSeller(unittest.TestCase):
    def setUp(self):
        pass


    def tearDown(self):
        pass



if __name__ == "__main__":
    unittest.main()
