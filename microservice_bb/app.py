import asyncio
import aiormq
from pydantic import BaseModel
from carrot import carrot_ask
from fastapi import FastAPI
from simple_print import sprint


# defer AMQP connection:
AMQP_URI = "amqp://admin:admin@carrot_rabbitmq/vhost"

# make pydantic schema:
class SumAAndB(BaseModel):
    caller: str
    number_a: int
    number_b: int

# you can protect called function with pydantic schema
@carrot_ask(SumAAndB)
async def sum_a_and_b(sum_model: BaseModel) -> dict:
    sprint(sum_model, c="green")
    dct = {}
    dct["sum"] = sum_model.number_a + sum_model.number_b
    return dct

# or use plain decorator carrot_ask() without protection
@carrot_ask()
async def sum_a_and_b_without_protect(incoming_dict: dict) -> dict:
    dct = {}
    dct["sum"] = incoming_dict["number_a"] + incoming_dict["number_b"]
    return dct

# make amqp router:
async def amqp_router():
    connection = await aiormq.connect(AMQP_URI)
    channel = await connection.channel()
    sprint(f"AMQP:     ready [yes]", c="green")
    sum_a_and_b_queue = await channel.queue_declare(f"BB:sum_a_and_b", durable=False)
    await channel.basic_consume(sum_a_and_b_queue.queue, sum_a_and_b, no_ack=False)  
    
app = FastAPI()

@app.on_event("startup")
async def startup_aiormq_router():
    loop = asyncio.get_running_loop()
    loop.create_task(amqp_router())