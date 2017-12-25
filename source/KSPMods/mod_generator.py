import os

for i in range(5):
    os.makedirs(os.path.join(os.getcwd(),'mod'+str(i)+r'\modz'))
    with open(r'.\mod'+str(i)+r'\mod.txt','w') as f:
        f.write('mods...')

