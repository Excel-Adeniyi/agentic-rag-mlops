
## Pipeline Syntax

Declarative PipelineLimitationsSectionsagentpoststagesstepsDirectivesenvironmentoptionsparameterstriggersJenkins cron syntaxstagetoolsinputwhenSequential StagesParallelMatrixaxesstagesexcludes (optional)Matrix cell-level directives (optional)Stepsscript
Limitations
Sectionsagentpoststagessteps
DirectivesenvironmentoptionsparameterstriggersJenkins cron syntaxstagetoolsinputwhen
environment
Jenkins cron syntax
Sequential Stages
Matrixaxesstagesexcludes (optional)Matrix cell-level directives (optional)
excludes (optional)
Matrix cell-level directives (optional)
Stepsscript
Scripted PipelineFlow ControlStepsDifferences from plain Groovy
Flow Control
Differences from plain Groovy
Syntax Comparison
This section builds on the information introduced inGetting started with Pipelineand should be treated solely as a reference. For more information on how to use Pipeline syntax in practical examples, refer to:
Using a Jenkinsfile
Using a Jenkinsfile
Pipeline-as-Code
Pipeline-as-Code
As of version 2.5 of the Pipeline plugin, Pipeline supports two discretesyntaxes- Declarative and Scripted. For the pros and cons of each, refer to thecomparison.
As discussed at thestart of this chapter, the most fundamental part of a Pipeline is the"step". Basically, steps tell Jenkinswhatto do and serve as the basic building block for both Declarative and Scripted Pipeline syntax.
For an overview of available steps, please refer to thePipeline Steps referencewhich contains a comprehensive list of steps built into Pipeline as well as steps provided by plugins.

## Declarative Pipeline

Declarative Pipeline presents a more simplified and opinionated syntax on top of the Pipeline sub-systems.
In order to use them, install thePipeline: Declarative Plugin.
All valid Declarative Pipelines must be enclosed within apipelineblock, for example:
`pipeline{/* insert Declarative Pipeline here */}`
`pipeline{/* insert Declarative Pipeline here */}`
The basic statements and expressions which are valid in Declarative Pipeline follow the same rules asGroovy’s syntaxwith the following exceptions:
The top-level of the Pipeline must be ablock, specifically:pipeline { }.
The top-level of the Pipeline must be ablock, specifically:pipeline { }.
`pipeline { }`
No semicolons as statement separators.
Each statement has to be on its own line.
No semicolons as statement separators.
Each statement has to be on its own line.
Blocks must only consist ofSections,Directives,Steps, or assignment statements.
Blocks must only consist ofSections,Directives,Steps, or assignment statements.
A property reference statement is treated as a no-argument method invocation.
So, for example,inputis treated asinput().
A property reference statement is treated as a no-argument method invocation.
So, for example,inputis treated asinput().
You can use theDeclarative Directive Generatorto help you get started with configuring the directives and sections in your Declarative Pipeline.

## Limitations

