from aifc import Error

from flask import jsonify,Flask,request
import mysql.connector

app = Flask(__name__)
def get_db_connection():
    try:
        return mysql.connector.connect(
            host='localhost',
            user='root',
            password='hasan099',
            database='swift'
        )
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None
@app.route('/api/swift_codes', methods=['GET'])
def get_swift_codes():
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'No database connection'})
    try:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM swift_codes')
        swift_codes = cursor.fetchall()

        return jsonify(swift_codes)
    except Error as e:
        return jsonify({'error': f"Error fetching data {e}"}),500
    finally:
        cursor.close()
        connection.close()

@app.route('/api/swift_codes/<swift_code>', methods=['GET'])
def get_swift_code(swift_code):
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'No database connection'})
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM swift_codes WHERE swiftCode = %s", (swift_code,))
        swift_code_data = cursor.fetchone()
        print(swift_code_data)
        if not swift_code_data:
            return jsonify({"error": "SWIFT Code not found"}), 404

        is_headquarter = swift_code_data['isHeadquarter']

        response = {
            "address": swift_code_data['address'],
            "bankName": swift_code_data['bankName'],
            "countryISO2": swift_code_data['countryISO2'],
            "countryName": swift_code_data['countryName'],
            "isHeadquarter": is_headquarter,
            "swiftCode": swift_code_data['swiftCode']
        }

        if is_headquarter:
            cursor.execute("""
                SELECT * FROM swift_codes 
                WHERE bankName = %s AND countryISO2 = %s AND swiftCode != %s
            """, (swift_code_data['bankName'], swift_code_data['countryISO2'], swift_code))

            branches_data = cursor.fetchall()
            print(branches_data)
            branches = []
            for branch in branches_data:
                branches.append({
                    "address": branch['address'],
                    "bankName": branch['bankName'],
                    "countryISO2": branch['countryISO2'],
                    "isHeadquarter": branch['isHeadquarter'],
                    "swiftCode": branch['swiftCode']
                })
            response["branches"] = branches
            return jsonify(response)
    except Error as e:
        return jsonify({"error": f"Error fetching data: {e}"}), 500
    finally:
        cursor.close()
        connection.close()


@app.route('/api/swift_codes/country/<countryISO2code>', methods=['GET'])
def get_swift_code_by_country(countryISO2code):
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Failed to connect to the database"}), 500
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT swiftCode, bankName, countryISO2, countryName,"
                       " address, isHeadquarter FROM swift_codes where countryISO2 = %s", (countryISO2code.upper(),))
        rows = cursor.fetchall()


        if not rows:
            return jsonify({"error": "No SWIFT codes found for this country"}), 404

        country_name=rows[0]['countryName']
        mainone={"countryISO2": countryISO2code.upper(),
                "countryName": country_name,}
        response=[]
        for row in rows:
            response.append({
                    "address": row['address'],
                    "bankName": row['bankName'],
                    "countryISO2": row['countryISO2'],
                    "isHeadquarter": row['isHeadquarter'],
                    "swiftCode": row['swiftCode']
            })
        mainone["swiftCodes"]=response
        return jsonify(mainone), 200
    except Error as e:
        return jsonify({"error": f"Error fetching data: {e}"}), 500
    finally:
        cursor.close()
        connection.close()

def validate_swift_code(code):
    required_fields = ["address", "bankName", "countryISO2", "countryName", "isHeadquarter"]
    for field in required_fields:
        if field not in code:
            return False,f"Missing required field: {field}"
    return True,""


@app.route('/api/swift_codes', methods=['POST'])
def create_swift_code():
    new_swiftcode = request.get_json()
    print(new_swiftcode)
    valid, error_message = validate_swift_code(new_swiftcode)
    if not valid:
        return jsonify({"error": error_message}), 400
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Failed to connect to the database"}), 500

    try:

        cursor = connection.cursor()


        cursor.execute("SELECT * FROM swift_codes WHERE swiftCode = %s", (new_swiftcode['swiftCode'],))
        existing = cursor.fetchone()

        if existing:
            return jsonify({"message": f"SWIFT code {new_swiftcode['swiftCode']} already exists."}), 409


        cursor.execute('''INSERT INTO swift_codes (swiftCode, bankName, countryISO2, countryName, address, isHeadquarter) 
                          VALUES (%s, %s, %s, %s, %s, %s)''',
                       (new_swiftcode["swiftCode"], new_swiftcode['bankName'], new_swiftcode['countryISO2'],
                        new_swiftcode['countryName'], new_swiftcode['address'], new_swiftcode['isHeadquarter']))
        connection.commit()

        return jsonify({'message': f"SWIFT code {new_swiftcode['swiftCode']} added successfully."}), 201

    except Error as e:
        return jsonify({"error": f"Error adding SWIFT code: {e}"}), 500

    finally:
        cursor.close()
        connection.close()

@app.route('/api/swift_codes/<swift_code>', methods=['PUT'])
def update_swiftcode(swift_code):
    try:
        updated_swiftcode = request.get_json()
        valid,error_message=validate_swift_code(updated_swiftcode)
        if not valid:
            return jsonify({"error": error_message}), 400
        connection = get_db_connection()
        if not connection:
            return jsonify({"error": "Failed to connect to the database"}), 500

        cursor = connection.cursor()
        cursor.execute('''UPDATE swift_codes SET bankName = %s, countryISO2 = %s, countryName = %s, 
                          address = %s, isHeadquarter = %s WHERE swiftCode = %s''',
                       (updated_swiftcode['bankName'], updated_swiftcode['countryISO2'],
                        updated_swiftcode['countryName'], updated_swiftcode['address'], updated_swiftcode['isHeadquarter'],swift_code))
        print(cursor.fetchone())
        if cursor.rowcount == 0:
            return jsonify({"error": f"SWIFT code {swift_code} not found"}), 404
        connection.commit()
        return jsonify({'message': 'SWIFT code updated'}), 200
    except Error as e:
        return jsonify({"error": f"Error updating SWIFT code: {e}"}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/api/swift_codes/<swift_code>', methods=['DELETE'])
def delete_swiftcode(swift_code):
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({"error": "Failed to connect to the database"}), 500
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM swift_codes WHERE swiftCode = %s", (swift_code,))
        row = cursor.fetchone()
        if not row:
            return jsonify({"message": f"SWIFT code {swift_code} not found."}), 404
        cursor.execute('DELETE FROM swift_codes WHERE swiftCode = %s', (swift_code,))
        connection.commit()
        return jsonify({'message': f"SWIFT code {swift_code} deleted successfully"}), 200
    except Error as e:
        return jsonify({"error": f"Error deleting SWIFT code: {e}"}), 500
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)