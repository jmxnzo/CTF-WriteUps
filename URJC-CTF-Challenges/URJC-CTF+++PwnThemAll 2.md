![[Pasted image 20231231152640.png]]

# Reversing using ghydra
- after reversing the provided binary, we can see the source code of our functions pwnThemAll, which in this case implements a similar check to PwnThemAll1
- but if we run the binary with the same input, we see that printflag() doesn't provide us the real flag 
- furthermore we can find the function give_shell in the decompiled source code, which can be used by our buffer overflow to spawn a shell

![[Pasted image 20240104170522.png]]
![[Pasted image 20240104170501.png]]
# Analysis of our binary with gdb
1. We set a breakpoint to the pwnThemAll function to see which base pointer and which return address is set in the function pwnThemAll(), to later on manipulate those two to jump to the give_shell function , which is aso part of the binary
![[Screenshot from 2023-12-31 15-42-45.png]]
- to see the stack layout, we use following prompt to let gdb print all 64 bytes from the stack pointer address on and we can find our basepointer and return adress laying on the stack at the position 0x7fffffffdc40
![[Screenshot from 2023-12-31 15-42-57.png]]

3. Now we do the same after the creation of the first buffer:
![[Screenshot from 2023-12-31 15-46-27.png]]
- and again after the creation of the second buffer:
![[Screenshot from 2023-12-31 15-52-10.png]]
4. This step finally show us how the stack layout of the functions does look like and provides us all the required information on how to design the buffer overflow
![[Screenshot from 2023-12-31 15-52-31.png]]
#### Graphic of our stack layout of the function pwnThemAll()
![[Screenshot from 2023-12-31 15-54-38.png]]



# Manipulating the return address
#### Finding the address of function give_shell
- For this we use objdump, which prints us all the addresses of our functions and we see that the function of give_shell is laying at 0x40127c.
![[Pasted image 20240104172732.png]]
- keeping this in mind, we can construct how the new stack should look like after the bufferoverflow
![[Pasted image 20240104173043.png]]


# Writing payload
- because we can't insert null bytes into our binary, we need to accept, that the old base pointer can't be repaired after our buffer overflow attack. Even though the shell will be still spawned and we can obtain the flag. 
- To do so we create the following attack payload user python buffer write function.
```python
python3 -c'__import__("sys").stdout.buffer.write(b"\x41"*64+ b"\xff\xf\x7f\xff\xff\xff\xdc\x50"[::-1] + b"\x40\x12\x7c"[::-1])```
```
- Injecting this attack_payload into gdb with run < attack_payload, we see that we finally get into the give_shell function. So our payload is ready to pwn the real binary laying on the server.
![[Screenshot from 2023-12-31 16-35-26.png]]






# Writing the final python code using pwn library
- In the last step we write a python code, connect to the tcp port 9992 on the host and wait for the input prompt "Enter your message prediction". After receiving the prompt we send our generated payload, which performs the buffer overflow and injects the function give_shell to our return address. 
![[Screenshot from 2024-01-01 18-06-57.png]]
- Finally we end up having a system shell and we can obtain the challenge flag.
![[Screenshot from 2024-01-01 18-21-10.png]]
