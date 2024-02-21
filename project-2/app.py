from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_mail import Mail, Message
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash
from flask_mysqldb import MySQL
from flask_session import Session

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flight'
mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()

        if user and check_password_hash(user[2], password):
            session['username'] = user[1]
            return redirect(url_for('main'))
        else:
            message = "wrong username/password"
            return render_template('user/login.html', message=message)
    return render_template('user/login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        with mysql.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            existing_user = cursor.fetchone()

        if existing_user:
            message = "username already exists"
            return render_template('user/signup.html', message=message)

        if password == confirm_password:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

            with mysql.connection.cursor() as cursor:
                cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, hashed_password))
                mysql.connection.commit()

            session['username'] = username
            return redirect(url_for('main'))
        else:
            return render_template('user/signup.html')

    return render_template('user/signup.html')

@app.route('/main', methods=['GET', 'POST'])
def main():
    if 'username' in session:
        if request.method == 'POST':
            date = request.form['date']
            time = request.form.get('time')
            print(time)
            if time:
                datetime_input = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
                datetime_input = datetime_input.replace(second=0, microsecond=0)
                condition = "STR_TO_DATE(DATE_FORMAT(departure_time, '%%Y-%%m-%%d %%H:%%i'), '%%Y-%%m-%%d %%H:%%i') = %s AND available_seats > 0"
                params = (datetime_input.strftime('%Y-%m-%d %H:%M'),)
            else:
                datetime_input = datetime.strptime(date, "%Y-%m-%d")
                condition = "DATE(departure_time) = %s AND available_seats > 0"
                params = (datetime_input.strftime('%Y-%m-%d'),)

            cursor = mysql.connection.cursor()

            query = f"SELECT * FROM flights WHERE {condition}"
            cursor.execute(query, params)

            exact_time_flights = cursor.fetchall()

            if exact_time_flights:
                return render_template('user/main.html', available_flights=exact_time_flights)
            else:
                cursor.execute("SELECT * FROM flights WHERE DATE(departure_time) = %s AND available_seats > 0 ORDER BY departure_time ASC", (datetime_input.strftime('%Y-%m-%d'),))
                all_day_flights = cursor.fetchall()

                if all_day_flights:
                    return render_template('user/main.html', available_flights=all_day_flights)
                else:
                    message = f"No available flights on {datetime_input}."
                    return render_template('user/main.html', message=message)

        return render_template('user/main.html')  
    else:
        return redirect(url_for('login'))

@app.route('/book_flight/<int:flight_id>', methods=['GET', 'POST'])
def book_flight(flight_id):
    if 'username' in session:
        if request.method == 'POST':
            username = session['username']
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            seats = int(request.form['seats'])

            with mysql.connection.cursor() as cursor:
                cursor.execute("INSERT INTO bookings (username, flight_id, booking_time, name, email, phone, seats) "
                               "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                               (username, flight_id, datetime.now(), name, email, phone, seats))
                mysql.connection.commit()
                cursor.execute("select available_seats from flights where flight_id=%s",(flight_id,))
                available_seats = cursor.fetchone()

                if seats > available_seats[0]:
                    return render_template('user/main.html', message="not enough seats for the booking")

                cursor.execute("UPDATE flights SET available_seats = available_seats - %s WHERE flight_id = %s",
                               (seats, flight_id))
                mysql.connection.commit()

            return redirect(url_for('my_bookings'))

        return render_template('user/booking.html', flight_id=flight_id)

    else:
        return redirect(url_for('login'))

@app.route('/my_bookings')
def my_bookings():
    if 'username' in session:
        username = session['username']

        with mysql.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM bookings WHERE username = %s", (username,))
            bookings = cursor.fetchall()

        return render_template('user/my_bookings.html', bookings=bookings)
    else:
        return redirect(url_for('login'))

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username1 = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM admins WHERE username = %s and password=%s", (username1,password,))
        user = cursor.fetchone()
        cursor.close()

        if user:
            session['username1'] = user[0]
            return redirect(url_for('admin_dashboard'))

        else:
            message = "wrong username/password"
            return render_template('admin/admin_login.html', message=message)
    return render_template('admin/admin_login.html')

@app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if 'username1' in session:
        return render_template('admin/admin_dashboard.html')
    else:
        return redirect(url_for('admin_login'))

@app.route('/add_flight', methods=['GET', 'POST'])
def add_flight():
    if 'username1' in session:
        if request.method == 'POST':
            flight_number = request.form['flight_number']
            departure_city = request.form['departure_city']
            arrival_city = request.form['arrival_city']
            departure_time = request.form['departure_time']
            available_seats = 60

            print(departure_time)

            try:
                cursor = mysql.connection.cursor()

                formatted_departure_time = departure_time.replace('T', ' ') + ':00'

                print(formatted_departure_time)
                print(type(formatted_departure_time))

                cursor.execute("INSERT INTO flights (flight_number, departure_city, arrival_city, departure_time) VALUES (%s, %s, %s, %s)",
                               (flight_number, departure_city, arrival_city, formatted_departure_time))

                mysql.connection.commit()
                cursor.close()

                message = "Added flight successfully."
                return render_template('admin/add_flight.html', message=message)

            except mysql.connector.Error as err:
                print(f"Error: {err}")
                return render_template('admin/add_flight.html', message="Error adding flight. Please try again.")

        return render_template('admin/add_flight.html')

    else:
        return redirect(url_for('admin_login'))

@app.route('/remove_flight', methods=['POST','GET'])
def remove_flight():
    if 'username1' in session:
        if request.method == 'POST':
            flight_number = request.form['flight_number']
            departure_time = request.form['departure_time']

            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM flights WHERE flight_number = %s and departure_time=%s", (flight_number,departure_time,))
            flight = cursor.fetchone()
            cursor.execute("SELECT flight_id FROM flights WHERE flight_number = %s", (flight_number,))
            flight_id = cursor.fetchone()

            if flight:
                cursor.execute("DELETE FROM bookings WHERE flight_id = %s", (flight_id,))

                cursor.execute("DELETE FROM flights WHERE flight_number = %s and departure_time=%s", (flight_number,departure_time,))
                mysql.connection.commit()
                cursor.close()

                message = f"Flight {flight_number} has been successfully removed."
                return render_template('admin/remove_flight.html', message=message)
            else:
                error_message = f"Flight with number {flight_number} does not exist."
                return render_template('admin/remove_flight.html', message=error_message)
        else:
            return render_template('admin/remove_flight.html')
    else:
        return redirect(url_for('admin_login'))

@app.route('/view_bookings', methods=['POST', 'GET'])
def view_bookings():
    if 'username1' in session:

        if request.method == 'POST':
            flight_number = request.form['flight_number']
            departure_time = request.form['departure_time']

            cursor = mysql.connection.cursor()
            cursor.execute("SELECT flight_id FROM flights WHERE flight_number = %s and departure_time=%s", (flight_number,departure_time))
            flight_id = cursor.fetchone()

            if flight_id:
                cursor.execute("SELECT * FROM bookings WHERE flight_id = %s ", (flight_id,))
                bookings = cursor.fetchall()
                print(bookings)

                cursor.close()

                return render_template('admin/view_bookings.html', bookings=bookings)
            else:
                message = "flight does not exist/ no bookings for that flight"
                return render_template('admin/view_bookings.html', message=message)

        elif request.method == 'GET':
            return render_template('admin/view_bookings.html', bookings=None)

    else:
        return redirect(url_for('admin_login'))

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('main'))

app.secret_key = 'abhinav1'

if __name__ == '__main__':
    app.run(debug=True)
