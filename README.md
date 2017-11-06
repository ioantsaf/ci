# Automatic mechanism for Continuous Integration
Combines [Jenkins](https://jenkins.io/) for CI, [SonarQube](https://www.sonarqube.org/) for 
static code analysis, and [Ansible](https://www.ansible.com/)  for automatic app deployments 
(Continuous Deployment, Continuous Delivery).

## CI creator webapp
The CI creator webapp manages the automatic creation of CIs.

To deploy the CI creator app on a host, Ansible is required. It can be installed by issuing
`pip install ansible`.

1. In the `<ci_repository>/ansible/hosts` (inventory) file, define the CI creator app host, 
inside the `ci-creator` host group.
2. `cd` into the `<ci_repository>/ansible/` directory, and issue the command: 
`ansible-playbook deploy-ci-creator.yml -i hosts --extra-vars "ci_creator_user=<ci_creator_user_name>"`,  
where ci_creator_user_name is the user that will be running the CI creator app.
SSH and access is required. The user must be able to run sudo without a password.

To obtain more info about creating and using CIs, consult the documentation in webapp/docs,
or on the "Usage Guide" link, on the CI creator host (`<ci_creator_url>/docs`).
