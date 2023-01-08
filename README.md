# WordPlay
#### Video Demo:  https://www.youtube.com/watch?v=KLwkMy3A-lQ
#### Description:
### About:
**WordPlay** is a web application to help people learn new vocabulary words, improve their vocabulary, and test their knowledge. I mainly got my inspiration from the earlier **Finance** project I did, and based my foundation on it.
### Tools:
I used the **Flask** framework for this, which includes:
 - Pythonn
 - HTML
 - CSS
I wanted to use a little bit of Javascript on it, but decided not to later. Oh wait, I forgot one language that works behind the scenes. **SQL**! I used a *lot* of Sqlite for this project.
### API:
I used a [dictionary API](dictionaryapi.dev) for my project. I tried to use Oxford and Webster API initially, but I faced some API key related issues. Hence, I decided to move forward with *dictionaryapi.dev*, which does not need any API key and it is absolutely free.
## Paths:
The key features offered in my application are:
 - Sign Up
 - Log In
 - Logout
 - Home
 - Add
 - Delete
 - Learn
 - Test
Let me go through the features in detail.
### Register/Login:
So first, there is the Register, Login, and Logout paths. I Used almost the same code as my Finance project for this. Then first, I decided to do the Add and Create page before the homepage, because the homepage would take some time. After a while, I realized it would be confusing.
We start by signing up using our username and password. Once we sign up, we can log in to the application.
We need to create a study set at first and then add new words to it. There are 2 ways to add words - one is to add using API and the other way is to use our own words.
### Other paths:
Another path in the application is the delete path. There are two options, delete a set and delete a word. At first I considered adding the Add & Delete function on the Homepage, but I decided it was *way* too crowded. Lastly, there is the Learn path, which uses a lot of CSS to style the flashcards, and the test function.
## SQL:
Like I said before, there is a *lot* of SQL in this project. At first I wanted to make a separate SQL table for each and every set created, but that would waste *way* too much memory, so I settled with making one big table. The columns are:
 - id
 - setName
 - word
 - definition
So instead of multiple tables which use up memory and can overlap, this option is better. This is the table structure I used:
```
CREATE TABLE sets ( setName TEXT NOT NULL, word TEXT NOT NULL, definition TEXT NOT NULL, id);
```
## What I learned:
Lastly, here are some things I learned while doing this project and CS50 in general, both related and unrelated to programming:

1. One of the classics, never give up. For some projects I spent days and days looking for a solution, and sometimes I just wanted to quit. But not quitting and persevering was worth it when I realized how much that would help me for future projects.
2. Think out of the box. For some problem sets, I just couldn't find a solution that fit right in place. So instead of always taking the straight path or the shortcut ahead, I try to get creative, which does the trick.
3. Although you might not have been expecting this, it is my favorite one. It's to ask for help. If you're like me, you might be wondering, *But I want to finish by myself!* but this can help a lot. Often in the real world, programmers and computer scientists are rarely ever alone, and asking for help is essential. There are plenty of communities on CS50, like Discord, Stack Overflow, and Reddit, just waiting for you to use!

## THIS WAS CS50!
"# WordPlay" 
