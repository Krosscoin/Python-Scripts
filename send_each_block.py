import pywaves as pw
import time

pw.setNode('https://nodes.krossexplorer.com','KrossChain','N')
block = pw.lastblock()
addr = pw.Address(seed='seeeee eeeeeeeeeee eeeeeeeeeeeeeeeeeee dddddddddddddddddd')
while True:
    try:
        while block['height'] == pw.lastblock()['height']:
            time.sleep(2)

        block = pw.lastblock()
        print(str(block['generator']))
        print(str(block['height']))
        print(str(addr.sendWaves(pw.Address(address=block['generator']),500000,attachment='Thanks for running a node')))
    except:
        time.sleep(2)
        print("except")
