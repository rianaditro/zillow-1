import pandas

d = [{"key1":1,"key2":2,"key3":3,"key4":4},
	 {"key1":11,"key2":0,"key3":0,"key4":44},
	 {"key1":111,"key2":222,"key3":0,"key4":444},
	 {"key1":111,"key2":2222,"key3":3333,"key4":4444}]

df = pandas.DataFrame(d)

print(df["key3"].tolist())