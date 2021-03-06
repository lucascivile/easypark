from .ConnectionFactory import ConnectionFactory
from modelo.grafos import Agente

class AgenteDAO:

    def __init__(self):
        self.session = ConnectionFactory.get_instance().get_session()

    def insert(self, agente):
        def __insert_bairro_if_not_exists(tx, bairro):
            tx.run("MERGE (:Bairro {nome:$bairro});", bairro=bairro)

        def __insert_agente_tx(tx, cpf):
            tx.run("CREATE (:Agente {cpf:$cpf});", cpf=cpf)

        def __insert_fiscaliza_tx(tx, cpf, bairro):
            tx.run(
                "MATCH (a:Agente {cpf:$cpf}), (b:Bairro {nome:$bairro}) " +
                "CREATE (a)-[:FISCALIZA]->(b);",
                cpf=cpf, bairro=bairro
            )

        self.session.write_transaction(__insert_bairro_if_not_exists, agente.get_bairro())
        self.session.write_transaction(__insert_agente_tx, agente.get_cpf())
        self.session.write_transaction(__insert_fiscaliza_tx, agente.get_cpf(), agente.get_bairro())

    def get(self, cpf):
        def __get_tx(tx, cpf):
            return tx.run(
                "MATCH (a:Agente {cpf:$cpf})-[:FISCALIZA]->(b:Bairro) " +
                "RETURN b.nome; ",
                cpf=cpf
            ).single()[0]

        record = self.session.read_transaction(__get_tx, cpf)

        agente = Agente()
        agente.set_cpf(cpf)
        agente.set_bairro(record)
        return agente

    def update(self, agente):
        def __insert_bairro_if_not_exists(tx, bairro):
            tx.run("MERGE (:Bairro {nome:$bairro});", bairro=bairro)

        def __delete_fiscaliza_tx(tx, cpf):
            tx.run("MATCH (:Agente {cpf:$cpf})-[f:FISCALIZA]->(:Bairro) DELETE f", cpf=cpf)

        def __insert_fiscaliza_tx(tx, cpf, bairro):
            tx.run(
                "MATCH (a:Agente {cpf:$cpf}), (b:Bairro {nome:$bairro}) " +
                "CREATE (a)-[:FISCALIZA]->(b);",
                cpf=cpf, bairro=bairro
            )

        self.session.write_transaction(__insert_bairro_if_not_exists, agente.get_bairro())
        self.session.write_transaction(__delete_fiscaliza_tx, agente.get_cpf())
        self.session.write_transaction(__insert_fiscaliza_tx, agente.get_cpf(), agente.get_bairro())
        