There is currently anopen issuewhich limits the maximum size of the code within thepipeline{}block.
This limitation does not apply to Scripted Pipelines.
Sections in Declarative Pipeline typically contain one or moreDirectivesorSteps.
Theagentsection specifies where the entire Pipeline, or a specific stage, will execute in the Jenkins environment depending on where theagentsection is placed.
The section must be defined at the top-level inside thepipelineblock, but stage-level usage is optional.
Described below
In the top-levelpipelineblock and eachstageblock.
There are some nuances when adding an agent to the top level or a stage level when theoptionsdirective is applied.
Check the sectionoptionsfor more information.
Inagentsdeclared at the top level of a Pipeline, an agent is allocated and then thetimeoutoption is applied.
The time to allocate the agentis not includedin the limit set by thetimeoutoption.
`pipeline{agentanyoptions{// Timeout counter starts AFTER agent is allocatedtimeout(time:1,unit:'SECONDS')}stages{stage('Example'){steps{echo'Hello World'}}}}`
`pipeline{agentanyoptions{// Timeout counter starts AFTER agent is allocatedtimeout(time:1,unit:'SECONDS')}stages{stage('Example'){steps{echo'Hello World'}}}}`
Inagentsdeclared within a stage, the options are invokedbeforeallocating theagentandbeforechecking anywhenconditions.
In this case, when usingtimeout, it is appliedbeforetheagentis allocated.
The time to allocate the agentis includedin the limit set by thetimeoutoption.
`pipeline{agentnonestages{stage('Example'){agentanyoptions{// Timeout counter starts BEFORE agent is allocatedtimeout(time:1,unit:'SECONDS')}steps{echo'Hello World'}}}}`
`pipeline{agentnonestages{stage('Example'){agentanyoptions{// Timeout counter starts BEFORE agent is allocatedtimeout(time:1,unit:'SECONDS')}steps{echo'Hello World'}}}}`
This timeout will include the agent provisioning time.
Because the timeout includes the agent provisioning time, the Pipeline may fail in cases where agent allocation is delayed.
In order to support the wide variety of use-cases Pipeline authors may have, theagentsection supports a few different types of parameters.
These parameters can be applied at the top-level of thepipelineblock, or within eachstagedirective.
Execute the Pipeline, or stage, on any available agent.
For example:agent any
When applied at the top-level of thepipelineblock no global agent will be allocated for the entire Pipeline run and eachstagesection will need to contain its ownagentsection.
For example:agent none
Execute the Pipeline, or stage, on an agent available in the Jenkins environment with the provided label.
For example:agent { label 'my-defined-label' }
`agent { label 'my-defined-label' }`
Label conditions can also be used:
For example:agent { label 'my-label1 && my-label2' }oragent { label 'my-label1 || my-label2' }
`agent { label 'my-label1 && my-label2' }`
`agent { label 'my-label1 || my-label2' }`
agent { node { label 'labelName' } }behaves the same asagent { label 'labelName' }, butnodeallows for additional options (such ascustomWorkspace).
`agent { node { label 'labelName' } }`
`agent { label 'labelName' }`
`customWorkspace`
Execute the Pipeline, or stage, with the given container which will be dynamically provisioned on anodepre-configured to accept Docker-based Pipelines, or on a node matching the optionally definedlabelparameter.dockeralso optionally accepts anargsparameter which may contain arguments to pass directly to adocker runinvocation, and analwaysPulloption, which will force adocker pulleven if the image name is already present.
For example:agent { docker 'maven:3.9.3-eclipse-temurin-17' }or
`docker pull`
`agent { docker 'maven:3.9.3-eclipse-temurin-17' }`
`agent{docker{image'maven:3.9.3-eclipse-temurin-17'label'my-defined-label'args'-v /tmp:/tmp'}}`
`agent{docker{image'maven:3.9.3-eclipse-temurin-17'label'my-defined-label'args'-v /tmp:/tmp'}}`
dockeralso optionally accepts aregistryUrlandregistryCredentialsIdparameters which will help to specify the Docker Registry to use and its credentials.
The parameterregistryCredentialsIdcould be used alone for private repositories within the docker hub.
For example:
`registryUrl`
`registryCredentialsId`
`registryCredentialsId`
`agent{docker{image'myregistry.com/node'label'my-defined-label'registryUrl'https://myregistry.com/'registryCredentialsId'myPredefinedCredentialsInJenkins'}}`
`agent{docker{image'myregistry.com/node'label'my-defined-label'registryUrl'https://myregistry.com/'registryCredentialsId'myPredefinedCredentialsInJenkins'}}`
Execute the Pipeline, or stage, with a container built from aDockerfilecontained in the source repository.
In order to use this option, theJenkinsfilemust be loaded from either aMultibranch Pipelineor aPipeline from SCM.
Conventionally this is theDockerfilein the root of the source repository:agent { dockerfile true }.
If building aDockerfilein another directory, use thediroption:agent { dockerfile { dir 'someSubDir' } }.
If yourDockerfilehas another name, you can specify the file name with thefilenameoption. You can pass additional arguments to thedocker build …​command with theadditionalBuildArgsoption, likeagent { dockerfile { additionalBuildArgs '--build-arg foo=bar' } }.
For example, a repository with the filebuild/Dockerfile.build, expecting a build argumentversion:
`Jenkinsfile`
`agent { dockerfile true }`
`agent { dockerfile { dir 'someSubDir' } }`
`docker build …​`
`additionalBuildArgs`
`agent { dockerfile { additionalBuildArgs '--build-arg foo=bar' } }`
`build/Dockerfile.build`
`agent{// Equivalent to "docker build -f Dockerfile.build --build-arg version=1.0.2 ./build/dockerfile{filename'Dockerfile.build'dir'build'label'my-defined-label'additionalBuildArgs'--build-arg version=1.0.2'args'-v /tmp:/tmp'}}`
`agent{// Equivalent to "docker build -f Dockerfile.build --build-arg version=1.0.2 ./build/dockerfile{filename'Dockerfile.build'dir'build'label'my-defined-label'additionalBuildArgs'--build-arg version=1.0.2'args'-v /tmp:/tmp'}}`
dockerfilealso optionally accepts aregistryUrlandregistryCredentialsIdparameters which will help to specify the Docker Registry to use and its credentials.
For example:
`registryUrl`
`registryCredentialsId`
`agent{dockerfile{filename'Dockerfile.build'dir'build'label'my-defined-label'registryUrl'https://myregistry.com/'registryCredentialsId'myPredefinedCredentialsInJenkins'}}`
`agent{dockerfile{filename'Dockerfile.build'dir'build'label'my-defined-label'registryUrl'https://myregistry.com/'registryCredentialsId'myPredefinedCredentialsInJenkins'}}`
Execute the Pipeline, or stage, inside a pod deployed on a Kubernetes cluster.
In order to use this option, theJenkinsfilemust be loaded from either aMultibranch Pipelineor aPipeline from SCM.
The Pod template is defined inside the kubernetes { } block.
For example, if you want a pod with a Kaniko container inside it, you would define it as follows:
`Jenkinsfile`
`agent{kubernetes{defaultContainer'kaniko'yaml'''
kind: Pod
spec:
  containers:
  - name: kaniko
    image: gcr.io/kaniko-project/executor:debug
    imagePullPolicy: Always
    command:
    - sleep
    args:
    - 99d
    volumeMounts:
      - name: aws-secret
        mountPath: /root/.aws/
      - name: docker-registry-config
        mountPath: /kaniko/.docker
  volumes:
    - name: aws-secret
      secret:
        secretName: aws-secret
    - name: docker-registry-config
      configMap:
        name: docker-registry-config
'''}`
`agent{kubernetes{defaultContainer'kaniko'yaml'''
kind: Pod
spec:
  containers:
  - name: kaniko
    image: gcr.io/kaniko-project/executor:debug
    imagePullPolicy: Always
    command:
    - sleep
    args:
    - 99d
    volumeMounts:
      - name: aws-secret
        mountPath: /root/.aws/
      - name: docker-registry-config
        mountPath: /kaniko/.docker
  volumes:
    - name: aws-secret
      secret:
        secretName: aws-secret
    - name: docker-registry-config
      configMap:
        name: docker-registry-config
'''}`
You will need to create a secretaws-secretfor Kaniko to be able to authenticate with ECR.
This secret should contain the contents of~/.aws/credentials.
The other volume is a ConfigMap which should contain the endpoint of your ECR registry.
For example:
`~/.aws/credentials`
`{"credHelpers":{"<your-aws-account-id>.dkr.ecr.eu-central-1.amazonaws.com":"ecr-login"}}`
`{"credHelpers":{"<your-aws-account-id>.dkr.ecr.eu-central-1.amazonaws.com":"ecr-login"}}`
Refer to the following example for reference:https://github.com/jenkinsci/kubernetes-plugin/blob/master/examples/kaniko.groovy
These are a few options that can be applied to two or moreagentimplementations.
They are not required unless explicitly stated.
A string.
The label or label condition on which to run the Pipeline or individualstage.
This option is valid fornode,docker, anddockerfile, and is required fornode.
A string.
Run the Pipeline or individualstagethisagentis applied to within this custom workspace, rather than the default.
It can be either a relative path, in which case the custom workspace will be under the workspace root on the node, or an absolute path.
For example:
`agent{node{label'my-defined-label'customWorkspace'/some/other/path'}}`
`agent{node{label'my-defined-label'customWorkspace'/some/other/path'}}`
This option is valid fornode,docker, anddockerfile.
A boolean, false by default.
If true, run the container on the node specified at the top-level of the Pipeline, in the same workspace, rather than on a new node entirely.
This option is valid fordockeranddockerfile, and only has an effect when used on anagentfor an individualstage.
A string.
Runtime arguments to pass todocker run.
This option is valid fordockeranddockerfile.
`pipeline{agent{docker'maven:3.9.3-eclipse-temurin-17'}(1)stages{stage('Example Build'){steps{sh'mvn -B clean verify'}}}}`
`pipeline{agent{docker'maven:3.9.3-eclipse-temurin-17'}(1)stages{stage('Example Build'){steps{sh'mvn -B clean verify'}}}}`
`maven:3.9.3-eclipse-temurin-17`
`pipeline{agentnone(1)stages{stage('Example Build'){agent{docker'maven:3.9.9-eclipse-temurin-21'}(2)steps{echo'Hello, Maven'sh'mvn --version'}}stage('Example Test'){agent{docker'openjdk:21-jre'}(3)steps{echo'Hello, JDK'sh'java -version'}}}}`
`pipeline{agentnone(1)stages{stage('Example Build'){agent{docker'maven:3.9.9-eclipse-temurin-21'}(2)steps{echo'Hello, Maven'sh'mvn --version'}}stage('Example Test'){agent{docker'openjdk:21-jre'}(3)steps{echo'Hello, JDK'sh'java -version'}}}}`
Thepostsection defines one or more additionalstepsthat are run upon the completion of a Pipeline’s or stage’s run (depending on the location of thepostsection within the Pipeline).postcan support any of the followingpost-conditionblocks:always,changed,fixed,regression,aborted,failure,success,unstable,unsuccessful, andcleanup.
These condition blocks allow the execution of steps inside each condition depending on the completion status of the Pipeline or stage.
The condition blocks are executed in the order shown below.
`unsuccessful`
In the top-levelpipelineblock and eachstageblock.
Run the steps in thepostsection regardless of the completion status of the Pipeline’s or stage’s run.
Only run the steps inpostif the current Pipeline’s run has a different completion status from its previous run.
Only run the steps inpostif the current Pipeline’s run is successful and the previous run failed or was unstable.
Only run the steps inpostif the current Pipeline’s or status is failure, unstable, or aborted and the previous run was successful.
Only run the steps inpostif the current Pipeline’s run has an "aborted" status, usually due to the Pipeline being manually aborted.
This is typically denoted by gray in the web UI.
Only run the steps inpostif the current Pipeline’s or stage’s run has a "failed" status, typically denoted by red in the web UI.
Only run the steps inpostif the current Pipeline’s or stage’s run has a "success" status, typically denoted by blue or green in the web UI.
Only run the steps inpostif the current Pipeline’s run has an "unstable" status, usually caused by test failures, code violations, etc.
This is typically denoted by yellow in the web UI.
`unsuccessful`
Only run the steps inpostif the current Pipeline’s or stage’s run has not a "success" status.
This is typically denoted in the web UI depending on the status previously mentioned (for stages this may fire if the build itself is unstable).
Run the steps in thispostcondition after every otherpostcondition has been evaluated, regardless of the Pipeline or stage’s status.
`pipeline{agentanystages{stage('Example'){steps{echo'Hello World'}}}post{(1)always{(2)echo'I will always say Hello again!'}}}`
`pipeline{agentanystages{stage('Example'){steps{echo'Hello World'}}}post{(1)always{(2)echo'I will always say Hello again!'}}}`
Containing a sequence of one or morestagedirectives, thestagessection is where the bulk of the "work" described by a Pipeline will be located.
At a minimum, it is recommended thatstagescontain at least onestagedirective for each discrete part of the continuous delivery process, such as Build, Test, and Deploy.
Inside thepipelineblock, or within astage.
`pipeline{agentanystages{(1)stage('Example'){steps{echo'Hello World'}}}}`
`pipeline{agentanystages{(1)stage('Example'){steps{echo'Hello World'}}}}`
Thestepssection defines a series of one or morestepsto be executed in a givenstagedirective.
Inside eachstageblock.
`pipeline{agentanystages{stage('Example'){steps{(1)echo'Hello World'}}}}`
`pipeline{agentanystages{stage('Example'){steps{(1)echo'Hello World'}}}}`

