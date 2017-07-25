pipeline {
  agent any
  stages {
    stage('WWW') {
      steps {
        parallel(
          "WWW": {
            dir(path: '/var/jenkins_home/worker/workspace/www.eea.europa.eu-hudson/src/eea.alchemy') {
              sh '''git checkout master
git pull
../../bin/coverage run ../../bin/xmltestreport -v -vv -s eea.alchemy
../../bin/report xml --include=*eea/alchemy*
mkdir -p xmltestreport
cp ../../parts/xmltestreport/testreports/*eea-alchemy*.xml xmltestreport/
'''
              sh 'bin/test -s eea.alchemy'
            }
            
            
          },
          "Plone4": {
            node(label: 'standalone') {
              dir(path: 'buildouts/plone4') {
                sh '''./install.sh
bin/buildout'''
                sh 'bin/test -s eea.alchemy'
              }
              
            }
            
            
          },
          "Docker: WWW": {
            node(label: 'docker-1.10') {
              sh 'docker run --rm eeacms/www:devel bash -c \'bin/develop up && bin/test -v -vv -s eea.alchemy\''
            }
            
            
          },
          "Docker: Plone4": {
            node(label: 'docker-1.10') {
              sh 'docker run --rm -e BUILDOUT_EGGS=eea.alchemy -e BUILDOUT_DEVELOP=src/eea.alchemy eeacms/plone-test bin/test -v -vv -s eea.alchemy'
            }
            
            
          }
        )
      }
    }
    stage('Coverage/Report') {
      steps {
        parallel(
          "Coverage/Report": {
            dir(path: '/var/jenkins_home/worker/workspace/www.eea.europa.eu-hudson/src/eea.alchemy') {
              sh '''../../bin/coverage run ../../bin/xmltestreport -v -vv -s eea.alchemy
../../bin/report xml --include=*eea/alchemy*
mkdir -p xmltestreport
cp ../../parts/xmltestreport/testreports/*eea-alchemy*.xml xmltestreport/
'''
            }
            
            
          },
          "ZPT Lint": {
            dir(path: '/var/jenkins_home/worker/workspace/www.eea.europa.eu-hudson/src/eea.alchemy') {
              sh '../../bin/zptlint-test'
            }
            
            
          },
          "PyFlakes": {
            dir(path: '/var/jenkins_home/worker/workspace/www.eea.europa.eu-hudson/src/eea.alchemy') {
              sh '../../bin/pyflakes-test'
            }
            
            
          },
          "PyLint": {
            dir(path: '/var/jenkins_home/worker/workspace/www.eea.europa.eu-hudson/src/eea.alchemy') {
              sh '../../bin/pylint-test'
            }
            
            
          },
          "JSLint": {
            dir(path: '/var/jenkins_home/worker/workspace/www.eea.europa.eu-hudson/src/eea.alchemy') {
              sh '../../bin/jslint-test eea'
            }
            
            
          },
          "i18n": {
            dir(path: '/var/jenkins_home/worker/workspace/www.eea.europa.eu-hudson/src/eea.alchemy') {
              sh 'find . -name *.pt | xargs ../../bin/i18ndude find-untranslated -n | wc -l'
            }
            
            
          }
        )
      }
    }
    stage('Report') {
      steps {
        dir(path: '/var/jenkins_home/worker/workspace/www.eea.europa.eu-hudson/src/eea.alchemy') {
          openTasks(excludePattern: '**/*.png, **/*.gif,  **/*.jpg, **/*.zip, **/*.ppt, **/*.jar,   **/*.stx, **/CHANGES.txt, **/HISTORY.txt, **/INSTALL.txt, **/*.rst, **/CHANGELOG.txt, **/ChangeLog')
          junit(testResults: '**/xmltestreport/*.xml', healthScaleFactor: 1)
        }
        
      }
    }
  }
}