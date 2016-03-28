# Author

NOUCHET Christophe <nouchet.christophe@gmail.com>

# Version

0.1.0

# License

Copyright (C) 2016 NOUCHET Christophe


This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.


This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.


You should have received a copy of the GNU General Public License along
with this program. If not, see <http://www.gnu.org/licenses/>.

# Introduction

A simple Pig kernel for Jupyter

# Installation

## Install the PigKernel

```bash
$ python setup.py install
```

## Modify the environment parameter in pig_kernel/kernel.json

vim pig_kernel/kernel.json

```json
{
    ...
    "env": {
        "JAVA_HOME": "/usr/lib/jvm/java-7-openjdk-amd64",
        "PIG_HOME": "/opt/pig-0.15.0",
        "HADOOP_HOME": "/opt/hadoop-2.6.4",
        "LOG4J_CONF_FILE": "/root/log4j.properties"
    }
    ...
}
```

** Specify a log4j.properties is important if you don't want to have all logs in Jupyter **

The log4j.properties could look like avaible in examples/log4j.properties:

```
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

# ***** Set root logger level to DEBUG and its only appender to A.
log4j.logger.org.apache.pig=ERROR, A
log4j.logger.org.apache.hadoop = ERROR, A

# ***** A is set to be a ConsoleAppender.
log4j.appender.A=org.apache.log4j.ConsoleAppender
# ***** A uses PatternLayout.
log4j.appender.A.layout=org.apache.log4j.PatternLayout
log4j.appender.A.layout.ConversionPattern=%-4r [%t] %-5p %c %x - %m%n
```

## Install the kernel

```bash
$ jupyter-kernelspec install pig_kernel
[InstallKernelSpec] Installed kernelspec pig_kernel in /usr/local/share/jupyter/kernels/pig_kernel
```
