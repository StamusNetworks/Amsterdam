#!/usr/bin/env python
# Copyright (C) 2015 Stamus Networks
#
# You can copy, redistribute or modify this Program under the terms of
# the GNU General Public License version 3 as published by the Free
# Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# version 3 along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.


import os
import sys
import subprocess
import shutil
from string import Template

class Amsterdam:
    def __init__(self, name, iface, basepath):
        self.name = name
        self.iface = iface
        self.basepath = os.path.abspath(basepath)

    def get_sys_data_dirs(self, component):
        this_dir, this_filename = os.path.split(__file__)
        datadir = os.path.join(this_dir, component)
        return datadir

    def create_data_dirs(self):
        for directory in ['scirius', 'suricata', 'elasticsearch']:
            dir_path = os.path.join(self.basepath, directory)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

    def update_config(self):
        try:
            shutil.copytree(self.get_sys_data_dirs('config'), os.path.join(self.basepath, 'config'))
            shutil.copytree(self.get_sys_data_dirs('docker'), os.path.join(self.basepath, 'docker'))
        # FIXME
        except:
            sys.stderr.write("Unable to copy config files")
            pass

    def update_docker(self):
        dockertree = os.path.join(self.basepath, 'docker')
        if os.path.exists(dockertree):
            shutil.rmtree(dockertree)
        if os.path.exists(self.basepath):
            shutil.copytree(self.get_sys_data_dirs('docker'), dockertree)
    
    def generate_template(self, options):
        template_path = os.path.join(self.get_sys_data_dirs('templates'), 'docker-compose.yml.j2')
        with open(template_path, 'r') as amsterdam_file:
            # get the string and build template
            amsterdam_tmpl = amsterdam_file.read()
            amsterdam_config_tmpl = Template(amsterdam_tmpl)
        
            amsterdam_config = amsterdam_config_tmpl.substitute(options)
        
            with open(os.path.join(self.basepath, 'docker-compose.yml'), 'w') as amsterdam_compose_file:
                if sys.version < '3':
                    amsterdam_compose_file.write(amsterdam_config)
                else:
                    amsterdam_compose_file.write(bytes(amsterdam_grep, 'UTF-8'))
    
    def run_docker_compose(self, cmd, options = None):
        docker_cmd = ['docker-compose', '-p', self.name, '-f',
                      os.path.join(self.basepath, 'docker-compose.yml'), cmd]
        if options:
            docker_cmd.extend(options)
        return subprocess.call(docker_cmd)
    
    def setup(self, args):
        options = {}
        options['capture_option'] =  "--af-packet=%s" % args.iface
        options['basepath'] = self.basepath
        if args.verbose:
            sys.stdout.write("Generating docker compose file\n")
        self.create_data_dirs()
        self.update_config()
        self.generate_template(options)    
        return 0

    def start(self, args):
        if not os.path.exists(os.path.join(self.basepath, 'docker-compose.yml')):
            sys.stderr.write("'%s' directory does not exist or is empty, please run setup command\n" % (self.basepath))
            return False
        return self.run_docker_compose('up')

    def stop(self, args):
        return self.run_docker_compose('stop')

    def rm(self, args):
        self.stop(args)
        return self.run_docker_compose('rm')
    
    def restart(self, args):
        self.stop(None)
        self.start(None)
        return True

    def update(self, args):
        self.update_docker()
        self.run_docker_compose('pull')
        self.run_docker_compose('build', options = ['--no-cache'])
        return True
