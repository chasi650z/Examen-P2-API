from flask import Flask, request, jsonify
import psycopg2
import requests

app = Flask(__name__)

DB_CONFIG = {
    "dbname": "api_rest",
    "user": "postgres",
    "password": "password",
    "host": "postgres",
    "port": "5432"
}

SOAP_URL = "http://localhost:5000/updateAvailability"  # La URL del servicio SOAP para actualizar la disponibilidad

@app.route('/reservations', methods=['POST'])
def create_reservation():
    data = request.get_json()

    try:
        print("Conectando a la base de datos...")
        conn = psycopg2.connect(**DB_CONFIG)
        print("Conexión exitosa")

        cursor = conn.cursor()
        query = "INSERT INTO reservations (room_number, customer_name, start_date, end_date, status) VALUES (%s, %s, %s, %s, 'confirmed') RETURNING reservation_id;"
        cursor.execute(query, (data['room_number'], data['customer_name'], data['start_date'], data['end_date']))
        conn.commit()
        res_id = cursor.fetchone()[0]

        # Realizar la llamada SOAP para actualizar la disponibilidad de la habitación
        update_availability(data['room_number'], data['start_date'], data['end_date'])

        return jsonify({"reservation_id": res_id}), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Ha ocurrido un error en el servidor", "message": str(e)}), 500
    finally:
        # Asegúrate de cerrar la conexión y el cursor solo si se crearon correctamente
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


def update_availability(room_number, start_date, end_date):
    # Hacer la solicitud POST al servicio SOAP
    payload = {"room_number": room_number, "start_date": start_date, "end_date": end_date}
    response = requests.post(SOAP_URL, json=payload)

    if response.status_code == 200:
        print("Disponibilidad actualizada correctamente en el servicio SOAP.")
    else:
        print(f"Error al actualizar disponibilidad: {response.text}")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
