---
layout: default
title: ECS Server High Availability - Failure Domain Testing and Troubleshooting
nav_order: 15
parent: Operations
grand_parent: Data Service
---

# ECS Server High Availability - Failure Domain Testing and Troubleshooting
{: .no_toc }

- TOC
{:toc}

---

## 1. Introduction to the test environment

|CDP Runtime version |CDP PvC Base 7.1.7 SP1|
|CM version |Cloudera Manager 7.8.1|
|ECS version |CDP PvC DataServices 1.4.1|
|OS version |Centos 7.9|
|K8S version |RKE 1.21|
|Whether to enable Kerberos |Yes|
|Whether to enable TLS |Yes|
|Auto-TLS |Yes|
|Kerberos |FreeIPA|
|LDAP |FreeIPA|
|DB Configuration |External Postgres 12|
|Vault |Embedded|
|Docker registry |Embedded|
|Install Method |Internet|

|IP addresss |hostname |description|
|192.168.8.141	|ds01.ecs.openstack.com |ECS master node 1|
|192.168.8.142	|ds02.ecs.openstack.com |ECS master node 2|
|192.168.8.143	|ds03.ecs.openstack.com |ECS master node 3|
|192.168.8.144	|ds04.ecs.openstack.com |ECS worker node 1|
|192.168.8.145	|ds05.ecs.openstack.com |ECS worker node 2|
|192.168.8.146	|ds06.ecs.openstack.com |ECS worker node 3|

