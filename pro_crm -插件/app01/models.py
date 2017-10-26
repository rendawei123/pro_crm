from django.db import models

# Create your models here.


class Department(models.Model):
    """
    部门表
    """
    title = models.CharField(verbose_name='部门名称', max_length=16)


class UserInfo(models.Model):
    """
    员工表
    """
    name = models.CharField(verbose_name='员工姓名', max_length=16)
    username = models.CharField(verbose_name='用户名', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=64)
    email = models.EmailField(verbose_name='邮箱', max_length=64)

    depart = models.ForeignKey(verbose_name='部门', to="Department")


class Course(models.Model):
    """
    课程表
    如：
        Linux基础
        Linux架构师
        Python自动化开发精英班
        Python自动化开发架构师班
    """
    name = models.CharField(verbose_name='课程名称', max_length=32)


class School(models.Model):
    """
    校区表
    如：
        北京海淀校区
        北京昌平校区
        上海虹口校区
        广州白云山校区
    """
    title = models.CharField(verbose_name='校区名称', max_length=32)


class ClassList(models.Model):
    """
    班级表
    如：
        Python全栈  面授班  5期  10000  2017-11-11  2018-5-11
    """
    school = models.ForeignKey(verbose_name='校区', to='School')
    course = models.ForeignKey(verbose_name='课程名称', to='Course')
    semester = models.IntegerField(verbose_name="班级(期)")
    price = models.IntegerField(verbose_name="学费")
    start_date = models.DateField(verbose_name="开班日期")
    graduate_date = models.DateField(verbose_name="结业日期", null=True, blank=True)
    memo = models.CharField(verbose_name='说明', max_length=256, blank=True, null=True, )
    teachers = models.ManyToManyField(verbose_name='任课老师', to='UserInfo', related_name='teach_classes')
    tutor = models.ForeignKey(verbose_name='班主任', to='UserInfo', related_name='classes')