## environment

Theenvironmentdirective specifies a sequence of key-value pairs which will be defined as environment variables for all steps, or stage-specific steps, depending on where theenvironmentdirective is located within the Pipeline.
`environment`
`environment`
This directive supports a special helper methodcredentials()which can be used to access pre-defined Credentials by their identifier in the Jenkins environment.
`credentials()`
Inside thepipelineblock, or withinstagedirectives.
The environment variable specified will be set to the Secret Text content.
The environment variable specified will be set to the location of the File file that is temporarily created.
The environment variable specified will be set tousername:passwordand two additional environment variables will be automatically defined:MYVARNAME_USRandMYVARNAME_PSWrespectively.
`username:password`
`MYVARNAME_USR`
`MYVARNAME_PSW`
The environment variable specified will be set to the location of the SSH key file that is temporarily created and two additional environment variables will be automatically defined:MYVARNAME_USRandMYVARNAME_PSW(holding the passphrase).
`MYVARNAME_USR`
`MYVARNAME_PSW`
Unsupported credentials type causes the pipeline to fail with the message:org.jenkinsci.plugins.credentialsbinding.impl.CredentialNotFoundException: No suitable binding handler could be found for type <unsupportedType>.
`org.jenkinsci.plugins.credentialsbinding.impl.CredentialNotFoundException: No suitable binding handler could be found for type <unsupportedType>.`
`pipeline{agentanyenvironment{(1)CC='clang'}stages{stage('Example'){environment{(2)AN_ACCESS_KEY=credentials('my-predefined-secret-text')(3)}steps{sh'printenv'}}}}`
`pipeline{agentanyenvironment{(1)CC='clang'}stages{stage('Example'){environment{(2)AN_ACCESS_KEY=credentials('my-predefined-secret-text')(3)}steps{sh'printenv'}}}}`
`environment`
`environment`
`environment`
`credentials()`
`pipeline{agentanystages{stage('Example Username/Password'){environment{SERVICE_CREDS=credentials('my-predefined-username-password')}steps{sh'echo "Service user is $SERVICE_CREDS_USR"'sh'echo "Service password is $SERVICE_CREDS_PSW"'sh'curl -u $SERVICE_CREDS https://myservice.example.com'}}stage('Example SSH Username with private key'){environment{SSH_CREDS=credentials('my-predefined-ssh-creds')}steps{sh'echo "SSH private key is located at $SSH_CREDS"'sh'echo "SSH user is $SSH_CREDS_USR"'sh'echo "SSH passphrase is $SSH_CREDS_PSW"'}}}}`
`pipeline{agentanystages{stage('Example Username/Password'){environment{SERVICE_CREDS=credentials('my-predefined-username-password')}steps{sh'echo "Service user is $SERVICE_CREDS_USR"'sh'echo "Service password is $SERVICE_CREDS_PSW"'sh'curl -u $SERVICE_CREDS https://myservice.example.com'}}stage('Example SSH Username with private key'){environment{SSH_CREDS=credentials('my-predefined-ssh-creds')}steps{sh'echo "SSH private key is located at $SSH_CREDS"'sh'echo "SSH user is $SSH_CREDS_USR"'sh'echo "SSH passphrase is $SSH_CREDS_PSW"'}}}}`
Theoptionsdirective allows configuring Pipeline-specific options from within the Pipeline itself.
Pipeline provides a number of these options, such asbuildDiscarder, but they may also be provided by plugins, such astimestamps.
`buildDiscarder`
Inside thepipelineblock, or (with certain limitations) withinstagedirectives.
Persist artifacts and console output for the specific number of recent Pipeline runs.
For example:options { buildDiscarder(logRotator(numToKeepStr: '1')) }
`options { buildDiscarder(logRotator(numToKeepStr: '1')) }`
Perform the automatic source control checkout in a subdirectory of the workspace.
For example:options { checkoutToSubdirectory('foo') }
`options { checkoutToSubdirectory('foo') }`
Disallow concurrent executions of the Pipeline.
Can be useful for preventing simultaneous accesses to shared resources, etc.
For example:options { disableConcurrentBuilds() }to queue a build when there’s already an executing build of the Pipeline, oroptions { disableConcurrentBuilds(abortPrevious: true) }to abort the running one and start the new build.
`options { disableConcurrentBuilds() }`
`options { disableConcurrentBuilds(abortPrevious: true) }`
Do not allow the pipeline to resume if the controller restarts.
For example:options { disableResume() }
`options { disableResume() }`
Used withdockerordockerfiletop-level agent.
When specified, each stage will run in a new container deployed on the same node, rather than all stages running in the same container deployment.
Allows overriding default treatment of branch indexing triggers.
If branch indexing triggers are disabled at the multibranch or organization label,options { overrideIndexTriggers(true) }will enable them for this job only.
Otherwise,options { overrideIndexTriggers(false) }will disable branch indexing triggers for this job only.
`options { overrideIndexTriggers(true) }`
`options { overrideIndexTriggers(false) }`
Preserve stashes from completed builds, for use with stage restarting.
For example:options { preserveStashes() }to preserve the stashes from the most recent completed build, oroptions { preserveStashes(buildCount: 5) }to preserve the stashes from the five most recent completed builds.
`options { preserveStashes() }`
`options { preserveStashes(buildCount: 5) }`
Set the quiet period, in seconds, for the Pipeline, overriding the global default.
For example:options { quietPeriod(30) }
`options { quietPeriod(30) }`
On failure, retry the entire Pipeline the specified number of times.
For example:options { retry(3) }
`options { retry(3) }`
Skip checking out code from source control by default in theagentdirective.
For example:options { skipDefaultCheckout() }
`options { skipDefaultCheckout() }`
Skip stages once the build status has gone to UNSTABLE.
For example:options { skipStagesAfterUnstable() }
`options { skipStagesAfterUnstable() }`
Set a timeout period for the Pipeline run, after which Jenkins should abort the Pipeline.
For example:options { timeout(time: 1, unit: 'HOURS') }
`options { timeout(time: 1, unit: 'HOURS') }`
`pipeline{agentanyoptions{timeout(time:1,unit:'HOURS')(1)}stages{stage('Example'){steps{echo'Hello World'}}}}`
`pipeline{agentanyoptions{timeout(time:1,unit:'HOURS')(1)}stages{stage('Example'){steps{echo'Hello World'}}}}`
Prepend all console output generated by the Pipeline run with the time at which the line was emitted.
For example:options { timestamps() }
`options { timestamps() }`
Set failfast true for all subsequent parallel stages in the pipeline.
For example:options { parallelsAlwaysFailFast() }
`options { parallelsAlwaysFailFast() }`
Completely disable option "Restart From Stage" visible in classic Jenkins UI and Blue Ocean as well.
For example:options { disableRestartFromStage() }.
This option can not be used inside of the stage.
`options { disableRestartFromStage() }`
A comprehensive list of available options is pending the completion ofhelp desk ticket 820.
Theoptionsdirective for astageis similar to theoptionsdirective at the root of the Pipeline.
However, thestage-leveloptionscan only contain steps likeretry,timeout, ortimestamps, or Declarative options that are relevant to astage, likeskipDefaultCheckout.
`skipDefaultCheckout`
Inside astage, the steps in theoptionsdirective are invoked before entering theagentor checking anywhenconditions.
Skip checking out code from source control by default in theagentdirective.
For example:options { skipDefaultCheckout() }
`options { skipDefaultCheckout() }`
Set a timeout period for this stage, after which Jenkins should abort the stage.
For example:options { timeout(time: 1, unit: 'HOURS') }
`options { timeout(time: 1, unit: 'HOURS') }`
`pipeline{agentanystages{stage('Example'){options{timeout(time:1,unit:'HOURS')(1)}steps{echo'Hello World'}}}}`
`pipeline{agentanystages{stage('Example'){options{timeout(time:1,unit:'HOURS')(1)}steps{echo'Hello World'}}}}`
On failure, retry this stage the specified number of times.
For example:options { retry(3) }
`options { retry(3) }`
Prepend all console output generated during this stage with the time at which the line was emitted.
For example:options { timestamps() }
`options { timestamps() }`
Theparametersdirective provides a list of parameters that a user should provide when triggering the Pipeline.
The values for these user-specified parameters are made available to Pipeline steps via theparamsobject, refer to theParameters, Declarative Pipelinefor its specific usage.
Each parameter has aNameandValue, depending on the parameter type.
This information is exported as environment variables when the build starts, allowing subsequent parts of the build configuration to access those values.
For example, use the${PARAMETER_NAME}syntax with POSIX shells likebashandksh, the${Env:PARAMETER_NAME}syntax with PowerShell, or the%PARAMETER_NAME%syntax with Windowscmd.exe.
`${PARAMETER_NAME}`
`${Env:PARAMETER_NAME}`
`%PARAMETER_NAME%`
Only once, inside thepipelineblock.
A parameter of a string type, for example:parameters { string(name: 'DEPLOY_ENV', defaultValue: 'staging', description: '') }.
`parameters { string(name: 'DEPLOY_ENV', defaultValue: 'staging', description: '') }`
A text parameter, which can contain multiple lines, for example:parameters { text(name: 'DEPLOY_TEXT', defaultValue: 'One\nTwo\nThree\n', description: '') }.
`parameters { text(name: 'DEPLOY_TEXT', defaultValue: 'One\nTwo\nThree\n', description: '') }`
A boolean parameter, for example:parameters { booleanParam(name: 'DEBUG_BUILD', defaultValue: true, description: '') }.
`parameters { booleanParam(name: 'DEBUG_BUILD', defaultValue: true, description: '') }`
A choice parameter, for example:parameters { choice(name: 'CHOICES', choices: ['one', 'two', 'three'], description: '') }.
The first value is the default.
`parameters { choice(name: 'CHOICES', choices: ['one', 'two', 'three'], description: '') }`
A password parameter, for example:parameters { password(name: 'PASSWORD', defaultValue: 'SECRET', description: 'A secret password') }.
`parameters { password(name: 'PASSWORD', defaultValue: 'SECRET', description: 'A secret password') }`
`pipeline{agentanyparameters{string(name:'PERSON',defaultValue:'Mr Jenkins',description:'Who should I say hello to?')text(name:'BIOGRAPHY',defaultValue:'',description:'Enter some information about the person')booleanParam(name:'TOGGLE',defaultValue:true,description:'Toggle this value')choice(name:'CHOICE',choices:['One','Two','Three'],description:'Pick something')password(name:'PASSWORD',defaultValue:'SECRET',description:'Enter a password')}stages{stage('Example'){steps{echo"Hello ${params.PERSON}"echo"Biography: ${params.BIOGRAPHY}"echo"Toggle: ${params.TOGGLE}"echo"Choice: ${params.CHOICE}"echo"Password: ${params.PASSWORD}"}}}}`
`pipeline{agentanyparameters{string(name:'PERSON',defaultValue:'Mr Jenkins',description:'Who should I say hello to?')text(name:'BIOGRAPHY',defaultValue:'',description:'Enter some information about the person')booleanParam(name:'TOGGLE',defaultValue:true,description:'Toggle this value')choice(name:'CHOICE',choices:['One','Two','Three'],description:'Pick something')password(name:'PASSWORD',defaultValue:'SECRET',description:'Enter a password')}stages{stage('Example'){steps{echo"Hello ${params.PERSON}"echo"Biography: ${params.BIOGRAPHY}"echo"Toggle: ${params.TOGGLE}"echo"Choice: ${params.CHOICE}"echo"Password: ${params.PASSWORD}"}}}}`
A comprehensive list of available parameters is pending the completion ofhelp desk ticket 820.
Thetriggersdirective defines the automated ways in which the Pipeline should be re-triggered.
For Pipelines which are integrated with a source such as GitHub or BitBucket,triggersmay not be necessary as webhooks-based integration will likely already be present.
The triggers currently available arecron,pollSCMandupstream.
Only once, inside thepipelineblock.
Accepts a cron-style string to define a regular interval at which the Pipeline should be re-triggered, for example:triggers { cron('H */4 * * 1-5') }.
`triggers { cron('H */4 * * 1-5') }`
Accepts a cron-style string to define a regular interval at which Jenkins should check for new source changes.
If new changes exist, the Pipeline will be re-triggered.
For example:triggers { pollSCM('H */4 * * 1-5') }
`triggers { pollSCM('H */4 * * 1-5') }`
Accepts a comma-separated string of jobs and a threshold.
When any job in the string finishes with the minimum threshold, the Pipeline will be re-triggered.
For example:triggers { upstream(upstreamProjects: 'job1,job2', threshold: hudson.model.Result.SUCCESS) }
`triggers { upstream(upstreamProjects: 'job1,job2', threshold: hudson.model.Result.SUCCESS) }`
ThepollSCMtrigger is only available in Jenkins 2.22 or later.
`// Declarative //pipeline{agentanytriggers{cron('H */4 * * 1-5')}stages{stage('Example'){steps{echo'Hello World'}}}}`
`// Declarative //pipeline{agentanytriggers{cron('H */4 * * 1-5')}stages{stage('Example'){steps{echo'Hello World'}}}}`

