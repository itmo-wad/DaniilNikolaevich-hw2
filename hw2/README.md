# Assignment №2

## Launch postgresql
```
cd postgresql
docker-compose up -d
```

## Create tables in database
```
python3 database_setup.py
```

## Launch Flask
```
python3 main.py
```

##What have been done?
- ✅ Listen on localhost:5000
- ✅ Render authentication form at http://localhost:5000/
- ✅ Redirect user to profile page if successfully authenticated
- ✅ Show profile page for authenticated user only at http://localhost:5000/profile
- ✅ Username and password are stored in postgresql
- ✅ Implement feature that allows users to create new account, profile will be shown with data respected to each account.
- ✅ Implement password hashing and logout
- ✅ Allow users to set profile picture (new user will have a default profile picture)
