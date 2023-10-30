-- drop database BRASILEIRAO;
use BRASILEIRAO;
desc GOLS;
desc CARTAO;

select nome 
FROM JOGADOR
WHERE JOGADOR.clube = "Corinthians - SP";

ALTER TABLE GOLS DROP CONSTRAINT tempo_gol;
ALTER TABLE GOLS DROP CONSTRAINT minuto_gol;

ALTER TABLE ARBITRAGEM DROP CONSTRAINT nome;
ALTER TABLE GOLS MODIFY jogador int;
ALTER TABLE CARTAO MODIFY tipo_cartao enum('Y', 'R');
ALTER TABLE CARTAO MODIFY punido int;
DELETE FROM CARTAO;
select * FROM PARTIDA;

SELECT * FROM GOLS;
SELECT * FROM CARTAO;

DROP TABLE CARTAO;

select * FROM JOGADOR;

DELETE FROM PARTIDA;

desc ARBITRAGEM;

desc SUBSTITUICAO;

drop table SUBSTITUICAO;

alter table PARTIDA MODIFY data_partida DATETIME;
alter table ARBITRAGEM MODIFY nome varchar(50);

desc ARBITRAGEM;
delete from ARBITRAGEM;

desc RELACIONADOS_PARA;

select * FROM TIME order by (TIME.vitorias*3 + TIME.empates) DESC;

select * from CARTAO;
select * FROM GOLS;



select * FROM PARTIDA;

select * FROM SUBSTITUICAO;

select COUNT(tipo_cartao) from CARTAO WHERE clube_punido LIKE 'Fluminense%' AND tipo_cartao='R';

select * FROM RELACIONADOS_PARA;
