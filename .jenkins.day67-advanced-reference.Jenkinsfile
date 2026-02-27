pipeline {
  agent any

  stages {
    stage('Lint') {
      steps {
        sh 'python -m pip install -r requirements-test.txt'
        sh 'ruff check src tests'
      }
    }

    stage('Test Matrix') {
      matrix {
        axes {
          axis {
            name 'PYTHON_VERSION'
            values '3.10', '3.11'
          }
        }
        stages {
          stage('Run Unit Tests') {
            steps {
              sh "echo Running against ${PYTHON_VERSION}"
              sh 'pytest -q'
            }
          }
        }
      }
    }

    stage('Parallel Governance Checks') {
      parallel {
        stage('Contract') {
          steps {
            sh 'python scripts/check_day67_integration_expansion3_closeout_contract.py --skip-evidence'
          }
        }
        stage('Security') {
          steps {
            sh './security.sh'
          }
        }
      }
    }
  }

  post {
    always {
      archiveArtifacts artifacts: 'docs/artifacts/day67-integration-expansion3-closeout-pack/**', allowEmptyArchive: true
    }
    unsuccessful {
      echo 'Trigger rollback runbook for Day 67 integration expansion lane.'
    }
  }
}
