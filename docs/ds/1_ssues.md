---
layout: default
title: Issues
nav_order: 3
has_children: true
parent: Data Service
grand_parent: CDP Private Cloud
---

# Issue List
{: .no_toc }

- TOC
{:toc}

---

## 1. rendered manifests contain a resource that already exists

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

## 2. Name or service not known

--- 
DESCRIPTION: 
{: .label .label-yellow } 

- Get errors when installing Control Plane :
Process install-cp (id=1546338729) on host ip-10-113-204-13.se.fuse.cloudera.com (id=1546338574) exited with 1 and expected 0

```console
+ ./install-cdp.sh -n cp
+ popd
+ pushd logs
+ python /opt/cloudera/cm-agent/service/ecs/get_creds.py https://console-cp.apps.ecs-ycloud.sme-feng.athens.cloudera.com
Traceback (most recent call last):
  File "/opt/cloudera/cm-agent/service/ecs/get_creds.py", line 64, in <module>
    result = generate_initial_access_and_private_keys(sys.argv[1])
  File "/opt/cloudera/cm-agent/service/ecs/get_creds.py", line 15, in generate_initial_access_and_private_keys
    local_account_id = get_cdp_account_id(management_console_url)
  File "/opt/cloudera/cm-agent/service/ecs/get_creds.py", line 49, in get_cdp_account_id
    initial_auth_response = requests.get(api_path, verify=False)
  File "/usr/lib/python2.7/site-packages/requests/api.py", line 68, in get
    return request('get', url, **kwargs)
  File "/usr/lib/python2.7/site-packages/requests/api.py", line 50, in request
    response = session.request(method=method, url=url, **kwargs)
  File "/usr/lib/python2.7/site-packages/requests/sessions.py", line 486, in request
    resp = self.send(prep, **send_kwargs)
  File "/usr/lib/python2.7/site-packages/requests/sessions.py", line 598, in send
    r = adapter.send(request, **kwargs)
  File "/usr/lib/python2.7/site-packages/requests/adapters.py", line 415, in send
    raise ConnectionError(err, request=request)
requests.exceptions.ConnectionError: ('Connection aborted.', gaierror(-2, 'Name or service not known'))
```
--- 
CAUSE CONFIRMED: 
{: .label .label-red }

- need to define wildcard DNS entry `*.apps.ecs-ycloud.sme-feng.athens.cloudera.com`

---  
SOLUTION: 
{: .label .label-green } 
   
```bash
echo "strict-order
user=root
listen-address=172.27.27.9
address=/apps.ecs-ycloud.sme-feng.athens.cloudera.com/10.113.207.144
addn-hosts=/etc/dnsmasq.hosts
resolv-file=/etc/resolv.dnsmasq.conf
conf-dir=/etc/dnsmasq.d" > /etc/dnsmasq.conf

systemctl restart dnsmasq
```

## n. issue template

--- 
DESCRIPTION: 
{: .label .label-yellow } 

- 

```console
```
--- 
CAUSE CONFIRMED: 
{: .label .label-red }

- 

---  
SOLUTION: 
{: .label .label-green } 
   
```bash
```

