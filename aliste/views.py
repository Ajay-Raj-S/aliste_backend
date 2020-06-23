from aliste import APP
from flask_mysqldb import MySQL
from aliste import local_settings as ls
import uuid
import datetime
from hashlib import sha256
import json
import re
import html
from flask import request

# Database Constants
APP.config['MYSQL_HOST'] = ls.MYSQL_DATABASE_HOST_local
APP.config['MYSQL_USER'] = ls.MYSQL_DATABASE_USER_local
APP.config['MYSQL_PASSWORD'] = ls.MYSQL_DATABASE_PASSWORD_local
APP.config['MYSQL_DB'] = ls.MYSQL_DATABASE_DB_local
APP.config['MYSQL_PORT'] = ls.MYSQL_DATABASE_PORT_local

mysql = MySQL(APP)


def hash_me(password):
    h = sha256()
    h.update(password)
    hashed_pass = h.hexdigest()
    return hashed_pass


def create_user(admin):
    insert_stat = "insert into users (user_id, emp_fname, emp_lname, emp_dob, emp_username, emp_password, emp_isadmin, emp_isdeleted, emp_createdon) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    user_id = uuid.uuid4().hex
    emp_fname = "Brave"
    emp_lname = "Stone"
    emp_dob = datetime.date(1970, 1, 1)
    emp_username = "brave_stone"
    emp_password = hash_me(b'PlainPassword')
    emp_isadmin = 'y' if admin else 'n'
    emp_isdeleted = 'n'
    emp_createdon = datetime.date.today()
    data = (user_id, emp_fname, emp_lname, emp_dob, emp_username,
            emp_password, emp_isadmin, emp_isdeleted, emp_createdon)

    cur = mysql.connection.cursor()
    cur.execute(insert_stat, data)
    mysql.connection.commit()
    cur.close()


def toDate(dateString):
    try:
        return datetime.datetime.strptime(dateString, "%Y-%m-%d").date()
    except ValueError:
        return "Invalid Date Format"


def get_students_by_class(classname):
    cur = mysql.connection.cursor()
    cur.execute("select student_id from students where class=%s;", (classname,))
    students_list = list()
    for x in cur:
        students_list.append(str(x[0]))

    return students_list


def get_posted_attendance(dt):
    cur = mysql.connection.cursor()
    cur.execute("select attendance_date from student_attendance_map where attendance_date = %s", (dt,))
    posted = False
    for x in cur:
        posted = True
        break
    return posted


def insert_students():
    insert_stat = "insert into students (student_fname, student_lname, gender, class, dob, parents_phoneno) values (%s, %s, %s, %s, %s, %s)"
    stud_fnames = ['Dimple', 'Raja', 'Venkat', 'Nivetha', 'Tony']
    stud_lnames = ['Kumari', 'kannan', 'Kumar', 'K', 'Tiwari']
    stud_gender = ['F', 'M', 'M', 'F', 'M']
    stud_class = "3-B"
    stud_dob = datetime.date(1998, 1, 1)
    parents_num = ["7382239397", "8123459123",
                   "9979258884", "7296990956", "9753469384"]
    cur = mysql.connection.cursor()
    for i in range(5):
        data = (stud_fnames[i], stud_lnames[i], stud_gender[i],
                stud_class, stud_dob, parents_num[i])
        cur.execute(insert_stat, data)
        print(str(i) + " added")

    mysql.connection.commit()
    cur.close()


def check_if_posted_already(date):
    cur = mysql.connection.cursor()
    cur.execute("select id from student_attendance_map where attendance_date=%s;", (date,))
    posted = False
    for x in cur:
        posted = True
        break

    return posted    


@APP.route('/')
def home():
    post_data = {
        "date": "2020-6-30",
        "classname": "1-A",
        "attendance": {
            "1": {
                "status": "P",
                "remarks": "Nothing"
            },
            "2": {
                "status": "P",
                "remarks": "Nothing"
            },
            "3": {
                "status": "A",
                "remarks": "Nothing"
            },
            "4": {
                "status": "P",
                "remarks": "Nothing"
            },
            "5": {
                "status": "P",
                "remarks": "Nothing"
            }
            
        }
    }
    update_data = {
        "date": "2020-6-30",
        "classname": "1-A",
        "attendance": {
            "1": {
                "status": "P",
                "remarks": "Nothing"
            },
            "2": {
                "status": "P",
                "remarks": "Nothing"
            }            
        }
    }
    get_students = {
        "/get-students": {
           "example": "127.0.0.1/get-students"
        }
    }
    get_attendance = {
        "/get-attendance": {
            "example": "127.0.0.1/get-attendance?class=1-A&date=2020-6-1"
        }
    }
    post_attendance = {
        "/post-attendance": {
            "help": "Only accepts POST request, use postman, or something",
            "exmaple": "127.0.0.1/post-attendance",
            "data-format": post_data,
        }
    }
    update_attendance = {
        "/update-attendance": {
            "help": "Only accepts POST request, use postman, or something",
            "exmaple": "127.0.0.1/update-attendance",
            "data-format": update_data,
        }
    }
    return_json = {
        "APIs": [
            get_students, 
            get_attendance,
            post_attendance, 
            update_attendance,   
        ],
        "home": "You are home, try these APIs",
    }
    return return_json


