# AWS Python Spark - Customer Analytics

A customer analytics pipeline using AWS Glue, Redshift, S3, and Python. Generates sample transaction data, provisions AWS infrastructure via CloudFormation, and prepares schemas for ETL.

## Project Structure

```
.
├── aws/
│   ├── cloud_formation.yml   # CloudFormation template (Glue, Redshift, S3, IAM)
│   ├── provisioning.py      # Local provisioning script with stack polling
│   └── Redshift.sql         # Redshift table schema for analytics
├── sample_data/             # Sample CSV outputs (local)
├── .github/workflows/
│   └── deploy-cloudformation.yml  # CI/CD: deploys on push to main
├── file_generator.py        # Generates sample data and uploads to S3
├── requirements.txt
└── aws_config.env           # AWS configuration (git-ignored)
```

## AWS Resources

The CloudFormation template provisions:

| Resource | Type | Description |
|----------|------|-------------|
| AdDemoBucket | S3 | Bucket for customer data (`ad-demo-bucket`) |
| AdGlueRole | IAM | Role for Glue (S3, Secrets Manager) |
| AdRedshiftRole | IAM | Role for Redshift (S3, Glue) |
| AdGlueDatabase | Glue | Database `ad-glue-db` |
| AdGlueCrawler | Glue | Crawler for `s3://ad-demo-bucket/customer_data/` |
| AdRedshiftCluster | Redshift | Single-node RA3 cluster for `customer_analytics` |
| RedshiftSecret | Secrets Manager | Credentials for Glue → Redshift connection |
| GlueRedshiftConnection | Glue | JDBC connection to Redshift |

## Prerequisites

- Python 3.8+
- AWS CLI configured
- AWS account with permissions for CloudFormation, S3, Glue, Redshift, IAM, Secrets Manager

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### 1. Provision AWS Resources (Local)

```bash
cd aws
python provisioning.py
```

Creates the `customer-analytics-stack` CloudFormation stack and polls until complete. Uses `aws/cloud_formation.yml` and the default Redshift password from the template.

### 2. Generate Sample Data

```bash
python file_generator.py
```

Generates 10 rows of fake transaction data and uploads to S3. Update the bucket name in `file_generator.py` to match your S3 bucket (e.g. `ad-demo-bucket` for CloudFormation-provisioned bucket).

**Data format:** `channel_id`, `customer_id`, `transaction_id`, `transaction_date`, `amount`, `merchant_name`

### 3. Redshift Schema

After the Redshift cluster is available, run `aws/Redshift.sql` to create the analytics table:

```sql
CREATE TABLE customer_analytics.public.transactions_fact (
    channel_id        VARCHAR(20),
    customer_id       INT,
    transaction_id    VARCHAR(36),
    transaction_date  DATE,
    amount            DECIMAL(10,2),
    merchant_name     VARCHAR(100)
)
DISTSTYLE AUTO
SORTKEY(transaction_date);
```

## CI/CD (GitHub Actions)

On every push to `main`, the workflow deploys the CloudFormation stack.

**Required GitHub Secrets:**

| Secret | Required | Description |
|--------|----------|-------------|
| `AWS_ACCESS_KEY_ID` | Yes | AWS access key |
| `AWS_SECRET_ACCESS_KEY` | Yes | AWS secret key |
| `AWS_REGION` | Yes | e.g. `us-east-1` |
| `REDSHIFT_MASTER_PASSWORD` | No | Override template default |

Add secrets under **Settings → Secrets and variables → Actions**.

## Configuration

- **CloudFormation:** Edit `aws/cloud_formation.yml` (parameters, bucket names, etc.)
- **File generator:** Edit `file_generator.py` for S3 bucket, prefix, row count
- **AWS credentials:** Use `aws_config.env`, AWS CLI profile, or environment variables

## License

MIT
