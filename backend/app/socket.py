import socketio

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")


@sio.event
async def connect(sid, environ):
    return True


@sio.event
async def disconnect(sid):
    return None


@sio.event
async def join_project(sid, project_id):
    await sio.enter_room(sid, f"project:{project_id}")
    await sio.emit("project_joined", {"project_id": project_id}, to=sid)


@sio.event
async def leave_project(sid, project_id):
    await sio.leave_room(sid, f"project:{project_id}")
