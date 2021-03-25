Assumptions of the store


1. user can buy items
2. user can sell items
3. user can add items to cart , user can remove items from cart
4. user can checkout


1. buyer
2. seller
3. item
4. buy()
5. sell()
6. checkout()
7. cart
8. store


class item:
    id
    name
    description
    review_list = list() #add_review(user,review)   delete_review(user)

class store:
    items_to_sell = list() # add(item), remove(item)
    checkout(cart)
    search (item)

class Address
    full_address

class user:
    name
    id
    bank
    @abstract
    debit_bank()
    @abstract
    credit_bank()
    Address

class cart :
    list_of_cart_items
    insert(item)
    remove(item)

class buyer(user):
    items_in_cart = cart()

class seller(user):
    list_of_items_to_sell  = list() # add_items(item) remove_items(item)
    items_in_cart = cart()



