from .websocket import socketio

from flask_socketio import emit, join_room, leave_room

@socketio.on("connect")
def handle_connect():
    print("Client connected.")

@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected.")
    
@socketio.on("new_message")
def handle_new_message(message):
    print("new message: ", message)
    emit("chat", {"message": message})