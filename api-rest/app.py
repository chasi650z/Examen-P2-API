from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

DB_CONFIG = {
    "dbname": "api_rest",
    "user": "postgres",
    "password": "password",
    "host": "postgres",
    "port": "5432"
}

@app.route('/reservations', methods=['POST'])
def create_reservation():
    data = request.get_json()
    try:
        print("Conectando a la base de datos...")
        conn = psycopg2.connect(**DB_CONFIG)
        print("Conexión exitosa")

        cursor = conn.cursor()
        query = """
            INSERT INTO reservations (room_number, customer_name, start_date, end_date, status) 
            VALUES (%s, %s, %s, %s, 'confirmed') RETURNING reservation_id;
        """
        cursor.execute(query, (data['room_number'], data['customer_name'], data['start_date'], data['end_date']))
        conn.commit()
        res_id = cursor.fetchone()[0]
        return jsonify({"reservation_id": res_id}), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@app.route('/reservations/<int:reservation_id>', methods=['PUT'])
def update_reservation(reservation_id):
    data = request.get_json()
    try:
        print("Conectando a la base de datos para actualizar...")
        conn = psycopg2.connect(**DB_CONFIG)
        print("Conexión exitosa")
        
        cursor = conn.cursor()

        # Aquí asumimos que todos estos campos pueden ser actualizados.
        # En caso de querer actualizar solo algunos, habrá que añadir
        # lógica condicional.
        query = """
            UPDATE reservations
            SET room_number = %s,
                customer_name = %s,
                start_date = %s,
                end_date = %s,
                status = %s
            WHERE reservation_id = %s
        """
        cursor.execute(query, (
            data.get('room_number'),
            data.get('customer_name'),
            data.get('start_date'),
            data.get('end_date'),
            data.get('status', 'confirmed'),
            reservation_id
        ))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Reservation not found"}), 404
        
        return jsonify({"message": "Reservation updated successfully"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@app.route('/reservations/<int:reservation_id>', methods=['DELETE'])
def delete_reservation(reservation_id):
    try:
        print("Conectando a la base de datos para eliminar...")
        conn = psycopg2.connect(**DB_CONFIG)
        print("Conexión exitosa")
        
        cursor = conn.cursor()
        query = "DELETE FROM reservations WHERE reservation_id = %s"
        cursor.execute(query, (reservation_id,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Reservation not found"}), 404
        
        return jsonify({"message": "Reservation deleted successfully"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)



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
