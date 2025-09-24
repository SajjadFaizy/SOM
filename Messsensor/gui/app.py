import sys
from os import path
from bottle import Bottle, run, static_file, json_dumps
from threading import Thread

# Directories' path
web_server_dir = path.dirname(path.abspath(__file__))
proj_dir = path.abspath(path.join(web_server_dir, '..'))
frontend_dir = path.join(web_server_dir, 'frontend')

sys.path.append(proj_dir)

# Init Web Server
app = Bottle()

# Get data from subscriber
from subscribers.subscriber import temperature_data, start_subscriber

# Main Page
@app.route('/')
def index():
    return static_file('index.html', root=web_server_dir)


# Asign route to temperature_data -> make it accessible from Browser
# (Kind of "bridge" to the subscriber script)
@app.route('/data')
def get_data():
    if temperature_data:
        print(temperature_data) # Proofs data is being sent
        # Convert python list (temp_data) to JSON, so JavaScript can read it
        return json_dumps(temperature_data)
    else:
        return json_dumps([])


# Deliver browser style and js documents
@app.route('/frontend/<filename>')
# ^^^^^^^^^^^ Here ^^^^^^^^^^^^^^, filename dynamically captures
# any value requested from the browser after /frontend/ in the URL.
def serve_static(filename):
    return static_file(filename, root=frontend_dir)


# Init local web server
if __name__ == "__main__":

    # Start MQTT subscriber in separate thread
    subscriber_thread = Thread(target=start_subscriber, daemon=True)
    subscriber_thread.start()

    # Start the web server
    run(app, host='localhost', port=5000)   # Std port: 8080 | Uni port: 5000