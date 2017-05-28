import pickle

a = pickle.load(open("./test.dic", "rb"))
b = pickle.load(open("./test2.dic", "rb"))

a.update(b)

pickle.dump(a, open("tester.dic", "wb"))