## Jenkins cron syntax

The Jenkins cron syntax follows the syntax of thecron utility(with minor differences).
Specifically, each line consists of 5 fields separated by TAB or whitespace:
Minutes within the hour (0–59)
The hour of the day (0–23)
The day of the month (1–31)
The month (1–12)
The day of the week (0–7) where 0 and 7 are Sunday.
To specify multiple values for one field, the following operators are available.
In the order of precedence,
*specifies all valid values
*specifies all valid values
M-Nspecifies a range of values
M-Nspecifies a range of values
M-N/Xor*/Xsteps by intervals ofXthrough the specified range or whole valid range
M-N/Xor*/Xsteps by intervals ofXthrough the specified range or whole valid range
A,B,…​,Zenumerates multiple values
A,B,…​,Zenumerates multiple values
To allow periodically scheduled tasks to produce even load on the system, the symbolH(for “hash”) should be used wherever possible.
For example, using0 0 * * *for a dozen daily jobs will cause a large spike at midnight.
In contrast, usingH H * * *would still execute each job once a day, but not all at the same time, better using limited resources.
TheHsymbol can be used with a range.
For example,H H(0-7) * * *means some time between 12:00 AM (midnight) to 7:59 AM.
You can also use step intervals withH, with or without ranges.
`H H(0-7) * * *`
TheHsymbol can be thought of as a random value over a range, but it actually is a hash of the job name, not a random function, so that the value remains stable for any given project.
Beware that for the day of month field, short cycles such as*/3orH/3will not work consistently near the end of most months, due to variable month lengths.
For example,*/3will run on the 1st, 4th, …31st days of a long month, then again the next day of the next month.
Hashes are always chosen in the 1-28 range, soH/3will produce a gap between runs of between 3 and 6 days at the end of a month.
Longer cycles will also have inconsistent lengths, but the effect may be relatively less noticeable.
Empty lines and lines that start with#will be ignored as comments.
In addition,@yearly,@annually,@monthly,@weekly,@daily,@midnight, and@hourlyare supported as convenient aliases.
These use the hash system for automatic balancing.
For example,@hourlyis the same asH * * * *and could mean at any time during the hour.@midnightactually means some time between 12:00 AM and 2:59 AM.
every fifteen minutes (perhaps at :07, :22, :37, :52)
triggers{ cron('H/15 * * * *') }
`triggers{ cron('H/15 * * * *') }`
every ten minutes in the first half of every hour (three times, perhaps at :04, :14, :24)
triggers{ cron('H(0-29)/10 * * * *') }
`triggers{ cron('H(0-29)/10 * * * *') }`
once every two hours at 45 minutes past the hour starting at 9:45 AM and finishing at 3:45 PM every weekday.
triggers{ cron('45 9-16/2 * * 1-5') }
`triggers{ cron('45 9-16/2 * * 1-5') }`
once in every two hours slot between 9 AM and 5 PM every weekday (perhaps at 10:38 AM, 12:38 PM, 2:38 PM, 4:38 PM)
triggers{ cron('H H(9-16)/2 * * 1-5') }
`triggers{ cron('H H(9-16)/2 * * 1-5') }`
once a day on the 1st and 15th of every month except December
triggers{ cron('H H 1,15 1-11 *') }
`triggers{ cron('H H 1,15 1-11 *') }`
Thestagedirective goes in thestagessection and should contain astepssection, an optionalagentsection, or other stage-specific directives.
Practically speaking, all of the real work done by a Pipeline will be wrapped in one or morestagedirectives.
At least one
One mandatory parameter, a string for the name of the stage.
Inside thestagessection.
`// Declarative //pipeline{agentanystages{stage('Example'){steps{echo'Hello World'}}}}`
`// Declarative //pipeline{agentanystages{stage('Example'){steps{echo'Hello World'}}}}`
A section defining tools to auto-install and put on thePATH.
This is ignored ifagent noneis specified.
Inside thepipelineblock or astageblock.
`pipeline{agentanytools{maven'apache-maven-3.0.1'(1)}stages{stage('Example'){steps{sh'mvn --version'}}}}`
`pipeline{agentanytools{maven'apache-maven-3.0.1'(1)}stages{stage('Example'){steps{sh'mvn --version'}}}}`
Theinputdirective on astageallows you to prompt for input, using theinputstep.
Thestagewill pause after anyoptionshave been applied, and before entering theagentblock for thatstageor evaluating thewhencondition of thestage.
If theinputis approved, thestagewill then continue.
Any parameters provided as part of theinputsubmission will be available in the environment for the rest of thestage.
Required.
This will be presented to the user when they go to submit theinput.
An optional identifier for thisinput.
The default value is based on thestagename.
Optional text for the "ok" button on theinputform.
An optional comma-separated list of users or external group names who are allowed to submit thisinput.
Defaults to allowing any user.
An optional name of an environment variable to set with thesubmittername, if present.
An optional list of parameters to prompt the submitter to provide.
Refer toparametersfor more information.
`pipeline{agentanystages{stage('Example'){input{message"Should we continue?"ok"Yes, we should."submitter"alice,bob"parameters{string(name:'PERSON',defaultValue:'Mr Jenkins',description:'Who should I say hello to?')}}steps{echo"Hello, ${PERSON}, nice to meet you."}}}}`
`pipeline{agentanystages{stage('Example'){input{message"Should we continue?"ok"Yes, we should."submitter"alice,bob"parameters{string(name:'PERSON',defaultValue:'Mr Jenkins',description:'Who should I say hello to?')}}steps{echo"Hello, ${PERSON}, nice to meet you."}}}}`
Thewhendirective allows the Pipeline to determine whether the stage should be executed depending on the given condition.
Thewhendirective must contain at least one condition.
If thewhendirective contains more than one condition, all the child conditions must return true for the stage to execute.
This is the same as if the child conditions were nested in anallOfcondition (refer to theexamplesbelow).
If ananyOfcondition is used, note that the condition skips remaining tests as soon as the first "true" condition is found.
More complex conditional structures can be built using the nesting conditions:not,allOf, oranyOf.
Nesting conditions may be nested to any arbitrary depth.
Inside astagedirective
Execute the stage when the branch being built matches the branch pattern (ANT style path glob) given, for example:when { branch 'master' }. Note that this only works on a multibranch Pipeline.
`when { branch 'master' }`
The optional parametercomparatormay be added after an attribute to specify how any patterns are evaluated for a match:
EQUALSfor a simple string comparison
EQUALSfor a simple string comparison
GLOB(the default) for an ANT style path glob (same as for examplechangeset)
GLOB(the default) for an ANT style path glob (same as for examplechangeset)
REGEXPfor regular expression matching
REGEXPfor regular expression matching
For example:when { branch pattern: "release-\\d+", comparator: "REGEXP"}
`when { branch pattern: "release-\\d+", comparator: "REGEXP"}`
Execute the stage when the build is building a tag.
For example:when { buildingTag() }
`when { buildingTag() }`
Execute the stage if the build’s SCM changelog contains a given regular expression pattern, for example:when { changelog '.*^\\[DEPENDENCY\\] .+$' }.
`when { changelog '.*^\\[DEPENDENCY\\] .+$' }`
Execute the stage if the build’s SCM changeset contains one or more files matching the given pattern.
Example:when { changeset "**/*.js" }
`when { changeset "**/*.js" }`
The optional parametercomparatormay be added after an attribute to specify how any patterns are evaluated for a match:
EQUALSfor a simple string comparison
EQUALSfor a simple string comparison
GLOB(the default) for an ANT style path glob case insensitive (this can be turned off with thecaseSensitiveparameter).
GLOB(the default) for an ANT style path glob case insensitive (this can be turned off with thecaseSensitiveparameter).
`caseSensitive`
REGEXPfor regular expression matching
REGEXPfor regular expression matching
For example:when { changeset pattern: ".TEST\\.java", comparator: "REGEXP" }orwhen { changeset pattern: "*/*TEST.java", caseSensitive: true }
`when { changeset pattern: ".TEST\\.java", comparator: "REGEXP" }`
`when { changeset pattern: "*/*TEST.java", caseSensitive: true }`
Executes the stage if the current build is for a "change request" (a.k.a. Pull Request on GitHub and Bitbucket, Merge Request on GitLab, Change in Gerrit, etc.).
When no parameters are passed the stage runs on every change request, for example:when { changeRequest() }.
`when { changeRequest() }`
By adding a filter attribute with parameter to the change request, the stage can be made to run only on matching change requests.
Possible attributes areid,target,branch,fork,url,title,author,authorDisplayName, andauthorEmail.
Each of these corresponds to aCHANGE_*environment variable, for example:when { changeRequest target: 'master' }.
`authorDisplayName`
`authorEmail`
`when { changeRequest target: 'master' }`
The optional parametercomparatormay be added after an attribute to specify how any patterns are evaluated for a match:
EQUALSfor a simple string comparison (the default)
EQUALSfor a simple string comparison (the default)
GLOBfor an ANT style path glob (same as for examplechangeset)
GLOBfor an ANT style path glob (same as for examplechangeset)
REGEXPfor regular expression matching
REGEXPfor regular expression matching
Example:when { changeRequest authorEmail: "[\\w_-.]+@example.com", comparator: 'REGEXP' }
`when { changeRequest authorEmail: "[\\w_-.]+@example.com", comparator: 'REGEXP' }`
Execute the stage when the specified environment variable is set to the given value, for example:when { environment name: 'DEPLOY_TO', value: 'production' }.
`when { environment name: 'DEPLOY_TO', value: 'production' }`
Execute the stage when the expected value is equal to the actual value, for example:when { equals expected: 2, actual: currentBuild.number }.
`when { equals expected: 2, actual: currentBuild.number }`
Execute the stage when the specified Groovy expression evaluates to true, for example:when { expression { return params.DEBUG_BUILD } }.
`when { expression { return params.DEBUG_BUILD } }`
Execute the stage if theTAG_NAMEvariable matches the given pattern.
For example:when { tag "release-*" }If an empty pattern is provided the stage will execute if theTAG_NAMEvariable exists (same asbuildingTag()).
`when { tag "release-*" }`
`buildingTag()`
The optional parametercomparatormay be added after an attribute to specify how any patterns are evaluated for a match:
EQUALSfor a simple string comparison,
EQUALSfor a simple string comparison,
GLOB(the default) for an ANT style path glob (same as for examplechangeset), or
GLOB(the default) for an ANT style path glob (same as for examplechangeset), or
REGEXPfor regular expression matching.
REGEXPfor regular expression matching.
For example:when { tag pattern: "release-\\d+", comparator: "REGEXP"}
`when { tag pattern: "release-\\d+", comparator: "REGEXP"}`
Execute the stage when the nested condition is false.
Must contain one condition.
For example:when { not { branch 'master' } }
`when { not { branch 'master' } }`
Execute the stage when all of the nested conditions are true.
Must contain at least one condition.
For example:when { allOf { branch 'master'; environment name: 'DEPLOY_TO', value: 'production' } }
`when { allOf { branch 'master'; environment name: 'DEPLOY_TO', value: 'production' } }`
Execute the stage when at least one of the nested conditions is true.
Must contain at least one condition.
For example:when { anyOf { branch 'master'; branch 'staging' } }
`when { anyOf { branch 'master'; branch 'staging' } }`
Execute the stage when the current build has been triggered by the param given.
For example:
when { triggeredBy 'SCMTrigger' }
when { triggeredBy 'SCMTrigger' }
`when { triggeredBy 'SCMTrigger' }`
when { triggeredBy 'TimerTrigger' }
when { triggeredBy 'TimerTrigger' }
`when { triggeredBy 'TimerTrigger' }`
when { triggeredBy 'BuildUpstreamCause' }
when { triggeredBy 'BuildUpstreamCause' }
`when { triggeredBy 'BuildUpstreamCause' }`
when { triggeredBy  cause: "UserIdCause", detail: "vlinde" }
when { triggeredBy  cause: "UserIdCause", detail: "vlinde" }
`when { triggeredBy  cause: "UserIdCause", detail: "vlinde" }`
By default, thewhencondition for astagewill be evaluated after entering theagentfor thatstage, if one is defined.
However, this can be changed by specifying thebeforeAgentoption within thewhenblock.
IfbeforeAgentis set totrue, thewhencondition will be evaluated first, and theagentwill only be entered if thewhencondition evaluates to true.
`beforeAgent`
`beforeAgent`
By default, the when condition for a stage will not be evaluated before the input, if one is defined.
However, this can be changed by specifying thebeforeInputoption within the when block.
IfbeforeInputis set to true, the when condition will be evaluated first, and the input will only be entered if the when condition evaluates to true.
`beforeInput`
`beforeInput`
beforeInput truetakes precedence overbeforeAgent true.
`beforeInput true`
`beforeAgent true`
By default, thewhencondition for astagewill be evaluated after entering theoptionsfor thatstage, if any are defined.
However, this can be changed by specifying thebeforeOptionsoption within thewhenblock.
IfbeforeOptionsis set totrue, thewhencondition will be evaluated first, and theoptionswill only be entered if thewhencondition evaluates to true.
`beforeOptions`
`beforeOptions`
beforeOptions truetakes precedence overbeforeInput trueandbeforeAgent true.
`beforeOptions true`
`beforeInput true`
`beforeAgent true`
`pipeline{agentanystages{stage('Example Build'){steps{echo'Hello World'}}stage('Example Deploy'){when{branch'production'}steps{echo'Deploying'}}}}`
`pipeline{agentanystages{stage('Example Build'){steps{echo'Hello World'}}stage('Example Deploy'){when{branch'production'}steps{echo'Deploying'}}}}`
`pipeline{agentanystages{stage('Example Build'){steps{echo'Hello World'}}stage('Example Deploy'){when{branch'production'environmentname:'DEPLOY_TO',value:'production'}steps{echo'Deploying'}}}}`
`pipeline{agentanystages{stage('Example Build'){steps{echo'Hello World'}}stage('Example Deploy'){when{branch'production'environmentname:'DEPLOY_TO',value:'production'}steps{echo'Deploying'}}}}`
`pipeline{agentanystages{stage('Example Build'){steps{echo'Hello World'}}stage('Example Deploy'){when{allOf{branch'production'environmentname:'DEPLOY_TO',value:'production'}}steps{echo'Deploying'}}}}`
`pipeline{agentanystages{stage('Example Build'){steps{echo'Hello World'}}stage('Example Deploy'){when{allOf{branch'production'environmentname:'DEPLOY_TO',value:'production'}}steps{echo'Deploying'}}}}`
`pipeline{agentanystages{stage('Example Build'){steps{echo'Hello World'}}stage('Example Deploy'){when{branch'production'anyOf{environmentname:'DEPLOY_TO',value:'production'environmentname:'DEPLOY_TO',value:'staging'}}steps{echo'Deploying'}}}}`
`pipeline{agentanystages{stage('Example Build'){steps{echo'Hello World'}}stage('Example Deploy'){when{branch'production'anyOf{environmentname:'DEPLOY_TO',value:'production'environmentname:'DEPLOY_TO',value:'staging'}}steps{echo'Deploying'}}}}`
`pipeline{agentanystages{stage('Example Build'){steps{echo'Hello World'}}stage('Example Deploy'){when{expression{BRANCH_NAME==~/(production|staging)/}anyOf{environmentname:'DEPLOY_TO',value:'production'environmentname:'DEPLOY_TO',value:'staging'}}steps{echo'Deploying'}}}}`
`pipeline{agentanystages{stage('Example Build'){steps{echo'Hello World'}}stage('Example Deploy'){when{expression{BRANCH_NAME==~/(production|staging)/}anyOf{environmentname:'DEPLOY_TO',value:'production'environmentname:'DEPLOY_TO',value:'staging'}}steps{echo'Deploying'}}}}`
`beforeAgent`
`pipeline{agentnonestages{stage('Example Build'){steps{echo'Hello World'}}stage('Example Deploy'){agent{label"some-label"}when{beforeAgenttruebranch'production'}steps{echo'Deploying'}}}}`
`pipeline{agentnonestages{stage('Example Build'){steps{echo'Hello World'}}stage('Example Deploy'){agent{label"some-label"}when{beforeAgenttruebranch'production'}steps{echo'Deploying'}}}}`
`beforeInput`
`pipeline{agentnonestages{stage('Example Build'){steps{echo'Hello World'}}stage('Example Deploy'){when{beforeInputtruebranch'production'}input{message"Deploy to production?"id"simple-input"}steps{echo'Deploying'}}}}`
`pipeline{agentnonestages{stage('Example Build'){steps{echo'Hello World'}}stage('Example Deploy'){when{beforeInputtruebranch'production'}input{message"Deploy to production?"id"simple-input"}steps{echo'Deploying'}}}}`
`beforeOptions`
`pipeline{agentnonestages{stage('Example Build'){steps{echo'Hello World'}}stage('Example Deploy'){when{beforeOptionstruebranch'testing'}options{locklabel:'testing-deploy-envs',quantity:1,variable:'deployEnv'}steps{echo"Deploying to ${deployEnv}"}}}}`
`pipeline{agentnonestages{stage('Example Build'){steps{echo'Hello World'}}stage('Example Deploy'){when{beforeOptionstruebranch'testing'}options{locklabel:'testing-deploy-envs',quantity:1,variable:'deployEnv'}steps{echo"Deploying to ${deployEnv}"}}}}`
`triggeredBy`
`pipeline{agentnonestages{stage('Example Build'){steps{echo'Hello World'}}stage('Example Deploy'){when{triggeredBy"TimerTrigger"}steps{echo'Deploying'}}}}`
`pipeline{agentnonestages{stage('Example Build'){steps{echo'Hello World'}}stage('Example Deploy'){when{triggeredBy"TimerTrigger"}steps{echo'Deploying'}}}}`

