pipeline {
    agent any

    stages {

        // ════════════════════════════════════════════════════════════
        // Dispara Backend y Frontend al mismo tiempo
        // Cada uno corre su propio pipeline completo:
        //   Checkout → Install → Tests → SonarQube → Quality Gate → Deploy
        // ════════════════════════════════════════════════════════════
        stage('EcoEnergy - Full Deploy') {
            parallel {
                stage('Backend Pipeline') {
                    steps {
                        build job: 'Pipeline-Backend', wait: true, propagate: true
                    }
                }
                stage('Frontend Pipeline') {
                    steps {
                        build job: 'Pipeline-Frontend', wait: true, propagate: true
                    }
                }
            }
        }
    }

    post {
        success {
            echo '✅ Ambos pipelines completados — Backend en localhost:5000 | Frontend en localhost:3001'
        }
        failure {
            echo '❌ Uno o ambos pipelines fallaron — revisa los resultados individuales.'
        }
    }
}