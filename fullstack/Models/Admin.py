from fullstack import db
from werkzeug.security import generate_password_hash,check_password_hash


class Admin(db.Model):
     __tablename__='Admin'
     id=db.Column(db.Integer, primary_key=True) 
     username=db.Column(db.String(20)) #用户名
     password_hash=db.Column(db.String(256)) #密码散列值

     # 设置密码
     def set_password(self,password):
          # 将生成的密码保持到对应字段
          self.password_hash=generate_password_hash(password) 
     # 验证密码
     def check_password(self,password):
          # 返回bool
          return check_password_hash(self.password_hash,password)