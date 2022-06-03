layout	title	parent	grand_parent	nav_order
default
CDP PvC Base Cluster
Installation
CDP Private Cloud
3
CDP PvC Base Cluster Deployment
{: .no_toc }

This article explains the necessary steps to install the minimum services on CDP PvC Base platform prior to installing the CDP Data Services on the ECS platform. Please ensure that all the [prerequisites]({{ site.baseurl }}{% link docs/cdppvc/prerequisites.md %}) have been prepared and [CM]({{ site.baseurl }}{% link docs/cdppvc/cm.md %}) has already been installed successfully before running this procedure.

TOC {:toc}
Sanity Check
Ensure that JDK has already been installed in each CDP PvC Base host.

# rpm -qa | grep jdk
copy-jdk-configs-3.3-10.el7_5.noarch
java-11-openjdk-11.0.14.1.1-1.el7_9.x86_64
java-11-openjdk-headless-11.0.14.1.1-1.el7_9.x86_64
java-11-openjdk-devel-11.0.14.1.1-1.el7_9.x86_64
The external DNS server must contain the forward and reverse zones of the company domain name. The external DNS server must be able to resolve the hostname of all CDP PvC Base hosts and the 3rd party components (includes Kerberos, LDAP server, external database, NFS server) and perform reverse DNS lookup. Repeat this step for every CDP PvC Base host.

# nslookup idm
Server:	10.15.4.150
Address:	10.15.4.150#53

Name:	idm.cdpkvm.cldr
Address: 10.15.4.150

# nslookup 10.15.4.150
150.4.15.10.in-addr.arpa	name = idm.cdpkvm.cldr.
NTP client of each CDP PvC Base host is synchronizing time with the external NTP server.

Each CDP PvC Base host has already been registered with the external Kerberos server.

# ipa host-show bmaster1
Host name: bmaster1.cdpkvm.cldr
Principal name: host/bmaster1.cdpkvm.cldr@CDPKVM.CLDR
Principal alias: host/bmaster1.cdpkvm.cldr@CDPKVM.CLDR
SSH public key fingerprint: SHA256:dyShLpzkqlRHc2LHiqXDbhM8ynT7v4yjZP4CZ212tqU root@bmaster1.cdpkvm.cldr (ssh-rsa),
                          SHA256:C+BAHEBbVAXfhUIpdFxoL2MOkF5pUGATuKnFQXCgJnc root@bmaster1.cdpkvm.cldr (ssh-rsa),
                          SHA256:/COofNFRyGmwAGR6sfonAcXtc/Knjs5/an1+SMX/8GA (ecdsa-sha2-nistp256), SHA256:OL8ZeU7+2E4yl7rsvKftXYTM7Bvr8fEVuxQaQBouwwo
                          (ssh-ed25519)
Password: False
Keytab: True
Managed by: bmaster1.cdpkvm.cldr
Session Timeout
Navigate to Administration > Settings. Search for session timeout. Key in 5 days. This is a temporary setting to avoid session timeout during CDP PvC Base installation (You may revert this setting after successful installation). Log out and log in CM portal.

