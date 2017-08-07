pipeline {
  agent any
  stages {
    stage('Tests') {
      steps {
        parallel(
          "WWW": {
            dir(path: '/var/jenkins_home/worker/workspace/www.eea.europa.eu-hudson/src/eea.alchemy') {
              sh '''
git checkout master
git pull
../../bin/test -v -vv -s eea.alchemy
'''
            }
            
            
          },
          "Plone4": {
            node(label: 'standalone') {
              git(url: 'https://github.com/eea/eea.alchemy.git', changelog: true)
              sh '''
cd buildouts/plone4
./install.sh
bin/python bin/buildout
bin/python bin/test -v -vv -s eea.alchemy
'''
            }
            
            
          },
          "Docker: WWW": {
            node(label: 'docker-1.10') {
              sh '''
NAME="$BUILD_TAG-www"
docker run -i --net=host --name=$NAME eeacms/www:devel bash -c 'bin/develop up && bin/test -v -vv -s eea.alchemy'
docker rm -v $NAME'''
            }
            
            
          },
          "Docker: Plone4": {
            node(label: 'docker-1.10') {
              sh '''
NAME="$BUILD_TAG-plone4"
docker run -i --net=host --name=$NAME -v /plone/instance/parts -e BUILDOUT_EGGS=eea.alchemy -e BUILDOUT_DEVELOP=src/eea.alchemy eeacms/plone-test bin/test -v -vv -s eea.alchemy
docker rm -v $NAME'''
            }
            
            
          }
        )
      }
    }
    stage('Code Analysis') {
      steps {
        parallel(
          "Tests Coverage": {
            dir(path: '/var/jenkins_home/worker/workspace/www.eea.europa.eu-hudson/src/eea.alchemy') {
              sh '''
../../bin/coverage run ../../bin/xmltestreport -v -vv -s eea.alchemy
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