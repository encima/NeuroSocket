from couchbase.bucket import Bucket 

c = Bucket('couchbase://localhost/default')
print(c)

obj = {"name":"test"}

c.upsert("1abc", obj)

res = c.get("1abc")

print(res.value)
