import re
from collections import Counter


file = open('access_log')
data = re.findall('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', file.read())
file.close()
for index in Counter(data).most_common(10):
    print("IP Address - %s, Count - %d" % (index[0], index[1]))