@APP.route('/get-students', methods=['GET'])
def get_students():
    cur = mysql.connection.cursor()

    return_json = dict()
    class_name = request.args.get('class', '')
    if class_name != '':
        class_name = html.escape(class_name)
        proper_class = re.search(r"^\d{0,2}[\-]\w+$", class_name)
        if proper_class is not None:
            cur.execute("select * from students where class=%s;",
                        (class_name,))
            count = 0
            for x in cur:
                count += 1
                break

            if count > 0:
                students_dict = dict()
                for x in cur:
                    students_dict[x[0]] = {"id": x[0], "Name": x[1] + " " + x[2], "Gender": x[3], "Class": x[4],
                                           "DOB": x[5], "Parent_Name": x[7], "Parent_phonenumber": x[6], "Admission_No.": x[8]}

                return_json = {"status": "Success", "students": students_dict}
            else:
                return_json = {"error": "No such class in the school."}
        else:
            return_json = {"error": "Invalid ClassName"}
    else:
        return_json = {"error": "No Class is Provided"}

    return return_json


@APP.route('/get-attendance', methods=["GET"])
def get_attendance():
    class_name = request.args.get('class', '')
    date = request.args.get('date', default=datetime.date.today(), type=toDate)
    
    return_json = dict()

    class_name = html.escape(class_name)
    proper_class = re.search(r"^\d{0,2}[\-]\w+$", class_name)
    if isinstance(date, str) or proper_class is None:
        return_json = {"status": "Failed", "error": "Invalid Date format or class name, try using like YYYY-MM-DD for the date and 3-B for the Class Name"}
    else:
        cur = mysql.connection.cursor()

        select_stat = """
            SELECT * FROM student_attendance_map 
            WHERE attendance_date = %s AND student_id IN (SELECT student_id FROM students WHERE class=%s);"""

        cur.execute(select_stat, (date, class_name))

        count = 0
        for x in cur:        
            count += 1
            break

        if count > 0:
            students_dict = dict()
            for x in cur:
                students_dict[x[0]] = {"Attendance_Date": x[1], "Status": x[2], "Remarks": x[3], "Student_Id": x[4], "Class_Name": class_name}

            return_json = {"status": "Success", "students": students_dict}
        else:
            return_json = {"status": "Failed", "error": "Invalid date or class name"}

    return return_json


@APP.route('/post-attendance', methods=["POST"])
def post_attendance():
    if request.method == 'POST':
        json_value = request.get_json()
        if json_value is not None:
            class_name = html.escape(json_value['class'])
            proper_class = re.search(r"^\d{0,2}[\-]\w+$", class_name)

            date = json_value['date']
            date = toDate(date)

            if isinstance(date, str) or proper_class is None or len(json_value['attendance']) < 1:
                return {"status":"Failed","error": "Invalid Data format"}
            else:
                # check if posting attendance for any future dates
                if datetime.date.today() >= date:
                    cur = mysql.connection.cursor()
                    insert_stat = "INSERT INTO student_attendance_map (attendance_date, status, remarks, student_id) VALUES (%s, %s, %s, %s)"

                    if check_if_posted_already(date):
                        return {"status": "Failed", "message": "Attendance posted already, go update if any."}

                    # get all the students of the class
                    students_list = get_students_by_class(class_name)
                    students_list.sort(key=int)
                    # converting from list to set, to remove duplicates
                    user_provided_list = set(list(json_value['attendance'].keys()))

                    # check if duplicates exists
                    if len(user_provided_list) != len(json_value['attendance']):
                        return {"status":"Failed","message": "Duplicate student attendances are present"}

                    # back to list from set and sort
                    user_provided_list = list(user_provided_list)
                    user_provided_list.sort(key=int)
                    
                    # check if the user is posting for all the students in a class
                    if students_list != user_provided_list:
                        return {"status":"Failed","message": "Should Post attendance for all the students"}
                    
                    for _id, values in json_value['attendance'].items():
                        data = (date, values['status'], values['remarks'], _id)
                        cur.execute(insert_stat, data)

                    mysql.connection.commit()
                    cur.close()
                    return {"status": "Success", "message": "Attendance posted successfully!"}

                else:
                    return {"status":"Failed", "message": "Cannot post attendance after today."}
        else:
            return {"status":"Failed", "message": "No values present in the json"}
    else:
        return {"status":"Failed", "message": "Needed POST request"}


@APP.route('/update-attendance', methods=["POST"])
def update_attendance():
    if request.method == 'POST':
        json_value = request.get_json()

        # checks if json is present
        if json_value is not None:
            proper_class = re.search(r"^\d{0,2}[\-]\w+$", json_value.get('class', ''))

            date = json_value['date']
            date = toDate(date)

            # checks for empty or invalid data sent
            if isinstance(date, str) or proper_class is None or len(json_value['attendance']) < 1:
                return {"status": "Failed", "message": "Invalid Data format or Nothing to Update."}
            else:
                return_json = dict()
                # check if attendance is already posted before updating
                if get_posted_attendance(date):
                    cur = mysql.connection.cursor()
                    update_stat = "UPDATE student_attendance_map SET status = %s,remarks = %s WHERE attendance_date = %s AND student_id = %s"

                    class_students_list = get_students_by_class(json_value.get('class'))

                    for _id, values in json_value['attendance'].items():
                        # checks if the student is in the class
                        if _id in class_students_list:
                            if values.get('status', '') != '':
                                data = (values['status'], values.get('remarks', ''), date, _id)
                                cur.execute(update_stat, data)
                            else:
                                return_json[_id] = "Either status or remarks is missing."
                                return_json["status"] = "Failed"
                        else:
                            return_json[_id] = "No such student in the class " + str(json_value.get('class'))
                            return_json["status"] = "Failed"

                    mysql.connection.commit()
                    cur.close()
                    return_json["message"] = "Attendance Updated successfully!"
                    return_json["status"] = "Success"
                    return return_json
                else:
                    return_json["message"] = "Attendance is not Posted Yet!"
                    return_json["status"] = "Failed"
                    return return_json
        else:
            return {"status":"Failed", "message": "No values present in the json"}
    else:
        return {"status":"Failed", "error": "Needed POST request"}
