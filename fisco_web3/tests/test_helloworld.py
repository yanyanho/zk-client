from contracts.HelloWorld import HelloWorld
import sys

print(sys.path)
si = HelloWorld("")
result = si.deploy("contracts/HelloWorld.bin")
address = result['contractAddress']
print("new address = ", address)

#address = "0x7b6cb85c667c6ec8a4d81be837270ddfcf1838d5"
helloworld = HelloWorld(address)
(outputresult, receipt) = helloworld.set("testeraaa")
# outputresult  = si.data_parser.parse_receipt_output("set", receipt['output'])
print("receipt output :", outputresult)
logresult = helloworld.data_parser.parse_event_logs(receipt["logs"])
i = 0
for log in logresult:
    if 'eventname' in log:
        i = i + 1
        print("{}): log name: {} , data: {}".format(i, log['eventname'], log['eventdata']))
print(helloworld.get())
