from flask import Flask, request, jsonify

app = Flask(__name__)

product_records = [
    {"product_id": "1", "product_name": "Hasbro Gaming Clue Game", 
     "description": "One murder... 6 suspects...", "price": 9.95, "active": True},
    {"product_id": "2", "product_name": "Monopoly Board Game The Classic Edition, "
    "2-8 players", "description": "Relive the Monopoly experiences...",
      "price": 35.50, "active": False}
]

# to create a new product
@app.route("/product", methods=["POST"])
def create_product():
    new_product = request.json
    product_records.append(new_product)
    return jsonify({"message": "Product added successfully!", 
                    "product": new_product}), 201

# to get all the products
@app.route("/products", methods=["GET"])
def get_products():
    return jsonify(product_records)

# to get all the active products
@app.route("/product/active", methods=["GET"])
def get_active_products():
    active_products = [product for product in product_records if product.get("active")]
    return jsonify(active_products)

# to get a product by ID number
@app.route("/products/<product_id>", methods=["GET"])
def get_product(product_id):
    product = next((p for p in product_records if p["product_id"] == product_id), None)
    return jsonify(product) if product else jsonify({"error": "Product not found"}), 404

# to update product details
@app.route("/product/<product_id>", methods=["PUT", "PATCH"])
def update_product(product_id):
    updated_data = request.json
    product = next((p for p in product_records if p["product_id"] == product_id), None)
    if product:
        product.update(updated_data)
        return jsonify(product)
    return jsonify({"error": "Product not found"}), 404

# to toggle the product activity status
@app.route("/product/activity/<product_id>", methods=["PATCH"])
def toggle_activity(product_id):
    product = next((p for p in product_records if p["product_id"] == product_id), None)
    if product:
        product["active"] = not product["active"]
        return jsonify(product)
    return jsonify({"error": "Product not found"}), 404

# to delete a product
@app.route("/product/delete/<product_id>", methods=["DELETE"])
def delete_product(product_id):
    global product_records
    product_records = [p for p in product_records if p["product_id"] != product_id]
    return jsonify({"message": "Product deleted successfully!"})

if __name__ == "__main__":
    app.run(debug=True)
