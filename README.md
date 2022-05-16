# MonitoraPA
Monitoring system for GDPR compliance of Public Administrations

Telegram: https://t.me/monitoraPA   
[Element/Matrix](https://element.io): https://matrix.to/#/%23MonitoraPA:matrix.opencloud.lu

# Project Organization

MonitoraPA is composed of several components.

- A command line interface (in Python3) to run various automatic GDPR
  compliance checks on several Public Administrations and to automate
  some statistics and notifications to proper authorities in [cli/](./cli/),
  as specified in [SPECIFICATION.md](./cli/SPECIFICATION.md) and
  documented in [MANUAL.md](./cli/MANUAL.md)
  
- A catalogue of compliance checks (in JavaScript, run by Selenium)
  in [check/](./check/).
  
- A minimal website about the project in [web/](./web/)

- Some datasets to further extend the reach and impact of the project
  in [datasets/](./datasets/)

# Authors, Copyright and Licensing

MonitoraPA has been created by several [AUTHORS](./AUTHORS.md).

It's brought to you under the [Hacking License](./LICENSE.txt) that, as
an explicit wrap contract between you and the authors, must also be
applied to all dependant and derivative works (including the outputs
you produce running the system), recursively.

You cannot mix (A)GPL code with hacks covered by the Hacking License.

# Coding Guidelines

Code like if your hack should be maintained by a child who
just learned how to code.

Do NOT try to solve problems that you haven't measured before.

Do NOT apply "enterprise best practice". We are not a company.  
Do NOT try to show us how smart you are. We don't give a shit.

Avoid dependencies.

Use good sense... but remember: it's not common.
