# Example

## Q1

-   查询上月末浦发银行下电子信息的最新保有规模和人数
    > 语料库中已有语句验证 ✅

```sql
select agencyname,fathercodename,sum(asset),count(distinct syscustomerid) from fdm.fact_retention_model where cdate=(select max(cdate) from fdm.fact_retention_model where islastwkday_month='是') and agencyname='浦发银行' and fathercodename='电子信息' and is_settlement='未清盘' group by agencyname,fathercodename;
```

-   那么工商银行下的呢？
    > chatbot 记忆功能验证 ✅

```sql
select agencyname,fathercodename,sum(asset),count(distinct syscustomerid) from fdm.fact_retention_model where cdate=(select max(cdate) from fdm.fact_retention_model where islastwkday_month='是') and agencyname='工商银行' and fathercodename='电子信息' and is_settlement='未清盘' group by agencyname,fathercodename;
```

-   那么上年末工商银行下的呢？

    > chatbot 记忆功能和变式验证 ✅

    > islastwkday_month ➡️ islastwkday_year

```sql
select agencyname,fathercodename,sum(asset),count(distinct syscustomerid) from fdm.fact_retention_model where cdate=(select max(cdate) from fdm.fact_retention_model where islastwkday_year='是') and agencyname='招商银行' and fathercodename='电子信息' and is_settlement='未清盘' group by agencyname,fathercodename;
```

## Q2

-   上月末银行业务模块各个渠道的货币型基金产品的保有规模分别是多少

    > 语料库中语句【**变式**】验证 ✅

    > 权益性 ➡️ 货币型

```sql
select agencyname,sum(asset) from fact_retention_model where product_type_bi='货币型' and business_module='银行' and cdate=(DATE_FORMAT(CURRENT_DATE(), '%Y-%m-01')-INTERVAL 1 DAY) group by agencyname;
```

-

## Q3

-   查询浙江，河北，陕西，福建，天津，四川，辽宁，吉林最新保有规模和人数，并且从高到低排序
    > 语料库外语句验证 ❓

```sql

```

> 提示纠正后正确 ✅

```sql
    select sum(asset) from fact_retention_model where fathercodename='时代先锋' and cdate=(DATE_FORMAT(CURRENT_DATE(), '%Y-%m-01')-INTERVAL 1 DAY)

select fathercodename,sum(asset),count(distinct syscustomerid) from fdm.fact_retention_model
    where cdate=(select max(cdate) from fdm.fact_retention_model where islastwkday_month='是')
    and fathercodename='时代先锋'
    and is_settlement='未清盘'
    group by fathercodename
```
