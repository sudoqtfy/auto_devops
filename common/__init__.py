import paramiko
import subprocess
import shlex
import sys
import logging 

logger = logging.getLogger(__name__)

class Dict(dict):

    def __init__(self, keys, values):
        for k, v in zip(keys, values):
            self[k] = v

    def __getattr__(self, k):
        if k not in self:
            raise KeyError('%s not found!' % k)
        return self[k]

    def __setattr__(self, k, v):
        self[k] = v


 
def ssh_command(username, password, host, command, port):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, port ,username, password)
    except Exception as e:
        logger.error(str(e))
        return ('', str(e))
        sys.exit(1)
    stdin, stdout, stderr = client.exec_command(command)
    stdout = stdout.read()
    stderr = stderr.read()
    return (stdout, stderr)
    ssh.close()


def mysql_select(dbhost, dbuser, dbpass, dbport, dbname, sql, vertical=False, compress=True, html=True, timeout=0):
    mysql_param = {
            'dbhost': dbhost, 
            'dbuser': dbuser,
            'dbpass': dbpass,
            'dbport': dbport,
            'sql': sql,
            'dbname': dbname,
    }
    options = []
    command_line = "mysql {0}  --host=%(dbhost)s --user=%(dbuser)s --password=%(dbpass)s --port=%(dbport)s --database=%(dbname)s --execute='%(sql)s'" % mysql_param
    if vertical:
        options.append('-E')
    if compress:
        options.append('-C')
    if html:
        options.append('-H')
    if timeout != 0:
        options.append('--connect-timeout=%s' % timeout)
    command_line = command_line.format(' '.join(options))
    print command_line
    p = subprocess.Popen(command_line, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout = p.stdout.read()
    stderr = p.stderr.read()
    return (stdout, stderr)

#mysql_select(vertical=True, timeout=22)
def mysql_script(dbhost, dbuser, dbpass, dbport, dbname, sql_script_path, compress=True):
    mysql_param = {
            'dbhost': dbhost, 
            'dbuser': dbuser,
            'dbpass': dbpass,
            'dbport': dbport,
            'sql_script_path': sql_script_path,
            'dbname': dbname,
    }
    options = []
    import os
    if not os.path.isfile(sql_script_path): return ('', 'sql script %s [no found!]' % sql_script_path)
    command_line = "mysql {0}  --host=%(dbhost)s --user=%(dbuser)s --password=%(dbpass)s --port=%(dbport)s --database=%(dbname)s < %(sql_script_path)s" % mysql_param
    if compress:
        options.append('-C')
    command_line = command_line.format(' '.join(options))
    print command_line
    p = subprocess.Popen(command_line, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout = p.stdout.read()
    stderr = p.stderr.read()
    return (stdout, stderr)

#mysql_script(dbhost='127.0.0.1', dbuser='root', dbpass='root', dbport=3306, dbname='tmp', sql_script_path='/tmp/test.sql', compress=True)


#ssh_command(
#        username="test",
#        password="QPxeh2a3amIVkDOv",
#        port=22,
#        command="df -hi",
#        host="117.27.139.221",
#        )
