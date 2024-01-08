## Reversing using ghidra
- If we reverse the executable, we can find a method called pwnThemAll, which has 3 buffers and different methods. The methods generaterandommsg() really generates a random msg, which looks hard to predict. But nonetheless we have the puts() method, which writes to our buffer without any boundaries, so it can be used to perform a buffer overflow attack. 
![[Pasted image 20240108204941.png]]

### Determining buffers in dynamic analisis using gdb
![[Screenshot from 2023-12-30 16-30-28.png]]
-> This screenshot show, that check_if_match uses the adresses dc70 and dcb0 as input, which are respectively the buf_sanized_message and the buf_to_generate_message.
![[Screenshot from 2023-12-30 16-59-13.png]]

So in conclusion the analysed code of ghidra is not 100% right and the order of the buffers is different to the provided code. Dynamically analyzing the code gives us following order of the buffers:
```C
buf_to_generate_message [32] <-- highest adress b0
buf_first_write [32]  -- 90
buf_sanitized_message [32] <-- lowest memory address --70
```


### Conclusion for length of input
This order of the buffer let's us know that we need to take a second look at the sanitize_msg function. For this i facilitate the code a little bit, to provide a better overview on what is performed in the function:
```C
void sanitize_msg(char *param_1, char *param_2) {
size_t sVar1;
int local_10;
int local_c;
sVar1 = strlen(param_1);
local_c = 0;
for (local_10 = 0; local_10 < (int)sVar1; local_10 = local_10 + 1) {
	if (param_1[local_10] != '%') {
		param_2[local_c] = param_1[local_10];
		local_c = local_c + 1;
		}
}
param_2[local_c] = '\0';  
// Corrected syntax errors: added semicolon and removed unnecessary newline
puts("You have introduced the message: ");
puts(param_2);

}
```
- The sanitize_msg code gives us more information about how long our buffer overflow needs to be. Because the bytes are copied after each other until the size of the buf_first_write is reached, we will end up writing a zero byte into the beginning of our buf_to_generate_message, bcs the bufferoverflow starting from this buffer using the puts() method would need to be 64 byte. Thus we need to overflow all 3 buffers using the sanitize_msg method, this implies that the overflowing input needs to be at least 96 Characters long, to keep all contents of the buffers equal.
![[Screenshot from 2023-12-30 16-25-17.png]]

