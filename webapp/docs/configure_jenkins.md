# Παραμετροποίηση του Jenkins

Κατά το βήμα αυτό, πραγματοποιείται η αρχική παραμετροποίηση και η εγκατάσταση των plugins του Jenkins CI.


### Ξεκλείδωμα του web interface

Για το ξεκλείδωμα του Jenkins web interface, θα πρέπει να κάνουμε SSH στο VM, όπου τρέχει το CI. Στη συνέχεια, θα πρέπει να τρέξουμε την εντολή `cat /opt/jenkins/secrets/initialAdminPassword`, και να κάνουμε copy-paste τον κωδικό, στο textbox που εμφανίζεται:
![](screenshots/1_init_jenkins/1_unlock_jenkins.png)


### Εγκατάσταση αρχικών plugins

Επιλέγουμε "Select plugins to install":
![](screenshots/1_init_jenkins/2_customize_jenkins.png)

Στη συνέχεια, επιλέγουμε τα plugins, που πρέπει να εγκατασταθούν:

* build timeout plugin
* Timestamper
* Workspace Cleanup Plugin
* NodeJS Plugin (αν το project είναι NodeJS)
* Pipeline
* Pipeline: Stage View Plugin
* Bitbucket Plugin (αν χρησιμοποιούμε Bitbucket)
* Git plugin
* Άλλα επιθυμητά plugins (π.χ. Mailer Plugin, αν θέλουμε ειδοποιήσεις μέσω mail, κ.ά.)

Στη συνέχεια, πατάμε "Install":
![](screenshots/1_init_jenkins/3_install_plugins.png)


### Δημιουργία χρήστη

Εισάγουμε τα στοιχεία του χρήστη, που θέλουμε να δημιουργήσουμε, και πατάμε "Save and Finish":
![](screenshots/1_init_jenkins/4_create_user.png)


### Εγκατάσταση επιπλέον plugins

Επιλέγουμε Manage Jenkins:
![](screenshots/1_init_jenkins/5_manage_jenkins.png)

Επιλέγουμε Manage Plugins:
![](screenshots/1_init_jenkins/6_manage_plugins.png)

Πηγαίνουμε στη λίστα με τα Available plugins, και επιλέγουμε τα:

* Ansible plugin
* AnsiColor
* Environment Injector Plugin
* SonarQube Scanner for Jenkins
* Blue Ocean (αν θέλουμε να χρησιμοποιήσουμε το νέο Jenkins UI)

![](screenshots/1_init_jenkins/7_available_plugins.png)

Πατάμε "Download now and install after restart":
![](screenshots/1_init_jenkins/8_download_and_restart.png)

Επιλέγουμε "Restart Jenkins when installation is complete and no jobs are running":
![](screenshots/1_init_jenkins/9_restart_after.png)


### Παραμετροποίηση των plugins

Στη σελίδα "Manage Jenkins", επιλέγουμε "Global Tool Configuration":
![](screenshots/2_config_jenkins/1_global_tools.png)

Πατάμε "Add SonarQube Scanner".  
Εισάγουμε ως Name "sonar scanner", και αφήνουμε τις υπόλοιπες επιλογές ως έχουν:
![](screenshots/2_config_jenkins/2_add_sonarqube_scanner.png)

Πατάμε "Add NodeJS".  
Εισάγουμε ως Name "recent node", και αφήνουμε τις υπόλοιπες επιλογές ως έχουν:
![](screenshots/2_config_jenkins/3_add_nodejs.png)

Πατάμε "Save", στο κάτω μέρος της σελίδας:
![](screenshots/2_config_jenkins/4_save.png)
