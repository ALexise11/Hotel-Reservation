from flask import Flask, render_template, request, session, redirect, url_for, send_from_directory
import mysql.connector
from werkzeug.utils import secure_filename
import os
import re
import requests

connection = mysql.connector.connect(
    host='localhost',
    port='3306',
    database='crud',
    user='root',
    password=''
)

cursor = connection.cursor()


app = Flask(__name__)
app.secret_key = "super secret key"




def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower()

def save_image(file):
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    return filename

@app.route('/static/<path:filename>')
def send_static(filename):
    return send_from_directory('static', filename)


@app.route('/homepage')
def homepage():
    return render_template('homepage.html')


@app.route('/')
def index():
    return render_template('index.html')

RECAPTCHA_SITE_KEY = '6Lc_cygpAAAAAN6nh78251AWEiNGpwxlSPekeaLx'
RECAPTCHA_SECRET_KEY = '6Lc_cygpAAAAAJjwSWvryXp_i8HEIMTw9ux1j1uP'

@app.route('/login', methods=['GET', 'POST'])
def login():
    text = ''
    
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        
        # Validate reCAPTCHA
        recaptcha_response = request.form['g-recaptcha-response']
        payload = {
            'secret': RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=payload)
        result = r.json()

        if result['success']:
            cursor.execute("SELECT * FROM accounts WHERE username = %s AND password = %s",
                           (username, password))
            user = cursor.fetchone()

            if user:
                session['loggedin'] = True
                session['id'] = user[1]
                session['username'] = user[0]
                session['role'] = user[8]  # Assuming 'role' is the 8th column in your accounts table

                if session['role'] == 'admin':
                    return redirect(url_for('manage_rooms'))
                else:
                    return redirect(url_for('home'))
            else:
                text = 'Incorrect username/password!'
        else:
            text = 'Please complete the reCAPTCHA.'

    return render_template('login.html', text=text, site_key=RECAPTCHA_SITE_KEY)

@app.route('/register', methods=['GET', 'POST'])
def register():
    alert = ''
    success_message = ''
    registration_success = False
    password_mismatch = False
    captcha_not_completed = False

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        address = request.form['address']
        contact = request.form['contact']
        recaptcha_response = request.form.get('g-recaptcha-response')

        # Check Passwords matches before proceeding
        if password != confirm_password:
            password_mismatch = True
            return render_template('register.html', password_mismatch=password_mismatch)

        # Check CAPTCHA before proceeding
        if not recaptcha_response:
            captcha_not_completed = True
            return render_template('register.html', captcha_not_completed=captcha_not_completed)

        secret_key = '6Lc_cygpAAAAAJjwSWvryXp_i8HEIMTw9ux1j1uP'  # Replace with your actual secret key
        response = requests.post('https://www.google.com/recaptcha/api/siteverify',
                                data={'secret': secret_key, 'response': recaptcha_response})
        data = response.json()
        if not data['success']:
            alert = "reCAPTCHA validation failed"
            return render_template('register.html', alert=alert)

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM accounts WHERE username = %s OR email = %s", (username, email))
        accounts = cursor.fetchall()

        if accounts:
            alert = "Account already exists"
            return render_template('register.html', alert=alert)

        cursor.execute(
            "INSERT INTO accounts (username, email, password, firstname, lastname, address, contact, role) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
            (username, email, password, firstname, lastname, address, contact, 'user'))
        connection.commit()

        success_message = "Account successfully created!"
        registration_success = True

    return render_template('register.html', alert=alert, success_message=success_message, registration_success=registration_success)


@app.route('/reservations')
def view_reservations():
    if 'loggedin' in session:
        # Assuming reservations are stored in a 'reservations' table
        cursor.execute("SELECT * FROM reservations")
        reservations = cursor.fetchall()
        return render_template('reservations.html', reservations=reservations)
    else:
        return redirect(url_for('login'))


from flask import render_template, request, session, redirect, url_for
from mysql.connector import Error
from datetime import datetime


from flask import render_template, redirect, url_for, session, flash
from flask import render_template, request, session, redirect, url_for
from mysql.connector import Error
from datetime import datetime

from flask import render_template, redirect, url_for, session, flash

