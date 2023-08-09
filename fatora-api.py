from flask import Flask, redirect, url_for , render_template , jsonify, request , send_file
import os
import uuid
from flask_restx import Api,Resource,namespace,fields,reqparse

#print(uuid.uuid4())

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

api = Api(app, version='1.0', title='fatora api',
    description='api to help you use fatora',
    #prefix='/DOCS'
)

ns = api.namespace('todos', description='TODO operations')
todo = api.model('Todo', {
    'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'task': fields.String(required=True, description='The task details')

})


@api.route('/hello/<string:id>')
class HelloWorld(Resource):
    def get(self):
        return 'hello'

post_model = api.model('PostModel', {
    'phone': fields.String(required=True, description='The phone number'),
    'file': fields.String(required=True, description='The file name or path'),
    'invoice_location': fields.String(required=True, description='The location of the invoice')

})

# Sample data store for demonstration purposes (replace this with a database in a real application)
posts = []
@api.route('/add')
class PostListResource(Resource):
    @api.expect(post_model, validate=True)  # Validate and expect the input payload
    def post(self):
        # Access the payload data using 'api.payload'
        phone = api.payload['phone']
        file = api.payload['file']
        invoice_location = api.payload['invoice_location']

        # Save the new post to the data store (again, this is just for demonstration purposes)
        new_post = {'phone': phone, 'file': file, 'invoice_location': invoice_location}
        posts.append(new_post)

        #return {'message': 'Data posted successfully', 'data': new_post}, 200
        return jsonify({'result':'Success','phone':phone,'file':file,'invoice_location':invoice_location})

invoices = [
    {'id': 1,'phone_number': '0541894366','date':'2023/09/21', 'inv_num': 'INV001', 'time': '12:23', 'name': 'بنده','description':'مواد غذائية','price':'23'},
    {'id': 2,'phone_number': '0547091521','date':'2023/09/21', 'inv_num': 'INV002', 'time': '11:10', 'name': 'امازون','description':'اجهزة منزلية','price':'403'},
    {'id': 3,'phone_number': '0543648741','date':'2023/09/21', 'inv_num': 'INV003', 'time': '07:12', 'name': 'ساسكو','description':'محطة','price':'110'}
]

@app.route('/show')
def home():
    return jsonify(invoices)
@app.route('/invoice/<int:invoice_id>')
def get_invoice(invoice_id):
    for invoice in invoices:
        if invoice['id'] == invoice_id:
            return jsonify(invoice)
    return jsonify({'error': 'Invoice not found'})

@app.route('/invoice/phone/<phone_number>')
def get_invoices_by_phone(phone_number):
    matching_invoices = [invoice for invoice in invoices if invoice['phone_number'] == phone_number]
    if matching_invoices:
        return jsonify(matching_invoices)
    return jsonify({'error': 'No invoices found for the phone number'})

@app.route("/")
def second():
    return render_template("api_doc.html")

# @app.route("/<nigga>")
# def first(nigga):
#     return render_template("index.html", content=nigga)




@app.route("/s/<name>")
def user(name):
    return f"hello {name}!"

@app.route("/admin")
def admin():
    return redirect(url_for("home",name="Admin!")) #when he direct he will replace name def with Admin!


@app.route("/add", methods=["POST"])
def add():
    data = request.get_json()
    phone = data['phone']
    file = data['file']
    invoice_location = data['invoice_location'] #id of the resturant or caftteria or any

    #print(jsonify({'result':'Success','phone':phone,'file':file,'invoice_location':invoice_location}))
    return jsonify({'result':'Success','phone':phone,'file':file,'invoice_location':invoice_location})

@app.route('/uploads/<filename>', methods=['GET'])
def serve_uploaded_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.isfile(file_path):
        return send_file(file_path)
    else:
        return jsonify({'message': 'File not found'}), 404

@app.route("/upload",methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'you need to attached the invoice'}) ,400
    file = request.files['file']

    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) #file name only
    return jsonify({'message': 'File uploaded successfully'}), 200


@app.route("/server")
def server():
    return "hllo world"



if __name__ == "__main__":
    app.run( port=8000)
