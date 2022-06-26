---
layout: default
title: Node crash demo 
nav_order: 10
parent: Operations
grand_parent: Data Service
---

# Node crash demo 
{: .no_toc }

- TOC
{:toc}

---

## 1. Introduction to the test environment

|CDP Runtime version |CDP PvC Base 7.1.7|
|CM version |Cloudera Manager 7.5.5|
|ECS version |CDP PvC DataServices 1.3.4|
|Whether to enable Kerberos |Yes|
|Whether to enable TLS |Yes|
|Auto-TLS |No, using manual TLS|

|IP addresss |hostname |description|
|10.113.207.140	|feng-base.sme-feng.athens.cloudera.com |CDP Base cluster, only a single node|
|10.113.207.141	|feng-ws1.sme-feng.athens.cloudera.com |ECS master node 1|
|10.113.207.142	|feng-ws2.sme-feng.athens.cloudera.com |ECS master node 2|
|10.113.207.143	|feng-ws3.sme-feng.athens.cloudera.com |ECS master node 3|
|10.113.207.144	|feng-ws4.sme-feng.athens.cloudera.com |ECS worker node 1|
|10.113.207.145	|feng-ws5.sme-feng.athens.cloudera.com |ECS worker node 2|
|10.113.207.146	|feng-ws6.sme-feng.athens.cloudera.com |ECS worker node 3|

## 2. remove taints of all master nodes 

```bash
# kubectl taint nodes feng-ws1.sme-feng.athens.cloudera.com node-role.kubernetes.io/control-plane=true:NoSchedule-
node/feng-ws1.sme-feng.athens.cloudera.com untainted
# kubectl taint nodes feng-ws2.sme-feng.athens.cloudera.com node-role.kubernetes.io/control-plane=true:NoSchedule-
node/feng-ws2.sme-feng.athens.cloudera.com untainted
# kubectl taint nodes feng-ws3.sme-feng.athens.cloudera.com node-role.kubernetes.io/control-plane=true:NoSchedule-
node/feng-ws3.sme-feng.athens.cloudera.com untainted
```

## 3. Create a Hive VW

- set LDAP auth rules

![](../../assets/images/ds/cdwfailover02.png)

- Activate DBC

![](../../assets/images/ds/cdwfailover01.png)

- build Hive VW

![](../../assets/images/ds/cdwfailover03.png)

- Hive VW is green

![](../../assets/images/ds/cdwfailover05.png)

## 4. get node status and feng-ws6 is Ready

```bash
# kubectl get node
NAME                                    STATUS   ROLES                       AGE     VERSION
feng-ws1.sme-feng.athens.cloudera.com   Ready    control-plane,etcd,master   3d15h   v1.21.8+rke2r2
feng-ws2.sme-feng.athens.cloudera.com   Ready    control-plane,etcd,master   3d15h   v1.21.8+rke2r2
feng-ws3.sme-feng.athens.cloudera.com   Ready    control-plane,etcd,master   3d15h   v1.21.8+rke2r2
feng-ws4.sme-feng.athens.cloudera.com   Ready    <none>                      3d15h   v1.21.8+rke2r2
feng-ws5.sme-feng.athens.cloudera.com   Ready    <none>                      3d15h   v1.21.8+rke2r2
feng-ws6.sme-feng.athens.cloudera.com   Ready    <none>                      3d15h   v1.21.8+rke2r2
```

## 5. get pod list on feng-ws6

