import asyncio
import aiormq
from carrot import carrot_ask
from simple_print import sprint


AMQP_URI = "amqp://admin:YTmJqsNx2@rabbitmq/vhost"


@carrot_ask
async def sum_a_and_b(incoming_dict: dict) -> dict:
    sprint(incoming_dict, c="yellow", s=1, p=1)
    dct = {}
    dct["who_am_i"] = "i am rpc function mounted on microservice_sum"
    dct["sum"] = incoming_dict["number_a"] + incoming_dict["number_b"]
    return dct


async def rpc_subscriptions():
    connection = await aiormq.connect(AMQP_URI)
    channel = await connection.channel()
    sprint(f"AMQP RPC:     ready [yes]", c="green", s=1, p=1)
    sum_a_and_b__declared = await channel.queue_declare(f"microservice_sum:sum_a_and_b", durable=False)
    await channel.basic_consume(sum_a_and_b__declared.queue, sum_a_and_b, no_ack=False)  
    

loop = asyncio.get_event_loop()
loop.create_task(rpc_subscriptions())
loop.run_forever()

