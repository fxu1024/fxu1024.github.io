---
layout: default
title: Cloudera Data Warehouse
nav_order: 2
parent: Concepts
grand_parent: Data Service
---

# Cloudera Data Warehouse
{: .no_toc }

- TOC
{:toc}

---

## 1. What's CDW?

- Cloudera Data Warehouse is the tool to provision Hive LLAP or Impala warehouses to query base cluster data 
- Cloudera Data Warehouse consists of two levels:
    - Database Catalog: Linked to 1 Environment, it contains 2 Hive Metastore Servers directly linked to base Hive Database and a Data Analytics Studio event processor (warehouse-$timestamp-$4_random_alphanum)
    - Virtual Warehouse: Linked to 1 Database Catalog, it contains 1 Hive Server 2, 1 Data Analytics Studio (if Hive one), 1 Hue (back and front-end) at least (compute-$timestamp-$4_random_alphanum)

- Database Catalog
- Two types:
    - Default one = Link to base cluster, plugged to Hive Metastore Database and Ranger policies
    - Standalone one = Create a new Database at start on internal Private Cloud Database, create on base Ranger a new Hadoop SQL services with based policies and can have demo data loaded at start, creates a Warehouse directory on base HDFS.


![](../../assets/images/ds/addcdw01.png)
