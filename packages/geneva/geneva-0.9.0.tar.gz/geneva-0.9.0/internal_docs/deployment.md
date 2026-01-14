# Geneva deployments

Geneva consists of a client Python library and server-side components to support distributed jobs using Ray and Kubernetes (Kuberay).

Currently Geneva can be installed in any k8s-based environment that supports Ray. Deployment options range from fully manual to fully automated for AWS EKS and GCP GKE.

For customers with an existing Ray cluster, the Geneva client can potentially be used standalone without requiring deployment of server-side components.

## Dedicated environments

Geneva resources are deployed automatically via Terraform in dedicated enterprise environments. This is currently supported in AWS and GCP, with Azure [coming in 2026 Q1](https://linear.app/lancedb/issue/GEN-177/azure-managed-deployments).

Geneva is **not** enabled by default for new LanceDB Enterprise deployments. It must be enabled with a feature flag following these [instructions](https://www.notion.so/lancedb/AWS-Enterprise-Deployment-Guide-Internal-4dfc1e647e8b466cb7eac548448d5cbb?source=copy_link#1fbfbb61f872802b923ac1d9222f3bb4).

## Self-managed/BYOC Kubernetes environments 

For self-managed/BYOC customers using Kubernetes, most server-side Geneva components can be installed via the [Geneva Helm chart](https://github.com/lancedb/sophon/tree/069f83b41b1a9f28280699592af2c27fcf25044e/helm/geneva).

This is separate from the lancedb helm chart but should be installed in the same cluster. By default, it is installed in the `geneva` namespace.

It requires some [customization](https://github.com/lancedb/sophon/blob/069f83b41b1a9f28280699592af2c27fcf25044e/helm/geneva/values.yaml#L6) to configure access to CSP-resources - namely 
service account for GCP and IAM roles for AWS. If LanceDB Enterprise is already installed, these can potentially be reused for Geneva. (in dedicated environments, Geneva uses the same [service account](https://github.com/lancedb/sophon/blob/d39298cbf3783b1534052993dacc5f25b396ba24/infra/terraform/lancedb-saas/aws-enterprise/kube/geneva.tf#L9) as LanceDB services)

Additionally, the Geneva client must be provided with access to the Kubernetes cluster and cloud resources as described [here](https://docs.lancedb.com/geneva/deployment/index#create-iam-role-for-geneva-client)

## Manual deployment (deprecated)

Steps for manual deployment are documented in [Geneva public docs](https://docs.lancedb.com/geneva/deployment/index). This is now deprecated in favor of Helm-based deployments described above.