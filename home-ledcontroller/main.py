import uvicorn
import logging
import config
from asyncio import Queue, QueueFull
from typing import Optional, List, Tuple
from fastapi import FastAPI, Request, WebSocket, Depends
from constants import BLUE, OFF
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from adapter import pixels

logger = logging.getLogger(__file__)
app = FastAPI()
settings = config.get()

app.mount("/static", StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory="templates")

DEFAULT_COLOR = BLUE

#TODO: settings section in advanced user guide of fastapi
leds: List[Tuple[int, int, int]] = [(0,0,0) for x in range(settings.num_leds)]

class MutationQueue:
    # When nothing is listening to the queue, mutations will be dropped
    q = Queue(maxsize=100)

    def put(self, led_num, r, g, b):
        try:
            self.q.put_nowait(f'{led_num},{r},{g},{b}')
        except QueueFull:
            logger.info("Mutation queue is full, dropping mutation")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("ui.html", {"request":request, "led_state": leds})

@app.get("/state/")
async def state():
    return [(r,g,b) for g,r,b in leds]

@app.post("/state/{led_num}/on/")
async def on(led_num: int, r:Optional[int]=0, g:Optional[int]=0, b: Optional[int]=0, queue: MutationQueue = Depends()):
    global leds
    if g+r+b == 0:
        g, r, b = DEFAULT_COLOR

    pixels[led_num] = (g, r, b)
    leds[led_num] = (g, r, b)
    queue.put(led_num, r, g, b)
    pixels.show()

    return True

@app.post("/state/{led_num}/off/")
async def off(led_num: int, queue: MutationQueue = Depends()):
    global leds
    leds[led_num] = OFF
    queue.put(led_num, OFF[1], OFF[0], OFF[2])
    pixels[led_num] = OFF
    pixels.show()

    return False

@app.websocket("/websocket/")
async def websocket_endpoint(websocket: WebSocket, queue: MutationQueue = Depends()):
    await websocket.accept()
    while True:
        data = await queue.q.get()
        await websocket.send_text(data)


def main():
    uvicorn.run(app, host=settings.host, port=settings.port, log_level="info")