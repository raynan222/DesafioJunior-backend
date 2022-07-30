from application.app import app


def usuario_add():
    stm = "INSERT INTO login (email, senha, acesso) " \
          "SELECT substr(RANDOM()::TEXT, 1, 10)," \
          "md5(RANDOM()::TEXT)," \
          "RANDOM()::TEXT" \
          "FROM generate_series(1, 10);"

    try:
        app.session.excute(stm)
        print("ok")
    except Exception:
        print("bad")
