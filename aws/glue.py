
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
  
sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
dyf = glueContext.create_dynamic_frame.from_catalog(database='ad-glue-db', table_name='customer_transactions_customer_data')
dyf.printSchema()
df = dyf.toDF()
df.show()
df=df.filter("channel_id='phone'")
df.show()
df=df.withColumn("new_amount",df["amount"]+500)
df.show()
dyf_output = DynamicFrame.fromDF(df, glueContext, "dyf_output")

glueContext.write_dynamic_frame.from_options(
    frame=dyf_output,
    connection_type="s3",
    connection_options={
        "path": "s3://ad-demo-bucket-205930608840/output/customer_data/"
    },
    format="parquet"
)
job.commit()