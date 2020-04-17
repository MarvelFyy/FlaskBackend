import click
from flask_login import LoginManager
from fullstack import db,app
from fullstack.Models.Admin import Admin

# 初始化数据库命令
@app.cli.command()
@click.option('--drop',is_flag=True,help='Create after drop.') #设置选项
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('初始化数据库完成') #输出提示信息

# 生成管理员账户
@app.cli.command()
@click.option('--username',prompt=True,help='The username used to login.')
@click.option('--password',prompt=True,hide_input=True,confirmation_prompt=True,help='The password used to login')
def admin(username,password):
    db.create_all()

    admin=Admin.query.first()
    if admin is not None:
        click.echo('Updating admin...')
        admin.username=username
        admin.set_password(password) #设置密码
    else:
        click.echo('Creating admin...')
        admin=Admin(username=username)
        admin.set_password(password)
        db.session.add(admin)
    
    db.session.commit()
    click.echo('Done.')

# 测试命令
@app.cli.command()
def hello():
    click.echo('Hello,Flask')