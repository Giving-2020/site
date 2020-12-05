from json import loads

credentials = loads(open("Giving2020/credentials.json","r").read())

print(credentials)