@app.route('/make_reservation', methods=['GET', 'POST'])
def make_reservation():
    message = None
    rooms = None
    selected_room = None
    conflicting_reservation = None

    room_number = request.args.get('room_number')
    if room_number:
        try:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM rooms WHERE room_number = %s", (room_number,))
                selected_room = cursor.fetchone()

            if not selected_room:
                message = "Invalid room selected."
        except Error as e:
            print(f"Database Error: {e}")
            selected_room = None
            message = "Error fetching room details."

    if request.method == 'POST':
        check_in_date = request.form.get('check_in_date')
        check_in_time = request.form.get('check_in_time')
        check_out_date = request.form.get('check_out_date')
        check_out_time = request.form.get('check_out_time')
        room_number = request.form.get('room_number')
        guest_id = session.get('id')

        # Check for None values and handle them
        if None in {check_in_date, check_in_time, check_out_date, check_out_time}:
            flash("Please provide both date and time for check-in and check-out.", 'danger')
            return redirect(url_for('make_reservation'))

        # Combine date and time strings into datetime objects
        try:
            check_in = datetime.strptime(f"{check_in_date} {check_in_time}", "%Y-%m-%d %H:%M")
            check_out = datetime.strptime(f"{check_out_date} {check_out_time}", "%Y-%m-%d %H:%M")
        except ValueError:
            flash("Invalid date or time format.", 'danger')
            return redirect(url_for('make_reservation'))

        try:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute(
                    "SELECT * FROM reservations WHERE room_number = %s AND ((check_in <= %s AND check_out >= %s) OR (check_in <= %s AND check_out >= %s) OR (check_in >= %s AND check_out <= %s))",
                    (room_number, check_in, check_in, check_out, check_out, check_in, check_out))
                conflicting_reservation = cursor.fetchone()

                if conflicting_reservation:
                    message = "Room and dates already reserved."
                    flash(message, 'danger')
                else:
                    cursor.execute(
                        "INSERT INTO reservations (room_number, check_in, check_in_time, check_out, check_out_time, guest_id) VALUES (%s, %s, %s, %s, %s, %s)",
                        (room_number, check_in.date(), check_in.time(), check_out.date(), check_out.time(), guest_id))
                    connection.commit()
                    flash("Reservation successfully made!", 'success')
                    return redirect(url_for('success'))

        except Error as e:
            print(f"Database Error: {e}")
            connection.rollback()
            message = "Error making reservation."
            flash(message, 'danger')

    if not conflicting_reservation:
        try:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM rooms")
                rooms = cursor.fetchall()
        except Error as e:
            print(f"Database Error: {e}")
            rooms = None
            message = "Error fetching room list."
            flash(message, 'danger')

    return render_template('make_reservation.html', message=message, selected_room=selected_room, rooms=rooms)

@app.route('/success')
def success():
    return render_template('success.html')
@app.route('/manage_reservation')
def manage_reservation():
    if 'loggedin' in session:
        try:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM reservations")
                reservations = cursor.fetchall()

            return render_template('manage_reservation.html', reservations=reservations)
        except Error as e:
            print(f"Database Error: {e}")
            return render_template('error.html', message="Error fetching reservations.")
    else:
        return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return render_template('index.html')




from flask import Flask, render_template, request, redirect, url_for, flash, session

# Your other imports...

@app.route('/person')
def person():
    if 'id' in session:
        sid = session['id']
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM accounts WHERE id = %s", (sid,))
        person_info = cursor.fetchone()
        cursor.close()
        return render_template('person.html', data=person_info)
    else:
        flash('You need to log in first.', 'danger')
        return redirect(url_for('login'))

from flask import Flask, render_template, request, session, redirect, url_for, flash
import mysql.connector


@app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        pid = session['id']
        # Use get method with a default value to safely retrieve form field values
        fullname = request.form.get('fullname', '')
        username = request.form.get('username', '')
        email = request.form.get('email', '')
        address = request.form.get('address', '')
        contact = request.form.get('contact', '')

        # Store the update details in the session for confirmation
        session['update_data'] = {
            'pid': pid,
            'username': username,
            'email': email,
            'fullname': fullname,
            'address': address,
            'contact': contact
        }

        # Render the confirmation page
        return render_template('confirm_update.html', data=session['update_data'])

    return redirect(url_for('home'))

@app.route('/confirm_update', methods=['POST'])
def confirm_update():
    if request.method == 'POST':
        confirmed = request.form.get('confirmed')

        if confirmed and confirmed.lower() == 'true':
            # Get the updated data from the session
            update_data = session.get('update_data', {})

            # Perform the update in the database using the update_data
            cursor.execute(
                "UPDATE accounts SET username=%s, email=%s, fullname=%s, address=%s, contact=%s WHERE id = %s",
                (update_data['username'], update_data['email'], update_data['fullname'],
                 update_data['address'], update_data['contact'], update_data['pid']))
            connection.commit()

            # Clear the update_data from the session
            session.pop('update_data', None)

            flash('Account successfully updated', 'success')
        else:
            flash('Update cancelled', 'info')

    return redirect(url_for('home'))

# ... (other routes and configurations)


