# SOLID ; single responsibility, open close principle, Liskov substitution,
# Inheritance vs composition

from abc import ABC, abstractmethod


class Item(object):

    def __init__(self, id, name, description):

        self.id = id
        self.name = name
        self.description = description
        self._review_list = []

    def __repr__(self):

        return """id : {id}, name : {name} , description : {desc}""".format(id=self.id, name=self.name, desc=self.description)

    @property
    def review(self):
        return self._review_list #  #add_review(user,review)   delete_review(user)

    @review.setter
    def review(self, text):
        print("TEXT : ", text)
        self._review_list.append(text)


class Store:
    def __init__(self):
        self.__items_to_sell = list() # add(item), remove(item)

    def checkout(self, cart):
        pass

    def search(self, item):
        pass


class Address:

    def __init__(self):
        self.__full_address = "MISSING ADDRESS"

    @property
    def full_address(self):
        return self.__full_address

    @full_address.setter
    def full_address(self, addr):
            self.__full_address = addr


class Cart:
    def __init__(self):

        self._list_of_cart_items = []

    def add_item(self, item):
        self._list_of_cart_items.append(item)

    def remove_item(self, item):
        self._list_of_cart_items.remove(item)


class User(ABC):
    def __init__(self, name , id):
        self._name = name
        self._id = id
        self._bank = []
        self._cart = Cart()

    @property
    def bank(self):
        return self._bank

    @bank.setter
    def bank(self, account_info):
        self._bank.append(account_info)

    def __repr__(self):
        return """name : {name}, id : {id}, bank : {bank}""".format(name=self._name, id=self._id, bank= self._bank)

    def debit_bank(self):
        return " Money added to Bank"

    def credit_bank(self):
        return " Money taken from Bank"

    def add_items_to_cart(self,item):
        self._cart.add_item(item=item)

    def remove_item_from_cart(self,item):
        self._cart.remove_item(item)


class Buyer(User):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Seller(User):

    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        self._seller_items = []

    def add_seller_items(self,item):
        self._seller_items.append(item)

    def remove_seller_items(self,item):
        self._seller_items.remove(item)




