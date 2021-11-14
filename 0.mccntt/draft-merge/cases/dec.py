import base64

data = open("raw.txt", "r").read()
decoded = base64.urlsafe_b64decode(data)
print (str(decoded, 'utf-8'))