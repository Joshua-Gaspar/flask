from flask import Flask,  request, render_template, redirect, url_for, make_response
import os
from werkzeug.utils import secure_filename
import time

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Get IP address of client
@app.route("/getIp")
def get_my_ip():
    time.sleep(5)

    myResponse = make_response({'ip': request.remote_addr})
    myResponse.headers['Access-Control-Allow-Origin'] = '*'
    myResponse.headers['customHeader'] = 'This is a custom header'
    myResponse.status_code = 200
    myResponse.mimetype = 'text/plain'

    return myResponse
    # return jsonify({'ip': request.remote_addr}), 200

#Get home page HTML
@app.route('/')
def home():
    myResponse = make_response(render_template('index3.html'))
    myResponse.headers['customHeader'] = 'This is a custom header'
    myResponse.status_code = 200
    myResponse.mimetype = 'text/html'

    return myResponse


@app.route('/upload', methods=['POST'])
def upload_file():
    #simple delay to test multi-threading
    time.sleep(10)
    file = request.files['file']

    if file.filename == '':
        myResponse = make_response({'message': 'There is no file'})
        myResponse.headers['customHeader'] = 'This is a custom header'
        myResponse.status_code = 400
        myResponse.mimetype = 'text/plain'

        return myResponse

    else:
        #Pass it a filename and it will return a secure version of it.
        #This filename can then safely be stored on a regular file system
       filename = secure_filename(file.filename)

       #save file in a particular directory
       file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

       myResponse = make_response({'message': 'Files successfully uploaded'})
       myResponse.headers['customHeader'] = 'This is a custom header'
       myResponse.status_code = 201

       return myResponse

#Search a image and display it
@app.route('/<filename>')
def display_image(filename):
    check = os.path.exists(UPLOAD_FOLDER + '/'+ filename)
    
    if check:
        return redirect(url_for('static', filename='uploads/' + filename), code=302)
    else:
        myResponse = make_response({'message': '404 Page Not Found'})
        myResponse.headers['customHeader'] = 'This is a custom header'
        myResponse.status_code = 404
        myResponse.mimetype = 'text/plain'

        return myResponse


@app.route('/allImages')
def get_all_image():
  imageList = os.listdir(UPLOAD_FOLDER)
  imagelist = ['uploads/' + image for image in imageList]

  return render_template("index3.html", imagelist=imagelist)


if __name__ == "__main__":
    # This work externally on the same network
    app.run(host='0.0.0.0', port=5000, Thread = True)
