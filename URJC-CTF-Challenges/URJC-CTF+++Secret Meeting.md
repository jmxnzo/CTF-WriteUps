![[Pasted image 20240103185326.png]]
- Regarding the source code, we see that we have to deal with a NoSql Injection in a MongoDB
- Depending on if an injected input is valid or not, we get a 401 or 200 status code send back, which allows us to keep track of our exploit

In first place we use the web developer tool to intercept a POST request to our host, to see possible required headers and parameters.
### Make use of $regex in NoSql
The $regex option allows us to make guesses about our passwort, the username "admin" is already given in the provided source code.
![[Pasted image 20240103191128.png]]


### Step 1: Guess password length
- Using this as our input ```password[$regex]=.{x}``` and iterating over x until a 401 is returned, let's us determine the password length of admin password
- the corresponding code can be seen in the first half of exploit.py

- In the first place i used a slightly wrong approach, as you see in the first provided. Trying to guess each character by itself ```password[$regex]=<character_guess>.{x}``` and decreasing x after every successful guess. This approach would work if the flag doesn't contain one character varies times, which isn't the case for our flag. But still sharing it, can avoid some pitfalls for following CTFs.
![[Pasted image 20240103192014.png]]
#### Burpsuite to get the idea of final exploit
- The appended Burpsuite screenshots, show the different response behaviour if a string does match or if it doesn't. Understanding this response directly takes us to the final code of our exploit.

![[Pasted image 20240103193632.png]]

![[Pasted image 20240103193751.png]]

### Step 2: Guess password contents
- We need to provide the full flag, that we discovered so for and char by char bruteforce the following character ```password[$regex]=URJC{x.*``` at the position of x we bruteforce for the next character. This checks if there's any matching regex to our flag in the password, we are trying to exploit, if this is the case, we discovered the next character of our flag.
- Corresponding source code:
![[Pasted image 20240103194225.png]]

![[Pasted image 20240103194007.png]]


Reference: https://x3tb3t.github.io/2017/05/15/NodeJS-and-MongoDB-NoSQL-Injection/
