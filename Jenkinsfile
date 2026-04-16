pipeline {
  agent any
  stages {
    stage('Install') {
      steps {
        sh 'python -m pip install --upgrade pip'
        sh 'pip install -r requirements.txt'
      }
    }
    stage('Test + Coverage') {
      steps {
        sh 'pytest -v --cov=app --cov-report=term --cov-report=html'
      }
    }
    stage('Security Scans') {
      steps {
        sh 'bandit -r app'
        sh 'pip-audit || true'
      }
    }
  }
  post {
    always {
      archiveArtifacts artifacts: 'htmlcov/**', fingerprint: true
    }
  }
}