## Sequential Stages

Stages in Declarative Pipeline may have astagessection containing a list of nested stages to be run in sequential order.
`pipeline{agentnonestages{stage('Non-Sequential Stage'){agent{label'for-non-sequential'}steps{echo"On Non-Sequential Stage"}}stage('Sequential'){agent{label'for-sequential'}environment{FOR_SEQUENTIAL="some-value"}stages{stage('In Sequential 1'){steps{echo"In Sequential 1"}}stage('In Sequential 2'){steps{echo"In Sequential 2"}}stage('Parallel In Sequential'){parallel{stage('In Parallel 1'){steps{echo"In Parallel 1"}}stage('In Parallel 2'){steps{echo"In Parallel 2"}}}}}}}}`
`pipeline{agentnonestages{stage('Non-Sequential Stage'){agent{label'for-non-sequential'}steps{echo"On Non-Sequential Stage"}}stage('Sequential'){agent{label'for-sequential'}environment{FOR_SEQUENTIAL="some-value"}stages{stage('In Sequential 1'){steps{echo"In Sequential 1"}}stage('In Sequential 2'){steps{echo"In Sequential 2"}}stage('Parallel In Sequential'){parallel{stage('In Parallel 1'){steps{echo"In Parallel 1"}}stage('In Parallel 2'){steps{echo"In Parallel 2"}}}}}}}}`
Stages in Declarative Pipeline may have aparallelsection containing a list of nested stages to be run in parallel.
In addition, you can force yourparallelstages to all be aborted when any one of them fails, by addingfailFast trueto thestagecontaining theparallel.
Another option for addingfailfastis adding an option to the pipeline definition:parallelsAlwaysFailFast().
`failFast true`
`parallelsAlwaysFailFast()`
`pipeline{agentanystages{stage('Non-Parallel Stage'){steps{echo'This stage will be executed first.'}}stage('Parallel Stage'){when{branch'master'}failFasttrueparallel{stage('Branch A'){agent{label"for-branch-a"}steps{echo"On Branch A"}}stage('Branch B'){agent{label"for-branch-b"}steps{echo"On Branch B"}}stage('Branch C'){agent{label"for-branch-c"}stages{stage('Nested 1'){steps{echo"In stage Nested 1 within Branch C"}}stage('Nested 2'){steps{echo"In stage Nested 2 within Branch C"}}}}}}}}`
`pipeline{agentanystages{stage('Non-Parallel Stage'){steps{echo'This stage will be executed first.'}}stage('Parallel Stage'){when{branch'master'}failFasttrueparallel{stage('Branch A'){agent{label"for-branch-a"}steps{echo"On Branch A"}}stage('Branch B'){agent{label"for-branch-b"}steps{echo"On Branch B"}}stage('Branch C'){agent{label"for-branch-c"}stages{stage('Nested 1'){steps{echo"In stage Nested 1 within Branch C"}}stage('Nested 2'){steps{echo"In stage Nested 2 within Branch C"}}}}}}}}`
`parallelsAlwaysFailFast`
`pipeline{agentanyoptions{parallelsAlwaysFailFast()}stages{stage('Non-Parallel Stage'){steps{echo'This stage will be executed first.'}}stage('Parallel Stage'){when{branch'master'}parallel{stage('Branch A'){agent{label"for-branch-a"}steps{echo"On Branch A"}}stage('Branch B'){agent{label"for-branch-b"}steps{echo"On Branch B"}}stage('Branch C'){agent{label"for-branch-c"}stages{stage('Nested 1'){steps{echo"In stage Nested 1 within Branch C"}}stage('Nested 2'){steps{echo"In stage Nested 2 within Branch C"}}}}}}}}`
`pipeline{agentanyoptions{parallelsAlwaysFailFast()}stages{stage('Non-Parallel Stage'){steps{echo'This stage will be executed first.'}}stage('Parallel Stage'){when{branch'master'}parallel{stage('Branch A'){agent{label"for-branch-a"}steps{echo"On Branch A"}}stage('Branch B'){agent{label"for-branch-b"}steps{echo"On Branch B"}}stage('Branch C'){agent{label"for-branch-c"}stages{stage('Nested 1'){steps{echo"In stage Nested 1 within Branch C"}}stage('Nested 2'){steps{echo"In stage Nested 2 within Branch C"}}}}}}}}`
Stages in Declarative Pipeline may have amatrixsection defining a multi-dimensional matrix of name-value combinations to be run in parallel.
We’ll refer these combinations as "cells" in a matrix.
Each cell in a matrix can include one or more stages to be run sequentially using the configuration for that cell.
In addition, you can force yourmatrixcells to all be aborted when any one of them fails, by addingfailFast trueto thestagecontaining thematrix.
Another option for addingfailfastis adding an option to the pipeline definition:parallelsAlwaysFailFast().
`failFast true`
`parallelsAlwaysFailFast()`
Thematrixsection must include anaxessection and astagessection.
Theaxessection defines the values for eachaxisin the matrix.
Thestagessection defines a list ofstages to run sequentially in each cell.
Amatrixmay have anexcludessection to remove invalid cells from the matrix.
Many of the directives available onstage, includingagent,tools,when, etc., can also be added tomatrixto control the behavior of each cell.
Theaxessection specifies one or moreaxisdirectives.
Eachaxisconsists of anameand a list ofvalues.
All the values from each axis are combined with the others to produce the cells.
`matrix{axes{axis{name'PLATFORM'values'linux','mac','windows'}}// ...}`
`matrix{axes{axis{name'PLATFORM'values'linux','mac','windows'}}// ...}`
`matrix{axes{axis{name'PLATFORM'values'linux','mac','windows'}axis{name'BROWSER'values'chrome','edge','firefox','safari'}}// ...}`
`matrix{axes{axis{name'PLATFORM'values'linux','mac','windows'}axis{name'BROWSER'values'chrome','edge','firefox','safari'}}// ...}`
`matrix{axes{axis{name'PLATFORM'values'linux','mac','windows'}axis{name'BROWSER'values'chrome','edge','firefox','safari'}axis{name'ARCHITECTURE'values'32-bit','64-bit'}}// ...}`
`matrix{axes{axis{name'PLATFORM'values'linux','mac','windows'}axis{name'BROWSER'values'chrome','edge','firefox','safari'}axis{name'ARCHITECTURE'values'32-bit','64-bit'}}// ...}`
Thestagessection specifies one or morestages to be executed sequentially in each cell.
This section is identical to any otherstagessection.
`matrix{axes{axis{name'PLATFORM'values'linux','mac','windows'}}stages{stage('build'){// ...}stage('test'){// ...}stage('deploy'){// ...}}}`
`matrix{axes{axis{name'PLATFORM'values'linux','mac','windows'}}stages{stage('build'){// ...}stage('test'){// ...}stage('deploy'){// ...}}}`
`matrix{axes{axis{name'PLATFORM'values'linux','mac','windows'}axis{name'BROWSER'values'chrome','edge','firefox','safari'}}stages{stage('build-and-test'){// ...}}}`
`matrix{axes{axis{name'PLATFORM'values'linux','mac','windows'}axis{name'BROWSER'values'chrome','edge','firefox','safari'}}stages{stage('build-and-test'){// ...}}}`

