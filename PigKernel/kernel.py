# coding: utf8

# Copyright (C) 2016 NOUCHET Christophe
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.

from ipykernel.kernelbase import Kernel
import pexpect
import os

# Author : Christophe NOUCHET
# Email : nouchet.christophe@gmail.com
# Information :     Don't be disturb by ';' at the end of my lines, just an automatism from C/C++.

GRUNT_NEW_LINE_MODEL = r"grunt> ";
GRUNT_NEW_LINE_MODEL_INDEX = 0;
GRUNT_CONTINUE_LINE_MODEL = r">> ";
GRUNT_CONTINUE_LINE_MODEL_INDEX = 1;
GRUNT_START_TIMEOUT = 60 * 5;
GRUNT_BLOC_TIMEOUT =  60 * 5;
GRUNT_TIMEOUT = None;
GRUNT_SEPARATOR = [GRUNT_NEW_LINE_MODEL, GRUNT_CONTINUE_LINE_MODEL];
EXECUTE_JUPYTER_BLOC_START = "--JUPYTER_KERNEL_START--";
EXECUTE_JUPYTER_BLOC_STOP = "--JUPYTER_KERNEL_STOP--";

class PigKernel(Kernel):
    """
    A simple Pig kernel for Jupyter
    """
    implementation = 'Pig Kernel';
    implementation_version = '0.1';
    language = 'pig';
    language_version = '0.15';
    language_info = {
        'name': "pig",
        'mimetype': 'text/x-pig',
        'file_extension': '.pig'
    };
    banner = "Pig Kernel";

    def __init__(self, **kwargs):
        """
        Constructor
        """
        Kernel.__init__(self, **kwargs);
        opt = "";
        if "LOG4J_CONF_FILE" in os.environ:
            opt += " -4 " + os.environ["LOG4J_CONF_FILE"];
        # Start grunt
        self.pig = pexpect.spawn("/opt/pig-0.15.0/bin/pig -x local " + opt);

        # Wait until grunt start
        self.pig.expect(GRUNT_NEW_LINE_MODEL, timeout=GRUNT_START_TIMEOUT);

    def remove_command(self, codeline, data):
        """
        Erase the line enter in the grunt in the data
        """
        lines = data.split('\n');
        entete = self.erase_code_line(codeline, lines[0] + "\n");
        if entete == "" or entete == "\r":
            entete = "";
        if len(lines) > 1:
            temp = '\n'.join(lines[1:]);
        else:
            temp = "";
        return entete + temp;

    def erase_code_line(self, codeline, data):
        """
        Erase the line enter in the grunt
        """
        if codeline != "":
            return data.replace(codeline + "\x0d\x0a", '').replace(codeline + "\x0a", '').replace(codeline + "\x0d", '').replace(codeline, '');

    def pre_command(self):
        """
        Send a start line to grunt
        """
        # Begin the bloc
        self.pig.sendline(';');
        self.pig.sendline(EXECUTE_JUPYTER_BLOC_START);
        self.pig.expect(EXECUTE_JUPYTER_BLOC_START);

        #self.pig.sendline(';');
        self.pig.expect(GRUNT_NEW_LINE_MODEL, timeout=GRUNT_BLOC_TIMEOUT);

    def post_command(self, silent):
        """
        Send a stop line to grunt and ensure that no lost line is active on grunt
        """
        # Send an end bloc
        self.pig.sendline(';');
        self.pig.expect(GRUNT_NEW_LINE_MODEL);
        if not silent:
            temp = self.pig.before.decode('utf-8').strip();
            if temp != ";":
                stream_content = {'name': 'stdout', 'text': "C est moi qui t est ramassé" + temp};
                self.send_response(self.iopub_socket, 'stream', stream_content);
        self.pig.sendline(';');
        self.pig.sendline(EXECUTE_JUPYTER_BLOC_STOP);
        self.pig.expect(EXECUTE_JUPYTER_BLOC_STOP);

    def fix_empty_result(self, silent):
        """
        Send a empty message to jupyter for fixing an empty reponse
        """
        if not silent:
            stream_content = {'name': 'stdout', 'text': "\x00" };
            self.send_response(self.iopub_socket, 'stream', stream_content);

    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):
        """
        Execute a cell
        """

        # Send a block request
        self.pre_command();

        # Fix for empty result
        self.fix_empty_result(silent);

        try:
            for line in code.split("\n"):
                # The working line
                working_line = line.strip();

                # Send the line to grunt
                self.pig.sendline(working_line);
                index = self.pig.expect(GRUNT_SEPARATOR, timeout=GRUNT_TIMEOUT);

                if not silent:
                    # Erase the line enter to the grunt shell
                    data = self.remove_command(working_line, self.pig.before.decode('utf-8'));

                    # Send it to jupyter front
                    stream_content = {'name': 'stdout', 'text': data };
                    self.send_response(self.iopub_socket, 'stream', stream_content);

                # If is the end of a command, isolate it from other command
                if index == GRUNT_NEW_LINE_MODEL_INDEX:
                    self.post_command(silent);
                    self.pre_command();

            # Send a end of a command
            self.post_command(silent);

        except Exception as e:
            stream_content = {'name': 'stderr', 'text': str(e) };
            self.send_response(self.iopub_socket, 'stream', stream_content);
            return {'status': 'error',
                    # The base class increments the execution count
                    'execution_count': self.execution_count,
                    'payload': [],
                    'user_expressions': {},
                   };
        return {'status': 'ok',
                # The base class increments the execution count
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {},
               };


if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=PigKernel)
