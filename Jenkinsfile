#!groovy

node {

    try {
        stage 'Checkout'
            checkout scm

            sh 'git log HEAD^..HEAD --pretty="%h %an - %s" > GIT_CHANGES'
            def lastChanges = readFile('GIT_CHANGES')
            slackSend color: "warning", message: "Started `${env.JOB_NAME}#${env.BUILD_NUMBER}`\n\n_The changes:_\n${lastChanges}"


        stage 'Clone repository'
            //sh 'git clone git@gitlab.com:Moringa-School/mat-api.git'
            echo 'Repository exists'
        stage 'Test'
            sh "cd mat-api"
            sh "pipenv --python 3.7"
            sh "exit"
            sh "python3 -m pip install pytest"
            sh "pipenv sync"
            echo "Testing"
        stage 'Deploy'
            sh 'chmod +x deployment/deploy_prod.sh '
            sh 'cd deployment/'
            // sh "./deploy_prod.sh" 
            
            echo "Testing deploy."

        stage 'Publish results'
            slackSend color: "good", message: "Build successful :banana_dance: \n `${env.JOB_NAME}#${env.BUILD_NUMBER}` <${env.BUILD_URL}|Open in Jenkins>"
    }

    catch (err) {
        slackSend color: "danger", message: "Build failed :face_with_head_bandage: \n`${env.JOB_NAME}#${env.BUILD_NUMBER}` <${env.BUILD_URL}|Open in Jenkins>"

        throw err
    }

}