```bash
# kubectl get pods -A -o wide --field-selector spec.nodeName=feng-ws6.sme-feng.athens.cloudera.com
NAMESPACE                   NAME                                                              READY   STATUS    RESTARTS   AGE     IP               NODE                                    NOMINATED NODE   READINESS GATES
compute-1655339175-lzmx     das-webapp-0                                                      1/1     Running   0          4m57s   10.42.4.118      feng-ws6.sme-feng.athens.cloudera.com   <none>           <none>
compute-1655339175-lzmx     hiveserver2-0                                                     1/1     Running   0          4m56s   10.42.4.122      feng-ws6.sme-feng.athens.cloudera.com   <none>           <none>
compute-1655339175-lzmx     huebackend-0                                                      1/1     Running   0          4m56s   10.42.4.120      feng-ws6.sme-feng.athens.cloudera.com   <none>           <none>
compute-1655339175-lzmx     huefrontend-5748485bdc-lzcls                                      1/1     Running   0          4m56s   10.42.4.119      feng-ws6.sme-feng.athens.cloudera.com   <none>           <none>
compute-1655339175-lzmx     query-coordinator-0-0                                             1/1     Running   0          4m55s   10.42.4.124      feng-ws6.sme-feng.athens.cloudera.com   <none>           <none>
compute-1655339175-lzmx     query-coordinator-0-1                                             1/1     Running   0          4m55s   10.42.4.123      feng-ws6.sme-feng.athens.cloudera.com   <none>           <none>
compute-1655339175-lzmx     standalone-compute-operator-0                                     1/1     Running   0          5m1s    10.42.4.117      feng-ws6.sme-feng.athens.cloudera.com   <none>           <none>
compute-1655339175-lzmx     usage-monitor-f7f98f4d-s2tfn                                      1/1     Running   0          4m56s   10.42.4.121      feng-ws6.sme-feng.athens.cloudera.com   <none>           <none>
infra-prometheus            infra-prometheus-operator-1-1655024696-prometheus-node-expmlgp7   1/1     Running   2          3d15h   10.113.207.146   feng-ws6.sme-feng.athens.cloudera.com   <none>           <none>
kube-system                 kube-proxy-feng-ws6.sme-feng.athens.cloudera.com                  1/1     Running   0          15m     10.113.207.146   feng-ws6.sme-feng.athens.cloudera.com   <none>           <none>
kube-system                 nvidia-device-plugin-daemonset-8f6gg                              1/1     Running   2          3d15h   10.42.4.104      feng-ws6.sme-feng.athens.cloudera.com   <none>           <none>
kube-system                 rke2-canal-7znlf                                                  2/2     Running   4          3d15h   10.113.207.146   feng-ws6.sme-feng.athens.cloudera.com   <none>           <none>
longhorn-system             engine-image-ei-d4c780c6-dzclh                                    1/1     Running   2          3d15h   10.42.4.99       feng-ws6.sme-feng.athens.cloudera.com   <none>           <none>
longhorn-system             instance-manager-e-02473d29                                       1/1     Running   0          13m     10.42.4.110      feng-ws6.sme-feng.athens.cloudera.com   <none>           <none>
longhorn-system             instance-manager-r-d9323b0a                                       1/1     Running   0          14m     10.42.4.109      feng-ws6.sme-feng.athens.cloudera.com   <none>           <none>
longhorn-system             longhorn-csi-plugin-glzkk                                         2/2     Running   4          3d15h   10.42.4.102      feng-ws6.sme-feng.athens.cloudera.com   <none>           <none>
longhorn-system             longhorn-manager-6klq2                                            1/1     Running   2          3d15h   10.42.4.103      feng-ws6.sme-feng.athens.cloudera.com   <none>           <none>
shared-services             log-router-l9sd4                                                  2/2     Running   4          3d      10.42.4.100      feng-ws6.sme-feng.athens.cloudera.com   <none>           <none>
warehouse-1655286088-44sn   das-event-processor-0                                             1/1     Running   0          14m     10.42.4.105      feng-ws6.sme-feng.athens.cloudera.com   <none>           <none>
warehouse-1655286088-44sn   metastore-0                                                       1/1     Running   0          14m     10.42.4.106      feng-ws6.sme-feng.athens.cloudera.com   <none>           <none>
```

## 6. shutdown feng-ws6 on Platform9

![](../../assets/images/ds/cdwfailover06.png)

![](../../assets/images/ds/cdwfailover07.png)


## 7. get node status and feng-ws6 is NotReady

```bash
# kubectl get node
NAME                                    STATUS     ROLES                       AGE     VERSION
feng-ws1.sme-feng.athens.cloudera.com   Ready      control-plane,etcd,master   3d15h   v1.21.8+rke2r2
feng-ws2.sme-feng.athens.cloudera.com   Ready      control-plane,etcd,master   3d15h   v1.21.8+rke2r2
feng-ws3.sme-feng.athens.cloudera.com   Ready      control-plane,etcd,master   3d15h   v1.21.8+rke2r2
feng-ws4.sme-feng.athens.cloudera.com   Ready      <none>                      3d15h   v1.21.8+rke2r2
feng-ws5.sme-feng.athens.cloudera.com   Ready      <none>                      3d15h   v1.21.8+rke2r2
feng-ws6.sme-feng.athens.cloudera.com   NotReady   <none>                      3d15h   v1.21.8+rke2r2
```

## 8. Most of pods on Node feng-ws6 are keeping in terminating state after 5 mins

