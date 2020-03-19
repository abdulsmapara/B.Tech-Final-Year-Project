from flask import Flask, render_template, request, session
from werkzeug import secure_filename
import os
from utils import get_facts, label_sentences, deleteDir
import traceback
import shutil

app = Flask(__name__)
app.secret_key = "password"

@app.route("/facts", methods=["GET"])
def fetch_facts(message=None, warning=None, error=None):
	session['identity'] = request.remote_addr
	app.config['UPLOAD_FOLDER'] = "uploads/" + session['identity']
	try:
		os.makedirs(app.config['UPLOAD_FOLDER'])
	except FileExistsError:
		deleteDir(app.config['UPLOAD_FOLDER'])
		os.makedirs(app.config['UPLOAD_FOLDER'])
	return render_template('facts.html')

@app.route("/upload",methods=["POST"])
def upload():
	import keras.backend.tensorflow_backend as tb
	tb._SYMBOLIC_SCOPE.value = True

	if request.method == 'POST':
		try:
			files = request.files.getlist('reports[]')
			filenames = []
			for f in files:
				filename = secure_filename(f.filename)
				filenames.append(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			timestamped_facts = get_facts(files=filenames, num=len(filenames))
			final_list = []
			for date, facts in timestamped_facts.items():
				year, month, d = date.split("-")
				mnt = "January"
				if int(month) == 2:
					mnt = "February"
				elif int(month) == 3:
					mnt = "March"
				elif int(month) == 4:
					mnt = "April"
				elif int(month) == 5:
					mnt = "May"
				elif int(month) == 6:
					mnt = "June"
				elif int(month) == 7:
					mnt = "July"
				elif int(month) == 8:
					mnt = "August"
				elif int(month) == 9:
					mnt = "September"
				elif int(month) == 10:
					mnt = "October"
				elif int(month) == 11:
					mnt = "November"
				else:
					mnt = "December"
				cp_facts = facts
				results = label_sentences(cp_facts)
				pos = []
				neg = []
				for result in results:
					if result[1] == "POS":
						pos.append(result[0])
					else:
						neg.append(result[0])
				final_list.append( ((year,mnt,d, month),pos,neg))
			final_list = sorted(final_list,key=lambda x: (int(x[0][0]), int(x[0][3]),int(x[0][2])))
			return render_template("display_facts.html",display_data1=enumerate(final_list), display_data2=final_list)

		except Exception as e:
			traceback.print_exc()
			return str(e)

if __name__ == "__main__":
	app.run(debug=True)
