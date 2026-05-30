
## Getting started with Pipeline

Prerequisites
Defining a PipelineThrough Blue OceanThrough the classic UIIn SCM
Through Blue Ocean
Through the classic UI
Built-in DocumentationSnippet GeneratorGlobal Variable ReferenceDeclarative Directive Generator
Snippet Generator
Global Variable Reference
Declarative Directive Generator
Further ReadingAdditional Resources
Additional Resources
As mentionedpreviously, Jenkins Pipeline is a suite of
plugins that supports implementing and integrating continuous delivery pipelines
into Jenkins. Pipeline provides an extensible set of tools for modeling
simple-to-complex delivery pipelines "as code" via the Pipeline DSL.[1]
This section describes how to get started with creating your Pipeline project in
Jenkins and introduces you to the various ways that aJenkinsfilecan be
created and stored.
`Jenkinsfile`

## Prerequisites

To use Jenkins Pipeline, you will need:
Jenkins 2.x or later (older versions back to 1.642.3 may work but are not
recommended)
Jenkins 2.x or later (older versions back to 1.642.3 may work but are not
recommended)
Pipeline plugin,[2]which is installed as part of the "suggested plugins" (specified when running
through thePost-installation setup wizardafterinstalling Jenkins).
Pipeline plugin,[2]which is installed as part of the "suggested plugins" (specified when running
through thePost-installation setup wizardafterinstalling Jenkins).
Read more about how to install and manage plugins inManaging Plugins.

## Defining a Pipeline

BothDeclarative and Scripted Pipelineare DSLs[1]to describe portions of your software delivery
pipeline. Scripted Pipeline is written in a limited form ofGroovy syntax.
Relevant components of Groovy syntax will be introduced as required throughout
this documentation, so while an understanding of Groovy is helpful, it is not
required to work with Pipeline.
A Pipeline can be created in one of the following ways:
Through Blue Ocean- after setting up a Pipeline project in Blue Ocean,
the Blue Ocean UI helps you write your Pipeline’sJenkinsfileand commit it
to source control.
Through Blue Ocean- after setting up a Pipeline project in Blue Ocean,
the Blue Ocean UI helps you write your Pipeline’sJenkinsfileand commit it
to source control.
`Jenkinsfile`
Through the classic UI- you can enter a basic Pipeline directly in
Jenkins through the classic UI.
Through the classic UI- you can enter a basic Pipeline directly in
Jenkins through the classic UI.
In SCM- you can write aJenkinsfilemanually, which you can commit to your project’s source control repository.[3]
In SCM- you can write aJenkinsfilemanually, which you can commit to your project’s source control repository.[3]
`Jenkinsfile`
The syntax for defining a Pipeline with either approach is the same, but while
Jenkins supports entering Pipeline directly into the classic UI, it is
generally considered best practice to define the Pipeline in aJenkinsfilewhich Jenkins will then load directly from source control.
`Jenkinsfile`
This video provides basic instructions on how to write both Declarative and Scripted Pipelines.

## Through Blue Ocean

If you are new to Jenkins Pipeline, the Blue Ocean UI helps youset up your Pipeline project, and
automatically creates and writes your Pipeline (i.e. theJenkinsfile) for you
through the graphical Pipeline editor.
`Jenkinsfile`
As part of setting up your Pipeline project in Blue Ocean, Jenkins configures a
secure and appropriately authenticated connection to your project’s source
control repository. Therefore, any changes you make to theJenkinsfilevia
Blue Ocean’s Pipeline editor are automatically saved and committed to source
control.
`Jenkinsfile`
Read more about Blue Ocean in theBlue Oceanchapter andGetting started with Blue Oceanpage.
Blue Ocean will be deprecated in July 2026.
It will not receive further security fixes or functionality updates.
ThePipeline syntax snippet generatorassists users as they define Pipeline steps with their arguments.
It is the preferred tool for Jenkins Pipeline creation, as it provides online help for the Pipeline steps available in your Jenkins controller.
It uses the plugins installed on your Jenkins controller to generate the Pipeline syntax.
Refer to thePipeline steps referencepage for information on all available Pipeline steps.

