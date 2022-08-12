---
layout: default
title: Cloudera Data Engineering
nav_order: 3
parent: Concepts
grand_parent: Data Service
---

# Cloudera Data Engineering
{: .no_toc }

- TOC
{:toc}

---

## 1. What's CDE?

- a virtual cluster is kind of like a YARN queue.  a dedicated / isolated playground with max quota on cpu&memory.  You can have multiple of these virtuals per CDE service.
    - CDE service == 1 K8s cluster
    - virtual cluster == 1 namespace in K8s cluster.  You can have 10 or 20 of them one for each BU / Team.
    
