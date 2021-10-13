import subprocess

class AIDMSHandler():

    #========configure============================
    AIDMS_db_configure = {
        'SERVER_1':{
            'IP':'172.16.10.150',
            'HOST_NAME':'ubuntu',
            'PATH_MAP':[{'/usr/local/aidms/workspace/AIDMS_DB':'/data2/AIDMS/aidms_18f'},
                        {'/home/kevintsai/aidms/model_management/AIDMS_DB':'/data2/AIDMS/aidms_model_management'},
                        {'/home/kevintsai/aidms/deploy/AIDMS_DB':'/data2/AIDMS/aidms_deploy'},
                        ]},
        'SERVER_2':{
            'IP':'125.227.129.220',
            'HOST_NAME':'ubuntu',
            'PATH_MAP':[{'/usr/local/aidms/workspace/AIDMS_DB':'/data2/AIDMS/aisms_8f'}
                        ]}               
        }
    
    @classmethod
    def mount_AIDMS_db_impl(cls):
        for key in cls.AIDMS_db_configure:
            server_config = cls.AIDMS_db_configure[key]
            IP = server_config['IP']
            HostName = server_config['HOST_NAME']
            PathMaps = server_config['PATH_MAP']
            for path_map in PathMaps:
                mount_path = next(iter(path_map))
                cmd = f'sshfs {HostName}@{IP}:{mount_path} {path_map[mount_path]}'
                pop = subprocess.Popen(cmd, executable='/bin/bash', shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                stdout,stderr = pop.communicate()
                stdout = stdout.decode('utf-8')
                stderr = stderr.decode('utf-8')
                if stderr:
                    print(f'mount {mount_path} AIDMS db fail: {stderr}')
                else:
                    print(f'mount {mount_path} AIDMS db success')        