## excludes (optional)

The optionalexcludessection lets authors specify one or moreexcludefilter expressions that select cells to be excluded from the expanded set of matrix cells (aka, sparsening).
Filters are constructed using a basic directive structure of one or more of excludeaxisdirectives each with anameandvalueslist.
Theaxisdirectives inside anexcludegenerate a set of combinations (similar to generating the matrix cells).
The matrix cells that match all the values from anexcludecombination are removed from the matrix.
If more than oneexcludedirective is supplied, each is evaluated separately to remove cells.
When dealing with a long list of values to exclude, excludeaxisdirectives can usenotValuesinstead ofvalues.
These will exclude cells thatdo notmatch one of the values passed tonotValues.
`matrix{axes{axis{name'PLATFORM'values'linux','mac','windows'}axis{name'BROWSER'values'chrome','edge','firefox','safari'}axis{name'ARCHITECTURE'values'32-bit','64-bit'}}excludes{exclude{axis{name'PLATFORM'values'mac'}axis{name'ARCHITECTURE'values'32-bit'}}}// ...}`
`matrix{axes{axis{name'PLATFORM'values'linux','mac','windows'}axis{name'BROWSER'values'chrome','edge','firefox','safari'}axis{name'ARCHITECTURE'values'32-bit','64-bit'}}excludes{exclude{axis{name'PLATFORM'values'mac'}axis{name'ARCHITECTURE'values'32-bit'}}}// ...}`
Exclude thelinux, safaricombination and exclude any platform that isnotwindowswith theedgebrowser.
`linux, safari`
`matrix{axes{axis{name'PLATFORM'values'linux','mac','windows'}axis{name'BROWSER'values'chrome','edge','firefox','safari'}axis{name'ARCHITECTURE'values'32-bit','64-bit'}}excludes{exclude{// 4 cellsaxis{name'PLATFORM'values'mac'}axis{name'ARCHITECTURE'values'32-bit'}}exclude{// 2 cellsaxis{name'PLATFORM'values'linux'}axis{name'BROWSER'values'safari'}}exclude{// 3 more cells and '32-bit, mac' (already excluded)axis{name'PLATFORM'notValues'windows'}axis{name'BROWSER'values'edge'}}}// ...}`
`matrix{axes{axis{name'PLATFORM'values'linux','mac','windows'}axis{name'BROWSER'values'chrome','edge','firefox','safari'}axis{name'ARCHITECTURE'values'32-bit','64-bit'}}excludes{exclude{// 4 cellsaxis{name'PLATFORM'values'mac'}axis{name'ARCHITECTURE'values'32-bit'}}exclude{// 2 cellsaxis{name'PLATFORM'values'linux'}axis{name'BROWSER'values'safari'}}exclude{// 3 more cells and '32-bit, mac' (already excluded)axis{name'PLATFORM'notValues'windows'}axis{name'BROWSER'values'edge'}}}// ...}`

