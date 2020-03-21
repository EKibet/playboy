#!groovy

node {

    try {
        stage 'Checkout'
            checkout scm

            sh 'git log HEAD^..HEAD --pretty="%h %an - %s" > GIT_CHANGES'
            def lastChanges = readFile('GIT_CHANGES')
            slackSend color: "warning", message: "Started `${env.JOB_NAME}#${env.BUILD_NUMBER}`\n\n_The changes:_\n${lastChanges}"


        stage 'Clone repository'
            sh 'git clone git@gitlab.com:Moringa-School/mat-api.git'
            sh "cd mat-api"


        stage 'Test'
            // sh 'virtualenv env -p python3.5'
            // sh '. env/bin/activate'
            // sh 'env/bin/pip install -r. requirements.txt'
            // sh 'env/bin/python3.5 manage.py test --testrunner=djtrump.tests.test_runners.NoDbTestRunner'..
            sh "pipenv --python 3.7"
            sh "pipenv shell"
            sh "pipenv install"
            sh "pytest"
            // echo "Testing"
        stage 'Deploy'
            echo "Testing deploy.."

        stage 'Publish results'
            slackSend color: "good", message: "Build successful: `${env.JOB_NAME}#${env.BUILD_NUMBER}` <${env.BUILD_URL}|Open in Jenkins>"
    }

    catch (err) {
        slackSend color: "danger", message: "Build failed :face_with_head_bandage: \n`${env.JOB_NAME}#${env.BUILD_NUMBER}` <${env.BUILD_URL}|Open in Jenkins>"

        throw err
    }

}