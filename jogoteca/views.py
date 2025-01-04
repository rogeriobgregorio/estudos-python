from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from dao import JogoDao, UsuarioDao
from models import Jogo
import os
from jogoteca import db, app

jogo_dao = JogoDao(db)
usuario_dao = UsuarioDao(db)

@app.route('/')
def index():
    lista = jogo_dao.listar()
    return render_template('lista.html', titulo='Jogos', jogos=lista)


@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Jogo')


@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    jogo = jogo_dao.salvar(jogo)
    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    arquivo.save(f'{upload_path}/capa{jogo.id}.jpg')
    return redirect(url_for('index'))


@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar')))
    jogo = jogo_dao.busca_por_id(id)
    capa_jogo = f'capa{id}.jpg'
    caminho_imagem = os.path.join(app.config['UPLOAD_PATH'], capa_jogo)
    if not os.path.exists(caminho_imagem):  
        capa_jogo = 'capa_padrao.jpg'  
    return render_template('editar.html', titulo='Editar Jogo', jogo=jogo, capa_jogo=capa_jogo)


@app.route('/atualizar', methods=['POST',])
def atualizar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console, id=request.form['id'])
    jogo_dao.salvar(jogo)
    return redirect(url_for('index'))


@app.route('/deletar/<int:id>')
def deletar(id):
    jogo_dao.deletar(id)
    imagem_jogo = os.path.join(app.config['UPLOAD_PATH'], f'capa{id}.jpg')
    if os.path.exists(imagem_jogo):
        os.remove(imagem_jogo)
    flash('O jogo foi removido com sucesso!')
    return redirect(url_for('index'))


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)


@app.route('/autenticar', methods=['POST',])
def autenticar():
    usuario = usuario_dao.buscar_por_id(request.form['usuario'])
    if usuario:
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.id
            flash(usuario.nome + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Falha ao tentar logar, tente novamente!')
        return redirect(url_for('login'))
    

@app.route('/logout', methods=['POST'])
def logout():
    session['usuario_logado'] = None
    flash('Você saiu da sua conta!')
    return redirect(url_for('login'))


@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)
