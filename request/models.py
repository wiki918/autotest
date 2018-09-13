from django.db import models

# Create your models here.
#测试环境表
class Environment(models.Model):
    env_ip=models.CharField(max_length=20)
    env_host = models.CharField(max_length=40)
    env_port = models.CharField(max_length=10)
    env_desc = models.CharField(max_length=100)

    def __str__(self):
        return self.env_ip

#开发数据库表
class Database(models.Model):
    db_type=models.CharField(max_length=4)
    db_typename=models.CharField(max_length=20,default="")
    db_name = models.CharField(max_length=100)
    db_ip = models.CharField(max_length=20)
    db_port = models.CharField(max_length=20)
    db_user = models.CharField(max_length=20)
    db_password = models.CharField(max_length=20)
    db_remark = models.CharField(max_length=100,default="")

    def __str__(self):
        return self.db_name

#邮件配置表
class Email(models.Model):
    sender=models.CharField(max_length=20)
    receivers = models.CharField(max_length=100)
    host_dir = models.CharField(max_length=20)
    email_port=models.CharField(max_length=20, default="")
    username = models.CharField(max_length=20)
    passwd = models.CharField(max_length=20)
    Headerfrom = models.CharField(max_length=20)
    Headerto = models.CharField(max_length=100)
    subject = models.CharField(max_length=100,default="")

    def __str__(self):
        return self.username

#项目表
class Project(models.Model):
    project_name=models.CharField(max_length=20)
    Testers=models.CharField(max_length=100,default="")
    Developer = models.CharField(max_length=100,default="")
    status= models.BooleanField()
    project_desc = models.CharField(max_length=200)

    def __str__(self):
        return self.project_name

#模块表
class Modules(models.Model):
    Project = models.ForeignKey(Project, on_delete=models.CASCADE)
    Modules_name=models.CharField(max_length=20)
    Testers=models.CharField(max_length=100)
    Developer = models.CharField(max_length=100)
    status = models.BooleanField()
    Modules_desc = models.CharField(max_length=200)

    def __str__(self):
        return self.Modules_name

#用例表
class Case(models.Model):
    Modules=models.ForeignKey(Modules,on_delete=models.CASCADE)
    case_name = models.CharField(max_length=100)
    api = models.CharField(max_length=100)
    status = models.BooleanField()
    version = models.CharField(max_length=20)
    case_weights = models.IntegerField(default=0)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)
    case_desc = models.CharField(max_length=100,blank=True)

    def __str__(self):
        return self.case_name
#步骤表
class Step(models.Model):
    case=models.ForeignKey(Case,on_delete=models.CASCADE)
    step_name = models.CharField(max_length=100)
    step_desc = models.CharField(max_length=100)
    steplevel = models.CharField(max_length=10)
    method = models.CharField(max_length=10)
    params = models.CharField(max_length=500)
    headers = models.CharField(max_length=1000)
    files = models.CharField(max_length=500)
    assert_response = models.CharField(max_length=500)
    api_dependency = models.CharField(max_length=500,default="")
    step_weights = models.IntegerField(default=0)
    status = models.BooleanField()
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.step_name

#步骤依赖表
class Reference_step(models.Model):
    step=models.ForeignKey(Step,on_delete=models.CASCADE)
    step_name=models.CharField(max_length=100,default="")
    path = models.CharField(max_length=100, default="")
    reference_step_name = models.CharField(max_length=100,default="")
    variable = models.CharField(max_length=200)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.step

#sql表
class Sql(models.Model):
    step=models.ForeignKey(Step,on_delete=models.CASCADE)
    sql_condition = models.IntegerField()
    is_select = models.BooleanField()
    variable = models.CharField(max_length=200)
    sql = models.CharField(max_length=200)
    remake = models.CharField(max_length=200)
    status = models.BooleanField()
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sql
#任务表
class Task(models.Model):
    case=models.ForeignKey(Case,on_delete=models.CASCADE)
    task_name = models.CharField(max_length=40)
    task_run_time_regular = models.CharField(max_length=100)
    ip=models.CharField(max_length=40,default="")
    db = models.CharField(max_length=40,default="")
    email = models.CharField(max_length=40,default="")
    failcount = models.CharField(max_length=40,default="")
    remark = models.CharField(max_length=200)
    db_remark = models.CharField(max_length=100, default="")
    env_desc = models.CharField(max_length=100, default="")
    subject = models.CharField(max_length=100, default="")
    status = models.BooleanField()
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task_name

#测试结果表
class api_test_result(models.Model):
    task=models.ForeignKey(Task,on_delete=models.CASCADE)
    case = models.ForeignKey(Case,on_delete=models.CASCADE)
    step = models.ForeignKey(Step,on_delete=models.CASCADE)
    case_result = models.CharField(max_length=200)
    error_info = models.CharField(max_length=200)
    response_body = models.CharField(max_length=500)
    case_start_time = models.DateTimeField()
    case_end_time = models.DateTimeField()
    case_run_time = models.DateTimeField()
    def __str__(self):
        return self.case_result

#统计分析总表
#任务表
class StatisticsData(models.Model):
    casenumber = models.IntegerField()
    tasknumber = models.IntegerField()
    carrynumber = models.IntegerField()
    passnumber = models.IntegerField()
    asserterrornumber = models.IntegerField()
    failnumber = models.IntegerField()
    errorratio = models.IntegerField()
    def __str__(self):
        return self.casenumber

#邮件和日志的反馈
class LogAndHtmlfeedback(models.Model):
    test_step = models.CharField(max_length=100)
    test_status = models.IntegerField()
    test_response = models.CharField(max_length=500)
    test_carryTaskid = models.CharField(max_length=40,default="")
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

#第几次执行任务
class CarryTask(models.Model):
    task_name = models.CharField(max_length=40)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.task_name