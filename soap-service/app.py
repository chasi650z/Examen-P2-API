from flask import Flask, request, Response
import psycopg2
from xml.etree.ElementTree import Element, SubElement, tostring, fromstring

app = Flask(__name__)

DB_CONFIG = {
    "dbname": "soap_service",
    "user": "postgres",
    "password": "password",
    "host": "postgres",
    "port": "5432"
}

def build_soap_response(rooms):
    envelope = Element("soapenv:Envelope", xmlns="http://schemas.xmlsoap.org/soap/envelope/")
    body = SubElement(envelope, "soapenv:Body")
    rooms_element = SubElement(body, "Rooms")

    for room in rooms:
        room_element = SubElement(rooms_element, "Room")
        SubElement(room_element, "RoomID").text = str(room["room_id"])
        SubElement(room_element, "RoomType").text = room["room_type"]
        SubElement(room_element, "AvailableDate").text = str(room["available_date"])

    return tostring(envelope)

@app.route("/CheckAvailability", methods=["POST"])
def check_availability():
    try:
        data = request.data.decode("utf-8")  # Parse incoming XML
        root = fromstring(data)  # Convierte el texto XML en un objeto de árbol
        start_date = root.find(".//start_date").text
        end_date = root.find(".//end_date").text
        room_type = root.find(".//room_type").text

        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        query = """
        SELECT room_id, room_type, available_date
        FROM availability
        WHERE room_type = %s AND available_date BETWEEN %s AND %s;
        """
        cursor.execute(query, (room_type, start_date, end_date))
        rooms = [{"room_id": r[0], "room_type": r[1], "available_date": r[2]} for r in cursor.fetchall()]
        response_xml = build_soap_response(rooms)

        return Response(response_xml, mimetype="text/xml")
    except Exception as e:
        error_response = f"<Error>{str(e)}</Error>"
        return Response(error_response, mimetype="text/xml")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)



