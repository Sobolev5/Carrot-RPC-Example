from carrot import CarrotCall
from simple_print import sprint
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.responses import HTMLResponse
from starlette.routing import Route

# set amqp connection:
AMQP_URI = "amqp://admin:admin@carrot_rabbitmq/vhost"

# make template:
html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Starlette + RabbitMQ. Simple RPC calls to backend Microservices.</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    </head>
    <body style="background-color: #faf06c">
        <div class="container mt-1" style="text-align: center;">    
            <a href="https://github.com/Sobolev5/carrot-rpc"><img src="https://andrey-sobolev.ru/static/starlette_rabbit.jpg"></a> 
        </div>
        <div class="container mt-1">         
            <div class="card">
                <div class="card-header">
                    carrot-rpc==0.3.1
                </div>
                <div class"card-body">   
                    <div class="p-3"> 
                        1) This page render by <code>Microservice_AA</code>
                        <br>
                        2) Number A + Number B will be calculated on <code>Microservice_BB</code> with pydantic schema validation and 
                        <code>Microservice_AA</code> render response from <code>Microservice_BB</code>
                        </small>      
                        <hr>    
                        <form action="/" method="POST">
                            <div class="mb-3">
                                <label class="form-label">Number A</label>
                                <input type="number" class="form-control" name="number_a" value="4">
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Number B</label>
                                <input type="number" class="form-control" name="number_b" value="10">
                            </div>
                            <button type="submit" class="btn btn-primary">Calculate sum A and B on Microservice_BB and return result to Microservice_AA</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </body>
</html>
"""

# defer main function which call Microservice «Microservice_BB»:
async def call_sum_a_and_b(request):
    if request.method == "POST":
        data = await request.form()

        # make dict request:
        d = {}
        d["caller"] = "Function on Microservice_AA which call function on Microservice_BB"
        d["number_a"] = int(data["number_a"])
        d["number_b"] = int(data["number_b"])

        # defer carrot instance and make rpc call:
        carrot = await CarrotCall(AMQP_URI=AMQP_URI).connect()
        response_from_bb = await carrot.call(d, "BB:sum_a_and_b", timeout=5)  
        sprint(response_from_bb)
        # first arg is dict with data
        # second arg it routing key (through default AMQP exchange) 
        # third arg is optional (response timeout in seconds, 7 seconds by default)
        return JSONResponse(response_from_bb)    
    else:
        return HTMLResponse(html)


routes = [
    Route("/", call_sum_a_and_b, methods=['GET', 'POST']),
]


app = Starlette(routes=routes)
