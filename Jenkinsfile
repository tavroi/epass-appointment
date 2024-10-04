#!groovy

node {
    try {
        stage 'Checkout'
            checkout scm
            
        stage 'Deploy'
            sh 'whoami'
            switch (env.BRANCH_NAME) {
                case 'dev':
                    sh 'bash ./.deployment/dev_deploy.sh'
                    break
                case 'uat':
                    sh 'bash ./.deployment/uat_deploy.sh'
                    break
                case 'main':
                    sh 'bash ./.deployment/main_deploy.sh'
                    break
                default: 
                    echo "Deploy scripts only on dev, prod und master"
                    break
            }
    }

    catch (err) {
        throw err
    }


}
