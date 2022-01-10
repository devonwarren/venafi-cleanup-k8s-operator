
This operator will listen to any `certificate` object in k8s and upon deletion will also delete from Venafi

Installation steps:

1. Add CA certificate (if using internal CA) using
```bash
kubectl create secret generic venafi-cert -n cert-manager \
  --from-file=cert=path/to/cert/file
```

2. Modify any environment variables in the `deployment.yaml` file necessary (such as VENAFI_DNS_DOMAIN)

3. Deploy the operator into `cert-manager`:
```bash
kubectl apply -f rbac.yaml
kubectl apply -f deployment.yaml
```
