# Δημιουργία του CI creator

Στο βήμα αυτό περιγράφεται η διαδικασία δημιουργίας του CI creator. 
 
* Η διαδικασία έχει σχεδιαστεί για διανομές του CI creator host βασισμένες σε Debian, και έχει δοκιμαστεί σε Ubuntu Server 16.04.  
* Θα πρέπει να υπάρχει εγκατεστημένο το Ansible στον υπολογιστή μας, και να υπάρχει πρόσβαση μέσω SSH στον host, που θέλουμε να τρέξουμε το CI creator.
* Για να δημιουργηθεί το CI creator χρησιμοποιείται το playbook deploy-ci-creator.yml και ο ρόλος ci-creator.  

<br>

1. Αρχικά, ορίζουμε στο αρχείο `<ci_repository>/ansible/hosts` (inventory), τον host, που επιθυμούμε να τρέχει το CI creator app, μέσα στο host group `ci-creator`.
2. Στη συνέχεια, μέσα από το directory `<ci_repository>/ansible/`, τρέχουμε την εντολή:  
`ansible-playbook deploy-ci-creator.yml -i hosts --extra-vars "ci_creator_user=<ci_creator_user_name>"`,  
όπου ci_creator_user_name το όνομα χρήστη, στον οποίο έχουμε πρόσβαση SSH, και επιθυμούμε να τρέχει το CI creator service.
3. Μετά την επιτυχή εκτέλεση του Ansible playbook, το CI creator είναι έτοιμο για χρήση, και [δημιουργία CI servers](create_ci).
