from flask import Flask, render_template, request, redirect, url_for, session, flash
from index import BlockChain
import json

app = Flask(__name__)
app.secret_key = "alkdjfalkdjf"
fake_product_analyzer = FakeProductAnalyzer()
blockchain_manager = BlockchainManager()

@app.route("/")
def index():
		return render_template('index.html')

@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        session["user_type"] = request.form["user_type"]
        
        if user_type == "manufacturer" or user_type == "supplier":
            return redirect(url_for('manufacturer_supplier_login'))
        elif user_type == "customer":
            return redirect(url_for('search_product'))
    
    session["user"] = ""
    session["user_type"] = ""
    return render_template('index.html')

@app.route("/login", methods=["POST", "GET"])
def login():
	if request.method == "POST":
		user = request.form["username"]
		pswd = request.form["password"]

		if user == "Admin":
			if pswd == "password":
				session["user"] = "Admin"
				return redirect(url_for("admin"))
		
		elif user == "manu":
			if pswd == "password":
				session["user"] = "manu"
				return redirect(url_for("shoes"))
		
		else:
			flash("Invalid Login details")
			return redirect(url_for('login'))
	else:
		return render_template('login.html')


@app.route("/verify/<product_id>", methods=["GET"])
def verify(product_id):
		return render_template('verify.html', keyId=product_id)


@app.route("/verify", methods=["POST"])
def success():

	post_data = request.form["keyId"]

	with open('./NODES/N1/blockchain.json', 'r') as bfile:
		n1_data = str(bfile.read())
	with open('./NODES/N2/blockchain.json', 'r') as bfile:
		n2_data = str(bfile.read())
	with open('./NODES/N3/blockchain.json', 'r') as bfile:
		n3_data = str(bfile.read())
	with open('./NODES/N4/blockchain.json', 'r') as bfile:
		n4_data = str(bfile.read())

	pd = str(post_data)

	if (pd in n1_data) and (pd in n2_data) and (pd in n3_data) and (pd in n4_data):

		with open('./NODES/N1/blockchain.json', 'r') as bfile:
			for x in bfile:
				if pd in x:
					a = json.loads(x)["data"]
					b = a.replace("'", "\"")
					data = json.loads(b)

					product_brand = data["Manufacturer"]
					product_name = data["ProductName"]
					product_batch = data["ProductBatch"]
					manuf_date = data["ProductManufacturedDate"]
					expiry_date = data["ProductExpiryDate"]
					product_id = data["ProductId"]
					product_price = data["ProductPrice"]
					product_size = data["ProductSize"]
					product_type = data["ProductType"]
		
		return render_template('success.html', brand=product_brand, name=product_name, batch=product_batch, manfdate=manuf_date, exprydate=expiry_date, id=product_id, price=product_price, size=product_size, type=product_type)
	
	else:
		return render_template('fraud.html')


@app.route("/addproduct", methods=["POST", "GET"])
def addproduct():
	if request.method == "POST":
    session["product_details"] = {
      "brand": request.form["brand"],
		"name": request.form["name"],
		"batch": request.form["batch"],
		"pid": request.form["id"],
		"manfdate": request.form["manfdate"],
		"exprydate": request.form["exprydate"],
		"price": request.form["price"],
		"size": request.form["size"],
		"ptype": request.form["type"],
    }
    
		return redirect(url_for('confirm'))
	else:
		# return render_template('home.html')
		return redirect(url_for('home'))

@app.route("/confirm", methods=["GET", "POST"])
def confirm():
    product_details = session.get("product_details")
    print(product_details)
    if request.method == "POST":
        if product_details:
            blockchain_manager.add(product_details)
            session.pop("product_details", None)  # Clear product_details from the session
            return redirect(url_for('added'))
    
    return render_template('confirm.html', product_details=product_details)
	

@app.route("/admin")
def admin():
	if session["user"] == "Admin":
		return render_template('admin.html')
	else:
		return redirect(url_for('login'))

@app.route("/added")
def added():
	return render_template('added.html')

@app.route("/verifyNodes")
def verifyNodes():
	bc = BlockChain()
	isBV = bc.isBlockchainValid()

	if isBV:
		flash("All Nodes of Blockchain are valid")
		return redirect(url_for('admin'))
	else:
		flash("Blockchain Nodes are not valid")
		return redirect(url_for('admin'))

@app.route("/search_product", methods=["GET", "POST"])
def search_product():
    if request.method == "POST":
        product_details = {
            "brand": request.form["brand"],
            "name": request.form["name"],
             "price": request.form["price"],
        }

        # Analyze product with ML
        is_fake = fake_product_analyzer.analyze_product(product_details)

        # Verify product with blockchain
        product_id = request.form["product_id"]  # Assuming there's a field for product ID
        is_valid = blockchain_manager.verify_product(product_id)
        
        session["search_result"] = { "product_details": product_details, "is_fake_ml": is_fake_ml, "is_on_blockchain": is_on_blockchain }

        return redirect(url_for('search_result'))

    return render_template('search_product.html')

@app.route("/search_result")
def search_result():
    if request.method == "POST":
        search_result = session.pop("search_result", None)
        return redirect(url_for('search_product'))
    
    return render_template('search_result.html', search_result=search_result)

@app.route("/medicine")
def medicine():
	return render_template('MedicinePage.html')


@app.route("/fertilizer")
def fertilizer():
	return render_template('FertilizersPage.html')


@app.route("/shoes")
def shoes():
	return render_template('ShoesPage.html')


@app.route("/wine")
def wine():
	return render_template('WinePage.html')


@app.route("/logout")
def logout():
	session["user"] = ""
   session["user_type"] = ""
	return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
    session["user"] = ""