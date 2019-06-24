from flask import Flask, render_template, url_for, request, session, redirect
from pymongo import MongoClient
from flask import jsonify
from bson.objectid import ObjectId
from datetime import datetime

client = MongoClient('mongodb://localhost:27017')#localhost connection

db = client.track_location_db
app = Flask(__name__)

@app.route('/index')
def index():
    if 'username' in session:
        return ( 'You are logged in as name ' + session['username'])

    return render_template (jsonify('index.html'))

@app.route('/location', methods=['POST', 'GET'])
def location_details():
    try:
        if request.method == 'POST':
            data = request.get_json()
            location_details_db = db.location_details
            existing_location = location_details_db.find_one({'mob_no': data['mob_no']})

            if existing_location is None:
                lan = data['lontitude']
                long = data['longitutde']
                location = [lan, long]
                mob_no = data['mob_no']
                location_details_db.insert_one({'mob_no': mob_no, 'location': location})
                session['location'] = location
                return ( 'You are location   ' + str(session['location']))
            else:
                return ('That mobile number already exists!')

    except Exception as e:
        return "loding ......"

@app.route('/user_register', methods=['POST', 'GET'])
def user_register():
    try:
        if request.method == 'POST':
            data = request.get_json()
            user_details_db =db.user_details
            existing_user = user_details_db.find_one({'mob_no' : data['mob_no']})
            existing_user_id=existing_user.get('_id')
            # try:
            if existing_user is None:
                Mob_no = data['mob_no']
                gmail=data['mail_id']
                create_date_user=datetime.utcnow()
                # update_date=data['update_date']
                user_details_db.insert_one({'name' : data['username'], 'mob_no' : Mob_no,'mail_id':gmail,
                                  'create_date':create_date_user })
                session['username'] = data['username']
                new_user_id = str(user_details_db.inserted_id)
                session['new_user_id'] = new_user_id

                # print(jsonify(url_for('index')))
                return redirect(url_for('index'))
            else:
                return jsonify('That mobile number already exists!')

        if request.method == 'GET':
            data = request.get_json()
            user_details_db =db.user_details
            if session.get('new_user_id') == True:
                new_user_id_get = ObjectId(session['new_user_id'])
                print(new_user_id_get)
            else:
                new_user_id_get = ObjectId(data['new_user_id'])
                print(new_user_id_get)

    except Exception as e:
        return "loding ......"



@app.route('/agent_details', methods=['POST', 'GET','DELETE','PUT'])
def agent_details():
    try:
        if request.method == 'POST':
            data = request.get_json()
            # print("data:")
            # print(data)
            agent_details_db = db.agent_details
            # print(agent_details_db)
            existing_user = agent_details_db.find_one({'agency_mob_no': data['agency_mob_no']})

            if existing_user is None:
                agency_user_name = data['agency_user_name']
                agency_company_name = data['agency_company_name']
                agency_mob_no = data['agency_mob_no']
                agency_email_id = data['agency_email_id']
                agency_password = data['agency_password']
                is_admin = data['is_admin']
                create_date = datetime.utcnow()
                # update_date = data['update_date']

                inserted_agent_records=agent_details_db.insert_one({'agency_user_name': agency_user_name,'agency_company_name': agency_company_name,
                                  'agency_mob_no': agency_mob_no,'agency_email_id': agency_email_id,'agency_password':
                                      agency_password, 'is_admin': is_admin,'create_date': create_date})

                # after_registration = agent_details_db.find_one({'agency_mob_no': data['agency_mob_no']})
                agent_id=str(inserted_agent_records.inserted_id)

                session['agency_user_name'] = agency_user_name
                session['agent_id'] = agent_id

                return ( 'You are logged in as name ' + session['agency_user_name'])
            else:
                return ('That mobile number already exists!')


        if request.method == 'DELETE':
            data = request.get_json()
            agent_details_db = db.agent_details
            agent_id_del=ObjectId(session['agent_id'])
            record_del = agent_details_db.delete_one({'_id': agent_id_del})
            # record_del = agent_details_db.delete({'agency_user_name': data['agency_user_name']})
            return "sucessful Deleted"


        if request.method == 'GET':
            data = request.get_json()
            agent_details_db = db.agent_details_db
            if session.get('agent_id') == True:
                agent_id_get = ObjectId(session['agent_id'])
                print(agent_id_get)
            else:
                if data != {}:
                    agent_id_get = ObjectId(data['agent_id'])
                    print(agent_id_get)
            if data != {}:
                agent_records_get = agent_details_db.find_one({'_id': agent_id_get})
            else:
                agent_records_get = agent_details_db.find({'agent_id': str(session['agent_id'])})
            return str(agent_records_get)

        if request.method == 'PUT':
            data = request.get_json()
            agent_details_db = db.agent_details
            agent_id_put = ObjectId(session['agent_id'])
            agent_details_db.update_one({'_id': agent_id_put},
            {
            "$set":
                {'agency_user_name': data['agency_user_name'],'agency_company_name': data['agency_company_name'],
                'agency_mob_no': data['agency_mob_no'],'agency_email_id': data['agency_email_id'],'agency_password':
                data['agency_password'], 'is_admin': data['is_admin'],'update_date': datetime.utcnow()}
                    }
                    )
            return "updated sucessfully"
    except Exception as e:
        return "loding ......"