## Matrix cell-level directives (optional)

Matrix lets users efficiently configure the overall environment for each cell, by adding stage-level directives undermatrixitself.
These directives behave the same as they would on a stage but they can also accept values provided by the matrix for each cell.
Theaxisandexcludedirectives define the static set of cells that make up the matrix.
That set of combinations is generated before the start of the pipeline run.
The "per-cell" directives, on the other hand, are evaluated at runtime.
These directives include:
environment
environment
`pipeline{parameters{choice(name:'PLATFORM_FILTER',choices:['all','linux','windows','mac'],description:'Run on specific platform')}agentnonestages{stage('BuildAndTest'){matrix{agent{label"${PLATFORM}-agent"}when{anyOf{expression{params.PLATFORM_FILTER=='all'}expression{params.PLATFORM_FILTER==env.PLATFORM}}}axes{axis{name'PLATFORM'values'linux','windows','mac'}axis{name'BROWSER'values'firefox','chrome','safari','edge'}}excludes{exclude{axis{name'PLATFORM'values'linux'}axis{name'BROWSER'values'safari'}}exclude{axis{name'PLATFORM'notValues'windows'}axis{name'BROWSER'values'edge'}}}stages{stage('Build'){steps{echo"Do Build for ${PLATFORM} - ${BROWSER}"}}stage('Test'){steps{echo"Do Test for ${PLATFORM} - ${BROWSER}"}}}}}}}`
`pipeline{parameters{choice(name:'PLATFORM_FILTER',choices:['all','linux','windows','mac'],description:'Run on specific platform')}agentnonestages{stage('BuildAndTest'){matrix{agent{label"${PLATFORM}-agent"}when{anyOf{expression{params.PLATFORM_FILTER=='all'}expression{params.PLATFORM_FILTER==env.PLATFORM}}}axes{axis{name'PLATFORM'values'linux','windows','mac'}axis{name'BROWSER'values'firefox','chrome','safari','edge'}}excludes{exclude{axis{name'PLATFORM'values'linux'}axis{name'BROWSER'values'safari'}}exclude{axis{name'PLATFORM'notValues'windows'}axis{name'BROWSER'values'edge'}}}stages{stage('Build'){steps{echo"Do Build for ${PLATFORM} - ${BROWSER}"}}stage('Test'){steps{echo"Do Test for ${PLATFORM} - ${BROWSER}"}}}}}}}`
Declarative Pipelines may use all the available steps documented in thePipeline Steps reference, which contains a comprehensive list of steps, with the addition of the steps listed below which areonly supportedin Declarative Pipeline.
Thescriptstep takes a block ofScripted Pipelineand executes that in the Declarative Pipeline.
For most use-cases, thescriptstep should be unnecessary in Declarative Pipelines, but it can provide a useful "escape hatch".scriptblocks of non-trivial size and/or complexity should be moved intoShared Librariesinstead.
`pipeline{agentanystages{stage('Example'){steps{echo'Hello World'script{defbrowsers=['chrome','firefox']for(inti=0;i<browsers.size();++i){echo"Testing the ${browsers[i]} browser"}}}}}}`
`pipeline{agentanystages{stage('Example'){steps{echo'Hello World'script{defbrowsers=['chrome','firefox']for(inti=0;i<browsers.size();++i){echo"Testing the ${browsers[i]} browser"}}}}}}`

