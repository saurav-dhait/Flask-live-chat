# Flask live chat (LAN)  


Hello Everyone,


This is my first proper project over a github repository.
A simple Flask-based chat application designed for local area network (LAN) communication.

## Features

- **Real-time Communication:** Instant messaging within your local network.
- **User-friendly Interface:** Simple design for a seamless user experience.
- **Lightweight and Fast:** Built with Flask to ensure efficiency and speed.


## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Installation

### Prerequisites

- Python 3.x
- Flask

### Steps

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/your-flask-chat-app.git
    ```

2. Install dependencies:

    ```bash
    cd your-flask-chat-app
    pip install -r requirements.txt
    ```

3. Run the app:
   Remember to not use flask to run the python app because we are running the app through socketio library.
   Use the below method to simply run the _app.py_ file through python.

    ```bash
    python app.py
    ```

    The app will be accessible at `http://localhost:5000` by default.

## Usage

1. Open your web browser and navigate to `http://localhost:5000`.
2. Create a username and join the chat room.
3. Start chatting with others on your local network.

## LAN Configuration

1. By default, The app runs in local host mode where it cannot be accessed by any other computer on the network.
2. To Overcome this , add a small parameter in _socketio.run()_ function at the end of _app.py_ file as given below .
```bash
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True,host="0.0.0.0")
```
## Warning
There are two things to be careful about - 
1. This server will run with [werkzeug](https://flask-socketio.readthedocs.io/en/latest/getting_started.html#initialization).
2. Read about the potential dangers of  using externally visible server [here](https://flask.palletsprojects.com/en/3.0.x/quickstart/)

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE).