@app.route('/emp_details', methods=['POST', 'GET','DELETE','PUT'])
def emp_details():
    try:
        if request.method == 'POST':
            data = request.get_json()
            employee_details = db.employee_details
            emp_existing_user = employee_details.find_one({'emp_email_id': data['emp_email_id']})
        # try:
            if emp_existing_user is None:
                emp_user_name = data['emp_user_name']
                emp_company_name = data['emp_company_name']
                emp_mob_no = data['emp_mob_no']
                emp_email_id = data['emp_email_id']
                emp_password = data['emp_password']
                designation = data['designation']
                troll_plaza_name=data['troll_plaza_name']
                is_super_emp=data['is_super_emp']
                agent_id=session['agent_id']
                create_date = datetime.utcnow()
                # update_date = data['update_date']

                inserted_emp_records=employee_details.insert_one({'emp_user_name': emp_user_name,'emp_company_name': emp_company_name,
                                  'emp_mob_no': emp_mob_no,'emp_email_id': emp_email_id,
                                  'emp_password': emp_password, 'designation': designation,
                                  'troll_plaza_name': troll_plaza_name, 'is_super_emp': is_super_emp,
                                  'create_date': create_date,'agent_id':agent_id})
                session['emp_user_name'] = emp_user_name
                emp_inserted_id = str(inserted_emp_records.inserted_id)
                session['emp_inserted_id'] = emp_inserted_id

                return ( 'You are logged in as name ' + session['emp_user_name'])
            else:
                return ('That email id already exists!')

        if request.method == 'PUT':
            data = request.get_json()
            employee_details_put = db.employee_details
            employee_id_put=ObjectId(session['employee_id'])
            employee_details_put.update_one({'_id': employee_id_put},
              {
                  "$set":
                      {'emp_user_name':data['emp_user_name'], 'emp_company_name': data['emp_company_name'],
                       'emp_mob_no': data['emp_mob_no'], 'emp_email_id': data['emp_email_id'],
                       'emp_password': data['emp_password'], 'designation': data['designation'],
                       'troll_plaza_name': data['troll_plaza_name'], 'is_super_emp': data['is_super_emp'],
                       'update_date': datetime.utcnow()}
              }
              )
            return "updated sucessfully"

        if request.method == 'GET':
            data = request.get_json()
            employee_details = db.employee_details
            if session.get('employee_id') == True:
                employee_id=ObjectId(session['employee_id'])
            else:
                if data != {}:
                    employee_id=ObjectId(data['employee_id'])
            # records_get = employee_details.find_one({'_id': employee_id})
            if data!={}:
                records_get = employee_details.find_one({'_id': employee_id})
            else:
                records_get = employee_details.find({'agent_id':str(session['agent_id'])})
            return str(records_get)

        if request.method == 'DELETE':
            data = request.get_json()
            employee_details = db.employee_details
            if session.get('employee_id') == True:
                employee_id_session=ObjectId(session['employee_id'])
                employee_details.delete_one({'_id': employee_id_session})
            else:
                employee_id_parameter=ObjectId(data['employee_id'])
                employee_details.delete_one({'_id': employee_id_parameter})

            # record_get = employee_details.delete_one({'_id': employee_id})
            # record_get = employee_details.delete({'emp_user_name': data['user_name']})
            return "sucessful Deleted"
    except Exception as e:
        return "loding ......"

