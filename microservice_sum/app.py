import asyncio
import aiormq
from pydantic import BaseModel
from carrot import carrot_ask
from simple_print import sprint
from fastapi import FastAPI
from fastapi import APIRouter


## AMQP ######################################

# set amqp connection:
AMQP_URI = "amqp://admin:YTmJqsNx2@rabbitmq/vhost"

# make pydantic schema:
class SumAAndB(BaseModel):
    caller: str
    a: int
    b: int

# decorate called function with pydantic schema
@carrot_ask(SumAAndB)
async def sum_a_and_b(incoming_dict: dict) -> dict:
    sprint(incoming_dict, c="yellow", s=1, p=1)
    dct = {}
    dct["caller"] = "i am sum_a_and_b function mounted on microservice_sum"
    dct["sum"] = incoming_dict["number_a"] + incoming_dict["number_b"]
    return dct

# make amqp router:
async def amqp_router():
    connection = await aiormq.connect(AMQP_URI)
    channel = await connection.channel()
    sprint(f"AMQP:     ready [yes]", c="green", s=1, p=1)
    sum_a_and_b__declared = await channel.queue_declare(f"microservice_sum:sum_a_and_b", durable=False)
    await channel.basic_consume(sum_a_and_b__declared.queue, sum_a_and_b, no_ack=False)  
    
## AMQP END ###################################



## HTTP #######################################

# make http router
http_router = APIRouter()

# add http endpoint
@http_router.post("/")
async def main(request):
    return {"http": "ready"}

## HTTP END ###################################


class App(FastAPI):
    def __init__(self, *args, **kwargs):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.create_task(amqp_router())
        super().__init__(*args, **kwargs)

app = App()
app.include_router(http_router)

# So you can use this microservice for ampq and http together. enjoy. 
# and add you stars on github. Thank you.
