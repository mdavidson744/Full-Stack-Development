url = input("Please enter a valid url: ")
# url.split("http://")
# print(url)
# # print("Host is: " + host)
host = url.split("?")
hostT = host[0].split("/")
print("Host is: " + hostT[2])

#find values
#find p1 & value
url.join(url)
test = url.split("?")
test1 = test[1].split("&")
object1 = test1[0].split("=")

#find p2 & value
object2 = test1[1].split("=")

#find p3 & value
object3 = test1[2].split("=")







print("Name is " + object1[0] + ", value is " + object1[1])
print("Name is " + object2[0] + ", value is " + object2[1])
print("Name is " + object3[0] + ", value is " + object3[1])
