from flask import jsonify, request
from src import app
from src.settings import APP_VERSION
from src.trelloTasks import FactoryTask


@app.route("/v1/status", methods=["GET"])
def status():
    response = {
        "message": "Nan/SpaceX Challenge is running",
        "status_code": 200,
        "version": APP_VERSION,
    }
    return jsonify(response)


@app.route("/v1/create-task", methods=["POST"])
def create_task():
    try:
        req_data = request.get_json()
        factory_task = FactoryTask()
        task = factory_task.build_task(data=req_data)
        response = task.create_task()
        return jsonify(response), 200
    except Exception as err:
        response = {"create-task": False, "detail": str(err)}
        return jsonify(response), 400
