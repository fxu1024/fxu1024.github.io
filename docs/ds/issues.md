---
layout: default
title: Issues
parent: Data Service
---

# Issue List
{: .no_toc }

- TOC
{:toc}

---

## rendered manifests contain a resource that already exists

--- 
DESCRIPTION: 
{: .label .label-yellow } 

- failed to activate CDE service

```console
2021-09-07T01:40:29.556957Z:LogDebug:Error fetching chart info for dex-base, invalid chart, will retry
Sep 7, 2021, 9:40:30 AM:LogError:dex-base, version 1.10.0 installation failed, dex-base installation failed, rendered manifests contain a resource that already exists. Unable to continue with install: existing resource conflict: namespace: , name: pvccde-dex-base-dex-base-configs-manager, existing_kind: rbac.authorization.k8s.io/v1, Kind=ClusterRole, new_kind: rbac.authorization.k8s.io/v1, Kind=ClusterRole
```
--- 
CAUSE CONFIRMED: 
{: .label .label-red }

- Deleting from the CDE UI does not delete records in the backend database. 

---  
SOLUTION: 
{: .label .label-green } 
   
```bash
kubectl exec -it cdp-embedded-db-0 -n cp -- bash
psql -P pager=off -d db-dex

delete from instance where clusterid = 'cluster-spzq7cvg';

delete from cluster where id = 'cluster-spzq7cvg';
```

