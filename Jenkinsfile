#!groovy

node {
    stage('Preparation') {
        checkout scm
        env.GIT_URL = sh(returnStdout: true, script: 'git config --get remote.origin.url').trim()
        env.GIT_BRANCH = sh(returnStdout: true, script: 'git rev-parse --abbrev-ref HEAD').trim()
        env.GIT_COMMIT = sh(returnStdout: true, script: 'git rev-parse HEAD').trim()
        def workspace = pwd()
        sh "cp /var/jenkins_home/deploy-app-vars.yml ${workspace}/ci/ansible"

    }

    stage('Test') {

    }

    /*
    stage('SonarQube analysis') {
        // The SonarQube server requires at least 2GB of RAM to run efficiently and 1GB of free RAM for the OS.
        def scannerHome = tool 'Latest SonarQube Scanner';
        withSonarQubeEnv('Local SonarQube Server') {
            sh "${scannerHome}/bin/sonar-scanner -Dproject.settings=ci/sonar-project.properties"
        }
    }

    stage("SonarQube Quality Gate") {
        timeout(time: 1, unit: 'HOURS') {
            def qg = waitForQualityGate()
            if (qg.status != 'OK') {
                error "Pipeline aborted due to quality gate failure: ${qg.status}"
            }
        }
    }
    */

    stage('Staging deploy') {
        ansiColor('xterm') {
            ansiblePlaybook(
                    colorized: true,
                    installation: 'latest ansible',
                    inventory: 'ci/ansible/hosts',
                    playbook: 'ci/ansible/deploy-app.yml',
                    sudoUser: null
            )
        }
    }

}

stage('Production deploy approval') {
    timeout(time: 5, unit: 'DAYS') {
        def deployDelay = input(
                id: 'userInput', message: 'Deploy to production?', parameters: [
                [$class: 'TextParameterDefinition', defaultValue: '0', description: 'minutes', name: 'After'],
        ])
        sleep time: deployDelay.toInteger(), unit: 'MINUTES'
    }
}

node {
    stage('Production deploy') {
        ansiColor('xterm') {
            ansiblePlaybook(
                    colorized: true,
                    installation: 'latest ansible',
                    inventory: 'ci/ansible/hosts',
                    playbook: 'ci/ansible/production-deploy.yml',
                    sudoUser: null
            )
        }
    }
}