@app.route('/home')
def home():
    try:
        # Fetch rooms from the database
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM rooms")
            rooms = cursor.fetchall()

        # Debug: print fetched rooms to the console
        print("Fetched Rooms:", rooms)

        # Render the template
        return render_template('home.html', rooms=rooms, name=session['username'])

    except Exception as e:
        # Debug: print any exception that occurs
        print("Exception:", e)

        # Handle the exception gracefully (customize this based on your needs)
        return render_template('error.html', error_message="An error occurred while fetching data.")


@app.route('/admin_panel')
def admin_panel():
    # Fetch rooms from the database
    cursor.execute("SELECT * FROM rooms")
    rooms = cursor.fetchall()

    # Render the template with room data
    return render_template('admin_panel.html', rooms=rooms)


@app.route('/admin/manage_rooms')
def manage_rooms():
    if 'loggedin' in session and session['role'] == 'admin':
        # Fetch rooms from the database as dictionaries
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM rooms")
        rooms = cursor.fetchall()
        return render_template('manage_rooms.html', rooms=rooms)
    else:
        return redirect(url_for('login'))



@app.route('/admin/manage_users')
def manage_users():
    if 'loggedin' in session and session['role'] == 'admin':
        # Fetch users from the database (replace this with your actual database query)
        cursor.execute("SELECT * FROM accounts")
        users = cursor.fetchall()
        return render_template('manage_users.html', users=users)
    else:
        return redirect(url_for('login'))




from flask import jsonify

@app.route('/admin/add_room', methods=['GET', 'POST'])
def add_room():
    if 'loggedin' in session and session['role'] == 'admin':
        if request.method == 'POST':
            room_number = request.form['room_number']
            room_name = request.form['room_name']
            room_type = request.form['room_type']
            price = request.form['price']
            is_available = 'is_available' in request.form
            max_persons = request.form.get('max_persons')

            # Check if the post request has the file part
            room_image = request.files['room_image']
            if room_image:
                try:
                    room_image.save('static/images/' + secure_filename(room_image.filename))
                    room_image_filename = room_image.filename
                except Exception as e:
                    print('Error saving image:', e)
                    room_image_filename = None
            else:
                room_image_filename = None

            try:
                cursor.execute(
                    "INSERT INTO rooms (room_number, room_name, room_type, price, is_available, max_persons, room_image_path) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (room_number, room_name, room_type, price, is_available, max_persons, room_image_filename))
                connection.commit()

                # Redirect to the manage_rooms page after adding the room
                flash('Room added successfully!', 'success')
                return redirect(url_for('manage_rooms'))
            except Exception as e:
                # Handle database or other errors
                flash(f'Error adding room: {str(e)}', 'danger')
        else:
            # Handle invalid file type
            flash('Invalid file type for room image. Allowed types: jpg, jpeg, png, gif', 'danger')
    else:
        # Handle no file uploaded
        flash('No file uploaded for room image', 'danger')

    # If the request method is GET, render the add_room form
    return render_template('add_room.html')

    # Redirect to the login page if not logged in as an admin
    return redirect(url_for('login'))




@app.route('/admin/edit_room/<int:room_id>', methods=['GET', 'POST'])
def edit_room(room_id):
    if 'loggedin' in session and session['role'] == 'admin':
        if request.method == 'POST':
            # Retrieve form data for editing a room
            updated_room_number = request.form['room_number']
            updated_room_name = request.form['room_name']
            updated_room_type = request.form['room_type']
            updated_price = request.form['price']
            updated_is_available = request.form['is_available']  # This will be either '1' or '0'

            # Update the room in the database
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE rooms SET room_number=%s, room_name=%s, room_type=%s, price=%s, is_available=%s WHERE id=%s",
                (updated_room_number, updated_room_name, updated_room_type, updated_price, updated_is_available, room_id))
            connection.commit()

            # Redirect to the manage_rooms page after editing the room
            return redirect(url_for('manage_rooms'))

        # If the request method is GET, fetch the existing room details for editing
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM rooms WHERE id=%s", (room_id,))
        room = cursor.fetchone()

        # Render the edit_room form with the existing room details
        return render_template('edit_room.html', room=room)

    # Redirect to the login page if not logged in as an admin
    return redirect(url_for('login'))




@app.route('/admin/delete_room/<int:room_id>')
def delete_room(room_id):
    if 'loggedin' in session and session['role'] == 'admin':
        # Delete the room from the 'rooms' table
        cursor.execute("DELETE FROM rooms WHERE id=%s", (room_id,))
        connection.commit()

        # Redirect to the manage_rooms page after deleting the room
        return redirect(url_for('manage_rooms'))

    # Redirect to the login page if not logged in as an admin
    return redirect(url_for('login'))
    from flask import render_template



if __name__ == '__main__':
    app.run(debug=True)
