import json
import os
import requests

from flask import Flask, Response, request, render_template, jsonify

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('form.html')

#list all containers including inactive containers -- return json
@app.route('/listallcontainers')
def listallContainers():
    request.args.get('')
    return Response(requests.get('http://0.0.0.0:2375/containers/json?all=1'), mimetype='application/json')

#list all active containers ---- return json
@app.route('/listcontainers')
def listcontainers():
    return Response(requests.get('http://0.0.0.0:2375/containers/json?all=0'), mimetype='application/json')


#Config docker ip
@app.route('/getip',methods=['POST','GET'])
def getip():
    if(request.method=='POST'):
        ip=request.form['ip']
        return 'Docker daemon ip updated'
    return 'Get method not allowed'

#list all images
@app.route('/showimages')
def showimages():
    response = requests.get('http://0.0.0.0:2375/images/json').content
    images = json.loads(response)
    return jsonify(images)

    # return render_template('showimages.html', images=images)

#create container using shell --needs image id as input
# @app.route('/createcontainer')
# def createcontainer():
#     return render_template('formgetimage.html')


@app.route('/createcontainer',methods=['POST','GET'])
def createcontainer():
    if request.method=='POST':
        # id=request.form['id']
        id = request.get_data()
        l = id.split(':')
        id = l[1]
        op = os.popen(' docker -H tcp://0.0.0.0:2375 run -d '+id).read()
        return 'container created '+op+' for image '+id

    return 'Failed to create container'+' for image '+id

#kill container --needs container id from request body
@app.route('/killcontainer',methods=['POST','GET'])
def killcontainer():
    if request.method == 'POST':
        id=request.get_data()
        l=id.split(':')
        id=l[1]
        op = os.popen(' docker -H tcp://0.0.0.0:2375 kill ' + id).read()
        return 'container killed ' + op
    return 'failed to kill container'

    # return render_template('killcontainer.html')

# @app.route('/killcontainer1',methods=['POST','GET'])
# def killcontainer1():
#     if request.method=='POST':
#         id=request.form['id']
#
#         op = os.popen(' docker -H tcp://0.0.0.0:2375 kill '+id).read()
#         return 'container killed '+' docker -H tcp://0.0.0.0:2375 kill '+id
#
#     return 'Failed to kill container '+id

if __name__ == '__main__':
    app.run()
