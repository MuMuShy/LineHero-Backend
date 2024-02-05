from django.db import models

# Create your models here.
class User(models.Model):
    line_user_id = models.CharField(max_length=255, unique=True, primary_key=True)
    # 添加其他需要的字段，例如：
    name = models.CharField(max_length=100, blank=True, null=True)
    # 可以根据需要添加更多字段
    level = models.FloatField(default=1.0)  # 使用浮点数来表示等级
    experience = models.FloatField(default=0.0)  # 使用浮点数来表示经验值
    health_points = models.FloatField(default=100.0)  # 使用浮点数来表示血量
    mana_points = models.FloatField(default=50.0)  # 使用浮点数来表示魔力
    def __str__(self):
        return self.line_user_id

class LevelExperience(models.Model):
    level = models.IntegerField(unique=True)  # 等级
    experience_required = models.IntegerField()  # 对应的经验值要求


#基礎等級對照的血量魔力
class BasicAbilities(models.Model):
    level = models.IntegerField(unique=True)  # 等级
    health_points = models.IntegerField()  # 血量
    mana_points = models.IntegerField()  # 魔力
    atk_points = models.FloatField()
    matk_points = models.FloatField()