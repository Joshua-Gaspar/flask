from flask import Flask,  request, render_template, redirect, url_for, make_response
import os
from werkzeug.utils import secure_filename
import time

# Initialize the Flask application
app = Flask(__name__)

#Path directory for images
UPLOAD_FOLDER = './static/uploads/'

#Get home page HTML and show it in the browser 
@app.route('/',methods=['GET'])
def home():
  #returns a list containing the names of the entries in the directory given by path
  imageListName = os.listdir(UPLOAD_FOLDER)
  print(imageListName)
  
  #Array containing directory of every single images
  imagelist = ['uploads/' + image for image in imageListName]

  myResponse = make_response(render_template("index3.html", imageList=imagelist))
  myResponse.status_code = 200
  myResponse.headers['customHeader'] = 'This is a custom header'
  myResponse.mimetype = 'text/html'
  
  return myResponse

#Get IP address and PORT of client
@app.route("/getIp", methods=['GET'])
def get_my_ip():
    
    #simple delay to test multi-threading
    time.sleep(5)

    myResponse = make_response({'ip': request.environ['REMOTE_ADDR'],
                                'port':request.environ.get('REMOTE_PORT')})
    myResponse.headers['customHeader'] = 'This is a custom header'
    myResponse.status_code = 200
    myResponse.mimetype = 'text/plain'

    return myResponse

#Upload the image then save it to a to a folder
@app.route('/upload', methods=['POST'])
def upload_file():

    
    file = request.files['file-img']

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
       file.save(os.path.join(UPLOAD_FOLDER, filename))

       myResponse = make_response({'message': 'Files successfully uploaded'})
       myResponse.headers['customHeader'] = 'This is a custom header'
       myResponse.status_code = 201

       return myResponse

#Search the requested image and display it on the browser
@app.route('/<filename>', methods=['GET'])
def display_image(filename):
    
    #check whether the requestes file exist in the server
    check = os.path.exists(UPLOAD_FOLDER + filename)
    
    #If the file exist in the server, redirect the client to the image location
    if check:
        myResponse = redirect(url_for('static', filename='uploads/' + filename))
        myResponse.headers['customHeader'] = 'This is a custom header'
        myResponse.status_code = 302
        myResponse.mimetype = 'image/jpeg'
        
        return myResponse
    
    #Return a 404 response if the file doesnt exist 
    else:
        myResponse = make_response({'message': '404 Page Not Found'})
        myResponse.headers['customHeader'] = 'This is a custom header'
        myResponse.status_code = 404
        myResponse.mimetype = 'text/plain'

        return myResponse




if __name__ == "__main__":
    # start flask app
    
    # When the host is set to 0.0.0.0 it tell the flask framework to use the machine private ip address (to be able to use it externally and the port is set to 5000)
    
    #Additionally the framework is multithread by default and use the TCP connection
    app.run(host='0.0.0.0', port=5000)
