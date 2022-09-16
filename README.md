## Carrot-RPC. Simple RPC calls to backend microservices. Example of work.

This is working example of  `carrot-rpc` package: 
https://github.com/Sobolev5/carrot-rpc

# Run
To run use:
```no-highlight
https://github.com/Sobolev5/carrot-rpc.git
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
docker-compose up
```

To watch console logs use:

```no-highlight
docker logs microservice_interface --tail 100 --follow
docker logs microservice_sum --tail 100 --follow
```

You can see full working example on:
> http://5.187.4.179:5888/
