#!/usr/bin/env python
# Copyright (C) 2015,2016 Stamus Networks
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
import re
import time
from string import Template
from OpenSSL import crypto
from socket import gethostname

AMSTERDAM_VERSION = "0.8"

class AmsterdamException(Exception):
    """
    Generic class for Amsterdam exception
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

class Amsterdam:
    def __init__(self, name, iface, basepath):
        self.name = name
        self.iface = iface
        self.basepath = os.path.abspath(basepath)
        self.check_environment()

    def get_sys_data_dirs(self, component):
        this_dir, this_filename = os.path.split(__file__)
        datadir = os.path.join(this_dir, component)
        return datadir

    def create_data_dirs(self):
        for directory in ['scirius', 'suricata', 'elasticsearch', 'backups']:
            dir_path = os.path.join(self.basepath, directory)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

    def update_files(self, source='docker'):
        sourcetree = os.path.join(self.basepath, source)
        if os.path.exists(sourcetree):
            shutil.rmtree(sourcetree)
        if os.path.exists(self.basepath):
            shutil.copytree(self.get_sys_data_dirs(source), sourcetree)

    def update_config(self):
        try:
            shutil.copytree(self.get_sys_data_dirs('config'), os.path.join(self.basepath, 'config'))
            shutil.copytree(self.get_sys_data_dirs('docker'), os.path.join(self.basepath, 'docker'))
        # FIXME
        except Exception as err:
            sys.stderr.write("Unable to copy config files: %s\n" % (err))
            pass

    def update_docker(self):
        return self.update_files('docker')

    def update_config_files(self):
        return self.update_files('config')
    
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
                    amsterdam_compose_file.write(bytes(amsterdam_config, 'UTF-8'))
        template_path = os.path.join(self.get_sys_data_dirs('templates'), 'ethtool.conf.j2')
        with open(template_path, 'r') as ethtool_file:
            # get the string and build template
            ethtool_tmpl = ethtool_file.read()
            ethtool_config_tmpl = Template(ethtool_tmpl)
        
            ethtool_config = ethtool_config_tmpl.substitute(options)
        
        with open(os.path.join(self.basepath, 'config', 'suricata', 'ethtool.conf'), 'w') as ethtool_compose_file:
            if sys.version < '3':
                ethtool_compose_file.write(ethtool_config)
            else:
                ethtool_compose_file.write(bytes(ethtool_config, 'UTF-8'))

    def check_environment(self):
        try:
            self.name.decode('ascii')
        except UnicodeDecodeError:
            pass
            raise AmsterdamException("Name or data directory can't contain/finish with non ascii character")
        if " " in self.name:
            raise AmsterdamException("Name or data directory can't contain/finish with space")

        docker_cmd = ['docker-compose', '-v']
        try:
            out = subprocess.check_output(docker_cmd)
        except OSError as err:
            if err.errno == 2:
                pass
                raise AmsterdamException("No docker-compose binary in path")
        version = out.decode('UTF-8')
        if ':' in version:
            self.docker_compose_version = version.split(': ')[1]
        elif ',' in version:
            versionregexp = re.compile("([\d\.]+)")
            match = versionregexp.search(version)
            self.docker_compose_version = match.groups()[0]
        else:
            sys.stderr.write("docker-compose version number '%s' is not handled by code\n" % (version.rstrip()))
            self.docker_compose_version = version

        docker_compose_path = os.path.join(os.getcwd(), self.basepath)

        self.convertpath = False
        if os.environ.has_key('LANG'):
            if not 'utf8' in os.environ['LANG']:
                try:
                    docker_compose_path.decode('ascii')
                except UnicodeDecodeError:
                    self.convertpath = True

    def run_docker_compose(self, cmd, options = None):
        localenv = os.environ.copy()
        if self.convertpath:
            localenv['LANG'] = "en_US.utf8"
        docker_cmd = ['docker-compose', '-p', self.name, '-f',
                      os.path.join(self.basepath, 'docker-compose.yml'), cmd]
        if options:
            docker_cmd.extend(options)
        return subprocess.call(docker_cmd, env = localenv)
    
    def setup_options(self, args):
        self.options = {}
        self.options['capture_option'] =  "--af-packet=%s" % args.iface
        self.options['basepath'] = self.basepath
        self.options['iface'] = args.iface

    def setup(self, args):
        self.setup_options(args)
        if args.verbose:
            sys.stdout.write("Generating docker compose file\n")
        self.create_data_dirs()
        self.update_config()
        self.generate_template(self.options)
        self.create_self_signed_cert()
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
        if args.full:
            self.setup_options(args)
            self.update_docker()
            self.update_config_files()
            self.create_self_signed_cert()
            self.generate_template(self.options)
        self.run_docker_compose('pull')
        self.run_docker_compose('build', options = ['--no-cache'])
        return True

    def create_self_signed_cert(self):
        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 1024)
 
        # CREATE A SELF-SIGNED CERT
        cert = crypto.X509()
        cert.get_subject().C = "FR"
        cert.get_subject().ST = "Paris"
        cert.get_subject().L = "Paris"
        cert.get_subject().O = "Stamus Networks"
        cert.get_subject().OU = "Amsterdam"
        cert.get_subject().CN = gethostname()
        cert.set_serial_number(int(time.time() * 10))
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(365*24*60*60)
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(k)
        cert.sign(k, 'sha256')
        # export 

        dir_path =  os.path.join(self.basepath, 'config', 'nginx', 'ssl')
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        cert_file =  os.path.join(dir_path, 'amsterdam.crt')
        key_file =  os.path.join(dir_path, 'amsterdam.key')
        open(cert_file, "wt").write(
            crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
        open(key_file, "wt").write(
            crypto.dump_privatekey(crypto.FILETYPE_PEM, k))
