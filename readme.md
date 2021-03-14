# Run in dev environment
`FLASK_APP=app.py FLASK_ENV=development flask run`

# test endpoint
`curl -F "file=@machrie-1.jpg" http://localhost:5000/stream_predict`

# test production endpoint
`curl -F "file=@machrie-1.jpg" http://localhost:5000/stream_predict`