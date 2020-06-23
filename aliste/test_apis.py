from aliste import APP
import unittest
import json

class FlaskTest(unittest.TestCase):
	info_post = {
		    "date": "2020-4-1",
		    "class": "1-A",
		    "attendance": {
		        "1": {
		            "status": "P",
		            "remarks": "Nothing"
		        },
		        "2": {
		            "status": "A",
		            "remarks": "Nothing"
		        },
		        "3": {
		            "status": "P",
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

	info_update = {
		    "date": "2020-6-15",
		    "class": "1-A",
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
		        }
		    }
		}

	def test_get_students_message(self):
		tester = APP.test_client(self)
		response = tester.get('/get-students?class=3-A')
		loads = json.loads(response.data)
		# print(loads)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.content_type, 'application/json')
		self.assertEqual(str.encode(loads['status']), b'Success')

	def test_get_attendance_message(self):
		tester = APP.test_client(self)
		response = tester.get('/get-attendance?class=1-A&date=2020-6-15')
		loads = json.loads(response.data)
		print(loads)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.content_type, 'application/json')
		self.assertEqual(str.encode(loads['status']), b'Success')

	def test_post_attendance(self):
		tester = APP.test_client(self)		
		response = tester.post('/post-attendance', data=json.dumps(self.info_post), headers={'Content-Type': 'application/json'})		
		loads = json.loads(response.data)
		print(loads)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(str.encode(loads['status']), b'Success')

	def test_update_attendance(self):
		tester = APP.test_client(self)
		response = tester.post('/update-attendance', data=json.dumps(self.info_update), headers={'Content-Type': 'application/json'})
		loads = json.loads(response.data)
		print(loads)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(str.encode(loads['status']), b'Success')



if __name__ == "__main__":
	unittest.main(verbosity=2)
