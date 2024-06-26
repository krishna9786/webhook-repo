# webhook-repo

- action-repo: Set up a GitHub repository to trigger webhooks on actions.
- webhook-repo: Set up a Flask app to handle webhooks, store data in MongoDB, and display it via a simple UI.

#Approach 
1. installed the Python and pip(package manager)
2. used vscode ide for the development part
3. first created two folder one for front-end(HTML and Javascript) and backend (flask, mongoDB)
4. In backend(app.py) - written the logic(imported the library and created functions)
5. created a repo on GitHub then repo->setting->webhooks-> set the payload URL(got from ngrok named as forwarding with GitHub endpoint), changed the format to JSON and selected what I needed(push, pull, merge).
6. created a pull req to check if it is working or not
