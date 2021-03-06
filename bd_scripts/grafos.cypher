
CREATE (:Bairro {nome:'Paraíso'});

CREATE (:Bairro {nome:'Butantã'});

CREATE (:Bairro {nome:'Belém'});

CREATE (:Estacionamento {nome:'Multi Park', latitude: -45.67, longitude: 45.68});

CREATE (:Estacionamento {nome:'Estapar', latitude: -45.43, longitude: 44.97});

CREATE (:Agente {cpf:'12345678904'});

MATCH (a:Agente {cpf:'12345678904'}), (b:Bairro {nome: 'Paraíso'}) CREATE (a)-[:FISCALIZA]->(b);

CREATE (:Vaga {id_vaga: 1, latitude: -12.34, longitude: 43.21});

CREATE (:Vaga {id_vaga: 2, latitude: -12.35, longitude: 53.21});

CREATE (:Vaga {id_vaga: 3, latitude: 98.76, longitude: -67.89});
    
MATCH (v:Vaga {id_vaga: 1}), (b:Bairro {nome: 'Paraíso'}) CREATE (v)-[:ESTA_EM]->(b);

MATCH (v:Vaga {id_vaga: 2}), (b:Bairro {nome: 'Paraíso'}) CREATE (v)-[:ESTA_EM]->(b);

MATCH (v:Vaga {id_vaga: 3}), (b:Bairro {nome: 'Butantã'}) CREATE (v)-[:ESTA_EM]->(b);
