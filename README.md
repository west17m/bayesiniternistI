# Bayes 315 Team Project

![Screenshot](https://raw.githubusercontent.com/west17m/bayesiniternistI/master/screenshot.png)

This is the Bayesian implementation of InternistI knowledge base.

## Quickstart
1. pull from git
2. Log into (blackboard)(http://www.vanderbilt.edu/blackboard/)
  1. go to assignments>Decision Support Assignment
  2. download the following to [project]/data
    * Diseases_for_2015_decision_support_exercise_v03.txt
    * Findings_for_2015_decision_support_exercise_v03.txt
    * optionally the assignment instructions
3. run bayes.py from your command line or IDE

## Development Notes
* logging can be done with
  * self.logger.debug('debug message')
  * self.logger.info('info message')
  * self.logger.warn('warning message')
  * self.logger.error('error message')
* bayes.py --help will show contextual help
* dependencies: pandas
* @todo denotes tasks that need completed
* spacing for indention is set at two spaces

## Dependencies
* pandas
* numpy
* termcolor