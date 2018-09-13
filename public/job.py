from request import sched
from public.run import *
from request.models import *
from request.models import Database as DatabaseModel
from public.sqldb import *

class Job:
    def __init__(self,taskname,schedule):
        self.taskname=taskname
        self.schedule=schedule
    #把时间表做数据处理
    def __get_date(self):
        self.task_schedule = self.schedule.split(' ')
        for i in range(len(self.task_schedule)):
            if self.task_schedule[i]=='*':
                self.task_schedule[i]=None

    # 启动数据库和启动IP
    def __get_ip_database(self,request, env_desc, database_desc,subject):
        # 环境
        env_list = Environment.objects.filter(env_desc=env_desc).values("env_ip", "env_host", "env_port")
        if env_list[0]['env_ip'] != "":
            if env_list[0]['env_port']!="":
                env_ip = "http://{host}:{port}".format(host=env_list[0]['env_ip'], port=env_list[0]['env_port'])
            else:
                env_ip = "http://{host}".format(host=env_list[0]['env_ip'])
        else:
            if env_list[0]['env_port'] != "":
                env_ip = "http://{host}:{port}".format(host=env_list[0]['env_host'], port=env_list[0]['env_port'])
            else:
                env_ip = "http://{host}".format(host=env_list[0]['env_host'])

        #有个梗如果用Database找不到数据库模型
        if database_desc != "":
            db_list = DatabaseModel.objects.filter(db_remark=database_desc).values('db_type', 'db_name', 'db_ip', 'db_port',
                                                                              'db_user', 'db_password')
        # 不需要数据库
        else:
            db_list = []
            db_list.append({"db_type": "", "db_ip": "", "db_port": "", "db_user": "", "db_password": "", "db_name": ""})

        create_db(db_list[0]['db_type'], db_list[0]['db_ip'], db_list[0]['db_port'], db_list[0]['db_user'],
            db_list[0]['db_password'], db_list[0]['db_name'], env_ip)

        #邮件
        # 如果要发送邮件拿到邮件配置数据
        if subject != None and subject!="":
            email_data = \
            Email.objects.filter(subject=subject).values('id', 'sender', 'receivers', 'host_dir', 'email_port',
                                                         'username', 'passwd', 'Headerfrom', 'Headerto', 'subject')[0]
        else:
            email_data = None
        return email_data
    #添加定时任务
    def create_job(self,request,env_desc,database_desc,failcount,subject):
        self.__get_date()

        @sched.scheduled_job('cron', minute = self.task_schedule[0],hour = self.task_schedule[1], day  = self.task_schedule[2],month  = self.task_schedule[3], week   = self.task_schedule[4],id=self.taskname)
        def task():
            #启动数据库和启动IP和获取邮件配置数据
            email_data=self.__get_ip_database(request, env_desc, database_desc,subject)
            interface(self.taskname,failcount,email_data)

    #删除定时任务
    def delete_job(self):
        try:
            #如果有任务删除任务
            sched.remove_job(self.taskname)
        except:
            #没有任务就跳过
            pass