```bash
# kubectl get pods -A -o wide --field-selector spec.nodeName=feng-ws6.sme-feng.athens.cloudera.com
NAMESPACE                   NAME                                                              READY   STATUS        RESTARTS   AGE     IP               NODE                                    NOMINATED NODE   READINESS GATES
compute-1655339175-lzmx     das-webapp-0                                                      1/1     Terminating   0          12m     10.42.4.118      feng-ws6.sme-feng.athens.cloudera.com   <none>           <none>
compute-1655339175-lzmx     hiveserver2-0                                                     1/1     Terminating   0          12m     10.42.4.122      feng-ws6.sme-feng.athens.cloudera.com   <none>           <none>
compute-1655339175-lzmx     huebackend-0                                                      1/1     Terminating   0          12m     10.42.4.120      feng-ws6.sme-feng.athens.cloudera.com   <none>           <none>
compute-1655339175-lzmx     huefrontend-5748485bdc-lzcls                                      1/1     Terminating   0          12m     10.42.4.119      feng-ws6.sme-feng.athens.cloudera.com   <none>           <none>
compute-1655339175-lzmx     query-coordinator-0-0                                             1/1     Terminating   0          12m     10.42.4.124      feng-ws6.sme-feng.athens.cloudera.com   <none>           <none>
compute-1655339175-lzmx     query-coordinator-0-1                                             1/1     Terminating   0          12m     10.42.4.123      feng-ws6.sme-feng.athens.cloudera.com   <none>           <none>
compute-1655339175-lzmx     standalone-compute-operator-0                                     1/1     Terminating   0          12m     10.42.4.117      feng-ws6.sme-feng.athens.cloudera.com   <none>           <none>
compute-1655339175-lzmx     usage-monitor-f7f98f4d-s2tfn                                      1/1     Terminating   0          12m     10.42.4.121      feng-ws6.sme-feng.athens.cloudera.com   <none>           <none>
infra-prometheus            infra-prometheus-operator-1-1655024696-prometheus-node-expmlgp7   1/1     Running       2          3d15h   10.113.207.146   feng-ws6.sme-feng.athens.cloudera.com   <none>           <none>
kube-system                 kube-proxy-feng-ws6.sme-feng.athens.cloudera.com                  1/1     Running       0          22m     10.113.207.146   feng-ws6.sme-feng.athens.cloudera.com   <none>           <none>
kube-system                 nvidia-device-plugin-daemonset-8f6gg                              1/1     Running       2          3d15h   10.42.4.104      feng-ws6.sme-feng.athens.cloudera.com   <none>           <none>
kube-system                 rke2-canal-7znlf                                                  2/2     Running       4          3d15h   10.113.207.146   feng-ws6.sme-feng.athens.cloudera.com   <none>           <none>
longhorn-system             engine-image-ei-d4c780c6-dzclh                                    1/1     Running       2          3d15h   10.42.4.99       feng-ws6.sme-feng.athens.cloudera.com   <none>           <none>
longhorn-system             instance-manager-e-02473d29                                       1/1     Terminating   0          21m     10.42.4.110      feng-ws6.sme-feng.athens.cloudera.com   <none>           <none>
longhorn-system             instance-manager-r-d9323b0a                                       1/1     Terminating   0          21m     10.42.4.109      feng-ws6.sme-feng.athens.cloudera.com   <none>           <none>
longhorn-system             longhorn-csi-plugin-glzkk                                         2/2     Running       4          3d15h   10.42.4.102      feng-ws6.sme-feng.athens.cloudera.com   <none>           <none>
longhorn-system             longhorn-manager-6klq2                                            1/1     Running       2          3d15h   10.42.4.103      feng-ws6.sme-feng.athens.cloudera.com   <none>           <none>
shared-services             log-router-l9sd4                                                  2/2     Running       4          3d      10.42.4.100      feng-ws6.sme-feng.athens.cloudera.com   <none>           <none>
warehouse-1655286088-44sn   das-event-processor-0                                             1/1     Terminating   0          21m     10.42.4.105      feng-ws6.sme-feng.athens.cloudera.com   <none>           <none>
warehouse-1655286088-44sn   metastore-0                                                       1/1     Terminating   0          21m     10.42.4.106      feng-ws6.sme-feng.athens.cloudera.com   <none>           <none>
```

## 9. CDW UI shows error flag

![](../../assets/images/ds/cdwfailover08.png) 