import grafeo
from timeit import default_timer as timer


db = grafeo.RemoteDB(url='https://grafeo-server.herokuapp.com')

num_samples = 10

_p = grafeo.Producer(name="Test Producer Timing")
db.post(_p)
print(_p.is_valid())

start = timer()
for i in range(num_samples):
    print(i)
    _pp = db.get_producer(pub_key=_p.pub_key)
end = timer()
print("Producers (GET): {} per second".format(num_samples / (end-start)))


start = timer()
for i in range(num_samples):
    db.post_producer(
        name="Test Producer Timing"
    )
end = timer()
print("Producers (Create+Encrytp+Post): {} per second".format(num_samples / (end-start)))


# Compley Product
inputs = [grafeo.new_product(name="Test Product {}".format(j), producer=_p, inputs=[]) for j in range(100)]
num_samples = 10

start = timer()
for i in range(num_samples):
    db.post_product(
        name="Test Product Complex Timing",
        producer=_p,
        inputs=inputs
    )
end = timer()
print("Complex Product (Create+Encrytp+Post): {} per second".format(num_samples / (end-start)))

start = timer()
for i in range(num_samples):
    _product = grafeo.new_product(
        name="Test Product Complex Timing",
        producer=_p,
        inputs=inputs
    )
    _a = _product.__dict__
end = timer()
print("Complex Product (Create+Encrytp): {} per second".format(num_samples / (end-start)))
