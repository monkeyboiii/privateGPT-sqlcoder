import os
from dotenv import load_dotenv
from chromadb.config import Settings

load_dotenv()

# Define the folder for storing database
PERSIST_DIRECTORY = os.environ.get('PERSIST_DIRECTORY', "vectorstore/")
if PERSIST_DIRECTORY is None:
    raise Exception("Please set the PERSIST_DIRECTORY environment variable")

# Define the Chroma settings
CHROMA_SETTINGS = Settings(
    persist_directory=PERSIST_DIRECTORY,
    anonymized_telemetry=False
)

# prompt for SQLCoder
PROMPT_DICT = {
    "": """### Instruction:
Your task is find the most relevant example documents given the question `{question}`
""",

    "prompt":  """### Instructions:
Your task is convert a question into a SQL query, given a MYSQL database schema.
Adhere to these rules:
- **Deliberately go through the question and database schema word by word** to appropriately answer the question.
- **Use Table Aliases** to prevent ambiguity. For example, `SELECT table1.col1, table2.col1 FROM table1 JOIN table2 ON table1.id = table2.id`.
- When creating a ratio, always cast the numerator as float
- Input can contain example query given the question. In the format `Question: Give me col1 of table1;
Query: SELECT table1.col1 FROM table1`.

### Input:
Generate a SQL query that answers the question `{question}`.
This query will run on a database whose schema is represented in this string:
{context}

### Response:
Based on your instructions, here is the SQL query I have generated to answer the question `{question}`:
```sql
""",

    "example": {
        "context": """
CREATE TABLE products (
  product_id INTEGER PRIMARY KEY, -- Unique ID for each product
  name VARCHAR(50), -- Name of the product
  price DECIMAL(10,2), -- Price of each unit of the product
  quantity INTEGER  -- Current quantity in stock
);

CREATE TABLE customers (
   customer_id INTEGER PRIMARY KEY, -- Unique ID for each customer
   name VARCHAR(50), -- Name of the customer
   address VARCHAR(100) -- Mailing address of the customer
);

CREATE TABLE salespeople (
  salesperson_id INTEGER PRIMARY KEY, -- Unique ID for each salesperson
  name VARCHAR(50), -- Name of the salesperson
  region VARCHAR(50) -- Geographic sales region
);

CREATE TABLE sales (
  sale_id INTEGER PRIMARY KEY, -- Unique ID for each sale
  product_id INTEGER, -- ID of product sold
  customer_id INTEGER,  -- ID of customer who made purchase
  salesperson_id INTEGER, -- ID of salesperson who made the sale
  sale_date DATE, -- Date the sale occurred
  quantity INTEGER -- Quantity of product sold
);

CREATE TABLE product_suppliers (
  supplier_id INTEGER PRIMARY KEY, -- Unique ID for each supplier
  product_id INTEGER, -- Product ID supplied
  supply_price DECIMAL(10,2) -- Unit price charged by supplier
);

-- sales.product_id can be joined with products.product_id
-- sales.customer_id can be joined with customers.customer_id
-- sales.salesperson_id can be joined with salespeople.salesperson_id
-- product_suppliers.product_id can be joined with products.product_id
''''''
CREATE TABLE products (
  product_id INTEGER PRIMARY KEY, -- Unique ID for each product
  name VARCHAR(50), -- Name of the product
  price DECIMAL(10,2), -- Price of each unit of the product
  quantity INTEGER  -- Current quantity in stock
);

CREATE TABLE customers (
   customer_id INTEGER PRIMARY KEY, -- Unique ID for each customer
   name VARCHAR(50), -- Name of the customer
   address VARCHAR(100) -- Mailing address of the customer
);

CREATE TABLE salespeople (
  salesperson_id INTEGER PRIMARY KEY, -- Unique ID for each salesperson
  name VARCHAR(50), -- Name of the salesperson
  region VARCHAR(50) -- Geographic sales region
);

CREATE TABLE sales (
  sale_id INTEGER PRIMARY KEY, -- Unique ID for each sale
  product_id INTEGER, -- ID of product sold
  customer_id INTEGER,  -- ID of customer who made purchase
  salesperson_id INTEGER, -- ID of salesperson who made the sale
  sale_date DATE, -- Date the sale occurred
  quantity INTEGER -- Quantity of product sold
);

CREATE TABLE product_suppliers (
  supplier_id INTEGER PRIMARY KEY, -- Unique ID for each supplier
  product_id INTEGER, -- Product ID supplied
  supply_price DECIMAL(10,2) -- Unit price charged by supplier
);

-- sales.product_id can be joined with products.product_id
-- sales.customer_id can be joined with customers.customer_id
-- sales.salesperson_id can be joined with salespeople.salesperson_id
-- product_suppliers.product_id can be joined with products.product_id
""",
        "query": "What products has the biggest fall in sales in 2022 compared to 2021? Give me the product name, the sales amount in both years, and the difference."
    },
    "retention": {
        "context": """
CREATE TABLE fact_retention_model {
  fathercodename VARCHAR(50), -- Name of the main fund, 主基金名称
  raisetype VARCHAR(50), -- Type of issurance or raise, 发行类别
  product_type_bi VARCHAR(50), -- Type of product , 产品类型
  agencyname_adj VARCHAR(50), -- Name of agency, 销售渠道
  custtype VARCHAR(50), -- Type of customer, 客户类型
  tougu_flag TINYINT(1), -- If has tougu, 是否投顾
  business_module VARCHAR(50), -- Business module, 业务模块
  cdate DATETIME, -- Date of confirmation, 确认日
  invest_manager VARCHAR(50), -- Name of fund invest manager, 基金经理
  parentareaname VARCHAR(50), -- Name of parent area, 大区
  salescenter VARCHAR(50), -- Name of sales center 营销中心
  retail_brokername VARCHAR(50), -- Name of retail broker, 客户经理
  provname VARCHAR(50), -- Name of province, 省
  CITYNAME VARCHAR(50), -- Name of city, 市
  relaname VARCHAR(50), -- Name of real client, 事实客户
  age INT, -- Age, 年龄
  port_code VARCHAR(10) PRIMARY KEY, -- Code of fund, 基金代码
  fathercode VARCHAR(10), -- Code of main fund, 主基金代码
  fundname VARCHAR(10), -- Name of fund 基金名称
  shares FLOAT, -- Latest shares, 最新份额
  asset FLOAT, -- Latest size of fund, 最新规模
  asset_fof FLOAT -- Latest size of fund of fund(fof), 最新规模FOF双算
}

the example value of each field can be as listed:
fathercodename['中欧盛世', '新蓝筹', '时代先锋', '新常态', '潜力价值', '阿尔法', '时代先锋', '创新成长'],
raisetype['公募基金', '一对一专户', '投顾'],
product_type_bi['混合偏债', '债券类', '权益类', '货币类'],
agencyname_adj['南京证券', '光大证券', '招商银行', '中信证券', '工商银行', '浦发银行'],
custtype['机构', '个人'],
tougu_flag['0', '1'],
business_module['机构一部', '银行', '券商'],
cdate['2022-12-30', '2022-06-30'],
invest_manager['袁维德', '蓝小康', '洪慧梅', '刘金辉', '许文星'],
parentareaname['南方区', '北方区', '华东区'],
salescenter['江南营销中心', '华北营销中心', '西北营销中心', '东北营销中心', '深圳营销中心', '其他'],
retail_brokername['王鹏', '卢肇昱', '冯文欣', '吕霖', '段家庆'],
provname['湖南', '辽宁', '江苏', '河北', '陕西', '天津', '浙江'],
CITYNAME['天津', '无锡', '郑州', '聊城', '兰州', '莆田', '锦州', '重庆', '厦门'],
relaname['南京证券股份有限公司（非经纪业务）', '幸福人寿保险股份有限公司', '广发证券股份有限公司（非经纪业务）', '泰康资产管理有限责任公司'],
age[43, 45, 51, 59, 101, 60, 33],
port_code['005242', '013221', '166005', '150071', '166023'],
fathercode['001117', '001980', '578183', '166020', '166007'],
fundname['中欧创新成长灵活配置混合型证券投资基金A', '中欧增强回报债券（LOF）A', '中欧消费主题股票型证券投资基金A', '中欧远见两年定期开放混合A'],
shares[10002.334, 2566.31, 1026.524, 1539.786, 2789.145, 0],
asset[1424.9179644, 2137.3769466, 3560.064678, 1424.0258712, 2136.0388068],
asset_fof[3562.294911, 1424.9179644, 2137.3769466, 3560.064678, 1424.0258712]
"""
    }

}
