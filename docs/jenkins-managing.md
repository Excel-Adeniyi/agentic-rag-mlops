
## Managing Jenkins

Configuring the System
Configuration as Code
Managing Tools
Managing Plugins
About Jenkins
System Information
Jenkins Features Controlled with System Properties
Change System Time Zone
Jenkins CLI
Script Console
Groovy Hook Scripts
Managing Nodes
In-process Script Approval
Themes for user interface
User Content
Spawning Processes From Build
System Configuration group
Security group
Status Information group
Troubleshooting group
Tools and Actions group
Uncategorized group
Most standard administrative tasks can be performed from the screens
in theManage Jenkinssection of the dashboard.
In this chapter, we look at these screens and explain how to use them.
The tiles displayed on theManage Jenkinspage are grouped logically.
Here we discuss the pages that are part of the standard installation.
Plugins may add pages to this screen.
The top of theManage Jenkinsscreen may contain "Monitors"
that alert you when a new version
of the Jenkins software or a security update is available.
Each monitor includes a description of the issue it is reporting and links to additional information about the issue
Inline help is available on mostManage Jenkinspages:
To access the help, select the?icon to the right of each field.
To access the help, select the?icon to the right of each field.
Click the?icon again to hide the help text.
Click the?icon again to hide the help text.
Other system administration topics are discussed inJenkins System Administration.

## System Configuration group

Screens for configuring resources for your Jenkins controller.
Configure global settings and paths for the Jenkins controller
Configure tools, their locations, and automatic installers
Add, update, remove, disable/enable plugins
that extend the functionality of Jenkins.
Add, remove, control, and monitor the nodes used for the agents on which build jobs run.
Configure your Jenkins controller using a human-readable YAML file rather than the UI.
This is an optional feature that appears in this group
only when the plugin is installed on your controller.

## Security group

Screens for configuring security features for your Jenkins controller.
SeeSecuring Jenkinsfor general information
about managing Jenkins security.
Set configuration parameters that secure your Jenkins controller.
Configure the credentials that provide secure access
to third-party sites and applications that interact with Jenkins.
Configure credential providers and types
Manage users defined in the Jenkins user database.
This is not used if you use a different security realm such as LDAP or AD.

## Status Information group

Displays information about the Jenkins environment.
Jenkins log that contains alljava.util.loggingoutput related to Jenkins.
`java.util.logging`
Displays information about resource utilization on you Jenkins controller.
Provides version and license information for your Jenkins controller.

## Troubleshooting group

Remove configuration information related to plugins that have been removed from the controller.

## Tools and Actions group

Screens for common management tasks
and management tools that enable you to do administrative tasks without using the UI.
Discard all data that is loaded in memory and reload everything from the file system.
This is useful when you modify configuration files directly on disk.
How to use the Jenkins CLI from a shell or script.
Execute an Apache Groovy script for administration, troubleshooting, and diagnostics.
Prevents new builds from starting so that the system can be shut down safely.
Displays a red banner with a custom message so that users know what is about to happen.
`/safeRestart`
`Restart Safely`

## Uncategorized group

Screens for plugins that have not yet declared the category of their page.