## Scripted Pipeline

Scripted Pipeline, likeDeclarative Pipeline, is built on top of the underlying Pipeline sub-system.
Unlike Declarative, Scripted Pipeline is effectively a general-purpose DSL[1]built withGroovy.
Most functionality provided by the Groovy language is made available to users of Scripted Pipeline, which means it can be a very expressive and flexible tool with which one can author continuous delivery pipelines.

## Flow Control

Scripted Pipeline is serially executed from the top of aJenkinsfiledownwards, like most traditional scripts in Groovy or other languages.
Providing flow control, therefore, rests on Groovy expressions, such as theif/elseconditionals, for example:
`Jenkinsfile`
`node{stage('Example'){if(env.BRANCH_NAME=='master'){echo'I only execute on the master branch'}else{echo'I execute elsewhere'}}}`
`node{stage('Example'){if(env.BRANCH_NAME=='master'){echo'I only execute on the master branch'}else{echo'I execute elsewhere'}}}`
Another way Scripted Pipeline flow control can be managed is with Groovy’s exception handling support.
WhenStepsfail for whatever reason they throw an exception.
Handling behaviors on-error must make use of thetry/catch/finallyblocks in Groovy, for example:
`try/catch/finally`
`node{stage('Example'){try{sh'exit 1'}catch(exc){echo'Something failed, I should sound the klaxons!'throw}}}`
`node{stage('Example'){try{sh'exit 1'}catch(exc){echo'Something failed, I should sound the klaxons!'throw}}}`
As discussed at thestart of this chapter, the most fundamental part of a Pipeline is the "step".
Fundamentally, steps tell Jenkinswhatto do and serve as the basic building block for both Declarative and Scripted Pipeline syntax.
Scripted Pipeline doesnotintroduce any steps which are specific to its syntax;Pipeline Steps referencecontains a comprehensive list of steps provided by Pipeline and plugins.

## Differences from plain Groovy

In order to providedurability, which means that running Pipelines can survive a restart of the Jenkinscontroller, Scripted Pipeline must serialize data back to the controller.
Due to this design requirement, some Groovy idioms such ascollection.each { item → /* perform operation */ }are not fully supported.
Refer toJENKINS-27421andJENKINS-26481for more information.
`collection.each { item → /* perform operation */ }`

## Syntax Comparison

This video shares some differences between Scripted and Declarative Pipeline syntax.
When Jenkins Pipeline was first created, Groovy was selected as the foundation.
Jenkins has long shipped with an embedded Groovy engine to provide advanced scripting capabilities for admins and users alike.
Additionally, the implementors of Jenkins Pipeline found Groovy to be a solid foundation upon which to build what is now referred to as the "Scripted Pipeline" DSL.[1].
As it is a fully-featured programming environment, Scripted Pipeline offers a tremendous amount of flexibility and extensibility to Jenkins users.
The Groovy learning-curve isn’t typically desirable for all members of a given team, so Declarative Pipeline was created to offer a simpler and more opinionated syntax for authoring Jenkins Pipeline.
Both are fundamentally the same Pipeline sub-system underneath.
They are both durable implementations of "Pipeline as code".
They are both able to use steps built into Pipeline or provided by plugins.
Both are able to utilizeShared Libraries
Where they differ however is in syntax and flexibility.
Declarative limits what is available to the user with a more strict and pre-defined structure, making it an ideal choice for simpler continuous delivery pipelines.
Scripted provides very few limits, insofar that the only limits on structure and syntax tend to be defined by Groovy itself, rather than any Pipeline-specific systems, making it an ideal choice for power-users and those with more complex
requirements.
As the name implies, Declarative Pipeline encourages a declarative programming model.[2]Whereas Scripted Pipelines follow a more imperative programming model.[3]