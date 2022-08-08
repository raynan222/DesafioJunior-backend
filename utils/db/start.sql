INSERT INTO pais(nome) VALUES('Brasil');
--SELECT * from pais;

INSERT INTO estado(nome, sigla, pais_id) VALUES('Ceara','CE', 1);
--SELECT * from estado;

INSERT INTO municipio(nome, uf_id) VALUES('Fortaleza', 1);
--SELECT * from municipio;

INSERT INTO endereco(cep, rua, numero, bairro, complemento, municipio_id) VALUES('60862100','Rua 13', '260', 'JD. Castelinho', 'Nao há', 1);
--SELECT * from endereco;

INSERT INTO usuario(nome, pis, cpf, endereco_id) VALUES('Primeiro', '85226562360', '37897066045', 1);
--SELECT * from usuario;

INSERT INTO acesso(nome) VALUES('administracao');
INSERT INTO acesso(nome) VALUES('usuario');
INSERT INTO acesso(nome) VALUES('visitante');
--SELECT * from acesso;

INSERT INTO login(email, senha, usuario_id, acesso_id) VALUES('admin@local.com', 'sha256$F8yBZqAb$b1211446fb908d77692b6ed669a27399976872a98f03efab1225261310c56f8e', 1, 1);
--SELECT * from login;