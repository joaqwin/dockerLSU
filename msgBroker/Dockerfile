FROM rabbitmq:3-management

RUN rabbitmq-plugins enable --offline rabbitmq_management

COPY ./custom-entrypoint.sh /custom-entrypoint.sh
RUN chmod +x /custom-entrypoint.sh

ENTRYPOINT ["/custom-entrypoint.sh"]