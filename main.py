from flask import Flask, url_for, render_template
from routes.adm import adm_route
from routes.login import login_route
from routes.vend import vend_route

# inicialização do app
app = Flask(__name__)
app.register_blueprint(adm_route, url_prefix='/adm')
app.register_blueprint(login_route)
app.register_blueprint(vend_route, url_prefix='/vend')
app.secret_key = 's3nh4'
# rotas


# execução
app.run(debug=True)
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)
