from thterminal import *
tts=list()
b = [[0,0,0,1],[0,0,0,1],[0,0,0,1],[1,1,1,0]]
a = ['B','CL','DL','N']
tts.append(Battery(a[0], b[0], tts))
tts.append(CurtailibleLoad(a[1], b[1], tts))
tts.append(DefferableLoad(a[2], b[2], tts))
tts.append(Net(a[3], b[3], tts))
for t in tts:
    if(t.terminal_type is 'Device'):
        t.start()
for t in tts:
    if(t.terminal_type is 'Device'):
        t.join()
