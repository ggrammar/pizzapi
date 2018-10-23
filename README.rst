pizzapi
=======

Description
-----------

This is a Python wrapper for the Dominos Pizza API.

It's a port of `the pizzapi node.js module <https://github.com/RIAEvangelist/node-dominos-pizza-api>`_ written by `RIAEvangelist <https://github.com/RIAEvangelist>`_.

Quick Start
-----------

Pull the module into your namespace:

.. code-block:: python

    from pizzapi import *

First, construct a ``Customer`` object and set the customer's address:

.. code-block:: python

    customer = Customer('Donald', 'Trump', 'donald@whitehouse.gov', '2024561111')
    address = Address('700 Pennsylvania Avenue NW', 'Washington', 'DC', '20408')

Then, find a store that will deliver to the address.

.. code-block:: python

    store = address.closest_store()

In order to add items to your order, you'll need the items' product codes.
To find the codes, get the menu from the store, then search for items you want to add.
You can do this by asking your ``Store`` object for its ``Menu``.

.. code-block:: python

    menu = store.get_menu()

Then search ``menu`` with ``menu.search``. For example, running this command:

.. code-block:: python

    menu.search(Name='Coke')

Should print this to the console:

.. code-block:: text

    20BCOKE    20oz Bottle Coke®        $1.89
    20BDCOKE   20oz Bottle Diet Coke®   $1.89
    D20BZRO    20oz Bottle Coke Zero™   $1.89
    2LDCOKE    2-Liter Diet Coke®       $2.99
    2LCOKE     2-Liter Coke®            $2.99

After you've found your items' product codes, you can create an ``Order`` object add add your items:

.. code-block:: python

    order = Order(store, customer, address)
    order.add_item('P12IPAZA') # add a 12-inch pan pizza
    order.add_item('MARINARA') # with an extra marinara cup
    order.add_item('20BCOKE')  # and a 20oz bottle of coke

You can remove items as well!

.. code-block:: python

    order.remove_item('20BCOKE')

Wrap your credit card information in a ``PaymentObject``:

.. code-block:: python

    card = PaymentObject('4100123422343234', '0115', '777', '90210')

And that's it! Now you can place your order.

.. code-block:: python

    order.place(card)

Or if you're just testing and don't want to actually order something, use ``.pay_with``.

.. code-block:: python

    order.pay_with(card)
