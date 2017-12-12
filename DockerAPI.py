import json
import os
import requests

from flask import Flask, Response, request, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return "Welcome to docker CRUID"


@app.route('/listallcontainers')
def listallContainers():
    request.args.get('')
    # print '@@@@@@@@@@@@@@@@'+type(requests.get('http://0.0.0.0:2375/containers/json?all=1').content)
    return Response(requests.get('http://0.0.0.0:2375/containers/json?all=1'), mimetype='application/json')


@app.route('/listcontainers')
def listcontainers():
    return Response(requests.get('http://0.0.0.0:2375/containers/json?all=0'), mimetype='application/json')


@app.route('/showimages')
def showimages():
    response = requests.get('http://0.0.0.0:2375/images/json').content
    images = json.loads(response)
    # return jsonify(images)
    return render_template('showimages.html', images=images)


@app.route('/createcontainer')
def createcontainer():
    op = os.popen(' docker -H tcp://0.0.0.0:2375 run 20c44cd7596ff4807aef84273c99588d22749e2a7e15a7545ac96347baa65eda')
    return op


if __name__ == '__main__':
    app.run()
