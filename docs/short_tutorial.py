import grafeo2 as grafeo

# Establish connection to remote database which is a django dev. server in this case
db = grafeo.RemoteDB(url='http://localhost:8000')

# Get Information about a specific producer identified by the public key
producer_get = db.get_producer(
    pub_key='73b3e6a97035611f9d45ed2f3d061e51547e4d93df8cc09e7d45b61301bbe3c9'
)

# Check if the producer is valid
print(producer_get.is_valid())


# Get Information about a product identified by the public key
product_get = db.get_product(
    pub_key='c5ea7cd8744326961c7ebd1ca07456dc8d9e331329fea1aba0964c770f9929bf'
)

# Check vailidity
print(product_get.is_valid())


# Create a new producer (keys and version are choosen automatically)
producer = grafeo.Producer(
    name='Test Producer Tutorial'
)

# Sign the producer with its own private key
producer.sign()

# Check Validity
print(producer.is_valid())

# Post to database
db.post(producer)


# Create a product which is made by the producer from the tutorial and has no inputs
product_base = grafeo.Product(
    name='Base Product',
    producer_pub_key=producer.pub_key
)

# Sign
product_base.sign(
    producer_priv_key=producer.priv_key,
    input_priv_keys=[]
)

# Check
print(product_base.is_valid())

# Post to database
db.post(product_base)


