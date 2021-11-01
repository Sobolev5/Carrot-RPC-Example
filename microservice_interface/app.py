import asyncio
from carrot import Carrot
from simple_print import sprint
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.responses import HTMLResponse
from starlette.routing import Route

AMQP_URI = "amqp://admin:YTmJqsNx2@rabbitmq/vhost"


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Starlette + RabbitMQ. Simple RPC calls to backend microservices.</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    </head>
    <body style="background-color: #faf06c">
        <div class="container mt-1" style="text-align: center;">    
            <img src="https://andrey-sobolev.ru/static/starlette_rabbit.jpg">  
        </div>
        <div class="container mt-1">         
            <div class="card">
                <div class"card-body">   
                    <div class="p-3">  
                        Sum A and B (will be calculated on microservice «microservice_sum») *.
                        <br>
                        <small>* This page load via «microservice_interface».</small>               
                        <form action="/" method="POST">
                            <div class="mb-3">
                                <label class="form-label">Number A</label>
                                <input type="number" class="form-control" name="number_a" value="4">
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Number B</label>
                                <input type="number" class="form-control" name="number_b" value="10">
                            </div>
                            <button type="submit" class="btn btn-primary">Sum A and B</button>
                        </form>
                    </div>
                </div>
                <div class="p-3"> 
                    <p>
                        Buy me a coffee. Thanks!
                    </p> 
                    <p>0x6817b29f6a25B7BaE42158FAFad7b782415e4209 ETH</p>
                    <p>TZ1Hs1tkpPJFrPzmvo8xtHEKErXniV3x21 TRC (TRON)</p>
                </div>
            </div>
        </div>
    </body>
</html>
"""


async def call_sum_a_and_b(request):
    # sum_a_and_b - will be calculated on microservice «microservice_sum»
    if request.method == "POST":
        sprint(f"call_sum_a_and_b", с="green", s=1, p=1)
        data = await request.form()

        dct = {}
        dct["who_am_i"] = "i'm function on microservice_interface which call RPC in microservice_sum"
        dct["number_a"] = int(data["number_a"])
        dct["number_b"] = int(data["number_b"])

        carrot = await Carrot(AMQP_URI).connect()
        response_from_another_microservice = await carrot.call(dct, "microservice_sum:sum_a_and_b")    

        # dct: first arg is dict with data
        # "another_microservice:sum_a_and_b": second arg it is name of routing key (through default AMQP exchange) 

        sprint(f'Sum a and b: {response_from_another_microservice["sum"]}', c="yellow", s=1, p=1)
        return JSONResponse({"sum (response from microservice_sum)": response_from_another_microservice["sum"]})
    
    else:
        return HTMLResponse(html)


routes = [
    Route("/", call_sum_a_and_b, methods=['GET', 'POST']),
]


app = Starlette(routes=routes)
