# Crawling Data From E-commerce Page And Build ETL Pipeline to Warehouse For Analysis

### In this project i will get roughtly 50.000 products from e-commerce page(Tiki) store in the MongoDB, then, build ETL Pipeline to migrate data to PostgreSQL for analysis

The reason i choose Tiki to crawl data for this project is because it provide available API for crawling, This reduces the time when I collect data

Nowadays, almost all e-commerce websites use Javascript and css to render their websites, This make me difficult to crawl data from their website

But, To my knowledges, There are two ways to crawl such frustrating websites.

- First, if you crawl data by scrapy, you can use splash to render file html

- Second, you can use selenium to handle this problem

I have tried using selenium with scrapy to crawl data from Shopee but this way is very slow, roughly 20-30 products/minute

So i have chosen tiki to crawl data.

### Problems when crawling

I have used Scrapy to crawl API from tiki, Because, Scrapy has some great and useful features and it is also pretty easy to understand how this tool works since it is user-friendly.
Besides, it works great with proxies and usually doesn’t have any issues while doing the required tasks. So for those that are not a web crawling, Scrapy is a very common choice.


When crawling api from tiki i have trouble in website have blocked bot crawl, so i have faked user-agent to avoid forbidden

I also have trouble in recaptcha, For this problems, i have changed user-agent randomly for each request, this help me avoid being blocked IP, 
but if you crawl many in short time or too many pages, then changing user-agent is not enought to big website, 
it can detect you throught other parameters in headers, so you have to change all in headers and IP address.

When changing user-agent for each request i'm still in recaptcha, so i have rotated IP throught proxy, i have tried library scrapy-rotating-proxies, But using a free IP address has too many users, leading to the spider being overloaded. so i have tried proxy api, But it requires a fee to use, if not you only do 1000 or 5000 requests depends on api proxy provider

After, i try to change DOWNLOAD_DELAY(It specifies the time (in seconds) to wait between consecutive requests to the same domain) in settings of spider into 0.5s, The purpose of adding delays between requests is to be more considerate of the target website's server and avoid overloading it with too many requests in a short amount of time. This can help you avoid getting banned or IP-blocked by the website.

### Idea to crawl data

I will take 26 categories:
- Đồ Chơi - Mẹ & Bé
- Điện Thoại - Máy Tính Bảng
- NGON
- Làm Đẹp - Sức Khỏe
- Điện Gia Dụng
- Thời trang nữ
- Thời trang nam
- Giày - Dép nữ
- Túi thời trang nữ
- Giày - Dép nam
- Túi thời trang nam
- Balo và Vali
- Phụ kiện thời trang
- Đồng hồ và Trang sức
- Laptop - Máy Vi Tính - Linh kiện
- Nhà Cửa - Đời Sống
- Cross Border - Hàng Quốc Tế
- Bách Hóa Online
- Thiết Bị Số - Phụ Kiện Số
- Voucher - Dịch vụ
- Ô Tô - Xe Máy - Xe Đạp
- Nhà Sách Tiki
- Điện Tử - Điện Lạnh
- Thể Thao - Dã Ngoại
- Máy Ảnh - Máy Quay Phim
- Sản phẩm Tài chính - Bảo hiểm

Each category i see having 50 pages and each pages have roughly 40 products, so total product that i crawl is roughly 52.000 products

#### Data Flow Diagram

![image](https://github.com/nguyennamde/Crawl-Tiki-For-Analysis/blob/main/assess/data%20flow%20diagram.png)

#### Detailed code walkthrough

first I get the categories_id with a regular expression quickly, then I iterate through each category_id, with each category_id will have 50 pages, so i have iterate throught 50pages
with each category_id and page i send request to get all product_id in one page through api that tiki provides

After getting all product_id in one page of category, then i wil get all API of each product and save to MongoDB, Because the data sent back is in json format, it is very suitable to save the entire api to MongoDB.

![image](https://github.com/nguyennamde/Crawl-Tiki-For-Analysis/blob/main/assess/parse.png)
![image](https://github.com/nguyennamde/Crawl-Tiki-For-Analysis/blob/main/assess/parse_page.png)
![image](https://github.com/nguyennamde/Crawl-Tiki-For-Analysis/blob/main/assess/parse_product.png)

Save api to Mongodb

![image](https://github.com/nguyennamde/Crawl-Tiki-For-Analysis/blob/main/assess/Save_to_mongodb.png)

### ETL pipeline to migrate data from Mongodb to postgresSQL

#### Extract
![image](https://github.com/nguyennamde/Crawl-Tiki-For-Analysis/blob/main/assess/extract-1.png)
![image](https://github.com/nguyennamde/Crawl-Tiki-For-Analysis/blob/main/assess/extract-2.png)
![image](https://github.com/nguyennamde/Crawl-Tiki-For-Analysis/blob/main/assess/extract-3.png)
#### Transform
![image](https://github.com/nguyennamde/Crawl-Tiki-For-Analysis/blob/main/assess/transform-product.png)
#### Load

![image](https://github.com/nguyennamde/Crawl-Tiki-For-Analysis/blob/main/assess/load_to_psql.png)

### Using superset connect to warehouse to visualize data

#### 1. Top 10 danh mục có số lượng sản phẩm bán ra nhiều nhất
![image](https://github.com/nguyennamde/Crawl-Tiki-For-Analysis/blob/main/assess/cau1.jpg)

#### 2. Tạo Biểu đồ tròn để thể hiện tỷ lệ các sản phẩm có sẵn (inventory_status) so với sản phẩm hết hàng.
![image](https://github.com/nguyennamde/Crawl-Tiki-For-Analysis/blob/main/assess/cau2.jpg)
#### 3. Thống kê 5 brand có lượt bán nhiều nhất
![image](https://github.com/nguyennamde/Crawl-Tiki-For-Analysis/blob/main/assess/cau3.jpg)
#### 4. Tổng số sản phẩm bán ra
![image](https://github.com/nguyennamde/Crawl-Tiki-For-Analysis/blob/main/assess/cau%204.jpg)
#### 5. Số lượng seller
![image](https://github.com/nguyennamde/Crawl-Tiki-For-Analysis/blob/main/assess/cau5.jpg)
#### 6. Vẽ biểu đồ Phân phối rating
![image](https://github.com/nguyennamde/Crawl-Tiki-For-Analysis/blob/main/assess/cau6.jpg)
#### 7. Top 10 seller nhiều sản phẩm nhất trên Tiki, số lượng là bao nhiêu
![image](https://github.com/nguyennamde/Crawl-Tiki-For-Analysis/blob/main/assess/cau%207.jpg)




































