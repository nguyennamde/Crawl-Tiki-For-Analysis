from psycopg2 import Error
from pymongo import MongoClient
import psycopg2
from sqlalchemy import create_engine, text
import pandas as pd
import re

try:
    engine = create_engine("postgresql+psycopg2://postgres:123@localhost:5432/tiki_crawl")
    print("Connect to Database successfully")

except Error as e:
    print(e)

client = MongoClient("mongodb://localhost:27017/")
db_mongo = client.tiki_crawl
collection = db_mongo.product_tiki

def extract():
    data_product = {
    'product_id' : [],
    'sku' : [],
    'name_product' : [],
    'url_product' : [],
    'description' : [],
    'price' : [],
    'original_price' : [],
    'discount_rate' : [],
    'rating_average' : [],
    'review_count' : [],
    'inventory_status' : [],
    'day_ago_created' : [],
    'quantity_sold' : [],
    'category' : [],
    'brand' : [],
    'seller_id' : [],
}
    data_seller = {
        'seller_id' : [],
        'sku' : [],
        'name_seller' : [],
        'url_seller' : [],
        'is_best_store' : []
    }
    count = 0
    for document in collection.find({}, projection={"_id" : 0}):
        try:
            product_id = document["id"]
            sku = document['sku']
            name_product = document['name']
            url_product = document['short_url']
            description = document['description']
            price = document['price']
            original_price = document['original_price']
            discount_rate = document['discount_rate']
            rating_average = document['rating_average']
            review_count = document['review_count']
            inventory_status = document['inventory_status']
            day_ago_created = document['day_ago_created']
            quantity_sold = document['quantity_sold']['value']
            category = document['categories']['name']
            brand = document['brand']["name"]
            seller_id = document['current_seller']['id']
        except Exception as e:
            count += 1
            print(f"Skip product_id: {document['id']}")
        else:
            data_product['product_id'].append(product_id)
            data_product['sku'].append(sku)
            data_product['name_product'].append(name_product)
            data_product['url_product'].append(url_product)
            data_product['description'].append(description)
            data_product['price'].append(price)
            data_product['original_price'].append(original_price)
            data_product['discount_rate'].append(discount_rate)
            data_product['rating_average'].append(rating_average)
            data_product['review_count'].append(review_count)
            data_product['inventory_status'].append(inventory_status)
            data_product['day_ago_created'].append(day_ago_created)
            data_product['quantity_sold'].append(quantity_sold)
            data_product['category'].append(category)
            data_product['brand'].append(brand)
            data_product['seller_id'].append(seller_id)
        try:
            seller_id = document['current_seller']['id']
            sku_seller = document['current_seller']['sku']
            name_seller = document['current_seller']['name']
            url_seller = document['current_seller']['link']
            is_best_store = document['current_seller']['is_best_store']
        except Exception as e:
            pass
        else:
            if seller_id not in data_seller["seller_id"]:
                data_seller['seller_id'].append(seller_id)
                data_seller['sku'].append(sku_seller)
                data_seller['name_seller'].append(name_seller)
                data_seller['url_seller'].append(url_seller)
                data_seller['is_best_store'].append(is_best_store)
    df_product = pd.DataFrame(data_product)
    df_seller = pd.DataFrame(data_seller)
    print(f"The Number of skipped products is {count}")
    return df_product, df_seller

def transform_product(df_product):
    df_product.drop_duplicates("product_id", inplace=True)
    df_product.discount_rate = df_product.discount_rate / 100
    df_product.description = df_product.description.apply(lambda x: " ".join(re.sub("<.*?>|\n","", x).split()))
    return df_product


def create_table_postgres():
    global engine
    with engine.connect() as conn:
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS product_tiki (
            product_id int PRIMARY KEY,
            sku TEXT,
            name_product TEXT,
            url_product TEXT,
            description TEXT,
            price FLOAT,
            original_price FLOAT,
            discount_rate FLOAT,
            rating_average FLOAT,
            review_count INT,
            inventory_status VARCHAR(20),
            day_ago_created INT,
            quantity_sold INT,
            category VARCHAR(100),
            seller_id INT,
            brand VARCHAR(100)
        )
    """))
        
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS seller_tiki (
                seller_id int PRIMARY KEY,
                sku TEXT,
                name_seller TEXT,
                url_seller TEXT,
                is_best_store bool
                )
        """))

        conn.commit()

def load_to_psql(df_product, df_seller):
    df_product.to_sql("product_tiki", engine, if_exists="append", index=False)
    df_seller.to_sql("seller_tiki", engine, if_exists="append", index=False)

if __name__ == "__main__":
    print("Extracting data...")
    df_product, df_seller = extract()
    print("Transform data...")
    df_transformed_product = transform_product(df_product)
    print("Creataing table in postgreSQL...")
    create_table_postgres()
    print("Loading data to warehouse")
    load_to_psql(df_product, df_seller)
    print("*"*100)
    print("ETL process Finish!!!")
    print("*"*100)














