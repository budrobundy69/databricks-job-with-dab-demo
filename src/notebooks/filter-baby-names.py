# Databricks notebook source
babynames = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load("dbfs:/FileStore/baby-names.csv")
babynames.createOrReplaceTempView("babynames_table")
years = spark.sql("SELECT DISTINCT year FROM babynames_table ORDER BY year").rdd.map(lambda row: row.year).collect()
years.sort()
dbutils.widgets.dropdown("year", str(years[-1]), [str(x) for x in years])
display(spark.sql("SELECT * FROM babynames_table WHERE year = " + dbutils.widgets.get("year")))