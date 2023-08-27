# databricks-job-with-dab-demo

This is a demo of how to use the [Databricks CLI](https://docs.databricks.com/user-guide/dev-tools/databricks-cli.html) to create a job that runs a Databricks Archive (DAB) file.

## Prerequisites

* [Databricks CLI](https://docs.databricks.com/user-guide/dev-tools/databricks-cli.html) installed and configured
* [jq](https://stedolan.github.io/jq/) installed
* [Databricks workspace](https://docs.databricks.com/user-guide/workspace.html) with a cluster configured

## Instructions

add a bundle settings schema file to the project

```bash
databricks bundle schema > bundle-settings-schema.json
databricks bundle schema init
```

create a DAB file databricks.yaml

```bash
# yaml-language-server: $schema=bundle-settings-schema.json
bundle:
  name: baby-names

resources:
  jobs:
    retrieve-filter-baby-names-job:
      name: retrieve-filter-baby-names-job
      job_clusters:
        - job_cluster_key: common-cluster
          new_cluster:
            spark_version: 12.2.x-scala2.12
            node_type_id: Standard_DS3_v2
            num_workers: 1
      tasks:
        - task_key: retrieve-baby-names-task
          job_cluster_key: common-cluster
          notebook_task:
            notebook_path: ./retrieve-baby-names.py
        - task_key: filter-baby-names-task
          depends_on:
            - task_key: retrieve-baby-names-task
          job_cluster_key: common-cluster
          notebook_task:
            notebook_path: ./filter-baby-names.py

environments:
  development:
    workspace:
      host: <workspace-url>
  staging:
    workspace:
      host: <workspace-url>
  production:
    workspace:
      host: <workspace-url>
```

validate the DAB file

```bash
databricks bundle validate 
```

deploy the DAB file

```bash
databricks bundle deploy -e development -p AZURE_DEV
```

run the DAB file

```bash
databricks bundle run -e development retrieve-filter-baby-names-job -p AZURE_DEV
```

clean up the DAB file

```bash
databricks bundle clean -e development retrieve-filter-baby-names-job -p AZURE_DEV
```
