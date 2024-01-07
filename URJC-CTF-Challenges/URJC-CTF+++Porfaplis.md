1. Looking at the source code of our application, we can see that if we send a POST request to the /givemeflag path, there are three different branches to take. 
	1. The first one is if the user is not set to admin, so in the first step we definetly need to provide the admin flag. 
	2. The second branch checks if the provided magicword is given to the btoa() javascript function is unequal a specific base64 encoding. So we need to find the corresponding input, to be equal to this base64 encoding and landing in branch 3.
	3.  The third branch just prints the flag, so we need to get here.
![[Pasted image 20240104174415.png]]
### btoa function
The `btoa` function in JavaScript is used to encode binary data, such as strings, into base64-encoded ASCII strings. It is commonly used to represent binary content in a format suitable for transmission over text-based protocols or for embedding binary data in web pages. But nonetheless the process is reversible using the `atob` function in JavaScript, which decodes a base64-encoded ASCII string back into its original binary data.

# Exploitation

1. The first request we send shows us, let's us end up in the second branch, because the magicword is not set right for now.
![[Screenshot from 2023-12-18 18-51-16.png]]

2. Knowing that the btoa function is easily reversible, we can just right our own javascript to reverse it using atob. Doing this obtains us the required value for the magicword paramter: pretty please :3
![[Screenshot from 2023-12-18 18-55-46.png]]
3. In the last step of our exploit, we just set the magicword to pretty please :3 and send the post request to the server again. Finally the server replies with the flag:

![[Screenshot from 2023-12-18 18-56-12.png]]


```dataview
LIST WITHOUT ID
flat(list(
    list(
        join(list("mkdir -p \"", "\$targetdir/$(dirname '", string(file.path) , "')\""), ""),
        join(list("cp '", string(file.path), "' \"", "$targetdir/", string(file.path), "\""), "")
    ),
    map(file.outlinks, (x) =>
        join(list("mkdir -p \"", "\$targetdir/$(dirname '", meta(x).path , "')\""), "")
    ),
    map(file.outlinks, (x) =>
        join(list("cp '", meta(x).path, "' \"$targetdir/", meta(x).path, "\""), "")
    )
))
WHERE file.path = this.file.path
```