from flask import render_template
from flask import Flask
# from livereload import Server

app = Flask(__name__)

@app.route('/')
def index():
    #使用 render_template() 方法来渲染模板
    return render_template('index.html')

@app.route('/<filename>')
def req_file(filename):
    return render_template(filename)

if __name__ == '__main__':   
    app.DEBUG=True#代码调试立即生效
    app.jinja_env.auto_reload = True#模板调试立即生效
    app.run()#用 run() 函数来让应用运行在本地服务器上