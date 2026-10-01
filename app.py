from flask import Flask, render_template, request, redirect, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "123456"

DATABASE = "biblioteca.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/alunos")
def alunos():
    conn = get_db()
    dados = conn.execute("SELECT * FROM alunos").fetchall()
    conn.close()
    return render_template("alunos.html", alunos=dados)


@app.route("/alunos/cadastrar", methods=["POST"])
def cadastrar_aluno():
    nome = request.form.get("nome")
    email = request.form.get("email")
    telefone = request.form.get("telefone")
    matricula = request.form.get("matricula")

    conn = get_db()

    try:
        conn.execute(
            "INSERT INTO alunos (nome, email, telefone, matricula) VALUES (?, ?, ?, ?)",
            (nome, email, telefone, matricula)
        )
        conn.commit()
        flash("Aluno cadastrado com sucesso!")
    except sqlite3.IntegrityError:
        flash("Matrícula já cadastrada.")
    finally:
        conn.close()

    return redirect("/alunos")


@app.route("/professores")
def professores():
    conn = get_db()
    dados = conn.execute("SELECT * FROM professores").fetchall()
    conn.close()
    return render_template("professores.html", professores=dados)


@app.route("/professores/cadastrar", methods=["POST"])
def cadastrar_professor():
    nome = request.form.get("nome")
    especialidade = request.form.get("especialidade")
    email = request.form.get("email")
    telefone = request.form.get("telefone")

    conn = get_db()

    conn.execute(
        "INSERT INTO professores (nome, especialidade, email, telefone) VALUES (?, ?, ?, ?)",
        (nome, especialidade, email, telefone)
    )

    conn.commit()
    conn.close()

    flash("Professor cadastrado com sucesso!")

    return redirect("/professores")


@app.route("/turmas")
def turmas():
    conn = get_db()
    dados = conn.execute("SELECT * FROM turmas").fetchall()
    conn.close()
    return render_template("turmas.html", turmas=dados)


@app.route("/turmas/cadastrar", methods=["POST"])
def cadastrar_turma():
    nome = request.form.get("nome")
    serie = request.form.get("serie")
    turno = request.form.get("turno")
    sala = request.form.get("sala")

    conn = get_db()

    conn.execute(
        "INSERT INTO turmas (nome, serie, turno, sala) VALUES (?, ?, ?, ?)",
        (nome, serie, turno, sala)
    )

    conn.commit()
    conn.close()

    flash("Turma cadastrada com sucesso!")

    return redirect("/turmas")


if __name__ == "__main__":
    app.run(debug=True)