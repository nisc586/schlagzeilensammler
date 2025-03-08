# ReadMe to my *AWESOME* Schlagzeilensammler Application
Run the app in debug mode with this command:
```
flask run --debug
```

# Todo-List:
- Change list elements to "media-elements" with a nicer appearance than just the title-&-link on index.html
    -[x] Implement in html
    -[x] Add CSS
- Create some shell-commands for creating the database
- Add a feature to choose and load different rss-feeds
    - Add a new database model
    - Add a reference to the `Article` model
    - research some end-points
    - use `https://icons.duckduckgo.com/ip3/{domain}.ico` to load icons
- Figure out database migration