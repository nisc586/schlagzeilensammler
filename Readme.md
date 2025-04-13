# ReadMe to my *AWESOME* Schlagzeilensammler Application
Run the app in debug mode with this command:
```
flask run --debug
```

# Todo-List:

- Add a feature to choose and load different rss-feeds
    - ~~Add a new database model~~
    - ~~Add a reference to the `Article` model~~
    - ~~use `https://icons.duckduckgo.com/ip3/{domain}.ico` to load icons~~
    - ~~add pagination to index, article-list~~
    - ~~add buttons for different channels~~
    - add more channels
    - update css for channel-buttons
- Alter date format for `media-date`
- Add a page where you can add your own feeds
    - ~~end point for post requests~~
    - ~~add form in front-end to get an url~~
    - add navbar to index
    - move add-new-channel-form to channels template
- Add testing
    - test config
    - test database
    - test model to_dict methods
    - test route adding channels
    - test route adding articles
