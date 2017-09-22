# Παραμετροποίηση του SonarQube

Κατά το βήμα αυτό, πραγματοποιείται η αρχική παραμετροποίηση του SonarQube.


### Είσοδος στο SonarQube

Πατάμε "Log in", και βάζουμε ως username/password, admin/admin:
![](screenshots/3_config_sonar/1_sonar_login.png)
![](screenshots/3_config_sonar/2_sonar_login.png)


### Αλλαγή ρυθμίσεων ασφαλείας

Επιλέγουμε "Administration":
![](screenshots/3_config_sonar/3_administration.png)

Πηγαίνουμε στην κατηγορία "Security", και ενεργοποιούμε το "Force user authentication":
![](screenshots/3_config_sonar/4_security.png)
![](screenshots/3_config_sonar/5_user_authentication.png)
Με τον τρόπο αυτό, τα projects μας δεν θα είναι ορατά, αν δεν έχουμε κάνει login.


### Ενεργοποίηση του Jenkins webhook

Στο menu "Administration", πηγαίνουμε στην κατηγορία "Webhooks".  
Εισάγουμε ένα καινούργιο webhook, με όνομα jenkins, και URL: `http://jenkins:8080/jenkins/sonarqube-webhook/`:
![](screenshots/3_config_sonar/6_webhook.png)
Το URL αυτό αποτελεί το URL του Jenkins, στο εσωτερικό Docker network. Με τη χρήση του webhook, επιτυγχάνουμε την ενημέρωση του SonarQube Quality Gate, που θα ενσωματώσουμε στα Jenkins CI Pipelines.


### Αλλαγή κωδικού πρόσβασης ασφαλείας, και δημιουργία Jenkins token

Πατάμε το σύμβολο "A", στην πάνω δεξιά γωνία, και επιλέγουμε "My Account":
![](screenshots/3_config_sonar/7_my_account.png)

Στην φόρμα "Change password", εισάγουμε ως παλιό κωδικό "admin", και ως νέο, τον επιθυμητό κωδικό.
Στη συνέχεια, πατάμε "Change password":
![](screenshots/3_config_sonar/8_change_password.png)

Στην φόρμα "Generate New Token", εισάγουμε "jenkins", και πατάμε "Generate":
![](screenshots/3_config_sonar/9_generate_token.png)

Τέλος, πατάμε "Copy", για να αντιγράψουμε το token στο clipboard:
![](screenshots/3_config_sonar/10_copy_token.png)
Το token αυτό χρησιμοποιείται στην [σύνδεση του Jenkins με το SonarQube](jenkins-sonarqube.md).
