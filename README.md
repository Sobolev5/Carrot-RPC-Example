## Starlette + RabbitMQ. Simple RPC calls to backend microservices. Full working example.

To run use:

```no-highlight
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
docker-compose up
```

To watch console logs use:

```no-highlight
docker logs starlette_plus_rabbitmq_microservice_interface_1 --tail 100 --follow
docker logs starlette_plus_rabbitmq_microservice_sum_1 --tail 100 --follow
```

You can see full working example on:
> http://5.187.4.179:5888/
