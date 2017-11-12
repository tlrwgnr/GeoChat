import MySQLdb
from flask import Flask
from flask import jsonify
import json
from flask import request

app = Flask(__name__)

def query(query, isUpdate=False):
	db = MySQLdb.connect(host="hackitaldb.ce1doaue7cqd.us-east-1.rds.amazonaws.com", user="hackathon", passwd="thetatau", db="innodb")
	cur = db.cursor()
	cur.execute(query)

	if (isUpdate):
		db.commit()
		returnValues = None
	else:
		returnValues = cur.fetchall()

	db.close()
	return returnValues


#returnResults = []
#results = query("select niche_code, if(now()>niche_next_post_time, 1, 0) as is_due, niche_post_url, niche_post_url_image from niche where is_active = 1")

#for result in results:
#	returnResults.append((result[0], result[1], result[2], result[3]));

#return returnResults

#@app.route('/createEntry', methods=["POST", "GET"])
#def createEntry():
#	query("INSERT INTO entry (`entry_text`, `group_id`, `created_user`) VALUES ('" + request.form["test"] + "', 1, 1);", True)

@app.route('/allentrys', methods=["POST", "GET"])
def entries():
	returnResults = []
	results = query("select u.user_name, e.entry_text from entry e left join user u on (e.created_user = u.user_id)")
	for result in results:
		returnResults.append((result[0], result[1]))

	return jsonify({"results": returnResults})

@app.route('/allgroups', methods=["POST", "GET"])
def groups():
	returnResults = []
	results = query("select * from group")
	for result in results:
		returnResults.append(("Chris", result[1]))

	return jsonify(results)

# get the feed for a particular user (only groups the user wants to see posts about)
@app.route('/userentrys', methods=["POST", "GET"])
def feedByUser():
	if (request.method == 'POST'):
		user_id = request.form["user_id"]
	else:
		user_id = 1

	returnResults = []
	results = query("SELECT u.user_name, e.entry_text FROM entry e left join user u on (e.created_user = u.user_id) where group_id in (select group_id from user_group where user_id = " + str(user_id) + ");")
	for result in results:
		returnResults.append(("Chris", result[1]))

	return jsonify(results)

# get the feed for a particular group
@app.route('/groupentrys', methods=["POST", "GET"])
def feedByGroup():
	returnResults = []
	results = query("SELECT * FROM entry where group_id = 1;")
	for result in results:
		returnResults.append(("Chris", result[1]))

	return jsonify(results)

@app.route('/test', methods=['POST'])
def test():
	return jsonify("TYLER RULEZ")
