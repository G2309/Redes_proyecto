# Propuesta del Proyecto 
---
- Gustavo Adolfo Cruz Bardales #22779
---

La idea es utilizar Python para implementar un servidor MCP local que pueda correr dentro de un contenedor con Docker (Docker por tema de dependencias pero tambien podria cambiar a un entorno virtual de python). El propósito es tener un entorno controlado y fácil de desplegar, donde el servidor pueda manejar las solicitudes del cliente sin depender de servicios externos. Para de esta manera, asegurar portabilidad, facilidad de mantenimiento y un flujo de trabajo más estable.

El cliente haría uso de este servidor para enviar solicitudes y obtener respuestas en un formato definido, con la ventaja de que toda la comunicación se mantendría en la red local. Esto garantiza menor latencia y una mayor seguridad en el manejo de los datos, además de permitir que la lógica de negocio quede centralizada en un solo servicio.

Para la implementación se planea utilizar la librería FastAPI, que ofrece una manera sencilla y eficiente de exponer endpoints tipo REST. Ya se cuenta con experiencia previa en el uso de Python y Docker, así como conocimientos básicos de FastAPI, lo cual permitirá avanzar en la construcción y despliegue del servidor de forma más ágil.

