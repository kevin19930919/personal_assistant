import subprocess
import pexpect
import time 
class AIDMSHandler():

    #========configure============================
    AIDMS_db_configure = {
        'SERVER_1':{
            'IP':'172.16.10.150',
            'HOST_NAME':'ubuntu',
            'PASSWORD':'ubuntu',
            'PATH_MAP':[{'/usr/local/aidms/workspace/AIDMS_DB':'/data2/AIDMS/aidms_18f'},
                        {'/home/kevintsai/aidms/model_management/AIDMS_DB':'/data2/AIDMS/aidms_model_management'},
                        {'/home/kevintsai/aidms/deploy/AIDMS_DB':'/data2/AIDMS/aidms_deploy'},
                        ]},
        # 'SERVER_2':{
        #     'IP':'125.227.129.220',
        #     'HOST_NAME':'ubuntu',
        #     'PASSWORD':'1qazZSE$4rfv',
        #     'PATH_MAP':[{'/usr/local/aidms/workspace/AIDMS_DB':'/data2/AIDMS/aisms_8f'}
        #                 ]}               
        }
    
    @classmethod
    def mount_AIDMS_db_impl(cls):
        for key in cls.AIDMS_db_configure:
            server_config = cls.AIDMS_db_configure[key]
            IP = server_config['IP']
            HostName = server_config['HOST_NAME']
            PathMaps = server_config['PATH_MAP']
            Password = server_config['PASSWORD']
            for path_map in PathMaps:
                mount_path = next(iter(path_map))               
                cmd = f'sshfs -o reconnect {HostName}@{IP}:{mount_path} {path_map[mount_path]}'
                # pop = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                # stdout,stderr = pop.communicate(input=f'{Password}\n'.encode())
                # stdout = stdout.decode('utf-8')
                # stderr = stderr.decode('utf-8')
                # # p = subprocess.run(['sshfs', f'{HostName}@{IP}:{mount_path}',f'{path_map[mount_path]}'], stdout=subprocess.PIPE, input=f'{Password}\n', encoding='ascii')
                # if stderr:
                #     print(f'mount {mount_path} AIDMS db fail: {stderr}')
                # else:
                #     print(f'mount {mount_path} AIDMS db success')    
                child = pexpect.spawn(cmd)
                child.expect('.*password*')
                child.sendline(Password)
                print(child.read())
                # print(f'mount {HostName}@{IP}:{mount_path} success')
                child.expect(pexpect.EOF)
        print('successfully mount every dir')

