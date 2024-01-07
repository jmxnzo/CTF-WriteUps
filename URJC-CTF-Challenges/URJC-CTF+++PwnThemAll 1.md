```C
buf_to_generate_message [32] <-- highest adress b0
buf_first_write [32]  -- 90
buf_sanitized_message [32] <-- lowest memory address --70
```
### Without overflow
![[Screenshot from 2023-12-30 16-43-20.png]]
### Overflowing the first buffer and checking behaviour
![[Screenshot from 2023-12-30 16-30-28.png]]
-> This screenshot show, that check_if_match uses the adresses dc70 and dcb0 as input, which are respectively the buf_sanized_message and the buf_to_generate_message.


### Conclusion for length of input
![[Screenshot from 2023-12-30 16-59-13.png]]
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

- Bcs the buffer for sanitizing the message overflows has the lowest memory address, the method above will also overflow our buf_first_write, where the buffer overflow is performed again. Thus we need to overflow all 3 buffers with the sanitizing method, this implies that the overflowing input needs to be 96 Characters long, to keep all contents of the buffers equal.

![[Screenshot from 2023-12-30 16-25-17.png]]

