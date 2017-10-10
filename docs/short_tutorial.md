# Quick Tutorial

This tutorial will show you the basics of using the grafeo utils.
We first create a bunch of producers and products and post them to a remote database.

## Creation
```python
import grafeo


# Connect to a remote database, i.e. a database which uses the specific http based protocol
# Here we use a locally running django dev server
db = grafeo.RemoteDB(url='http://localhost:8000')

# Generate producers
# Those contain the private keys and are already signed
basf = grafeo.Producer(name="BASF")
grain_farmer = grafeo.Producer(name="Grain Farmer")
feed_producer = grafeo.Producer(name="Chicken Feed Producer")
chicken_farmer = grafeo.Producer(name="Chicken Farmer")
noodle_producer = grafeo.Producer(name="Noodle Producer")

# Post all to database
# If True is returned, the post request was successful
assert db.post(basf)
assert db.post(grain_farmer)
assert db.post(feed_producer)
assert db.post(chicken_farmer)
assert db.post(noodle_producer)


# Generate Products

# Produced by BASF
vitamins = grafeo.Product(
    name="Vitamins",
    producer_pub_key=basf.pub_key
)
# The producer has to also sign the product
# No inputs were used
vitamins.sign(
    producer_priv_key=basf.priv_key,
    input_priv_keys=[]
)

# Product by the grain farmer
grain = grafeo.Product(
    name="Grain",
    producer_pub_key=grain_farmer.pub_key
)
grain.sign(
    producer_priv_key=grain_farmer.priv_key,
    input_priv_keys=[]
)

# Product by the feed producer. Uses vitamins and grains
# Here we use inputs
chicken_feed = grafeo.Product(
    name="Chicken Feed",
    producer_pub_key=feed_producer.pub_key,
    input_pub_keys=[
        vitamins.pub_key,
        grain.pub_key
    ]
)
# Producer, and inputs have to sign
chicken_feed.sign(
    producer_priv_key=feed_producer.priv_key,
    input_priv_keys=[
        vitamins.priv_key,
        grain.priv_key
    ]
)

# Can be done with helper (signing is included)
eggs = grafeo.new_product(
    name="Eggs",
    producer=chicken_farmer,
    inputs=[chicken_feed]
)


# Post all to database
assert db.post(vitamins)
assert db.post(grain)
assert db.post(chicken_feed)
assert db.post(eggs)


# The following is even shorter
assert db.post_product(
    name="Egg Noodles",
    producer=noodle_producer,
    inputs=[eggs]
)
```


## Requesting the information for a Producer & Product
All information about a producer defined by the public key can be accessed as follows:
```python
_producer = db.get_producer(pub_key=basf.pub_key)
_product = db.get_product(pub_key=vitamins.pub_key)

assert _producer.is_valid()
assert _product.is_valid()
```

## Saving Producers & Products locally
The `LocalDB` class allows saving producers & products locally. This includes their <span style="color:red">**private keys**</span> and thus the resulting file must be kept <span style="color:red">**secret**</span>!
Also the implementation is currently <span style="color:red">**not at all**</span> thread safe. Use the database from one, and only one, program at a time!
```python
# Local Database (describe folder to store data in. This must be a secure location!)
ldb = grafeo.LocalDB(folderpath="/Users/lukas")

assert ldb.post(basf)
assert ldb.post(grain_farmer)
assert ldb.post(feed_producer)
assert ldb.post(chicken_farmer)
assert ldb.post(noodle_producer)

assert ldb.post(vitamins)
assert ldb.post(grain)
assert ldb.post(chicken_feed)
assert ldb.post(eggs)
assert ldb.post(eggs)
```

## Retrieving Producers & Products locally
```python
# The database copys the items when they are stored/loaded
_basf_copy = ldb.get_producer(pub_key=basf.pub_key)
_grain_copy = ldb.get_product(pub_key=grain.pub_key)

assert _basf_copy.is_valid()
assert _grain_copy.is_valid()

assert basf.__dict__ == _basf_copy.__dict__
assert grain.__dict__  == _grain_copy.__dict__
```
