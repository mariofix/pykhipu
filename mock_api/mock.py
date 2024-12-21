from flask import Flask, request, jsonify, request_finished

app = Flask(__name__)
app.debug = False


@app.route("/", defaults={"path": ""}, methods=["GET", "POST"])
@app.route("/<path:path>", methods=["GET", "POST"])
def catch_all(path):
    print(f"{path = }")
    return jsonify({"path": path})


@app.get("/v1/banks")
@app.get("/v3/banks")
def banks():
    banks = {
        "banks": [
            {
                "bank_id": "SDdGj",
                "name": "Banco Estado",
                "message": "Tarifa de $300 de transferencia a otros bancos, usando CuentaRUT.",
                "min_amount": 1000,
                "type": "Persona",
                "parent": "",
                "logo_url": "https://s3.amazonaws.com/static.khipu.com/logos/bancos/chile/estado-icon.png",
            },
            {
                "bank_id": "SDdGa",
                "name": "Banco Santander",
                "message": "",
                "min_amount": 1,
                "type": "Persona",
                "parent": "",
                "logo_url": "https://s3.amazonaws.com/static.khipu.com/logos/bancos/chile/santander-icon.png",
            },
        ]
    }
    print(f"{banks =}")
    return jsonify(banks)


@app.get("/v1/predict")
@app.get("/v3/predict")
def predict():
    prediction = {
        "result": "ok",
        "max_amount": 5000000,
        "cool_down_date": "2024-06-21T11:23:09.123Z",
        "new_destinatary_max_amount": 100000,
    }

    print(f"{prediction = }")
    return jsonify(prediction)


def log_data(sender, response, **extra):
    print("--------------------")
    print(f"{request.host = }")
    print(f"{request.host_url = }")
    print(f"{request.base_url = }")
    print(f"{request.full_path = }")
    print("--------------------")
    print(f"{request.content_encoding = }")
    print(f"{request.content_length = }")
    print(f"{request.content_type = }")
    print(f"{request.is_json = }")
    print(f"{request.origin = }")
    print(f"{request.method = }")
    print("--------------------")
    print(f"{request.args = }")
    print(f"{request.cookies = }")
    print(f"{request.data = }")
    print(f"{request.form = }")
    # if request.is_json:
    #     print(f"{request.json() = }")
    print(f"{request.query_string = }")
    print(f"{request.headers = }")
    print("--------------------")
    print(f"{sender = }")
    print(f"{response = }")
    print(f"{extra = }")


request_finished.connect(log_data, app)
