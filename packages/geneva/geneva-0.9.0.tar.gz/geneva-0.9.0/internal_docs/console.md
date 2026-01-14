## Accessing the Geneva Console

### Background

Currently we deploy a Geneva Console API and UI as part of dedicated enterprise deployment (if the Geneva feature flag is enabled in the Terraform workspace).

These can also be deployed for self-managed/BYOC customers via Geneva Helm chart.

The console does not yet have AuthN so we do not expose it via a load balancer/ingress, but self-managed customers are free to set up a service/ingress as required.

For managed deployments it can be accessed via k8s credentials using port-forwarding. 


### Accessing the UI via port-forwarding in Geneva client
When the client runs jobs, it automatically opens a portforward and logs a message like:

✨ Geneva UI is available at [http://localhost:55128](http://localhost:55128/)

While the client is running the UI can be accessed from a local browser.

### Accessing the UI via manual port-forwarding
A portforward can also be created manually to access the UI from outside of the client:

1. Set cloud credentials (i.e. `aws configure`)
2. Retrieve kubeconfig
   i.e. in AWS,
   `aws eks update-kubeconfig --region $REGION --name lancedb --role-arn arn:aws:iam::$ACCOUNT_ID:role/lancedb_eks_cluster_access`
   (test with kubectl or k9s)
3. Create portforward to geneva console UI

```bash
kubectl port-forward \
  $(kubectl get pods -n geneva -o name | grep '^pod/geneva-console-' | head -n1) \
   3000:3000 -n geneva
```

4. Open a browser to [http://localhost:3000](http://localhost:3000/)
5. Configure the database URL in the UI, i.e. `s3://{bucket}/{db_path}`, `gs://lancedb-lancedb-dev-us-central1/7848/data`, etc.