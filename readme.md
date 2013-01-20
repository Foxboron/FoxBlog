FoxBlog
=======

Project involving creating a basic microblog using git with Flask.   

Postys are contained inside `posts` and will be dynamically displayed on the front page. `sites` will be the files for the different sub-sites you create.   
Everything uses Markdown! 
  
  
I also added `prettify.js` with a little word change to we can use the Markdown lib Codehilite's code syntax.
  
    
Copy and save as `config.conf`.

```json
{
   "Github": github_username,
   "Repo": github_repo,
   "mail": gravatar_mail,
   "client_id": github_client_id,
   "client_secret": github_client_secret
}
```  
  
Requirements:
* Flask  
* Markdown for Python