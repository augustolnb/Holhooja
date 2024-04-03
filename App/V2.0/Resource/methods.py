

def autenticar():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(matricula=form.matricula.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data) and user.status == 1:
                login_user(user)
                # Tentativa de adicionar um registro ao banco 20/03
                # O trecho de código abaixo funcionar apenas 1 vez, ou seja, 
                # depois que o usuário tem o primeiro registro criado, 
                # a adição de um novo registro se torna incompativel
                """new_registro = Registros(matricula=form.matricula.data)
                try:
                    db.session.add(new_registro)
                    db.session.commit()
                except:
                    return redirect(url_for('login'))
                """
                if user.tipo == 1:
                    id = user.id
                    matricula = user.matricula
                    data = user.data_cadastro
                    redirect('/dashboard')
                    return render_template('dashboard.html', id=id, matricula=matricula, nome=user.nome_completo, data=data)

                if user.tipo == 2:
                    id = user.id
                    matricula = user.matricula
                    data = user.data_cadastro
                    return redirect('/admin_dash')
                    #return render_template('admin_dash.html', id=id, matricula=matricula, nome=user.nome_completo, data=data)




@app.route('/login', methods=['GET', 'POST'])
def login():
    # Adicionar validadores nos formulários
    
    if request.method == "POST":
        matricula = str(request.form.get('matricula'))
        password = str(request.form.get('password'))
        user = User.query.filter_by(matricula=matricula).first()
        if user:
            if bcrypt.check_password_hash(user.password, password) and user.status == 1:
                login_user(user)

                if user.tipo == 2:
                    id = user.id
                    matricula = user.matricula
                    data = user.data_cadastro
                    return redirect('/admin_dash')
                    #return render_template('admin_dash.html', id=id, matricula=matricula, nome=user.nome_completo, data=data)

            else:
                return "Senha nao confere"
        else:
            return "usuario n identificado"
    else:
        return render_template('login.html')