#### Code analysis
- Looking at the source code of our Web.java file, it is really obvious that we have to deal with the possibility of an Path/directory traversal. As well given is the static path, so in our words the starting point of our traversal.
![[Pasted image 20240103004542.png]]

1. 1. Keeping this in mind, it is straightforward to load the /etc/passwd file by using ../../../../../../../etc/passwd as the input for filename, but after using nmap there is no option to connect to the server knowing these details.

![[Screenshot from 2024-01-02 16-51-29.png]]
2. Taking a look at the provided dockerfile, we spot that the CHALLENGE_FLAG is set environmental variable. Even though we need to keep in mind that our process is running in a docker container.
 ![[Pasted image 20240103004954.png]]
3. If we would have to deal with a normal web server instance, this traversal should leak the environmental variable.
 https://083b22721f04-webth-vulnerable.numa.host/file?filename=../../../../../../../../etc/environmentBut because we have to deal with docker and docker doesn't store the environmental variable anywhere inside the container, we need to find another way. 
![[Screenshot from 2024-01-02 16-46-22.png]]


#### Trying directory traversal with common.txt 
https://github.com/v0re/dirb/blob/master/wordlists/common.txt
- Most of the time the flag is following a strict naming convention, so in this moment it seemed to be a good idea to just bruteforce different directory entries and try to find a flag.txt somewhere. For that i used the common.txt with a lot of know directory entries. Nonetheless it ended without success.
![[Screenshot from 2024-01-02 23-40-12.png]]



#### Coming back to env variable
- even without having the opportunity to see the flag in /etc/environmental, there is another option the Linux's /proc folder, which includes a lot of magic. With the folder we are able to query the running operating system. Because /proc/sched_debug doesn't provide us the PID of our running process to send the final query, we need to make use of the self keyword, which Linux offersin this case. Forming the link and sending the request to include the local file, stored on the server. We finally obtain the flag!

https://083b22721f04-webth-vulnerable.numa.host/file?filename=../../../../../../../../proc/self/environ


![[Screenshot from 2024-01-03 00-39-41.png]]


Really helpful resource:
https://thesecurityvault.com/path-traversal-lfi-can-be-worst-than-you-think/