@app.route('/toll_plaza', methods=['POST', 'GET','DELETE','PUT'])
def toll_plaza_details():
    try:
        if request.method == 'POST':
            data = request.get_json()
            plaza_details_db = db.toll_plaza_details
            existing_plaza = plaza_details_db.find_one({'toll_plaza_name':data['toll_plaza_name']})

            if existing_plaza is None:
                toll_plaza_name = data['toll_plaza_name']
                agent_id_plaza = session['agent_id']
                lantitude = data['lantitude']
                langititude = data['langititude']
                toll_plaza_area = data['toll_plaza_area']
                create_date = datetime.utcnow()
                # update_date = data['update_date']

                inserted_plaza_records=plaza_details_db.insert_one({'toll_plaza_name': toll_plaza_name,'agent_id': agent_id,
                                  'lantitude': lantitude,'langititude': langititude,
                                  'create_date': create_date,'toll_plaza_area':toll_plaza_area})
                toll_plaza_id = str(inserted_plaza_records.inserted_id)

                session['toll_plaza_name'] = toll_plaza_name
                session['toll_plaza_id'] = toll_plaza_id

                return ( 'You are logged in as id ' + session['toll_plaza_id'])
            else:
                return ('This plaza name already exists!')

        if request.method == 'GET':
            data = request.get_json()
            plaza_details_get = db.toll_plaza_details
            if session.get('toll_plaza_id') == True:
                toll_plaza_id_get = ObjectId(session['toll_plaza_id'])
                print(toll_plaza_id_get)
            else:
                if data != {}:
                    toll_plaza_id_get = ObjectId(data['toll_plaza_id'])
                    print(toll_plaza_id_get)
            if data != {}:
                plaza_records_get = plaza_details_get.find_one({'_id': toll_plaza_id_get})
            else:
                plaza_records_get = plaza_details_get.find({'toll_plaza_id': str(session['toll_plaza_id'])})
            return str(plaza_records_get)

        if request.method == 'DELETE':
            data = request.get_json()
            plaza_details_del = db.toll_plaza_details
            toll_plaza_del = ObjectId(session['toll_plaza_id'])
            plaza_record_del = plaza_details_del.delete_one({'_id': toll_plaza_del})
            # record_del = agent_details_db.delete({'agency_user_name': data['agency_user_name']})
            return "sucessful Deleted"

        if request.method == 'PUT':
            data = request.get_json()
            plaza_details_put = db.toll_plaza_details
            toll_plaza_put = ObjectId(session['toll_plaza_id'])
            plaza_details_put.update_one({'_id': toll_plaza_put},
            {
            "$set":
                {'toll_plaza_name': data['toll_plaza_name'],'agent_id': data['agent_id'],
                  'lantitude': data['lantitude'],'langititude': data['langititude'],'create_date':
                     data['create_date'],'toll_plaza_area':data['toll_plaza_area'],
                  'update_date': datetime.utcnow()}
                    }
                    )
            return "updated sucessfully"

    except Exception as e:
        return "loding ......"


@app.route('/agent_login', methods=['POST','GET'])
def agent_login():
    if request.method == 'POST':
        agent_details = db.agent_details
        data = request.get_json()

        login_user_agent = agent_details.find_one({'agency_user_name' : data['user_name'],'agency_password':data['password']})
        agent_id=str(login_user_agent.get('_id'))
        print(agent_id)
        if login_user_agent:

            # print(data['user_name'])
            session['agency_user_name'] = data['user_name']
            session['agent_id']=agent_id
            return ("successfull login")
        else:
            return 'Invalid username/password combination'

@app.route('/employee_login', methods=['POST','GET'])
def employee_login():

    if request.method == 'POST':
        employee_details = db.employee_details
        data = request.get_json()

        login_user_employee = employee_details.find_one({'emp_user_name' : data['user_name'],'emp_password':data['password']})
        employee_id=str(login_user_employee.get('_id'))
        print(employee_id)
        if login_user_employee:

            # print(data['user_name'])
            session['emp_user_name'] = data['user_name']
            session['employee_id']=employee_id
            print("session['employee_id']",session['employee_id'])
            return ("successfull login")
        else:
            return 'Invalid username/password combination'



if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)