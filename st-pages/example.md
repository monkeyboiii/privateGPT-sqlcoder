# Example

## Q1 记忆功能

-   上月末北方区下基金经理华李成的各基金产品的保有规模是多少
    > 语料库中已有语句验证 ✅

```sql
select fathercodename,sum(asset) from fact_retention_model where invest_manager='华李成' and cdate=(select max(cdate) from fact_retention_model where islastwkday_month='是') group by fathercodename;
```

-   那么基金经理袁维德的呢
    > chatbot 记忆功能验证 ✅

```sql
select fathercodename,sum(asset) from fact_retention_model where invest_manager='袁维德' and cdate=(select max(cdate) from fact_retention_model where islastwkday_month='是') group by fathercodename;
```

-   那么上年末基金经理洪慧梅的呢

    > chatbot 记忆功能和变式验证 ✅

    > islastwkday_month ➡️ islastwkday_year

```sql
select fathercodename,sum(asset) from fact_retention_model where invest_manager='洪慧梅' and cdate=(select max(cdate) from fact_retention_model where islastwkday_year='是') group by fathercodename;
```

## Q2 变式

-   上月末银行业务模块各个渠道的货币型基金产品的保有规模分别是多少

    > 语料库中语句【**变式 1**】验证 ✅

    > 权益性 ➡️ 货币型

```sql
-- fathercodename -> business_module
select business_module,sum(asset) from fact_retention_model where product_type_bi='货币型' and business_module='银行' and cdate=(select max(cdate) from fact_retention_model where islastwkday_month='是') group by agencyname;
```

-   查询上年末上海最新保有规模和人数

    > 语料库中语句【**变式 2**】验证 ✅

    > 浙江 ➡️ 上海

```sql
select province,sum(asset),count(distinct customer_id) from fact_retention_model where cdate=(select max(cdate) from fact_retention_model where islastwkday_year='是') and province='上海' and is_settlement='未清盘' group by province;
```

## Q3 简单新问题，排序

-   查询浙江，河北，陕西，福建，吉林最新保有规模和人数，并且按照人数从高到低排序
    > 语料库外语句验证 ✅

```sql
SELECT province, sum(asset) AS total_asset, count(*) AS total_number FROM fact_retention_model WHERE province in ('浙江省', '河北省', '陕西省', '福建省', '吉林省') GROUP BY province ORDER BY total_number desc;
```

---

-   上月末各业务模块权益类基金产品的保有规模和客户数分别是多少
    > 语料库中已有语句验证 ✅

```sql
select business_module,sum(asset),count(distinct customer_id) from fact_retention_model where product_type_bi='权益类' and cdate=(select max(cdate) from fact_retention_model where islastwkday_month='是') group by business_module;
```

-   上个月末保有客户数最多的是哪一种业务模块，并且列出保有客户数

    > 语法错误 ❌

    > order by 后不能跟 count

```sql
select business_module,count(distinct customer_id) from fact_retention_model where cdate=(select max(cdate) from fact_retention_model where islastwkday_month='是') group by business_module order by count(distinct customer_id) desc limit 1;
```

-   上一个返回语句，把保有客户数命名为 c_count 后再进行排序
    > 提示纠正后正确 ✅

```sql
select business_module,count(distinct customer_id) as c_count from fact_retention_model where cdate=(select max(cdate) from fact_retention_model where islastwkday_month='是') group by business_module order by c_count desc;
```

## Q4

-   返回结果

```shell
RETURN_DIRECT=True
```
