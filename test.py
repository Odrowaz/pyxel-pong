import struct

name = 'davide'
data = struct.pack(f'>B{len(name)}s', 1, name.encode())

print(len(data))

print(data)

type, = struct.unpack('>B', data[:1])

if type == 1:
    typeu, name = struct.unpack(f'>B{len(data) - 1}s', data)
    print(typeu, name.decode())




a = {}

a['a'] = []

a['a'].insert(1, 5)

a['a'][0] = 5

print(a)
