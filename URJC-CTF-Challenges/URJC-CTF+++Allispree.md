1. Looking at the source code of our Web.java file, it is really obvious that we have to deal with the possibility of an Path/directory traversal. As well given is the static path, so in our words the starting point of our traversal. To reveal the file on the WebPage the Files.readAllBytes() function in java is used to load the data from the directory and show it on the website.
![[Screenshot from 2023-12-30 19-57-56.png]]![[Screenshot from 2023-12-30 19-58-14.png]]
2. Now we can check the current working directory, injecting `localhost & pwd`
![[Screenshot from 2023-12-30 20-00-12.png]]

3. Continuing the exploit we use `localhost & ls` to get show the contents of our current directory and we directly find the flag.txt
![[Screenshot from 2023-12-30 20-00-51.png]]
4. Last step is to use `localhost & cat flag.txt` to succesfully obtain the flag
![[Screenshot from 2023-12-30 20-01-25.png]]

