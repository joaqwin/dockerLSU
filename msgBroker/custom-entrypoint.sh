#!/bin/bash

# wait for RabbitMQ server to start
rabbitmq-server -detached

sleep 30
# declare exchange
rabbitmqadmin declare exchange name=my_exchange type=fanout auto_delete=true

# declare queue
rabbitmqadmin declare queue name=my_queue auto_delete=true

# declare binding
rabbitmqadmin declare binding source=my_exchange destination_type=queue destination=my_queue routing_key=my_queue

tail -f /dev/null
