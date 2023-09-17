from transformers import AutoTokenizer

prompt = """You are a SQLite expert. Given an input question, first create a syntactically correct SQLite query to run, then look at the results of the query and return the answer to the input question.
Unless the user specifies in the question a specific number of examples to obtain, query for at most 3 results using the LIMIT clause as per SQLite. You can order the results to return the most informative data in the database.
Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in double quotes (") to denote them as delimited identifiers.
Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
Pay attention to use date('now') function to get the current date, if the question involves "today".

Use the following format:

Question: Question here
SQLQuery: SQL Query to run
SQLResult: Result of the SQLQuery
Answer: Final answer here

Only use the following tables:

CREATE TABLE fact_retention_model (
        fathercodename TEXT, 
        raisetype TEXT, 
        product_type_bi TEXT, 
        agencyname_adj TEXT, 
        custtype TEXT, 
        tougu_flag TEXT, 
        business_module TEXT, 
        cdate TEXT, 
        invest_manager TEXT, 
        parentareaname TEXT, 
        salescenter TEXT, 
        retail_brokername TEXT, 
        provname TEXT, 
        "CITYNAME" TEXT, 
        relaname TEXT, 
        age INTEGER, 
        port_code TEXT, 
        fathercode TEXT, 
        fundname TEXT, 
        shares REAL, 
        asset REAL, 
        asset_fof REAL
)

/*
2 rows from fact_retention_model table:
fathercodename  raisetype       product_type_bi agencyname_adj  custtype        tougu_flag      business_module cdate   invest_manager  parentareaname  salescenter  retail_brokername        provname        CITYNAME        relaname        age     port_code       fathercode      fundname        shares  asset   asset_fof
新蓝筹  公募基金        混合偏债        招商银行        机构    0       券商    2022-06-30      袁维德  华东区  深圳营销中心    卢肇昱  浙江    郑州    幸福人寿保险股份有限公司      45      150071  001117  中欧远见两年定期开放混合A       2566.31 2136.0388068    3562.294911
阿尔法  一对一专户      权益类  光大证券        机构    1       券商    2022-12-30      袁维德  北方区  其他    段家庆  陕西    锦州    幸福人寿保险股份有限公司     60       013221  001117  中欧增强回报债券（LOF）A        2566.31 2137.3769466    3560.064678
*/

Some examples of SQL queries response that correspond to human inquiry are listed below:
Example inquiry: 查询上月末产品类型为投顾类基金保有规模和人数
Corresponding response: select product_type_bi,sum(asset),count(distinct syscustomerid) from fdm.fact_retention_model where cdate=(select max(cdate) from fdm.fact_retention_model where islastwkday_month='是') and product_type_bi='投顾类' and is_settlement='未清盘' group by product_type_bi;

Example inquiry: 查询上季末基金类型为混合型保有规模和人数
Corresponding response: select propertys,sum(asset),count(distinct syscustomerid) from fdm.fact_retention_model where cdate=(select max(cdate) from fdm.fact_retention_model where islastwkday_quarter='是') and propertys='混合型' and is_settlement='未清盘' group by propertys;

Relevant pieces of previous conversation:

(You do not need to use these pieces of information if not relevant)

Question: 查询上月末产品类型为投顾类基金保有规模和人数
SQLQuery:
"""

tokenizer = AutoTokenizer.from_pretrained("defog/sqlcoder")

inputs = tokenizer(prompt)
print(f"[*] Word split of prompt {len(prompt.split(' '))}")
print(f"[*] Max input length: {tokenizer.max_model_input_sizes}")
print(f"[*] Token length: {len(inputs.tokens())}")
