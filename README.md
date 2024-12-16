https://github.com/chasi650z/Examen-P2-API

Sistema de Gestión de Reservas para un Hotel (LuxuryStay)
Este sistema permite gestionar las operaciones de reservas y disponibilidad de habitaciones de manera centralizada para la cadena hotelera LuxuryStay. El sistema está compuesto por tres microservicios:
1.	Servicio SOAP: Consultar la disponibilidad de habitaciones.
2.	API REST: Realizar, consultar y cancelar reservas.
3.	Microservicio de Inventario: Gestionar la actualización del inventario de habitaciones.
Requisitos
•	Docker
•	Docker Compose
Estructura del Proyecto
El proyecto está organizado en diferentes carpetas para cada servicio:

/hotel-reservation-system
    ├── /api-rest
    ├── /inventory-service
    ├── /soap-service
    └── docker-compose.yml
•	/api-rest: Contiene la API REST que maneja las reservas.
•	/inventory-service: Microservicio que gestiona las habitaciones.
•	/soap-service: Servicio SOAP que consulta la disponibilidad de las habitaciones.
•	docker-compose.yml: Configuración de Docker Compose para levantar todos los servicios.
Configuración y Ejecución
1. Configuración de Docker Compose
Asegúrate de tener Docker y Docker Compose instalados en tu máquina. Si no los tienes, puedes instalarlos desde Docker's Official Website.
2. Clonar el Repositorio
Clona el repositorio del proyecto:

git clone https://github.com/chasi650z/Examen-P2-API.git
cd hotel-reservation-system

3. Construcción y Ejecución de los Contenedores
Dentro del directorio raíz del proyecto, puedes levantar todos los servicios usando Docker Compose. Ejecuta el siguiente comando:

docker-compose up –build

Este comando hará lo siguiente:
•	Construirá las imágenes de los servicios (si no están construidas previamente).
•	Levantará los contenedores de los servicios:
o	API REST: El servicio para gestionar las reservas.
o	SOAP Service: El servicio que permite consultar la disponibilidad de habitaciones.
o	Inventory Service: El microservicio que gestiona el inventario de habitaciones.
o	PostgreSQL: Base de datos para almacenar las reservas y datos de las habitaciones.
4. Verificación de los Contenedores
Puedes verificar que todos los contenedores estén corriendo correctamente con el siguiente comando:

docker ps
Asegúrate de que los contenedores estén Up y funcionando correctamente.

5. Probar el Sistema
Una vez que los contenedores estén funcionando, puedes probar el sistema con las siguientes herramientas:
API REST
•	Crear Reserva (POST /reservations):
En Postman, realiza una solicitud POST a http://127.0.0.1:5003/reservations con el siguiente JSON en el cuerpo:

{
    "room_number": 10,
    "customer_name": "Pablo Chasipanta",
    "start_date": "2024-12-16",
    "end_date": "2024-12-17"
}
Esto creará una nueva reserva y actualizará el estado de la habitación.
•	Consultar Reserva (GET /reservations/{id}):
Para consultar una reserva específica, realiza una solicitud GET a http://127.0.0.1:5003/reservations/1, donde 1 es el reservation_id que obtuviste en el paso anterior.
•	Cancelar Reserva (DELETE /reservations/{id}):
Para cancelar una reserva, realiza una solicitud DELETE a http://127.0.0.1:5003/reservations/1, donde 1 es el reservation_id.
Servicio SOAP
•	Consultar Disponibilidad (POST /CheckAvailability):
En Postman, realiza una solicitud POST a http://127.0.0.1:5000/CheckAvailability con el siguiente cuerpo XML:

{
    "start_date": "2024-12-01",
    "end_date": "2024-12-18",
    "room_type": "Single"
}
Esto te devolverá un XML con las habitaciones disponibles para las fechas indicadas.
Microservicio de Inventario
•	Registrar Nueva Habitación (POST /rooms):
En Postman, realiza una solicitud POST a http://127.0.0.1:5002/rooms con el siguiente JSON en el cuerpo:

{
    "room_number": 10,
    "room_type": "Deluxe",
    "status": "available"
}

Esto registrará una nueva habitación en el inventario.
6. Acceder a las Bases de Datos
Si necesitas acceder a las bases de datos de los servicios, puedes hacerlo directamente desde la línea de comandos de Docker.
Para acceder a la base de datos PostgreSQL:
bash
Copiar código
docker exec -it hotel-reservation-system-postgres-1 psql -U postgres
Una vez dentro de PostgreSQL, puedes consultar las tablas usando los siguientes comandos:
•	Para ver las habitaciones disponibles:
SELECT * FROM availability;
•	Para ver las reservas:
SELECT * FROM reservations;
•	Para ver las habitaciones del inventario:
SELECT * FROM rooms;

7. Detener los Servicios
Cuando hayas terminado de probar los servicios, puedes detener todos los contenedores con el siguiente comando:

docker-compose down

Este comando detendrá todos los contenedores pero no eliminará las imágenes, por lo que puedes reiniciar los contenedores más tarde con docker-compose up.
