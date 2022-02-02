# Run in dev environment
`FLASK_APP=app.py FLASK_ENV=development flask run --port 4000`

# test endpoint
`curl -F "file=@static/animage.jpg" http://localhost:4000/stream_predict`

`curl --data "file_url=https://www.monumentmonitor.co.uk/static/media/machrie.602f34b9.jpg" -X POST http://localhost:4000/stream_url_predict`

# test production endpoint
`curl -F "file=@machrie-1.jpg" https://mmdetector.herokuapp.com/stream_predict`

# test production endpoint
`curl --data "file_url=https://www.monumentmonitor.co.uk/static/media/machrie.602f34b9.jpg" -X POST  https://mmdetector.herokuapp.com/stream_url_predict`