## Through the classic UI

AJenkinsfilecreated using the classic UI is stored by Jenkins itself (within
the Jenkins home directory).
`Jenkinsfile`
To create a basic Pipeline through the Jenkins classic UI:
If required, ensure you are logged in to Jenkins.
If required, ensure you are logged in to Jenkins.
From the Jenkins Dashboard, selectNew Item.
From the Jenkins Dashboard, selectNew Item.
In theEnter an item namefield, specify the name for your new Pipeline
project.Caution:Jenkins uses this item name to create directories on disk. It is
recommended to avoid using spaces in item names, since doing so may uncover
bugs in scripts that do not properly handle spaces in directory paths.
In theEnter an item namefield, specify the name for your new Pipeline
project.Caution:Jenkins uses this item name to create directories on disk. It is
recommended to avoid using spaces in item names, since doing so may uncover
bugs in scripts that do not properly handle spaces in directory paths.
Scroll down and clickPipeline, then clickOKat the end of the page to
open the Pipeline configuration page (whoseGeneraltab is selected).
Scroll down and clickPipeline, then clickOKat the end of the page to
open the Pipeline configuration page (whoseGeneraltab is selected).
Click thePipelinetab in the side panel of the page to scroll down to thePipelinesection.Note:If instead you are defining yourJenkinsfilein source control,
follow the instructions inIn SCMbelow.
Click thePipelinetab in the side panel of the page to scroll down to thePipelinesection.Note:If instead you are defining yourJenkinsfilein source control,
follow the instructions inIn SCMbelow.
`Jenkinsfile`
In thePipelinesection, ensure that theDefinitionfield indicates thePipeline scriptoption.
In thePipelinesection, ensure that theDefinitionfield indicates thePipeline scriptoption.
Enter your Pipeline code into theScripttext area.For instance, copy the following Declarative example Pipeline code (below theJenkinsfile ( …​ )heading) or its Scripted version equivalent and paste
this into theScripttext area. (The Declarative example below is used
throughout the remainder of this procedure.)Jenkinsfile (Declarative Pipeline)pipeline {
    agent any(1)stages {
        stage('Stage 1') {
            steps {
                echo'Hello world!'(2)}
        }
    }
}Toggle Scripted Pipeline(Advanced)Jenkinsfile (Scripted Pipeline)node {(3)stage('Stage 1') {
        echo'Hello World'(2)}
}1agentinstructs Jenkins to allocate an executor (on any available
agent/node in the Jenkins environment) and workspace for the entire Pipeline.2echowrites simple string in the console output.3nodeeffectively does the same asagent(above).Note:You can also select from cannedScriptedPipeline examples from thetry sample Pipelineoption at the top right of theScripttext area. Be
aware that there are no canned Declarative Pipeline examples available from this
field.
Enter your Pipeline code into theScripttext area.For instance, copy the following Declarative example Pipeline code (below theJenkinsfile ( …​ )heading) or its Scripted version equivalent and paste
this into theScripttext area. (The Declarative example below is used
throughout the remainder of this procedure.)
`pipeline {
    agent any(1)stages {
        stage('Stage 1') {
            steps {
                echo'Hello world!'(2)}
        }
    }
}`
`pipeline {
    agent any(1)stages {
        stage('Stage 1') {
            steps {
                echo'Hello world!'(2)}
        }
    }
}`
`node {(3)stage('Stage 1') {
        echo'Hello World'(2)}
}`
`node {(3)stage('Stage 1') {
        echo'Hello World'(2)}
}`
Note:You can also select from cannedScriptedPipeline examples from thetry sample Pipelineoption at the top right of theScripttext area. Be
aware that there are no canned Declarative Pipeline examples available from this
field.
ClickSaveto open the Pipeline project/item view page.
ClickSaveto open the Pipeline project/item view page.
On this page, clickBuild Nowon the left to run the Pipeline.
On this page, clickBuild Nowon the left to run the Pipeline.
UnderBuild Historyon the left, click#1to access the details for this
particular Pipeline run.
UnderBuild Historyon the left, click#1to access the details for this
particular Pipeline run.
ClickConsole Outputto see the full output from the Pipeline run. The
following output shows a successful run of your Pipeline.Notes:You can also access the console output directly from the Dashboard by clicking
the colored globe to the left of the build number (e.g.#1).Defining a Pipeline through the classic UI is convenient for testing Pipeline
code snippets, or for handling simple Pipelines or Pipelines that do not
require source code to be checked out/cloned from a repository. As mentioned
above, unlikeJenkinsfiles you define through Blue Ocean
(above) or in source control
(below),Jenkinsfiles entered into
theScripttext area of Pipeline projects are stored by Jenkins itself,
within the Jenkins home directory. Therefore, for greater control and
flexibility over your Pipeline, particularly for projects in source control
that are likely to gain complexity, it is recommended that you useBlue Oceanorsource controlto define yourJenkinsfile.
ClickConsole Outputto see the full output from the Pipeline run. The
following output shows a successful run of your Pipeline.
You can also access the console output directly from the Dashboard by clicking
the colored globe to the left of the build number (e.g.#1).
You can also access the console output directly from the Dashboard by clicking
the colored globe to the left of the build number (e.g.#1).
Defining a Pipeline through the classic UI is convenient for testing Pipeline
code snippets, or for handling simple Pipelines or Pipelines that do not
require source code to be checked out/cloned from a repository. As mentioned
above, unlikeJenkinsfiles you define through Blue Ocean
(above) or in source control
(below),Jenkinsfiles entered into
theScripttext area of Pipeline projects are stored by Jenkins itself,
within the Jenkins home directory. Therefore, for greater control and
flexibility over your Pipeline, particularly for projects in source control
that are likely to gain complexity, it is recommended that you useBlue Oceanorsource controlto define yourJenkinsfile.
Defining a Pipeline through the classic UI is convenient for testing Pipeline
code snippets, or for handling simple Pipelines or Pipelines that do not
require source code to be checked out/cloned from a repository. As mentioned
above, unlikeJenkinsfiles you define through Blue Ocean
(above) or in source control
(below),Jenkinsfiles entered into
theScripttext area of Pipeline projects are stored by Jenkins itself,
within the Jenkins home directory. Therefore, for greater control and
flexibility over your Pipeline, particularly for projects in source control
that are likely to gain complexity, it is recommended that you useBlue Oceanorsource controlto define yourJenkinsfile.
`Jenkinsfile`
`Jenkinsfile`
`Jenkinsfile`
Complex Pipelines are difficult to write and maintain within theclassic UI’sScripttext area of the Pipeline
configuration page.
To make this easier, your Pipeline’sJenkinsfilecan be written in a text
editor or integrated development environment (IDE) and committed to source
control[3](optionally with the application code that Jenkins
will build). Jenkins can then check out yourJenkinsfilefrom source control
as part of your Pipeline project’s build process and then proceed to execute
your Pipeline.
`Jenkinsfile`
`Jenkinsfile`
To configure your Pipeline project to use aJenkinsfilefrom source control:
`Jenkinsfile`
Follow the procedure above for defining your Pipelinethrough the classic UIuntil you reach step 5
(accessing thePipelinesection on the Pipeline configuration page).
Follow the procedure above for defining your Pipelinethrough the classic UIuntil you reach step 5
(accessing thePipelinesection on the Pipeline configuration page).
From theDefinitionfield, choose thePipeline script from SCMoption.
From theDefinitionfield, choose thePipeline script from SCMoption.
From theSCMfield, choose the type of source control system of the
repository containing yourJenkinsfile.
From theSCMfield, choose the type of source control system of the
repository containing yourJenkinsfile.
`Jenkinsfile`
Using Git as your Source Code Management (SCM) requires the Git plugin to be installed.
In most Jenkins installations, this plugin is included by default.
Using Git as your Source Code Management (SCM) requires the Git plugin to be installed.
In most Jenkins installations, this plugin is included by default.
Complete the fields specific to your repository’s source control system.Tip:If you are uncertain of what value to specify for a given field, click
its?icon to the right for more information.
Complete the fields specific to your repository’s source control system.Tip:If you are uncertain of what value to specify for a given field, click
its?icon to the right for more information.
In theScript Pathfield, specify the location (and name) of yourJenkinsfile. This location is the one that Jenkins checks out/clones the
repository containing yourJenkinsfile, which should match that of the
repository’s file structure. The default value of this field assumes that yourJenkinsfileis named "Jenkinsfile" and is located at the root of the
repository.
In theScript Pathfield, specify the location (and name) of yourJenkinsfile. This location is the one that Jenkins checks out/clones the
repository containing yourJenkinsfile, which should match that of the
repository’s file structure. The default value of this field assumes that yourJenkinsfileis named "Jenkinsfile" and is located at the root of the
repository.
`Jenkinsfile`
`Jenkinsfile`
`Jenkinsfile`
When you update the designated repository, a new build is triggered, as long as
the Pipeline is configured with an SCM polling trigger.
Since Pipeline code (i.e. Scripted Pipeline in particular) is written in
Groovy-like syntax, if your IDE is not correctly syntax highlighting yourJenkinsfile, try inserting the line#!/usr/bin/env groovyat the top of theJenkinsfile,[4][5]which may rectify the issue.
`Jenkinsfile`
`#!/usr/bin/env groovy`
`Jenkinsfile`

## Built-in Documentation

Pipeline ships with built-in documentation features to make it
easier to create Pipelines of varying complexities. This built-in documentation
is automatically generated and updated based on the plugins installed in the
Jenkins controller.
The built-in documentation can be found globally at${YOUR_JENKINS_URL}/pipeline-syntax.
The same documentation is also linked asPipeline Syntaxin the side-bar for any
configured Pipeline project.
`${YOUR_JENKINS_URL}/pipeline-syntax`

## Snippet Generator

The built-in "Snippet Generator" utility is helpful for creating bits of
code for individual steps, discovering new steps provided by plugins, or
experimenting with different parameters for a particular step.
The Snippet Generator is dynamically populated with a list of the steps
available to the Jenkins controller. The number of steps available is dependent
on the plugins installed which explicitly expose steps for use in Pipeline.
To generate a step snippet with the Snippet Generator:
Navigate to thePipeline Syntaxlink (referenced above) from a configured Pipeline, or at${YOUR_JENKINS_URL}/pipeline-syntax.
Navigate to thePipeline Syntaxlink (referenced above) from a configured Pipeline, or at${YOUR_JENKINS_URL}/pipeline-syntax.
`${YOUR_JENKINS_URL}/pipeline-syntax`
Select the desired step in theSample Stepdropdown menu
Select the desired step in theSample Stepdropdown menu
Use the dynamically populated area below theSample Stepdropdown to configure the selected step.
Use the dynamically populated area below theSample Stepdropdown to configure the selected step.
ClickGenerate Pipeline Scriptto create a snippet of Pipeline which can be
copied and pasted into a Pipeline.
ClickGenerate Pipeline Scriptto create a snippet of Pipeline which can be
copied and pasted into a Pipeline.
To access additional information and/or documentation about the step selected,
click on the help icon (indicated by the red arrow in the image above).

## Global Variable Reference

In addition to the Snippet Generator, which only surfaces steps, Pipeline also
provides a built-in "Global Variable Reference." Like the Snippet Generator,
it is also dynamically populated by plugins. Unlike the Snippet Generator
however, the Global Variable Reference only contains documentation forvariablesprovided by Pipeline or plugins, which are available for
Pipelines.
The variables provided by default in Pipeline are:
Exposes environment variables, for example:env.PATHorenv.BUILD_ID. Consult the built-in global variable reference at${YOUR_JENKINS_URL}/pipeline-syntax/globals#envfor a complete, and up to date, list of environment variables
available in Pipeline.
`env.BUILD_ID`
`${YOUR_JENKINS_URL}/pipeline-syntax/globals#env`
Exposes all parameters defined for the Pipeline as a read-onlyMap,
for example:params.MY_PARAM_NAME.
`params.MY_PARAM_NAME`
May be used to discover information about the currently executing Pipeline,
with properties such ascurrentBuild.result,currentBuild.displayName,
etc. Consult the built-in global variable reference at${YOUR_JENKINS_URL}/pipeline-syntax/globalsfor a complete, and up to date, list of properties available oncurrentBuild.
`currentBuild.result`
`currentBuild.displayName`
`${YOUR_JENKINS_URL}/pipeline-syntax/globals`
`currentBuild`
This video reviews using thecurrentBuildvariable in Jenkins Pipeline.
`currentBuild`

## Declarative Directive Generator

While the Snippet Generator helps with generating steps for a Scripted
Pipeline or for thestepsblock in astagein a Declarative Pipeline, it
does not cover thesectionsanddirectivesused to define a Declarative Pipeline.
The "Declarative Directive Generator" utility helps with that.
Similar to theSnippet Generator, the Directive Generator allows you
to choose a Declarative directive, configure it in a form, and generate the
configuration for that directive, which you can then use in your Declarative Pipeline.
To generate a Declarative directive using the Declarative Directive Generator:
Navigate to thePipeline Syntaxlink (referenced above) from a configured Pipeline,
and then click on theDeclarative Directive Generatorlink in the sidepanel,
or go directly to${YOUR_JENKINS_URL}/directive-generator.
Navigate to thePipeline Syntaxlink (referenced above) from a configured Pipeline,
and then click on theDeclarative Directive Generatorlink in the sidepanel,
or go directly to${YOUR_JENKINS_URL}/directive-generator.
`${YOUR_JENKINS_URL}/directive-generator`
Select the desired directive in the dropdown menu
Select the desired directive in the dropdown menu
Use the dynamically populated area below the dropdown to configure the selected directive.
Use the dynamically populated area below the dropdown to configure the selected directive.
ClickGenerate Directiveto create the directive’s configuration to copy
into your Pipeline.
ClickGenerate Directiveto create the directive’s configuration to copy
into your Pipeline.
The Directive Generator can generate configuration for nested directives,
such as conditions inside awhendirective, but it cannot generate Pipeline steps.
For the contents of directives which contain steps,
such asstepsinside astageor conditions likealwaysorfailureinsidepost,
the Directive Generator adds a placeholder comment instead.
You will still need to add steps to your Pipeline by hand.
`stage('Stage 1') {
    steps {// One or more steps need to be included within the steps block.}
}`
`stage('Stage 1') {
    steps {// One or more steps need to be included within the steps block.}
}`

## Further Reading

This section merely scratches the surface of what can be done with Jenkins
Pipeline, but should provide enough of a foundation for you to start
experimenting with a test Jenkins controller.
In the next section,The Jenkinsfile, more Pipeline steps
will be discussed along with patterns for implementing successful, real-world,
Jenkins Pipelines.

## Additional Resources

Pipeline Steps Reference,
encompassing all steps provided by plugins distributed in the Jenkins Update
Center.
Pipeline Steps Reference,
encompassing all steps provided by plugins distributed in the Jenkins Update
Center.
Pipeline Examples, a
community-curated collection of copyable Pipeline examples.
Pipeline Examples, a
community-curated collection of copyable Pipeline examples.