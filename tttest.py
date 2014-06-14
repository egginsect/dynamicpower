from terminal_th import *
devices = list()
for i in xrange(20):
    devices.append(Device('d'+str(i), 'D', None, None))
for dev in devices:
    dev.start()
for dev in devices:
    dev.join()
