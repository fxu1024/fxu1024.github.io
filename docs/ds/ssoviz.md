---
layout: default
title: SSO permission for Cloudera Viz in CDW+CML
nav_order: 7
parent: Operations
grand_parent: Data Service
---

# SSO permission for Cloudera Viz in CDW+CML
{: .no_toc }

- TOC
{:toc}

---

- SSO will be enabled for Cloudera Viz being launched as either an app within CML or an instance within CDW. The single SSO user will have various types of roles:

|Role Type|Role Name|Description|
|Environment role|MLUser/MLAdmin/DWUser/DWAdmin|provide permissions to perform tasks on a specific resource, such as a CDW virtual warehouse/CML workspace|
|CML workspace role|Owner/Contributor/Operator/Viewer|Restrict Access to CML Project/Session/Job|
|Viz role|System Admin/Database Admin/Analyst/Visual Consumer|Restrict Access to Viz connection/dataset/dashboard|

This topic will tell you which roles determine the permissions of the SSO user.

## 1. Introduction to the test environment

|CDP Runtime version |CDP PvC Base 7.1.7 SP2|
|CM version |Cloudera Manager 7.9.5|
|ECS version |CDP PvC DataServices 1.5.0|
|OS version |Centos 7.9|
|K8S version |RKE 1.21|
|Whether to enable Kerberos |Yes|
|Whether to enable TLS |Yes|
|Auto-TLS |Yes|
|Kerberos |FreeIPA|
|LDAP |FreeIPA|
|DB Configuration |PostgreSQL 10.21|
|Vault |Embedded|
|Docker registry |Embedded|
|Install Method |Internet|


## 2. Preparation for test environment

- By setting three LDAP user groups(cdwusers/cmlusers/cdeusers), each group contains 2 users. Please select the `Sync Groups on Login` option from Management Console > Administration > Authentication, so that the associated groups can be imported when you log in to CDV. 

![](../../assets/images/ds/cdvsso01.png)

![](../../assets/images/ds/cdvsso02.png)

- For example: cdwusers group contains two users cdw01 and cdw02.

![](../../assets/images/ds/cdvsso03.png)

- Assign the Environment DWUser/MLUser role to all three groups.

![](../../assets/images/ds/cdvsso04.png)


## 3. Viz in CDW test

- The cdv application is created by the user `admin`, the `user groups` are set to `cmlusers`, and the `admin groups` are set to `cdwusers`.
 
![](../../assets/images/ds/cdvsso05.png)

- Log in as admin, even if admin is the creator, because `admin` neither belongs to `user groups` nor `admin groups`, you still cannot log in to CDV UI.

![](../../assets/images/ds/cdvsso06.png)

- Log in as cdw01, since cdw01 belongs to admin groups, you can see the site administrator menu.

![](../../assets/images/ds/cdvsso07.png)

- Log in as cml01, because cml01 belongs to user groups, you cannot see the site administrator menu.

![](../../assets/images/ds/cdvsso08.png)

- Log in as cde01. Since cde01 does not belong to user groups or admin groups, you cannot log in to the CDV UI.

![](../../assets/images/ds/cdvsso06.png)

- Log in again as the administrator cdw01, and view user and user group permissions.
    - It indicates that `cdw01` is granted `Admin` permissions, and cml01 is granted `Normal` permissions. 

![](../../assets/images/ds/cdvsso09.png)

- The Normal user is automatically assigned to the viz_guest_group group, and the viz_guest_group group automatically has the Database admin role, which can also be confirmed from the figure below.

![](../../assets/images/ds/cdvsso10.png)
 
- Manually set cde01 and cml01 to have the system admin role:

![](../../assets/images/ds/cdvsso11.png)

- Login via cde01, still can't access cdv:

![](../../assets/images/ds/cdvsso06.png)

- Log in through cml01, and find that although cml01 is a normal user, you can see the site administrator menu.

![](../../assets/images/ds/cdvsso12.png)

## 4. Viz in CML test

- The cdv application is created by the user admin.

![](../../assets/images/ds/cdvsso13.png)

- Since the CDV application belongs to the project test01, it cannot be accessed by other users except admin by default. These users(cdw01/cml01/cde01) must be added as project collaborators.

![](../../assets/images/ds/cdvsso14.png)

- Log in as admin and it is only a Normal user. 

![](../../assets/images/ds/cdvsso15.png)

- cdw01/cml01/cde01 are Normal users as well and cannot see the Site Administration menu.

- Log in as the built-in administration user `vizapps_admin`(password=vizapps_admin).

![](../../assets/images/ds/cdvsso16.png)

- View all user and user group permissions:

![](../../assets/images/ds/cdvsso17.png)

- Every users are automatically assigned to the viz_guest_group group, and the viz_guest_group group automatically has the Database admin role, which can also be confirmed from the following figure.

![](../../assets/images/ds/cdvsso18.png)

- Manually assign the system admin role to viz_guest_group:

![](../../assets/images/ds/cdvsso19.png)

- User Admin can now see the Site Adminsitration menu now.

![](../../assets/images/ds/cdvsso20.png)

- Other users become administrator users as well.

![](../../assets/images/ds/cdvsso21.png)


## 5. Conclusion

- CDV is not an independent application. It is currently parasitic on CDW and CML, so the logged-in user is also an SSO user of CDW or CML.

- For Viz in CDW:
    - SSO users must have permission to access CDW resources, that is to say, they need to have one of DWUser/DWAdmin roles;
    - SSO users are limited by the parameters user groups and admin groups when creating the cluster. Users outside this range cannot access the Viz application, and subsequent authorization through Viz will be invalid;
    - If an SSO user belongs to admin groups, it will automatically become a Viz administrator;
If an SSO user belongs to user groups, it is automatically assigned to the viz_guest_group group and has Database Admin permissions. Subsequent administrators can perform Viz internal authorization to obtain other permissions.

- For Viz in CML:
    - SSO users must have permission to access CML resources, that is to say, they need to have one of the roles of MLUser/MLAdmin;
    - If the SSO user is not the creator of the Viz application, the Collaborators role must be added to gain access to the Viz application;
    - SO users are automatically assigned to viz_guest_group and have Database Admin permissions. Subsequent administrators can perform Viz internal authorization to obtain other permissions.
    