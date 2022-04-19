#app.py
from flask import Flask,  request, jsonify,render_template,redirect,url_for
import os
from werkzeug.utils import secure_filename
import time 
 
app = Flask(__name__)
 
app.secret_key = "caircocoders-ednalan"
 
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
 
#Get IP address of client
@app.route("/getIp")
def get_my_ip():
    time.sleep(10)
    return jsonify({'ip': request.remote_addr}), 200

#Get home page HTML
@app.route('/')
def home():
   return render_template('index3.html')

@app.route('/upload', methods = ['POST'])
def upload_file():
    #simple delay to test multi-threading
      time.sleep(10)
      file = request.files['file']
      
      if file.filename == '':
        resp = jsonify({'message' : 'There is no file'})
        # resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.status_code = 400
        return resp		
    
      else:
        #Pass it a filename and it will return a secure version of it. 
        #This filename can then safely be stored on a regular file system
       filename = secure_filename(file.filename)
       
       #save file in a particular directory
       file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
       
       resp = jsonify({'message' : 'Files successfully uploaded'})
    #    resp.headers['Access-Control-Allow-Origin'] = '*'
       resp.status_code = 201
       
       return resp	
    	
#Search a image and display it
@app.route('/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    
    return redirect(url_for('static', filename='uploads/' + filename), code=302)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True) #This work externally on the same network
