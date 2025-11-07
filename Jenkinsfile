pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Verificar Código') {
            steps {
                echo "✅ Código descargado correctamente"
                sh 'ls -la'
            }
        }
    }
}