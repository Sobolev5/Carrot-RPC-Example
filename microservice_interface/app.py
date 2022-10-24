import asyncio
from carrot import Carrot
from simple_print import sprint
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.responses import HTMLResponse
from starlette.routing import Route

# set amqp connection:
AMQP_URI = "amqp://admin:YTmJqsNx2@rabbitmq/vhost"

# make template:
html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Starlette + RabbitMQ. Simple RPC calls to backend microservices.</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    </head>
    <body style="background-color: #faf06c">
        <div class="container mt-1" style="text-align: center;">    
            <a href="https://github.com/Sobolev5/carrot-rpc"><img src="https://andrey-sobolev.ru/static/starlette_rabbit.jpg"></a> 
        </div>
        <div class="container mt-1">         
            <div class="card">
                <div class="card-header">
                    carrot-rpc==0.2.5
                </div>
                <div class"card-body">   
                    <div class="p-3">  
                        Sum A and B will be calculated on microservice «microservice_sum» and validated with pydantic schema.
                        <br>
                        <small><b>Note</b> This page render by «microservice_interface».</small>               
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
            </div>
        </div>
    </body>
</html>
"""

# defer main function which call microservice «microservice_sum»:
async def call_sum_a_and_b(request):
    if request.method == "POST":
        sprint(f"call_sum_a_and_b", с="green", s=1, p=1)
        data = await request.form()

        # make dict request:
        dct = {}
        dct["caller"] = "Function on microservice_interface which call RPC in microservice_sum"
        dct["number_a"] = int(data["number_a"])
        dct["number_b"] = int(data["number_b"])

        # defer carrot instance and make rpc call:
        carrot = await Carrot(AMQP_URI).connect()
        response_from_another_microservice = await carrot.call(dct, "microservice_sum:sum_a_and_b")    

        # dct: first arg is dict with data
        # another_microservice:sum_a_and_b: second arg it routing key (through default AMQP exchange) 

        # get response dict from microservice «microservice_sum»
        sprint(f'Sum a and b: {response_from_another_microservice["sum"]}', c="yellow", s=1, p=1)
        return JSONResponse({"sum (response from microservice_sum)": response_from_another_microservice["sum"]})    
    else:
        return HTMLResponse(html)


routes = [
    Route("/", call_sum_a_and_b, methods=['GET', 'POST']),
]


app = Starlette(routes=routes)