- For ECS cluster install/config guide, see [Fresh install of ECS 1.3.4 HA Cluster](https://fxu1024.github.io/docs/ds/freshinstall/). 

## 2. Basic Concept

### 2.1 Pod Eviction on the NotReady Node

- kube-controller-manager checks the node status periodically. Whenever the node status is NotReady and the podEvictionTimeout time is exceeded, all pods on the node will be expelled to other nodes. The specific expulsion speed is also affected by expulsion speed parameters, cluster size, and so on. See [kubernetes pod evictions](https://www.containiq.com/post/kubernetes-pod-evictions).

### 2.2 Pod Deletion on the NotReady Node

- A Pod is not deleted automatically when a node is unreachable. The Pods running on an unreachable Node enter the 'Terminating' or 'Unknown' state after a timeout. Pods may also enter these states when the user attempts graceful deletion of a Pod on an unreachable Node. See [delete pods](https://kubernetes.io/docs/tasks/run-application/force-delete-stateful-set-pod/#delete-pods)

- The only ways in which a Pod in such a state can be removed from the apiserver are as follows:
    - The Node object is deleted (either by you, or by the Node Controller).
    - The kubelet on the unresponsive Node starts responding, kills the Pod and removes the entry from the apiserver.
    - Force deletion of the Pod by the user.

- The recommended best practice is to use the first or second approach. If a Node is confirmed to be dead (e.g. permanently disconnected from the network, powered down, etc), then delete the Node object. If the Node is suffering from a network partition, then try to resolve this or wait for it to resolve. When the partition heals, the kubelet will complete the deletion of the Pod and free up its name in the apiserver.

- Normally, the system completes the deletion once the Pod is no longer running on a Node, or the Node is deleted by an administrator. You may override this by force deleting the Pod.

### 2.3 Safely Drain a Node before you bring down the node

- You can use kubectl drain to safely evict all of your pods from a node before you perform maintenance on the node (e.g. kernel upgrade, hardware maintenance, etc.). Safe evictions allow the pod's containers to gracefully terminate and will respect the PodDisruptionBudgets you have specified. See (use kubectl drain to remove a node from service)[https://kubernetes.io/docs/tasks/administer-cluster/safely-drain-node/#use-kubectl-drain-to-remove-a-node-from-service]. 
- When kubectl drain returns successfully, that indicates that all of the pods (except the ones excluded as described in the previous paragraph) have been safely evicted (respecting the desired graceful termination period, and respecting the PodDisruptionBudget you have defined). It is then safe to bring down the node by powering down its physical machine or, if running on a cloud platform, deleting its virtual machine.


## 3. ECS HA test cases

|No.|Use cases|Pod Eviction Triggered by|Pod Deletion Triggered by|
|CASE #1|Unexpected offline node|kube-controller-manager|kubectl delete node <node-name>|
|CASE #2|Unexpected offline node|kube-controller-manager|kubectl delete pod <pod-name> --grace-period=0 --force|
|CASE #3|Regular node maintenance|kubectl drain|kubectl drain|

### 3.1 CASE #1. Shutdown ECS server, delete node and then add it back

#### STAGE 1: Shutdown ECS server

- Step1.1 Check all ECS nodes

```bash
$ kubectl get node
NAME                                    STATUS   ROLES                       AGE    VERSION
feng-ws1.sme-feng.athens.cloudera.com   Ready    control-plane,etcd,master   17m    v1.20.8+rke2r1
feng-ws2.sme-feng.athens.cloudera.com   Ready    control-plane,etcd,master   9h     v1.20.8+rke2r1
feng-ws3.sme-feng.athens.cloudera.com   Ready    control-plane,etcd,master   7h5m   v1.20.8+rke2r1
feng-ws4.sme-feng.athens.cloudera.com   Ready    <none>                      11h    v1.20.8+rke2r1
feng-ws5.sme-feng.athens.cloudera.com   Ready    <none>                      11h    v1.20.8+rke2r1
feng-ws6.sme-feng.athens.cloudera.com   Ready    <none>                      11h    v1.20.8+rke2r1
```

- Step1.2. Shutdown node feng-ws1


- Step1.3. Confirm that only feng-ws1 is NotReady

```bash
$ kubectl get node
NAME                                    STATUS     ROLES                       AGE    VERSION
feng-ws1.sme-feng.athens.cloudera.com   NotReady   control-plane,etcd,master   18m    v1.20.8+rke2r1
feng-ws2.sme-feng.athens.cloudera.com   Ready      control-plane,etcd,master   9h     v1.20.8+rke2r1
feng-ws3.sme-feng.athens.cloudera.com   Ready      control-plane,etcd,master   7h7m   v1.20.8+rke2r1
feng-ws4.sme-feng.athens.cloudera.com   Ready      <none>                      11h    v1.20.8+rke2r1
feng-ws5.sme-feng.athens.cloudera.com   Ready      <none>                      11h    v1.20.8+rke2r1
feng-ws6.sme-feng.athens.cloudera.com   Ready      <none>                      11h    v1.20.8+rke2r1
```

- Step1.4. As you can see from the HAProxy UI, all ports on feng-ws1 ( http port 80, https port 434) have become Down state 


    - ECS server (feng-ws2, feng-ws3) stderr.log indicated Stopped tunnel to 10.113.207.141.
    ```console
    time="2022-01-08T10:34:31Z" level=info msg="Connecting to proxy" url="wss://10.113.207.141:9345/v1-rke2/connect"
    time="2022-01-08T10:34:40Z" level=info msg="Stopped tunnel to 10.113.207.141:9345"
    ```

    - ECS Agent (feng-ws4, feng-ws5, feng-ws6 ) stderr.log indicated Updating load balancer server addresses and Stopped tunnel to 10.113.207.141.
    ```console 
    time="2022-01-08T10:34:31Z" level=info msg="Connecting to proxy" url="wss://10.113.207.141:9345/v1-rke2/connect"
    time="2022-01-08T10:34:40Z" level=info msg="Updating load balancer server addresses -> [10.113.207.143:6443 10.113.207.142:6443]"
    time="2022-01-08T10:34:40Z" level=info msg="Updating load balancer server addresses -> [10.113.207.142:9345 10.113.207.143:9345]"
    time="2022-01-08T10:34:40Z" level=info msg="Stopped tunnel to 10.113.207.141:9345"
    ```

- As you can see from the CM UI, ECS server health/Control Plane Health/Kubernetes Health/Longhorn Health start to alarm.  

- You can also see many pod failures on the k8s web UI.
 

- Most of the pods from feng-ws1 are stuck in terminating state after 300 seconds.

```bash
# kubectl get pods -A -o wide --field-selector spec.nodeName=feng-ws1.sme-feng.athens.cloudera.com
```

 
#### STAGE 2: Delete Node

- Step2.1. The above are all expected behaviors when the ECS server node is down. Pods in terminating state can be removed from the apiserver when the Node object is manually deleted.

```bash
# kubectl delete node feng-ws1.sme-feng.athens.cloudera.com
node "feng-ws1.sme-feng.athens.cloudera.com" deleted
```

- Note: Deletion may be stuck intermittently due to issue 5. Please use the following workaround:

```
# kubectl get node -o name feng-ws1.sme-feng.athens.cloudera.com | xargs -i kubectl patch {} -p '{"metadata":{"finalizers":[]}}' --type=merge
node/feng-ws3.sme-feng.athens.cloudera.com patched
```

- Step2.2. Confirm that Node feng-ws1 disappeared.

```bash
# kubectl get node
NAME                                    STATUS   ROLES                       AGE     VERSION
feng-ws2.sme-feng.athens.cloudera.com   Ready    control-plane,etcd,master   9h      v1.20.8+rke2r1
feng-ws3.sme-feng.athens.cloudera.com   Ready    control-plane,etcd,master   7h15m   v1.20.8+rke2r1
feng-ws4.sme-feng.athens.cloudera.com   Ready    <none>                      11h     v1.20.8+rke2r1
feng-ws5.sme-feng.athens.cloudera.com   Ready    <none>                      11h     v1.20.8+rke2r1
feng-ws6.sme-feng.athens.cloudera.com   Ready    <none>                      11h     v1.20.8+rke2r1
```

- Step2.3. Stop ECS server role on feng-ws1.
 

- Step2.4. Delete ECS server role on feng-ws1.

 

 

- Step2.5. Youll see the warning This entity is currently running with an outdated configuration. 
 

    - Option: If you click the refresh icon, the whole ECS cluster will restart.
 
 

    - In most cases, you don't need to click the refresh icon. You only need refresh ECS.
 

 

- Step2.6. Please refer to Common operations after pod eviction to recovery all failed Pods.

- Step2.7. Confirm that all pods are green.

 


- Step2.8. Confirm that ECS service has no alerts except ECS server health.

 


- Step2.9. Confirm that CP/CDW/CML works well


 

 

 



#### STAGE 3: Add node back

- Step3.1. Boot up feng-ws1 

 

- Step3.2. Please ssh into feng-ws1 and manually clean up rke2 server.

```bash
[centos@feng-ws1 ~]$ sudo /opt/cloudera/parcels/ECS/bin/rke2-killall.sh

[centos@feng-ws1 ~]$ sudo /opt/cloudera/parcels/ECS/bin/rke2-uninstall.sh
```

- Step3.3. Add feng-ws1 as ECS server role by CM UI

 

 

 

- Step3.4. Start ECS role on feng-ws1.
 
 

 

- Step3.5. Youll see the warning This entity is currently running with an outdated configuration.  If you click the refresh icon, the whole ECS cluster will restart.
In most cases, you don't need to click the refresh icon. You just need refresh ECS.

 

 
 

- Step3.6. Confirm that feng-ws1 started successfully.

```bash
# kubectl get node
NAME                                    STATUS   ROLES                       AGE     VERSION
feng-ws1.sme-feng.athens.cloudera.com   Ready    control-plane,etcd,master   4m39s   v1.20.8+rke2r1
feng-ws2.sme-feng.athens.cloudera.com   Ready    control-plane,etcd,master   10h     v1.20.8+rke2r1
feng-ws3.sme-feng.athens.cloudera.com   Ready    control-plane,etcd,master   8h      v1.20.8+rke2r1
feng-ws4.sme-feng.athens.cloudera.com   Ready    <none>                      12h     v1.20.8+rke2r1
feng-ws5.sme-feng.athens.cloudera.com   Ready    <none>                      12h     v1.20.8+rke2r1
feng-ws6.sme-feng.athens.cloudera.com   Ready    <none>                      12h     v1.20.8+rke2r1
```


    - ECS server (feng-ws2, feng-ws3) stderr.log indicated Connecting to proxy" url="wss://10.113.207.141:9345/v1-rke2/connect.
    ```bash
    time="2022-01-08T11:44:00Z" level=info msg="Promoted learner feng-ws1-f4c85849"
    time="2022-01-08T11:44:15Z" level=info msg="Handling backend connection request [feng-ws1.sme-feng.athens.cloudera.com]"
    time="2022-01-08T11:44:16Z" level=info msg="Connecting to proxy" url="wss://10.113.207.141:9345/v1-rke2/connect"
    ```

    - ECS Agent (feng-ws4, feng-ws5, feng-ws6 ) stderr.log indicated Updating load balancer server addresses and Connecting to proxy" url="wss://10.113.207.141:9345/v1-rke2/connect.
    ```bash
    time="2022-01-08T11:44:16Z" level=info msg="Updating load balancer server addresses -> [10.113.207.143:6443 10.113.207.141:6443 10.113.207.142:6443]"
    time="2022-01-08T11:44:16Z" level=info msg="Updating load balancer server addresses -> [10.113.207.143:9345 10.113.207.141:9345 10.113.207.142:9345]"
    time="2022-01-08T11:44:16Z" level=info msg="Connecting to proxy" url="wss://10.113.207.141:9345/v1-rke2/connect"
    ```

- Step3.7.   As you can see from the HAProxy UI, http port 80 &  https port 434 ports on feng-ws1 are UP now.
 

- Step3.8. Confirm that all pods are green
 


- Step3.9. Confirm that ECS service has no alerts

 

- Step3.10. Confirm that CP/CDW/CML works well

 

 

 

 



