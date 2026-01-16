import os
import paramiko

def upload_report(report_server_ip, report_server_username, report_server_password, report_path, report_server_dir='/var/www/html'):
    """上传报告到指定服务器"""
    try:
        # 创建SSH客户端
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # 连接服务器
        print(f"正在连接服务器 {report_server_ip}...")
        ssh.connect(report_server_ip, username=report_server_username, password=report_server_password)
        
        # 创建SCP客户端
        scp = paramiko.SFTPClient.from_transport(ssh.get_transport())
        
        # 获取报告目录名称
        report_dir_name = os.path.basename(report_path)
        
        # 上传报告目录
        print(f"正在上传报告到 {report_server_dir}/{report_dir_name}...")
        
        # 确保目标目录存在
        try:
            scp.stat(f'{report_server_dir}/{report_dir_name}')
        except FileNotFoundError:
            # 在SSH shell中创建目录
            stdin, stdout, stderr = ssh.exec_command(f'mkdir -p {report_server_dir}/{report_dir_name}')
            exit_code = stdout.channel.recv_exit_status()
            if exit_code != 0:
                raise Exception(f"创建目标目录失败: {stderr.read().decode('utf-8')}")
        
        # 递归上传目录
        for root, dirs, files in os.walk(report_path):
            # 处理当前目录的相对路径（处理Windows和Linux路径分隔符差异）
            relative_path = os.path.relpath(root, report_path)
            if relative_path == '.':
                remote_current_dir = f'{report_server_dir}/{report_dir_name}'
            else:
                # 将Windows路径分隔符替换为Linux的
                linux_relative_path = relative_path.replace('\\', '/')
                remote_current_dir = f'{report_server_dir}/{report_dir_name}/{linux_relative_path}'
            
            # 创建所有子目录
            for dir_name in dirs:
                # 处理子目录的远程路径
                linux_dir_name = dir_name.replace('\\', '/')
                remote_dir = os.path.join(remote_current_dir, linux_dir_name).replace('\\', '/')
                try:
                    scp.stat(remote_dir)
                except FileNotFoundError:
                    stdin, stdout, stderr = ssh.exec_command(f'mkdir -p "{remote_dir}"')
                    exit_code = stdout.channel.recv_exit_status()
                    if exit_code != 0:
                        raise Exception(f"创建子目录失败: {stderr.read().decode('utf-8')}")
            
            # 上传所有文件
            for file_name in files:
                local_file_path = os.path.join(root, file_name)
                # 处理文件的远程路径
                linux_file_name = file_name.replace('\\', '/')
                remote_file_path = os.path.join(remote_current_dir, linux_file_name).replace('\\', '/')
                
                try:
                    print(f"正在上传: {local_file_path} -> {remote_file_path}")
                    scp.put(local_file_path, remote_file_path)
                except Exception as file_error:
                    print(f"上传文件 {file_name} 失败: {str(file_error)}")
        
        scp.close()
        ssh.close()
        print(f"报告上传成功！访问地址: http://{report_server_ip}/{report_dir_name}/")
    except Exception as e:
        print(f"报告上传失败: {str(e)}")
        # 确保资源被释放
        try:
            if 'scp' in locals() and scp:
                scp.close()
            if 'ssh' in locals() and ssh:
                ssh.close()
        except:
            pass