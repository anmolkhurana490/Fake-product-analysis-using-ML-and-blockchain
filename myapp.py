from flask import Flask, render_template, request, redirect, url_for, session, flash
from blockchain_layer.blockchain_layer import Blockchain
import json

app = Flask(__name__)
app.secret_key = "alkdjfalkdjf"
#fake_product_analyzer = FakeProductAnalyzer()
blockchain = Blockchain()


# Load user information from JSON file
with open("users.json", "r") as file:
    users_data = json.load(file)


# Helper function to authenticate users
def authenticate(username, password, user_type):
    for user in users_data["users"]:
        if user["username"] == username and user["password"] == password and user["role"] == user_type:
            return user
    return None


@app.route("/set_user_type/<user_type>")
def set_user_type(user_type):
    session["user_type"] = user_type

    if user_type in ["manufacturer", "supplier", "admin"]:
        return redirect(url_for("login"))
    elif user_type == "customer":
        return redirect(url_for("search_product"))


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/home", methods=["GET", "POST"])
def home():
    if "user" in session:
        if session["user_type"] == "admin":
            return redirect(url_for('admin'))
        elif session["user_type"] == "manufacturer":
            return redirect(url_for('manufacturer'))
        elif session["user_type"] == "supplier":
            return redirect(url_for('supplier'))
        else:
            session["user_type"] = ""
            return redirect(url_for('index'))
    else:
        flash("Please login to access the home page.")
        return redirect(url_for('index'))


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pswd = request.form["password"]

        session["user_auth"] = authenticate(user, pswd, session["user_type"])
        
        if session["user_auth"]:
            if session["user_type"] == "admin":
                return redirect(url_for('admin'))
            elif session["user_type"] == "manufacturer":
                return redirect(url_for('manufacturer'))
            elif session["user_type"] == "supplier":
                return redirect(url_for('supplier'))
            else:
                session["user_type"]=""
                session.pop("user_auth", None)
                return redirect(url_for('index'))
        else:
                flash("Invalid Username or Password")
                return render_template('login.html', error_message="Invalid Username or Password")
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


@app.route("/add_product", methods=["POST", "GET"])
def add_product():
    if request.method == "POST":
        session["product_details"] = {
            "name": request.form["productname"],
            "brand": request.form["brand"],
            "product_id": request.form["productid"],
            "retail_price": request.form["retailprice"],
            "discounted_price": request.form["discountedprice"],
            "unique_id": blockchain.unique_id
        }
        return redirect(url_for('confirm'))
    else:
        return render_template('add_product.html')


@app.route("/confirm", methods=["GET", "POST"])
def confirm():
    product_details = session.get("product_details")
    if request.method == "POST":
        if product_details:
            blockchain.addproduct(product_details, session["user_auth"])
            session.pop("product_details", None)  # Clear product_details from the session
            flash("The Product has been added in the Blockchain")
            return render_template('confirm.html', product_details=product_details, message="The Product has been added in the Blockchain")

    return render_template('confirm.html', product_details=product_details)


@app.route("/admin")
def admin():
	if session["user_type"] == "admin":
		return render_template('add_product.html')
	else:
		return redirect(url_for('home'))

@app.route("/manufacturer")
def manufacturer():
	if session["user_type"] == "manufacturer":
		return render_template('manufacturer.html')
	else:
		return redirect(url_for('home'))

@app.route("/supplier")
def supplier():
	if session["user_type"] == "supplier":
		return render_template('supplier.html')
	else:
		return redirect(url_for('home'))

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
            "name": request.form["productname"],
            "productid": request.form["productid"],
            "uniqueid": request.form["uniqueid"],
            "retailprice": request.form["retailprice"],
            "discountedprice": request.form["discountedprice"],
        }

        # Analyze product with ML
        is_authentic_ml = fake_product_analyzer.analyze_product(product_details)

        # Verify product with blockchain
        product_details = blockchain.getProduct(product_details("uniqueid"))
        is_on_blockchain = blockchain.verifyProduct(product_details("uniqueid"))
        
        if is_on_blockchain and is_authentic_ml:
            isAuthentic = True
        else:
            isAuthentic = False

        session["search_result"] = {
            "product_details": product_details,
            "isAuthentic": isAuthentic
        }

        return redirect(url_for('search_result'))

    return render_template('search_product.html')


@app.route("/search_result")
def search_result():
    search_result = session.get("search_result")
    session.pop("search_result", None)
    return render_template('search_result.html', search_result=search_result)


@app.route("/logout")
def logout():
    session["user"] = ""
    session["user_type"] = ""
    flash("You have been logged out.")
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
    session["user"] = ""