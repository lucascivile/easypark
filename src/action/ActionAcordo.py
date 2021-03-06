from modelo.relacional import Acordo, Solicitacao
from modelo.documentos import Acordo as AcordoDoc
from bd.documentos import AcordoDAO as AcordoDAODoc
from bd.relacional import SolicitacaoDAO
from bd.relacional import AcordoDAO
from bd.relacional import VagaDAO

import datetime

class ActionAcordo:

    @staticmethod
    def insert(id_solicitacao, cpf_proprietario, cpf_motorista):
        solicitacaoDAO = SolicitacaoDAO()
        solicitacao = solicitacaoDAO.get(id_solicitacao)
        id_vaga = solicitacao.get_id_vaga()

        acordoDAO = AcordoDAO()
        acordo = Acordo()

        acordo.set_id_solicitacao(id_solicitacao)

        acordoDAODoc = AcordoDAODoc()
        acordoDoc = AcordoDoc()

        try:
            id_acordo = acordoDAO.insert(acordo)
            acordoDoc.set_id_acordo(id_acordo)
            acordoDAODoc.insert(acordoDoc, cpf_proprietario, cpf_motorista, id_vaga)
        except:
            return False
        else:
            return True

    @staticmethod
    def list_future_by_motorista(cpf):
        acordoDAO = AcordoDAO()
        acordo_output = []
        
        try:
            acordos = acordoDAO.list()
            solicitacaoDAO = SolicitacaoDAO()

            for a in acordos:
                s = solicitacaoDAO.get(a.get_id_solicitacao())

                now = datetime.datetime.now()
                if s.get_cpf_motorista() == cpf and s.get_inicio() > now:
                    acordo = {"id_acordo": a.get_id_acordo(),
                                      "id_solicitacao": a.get_id_solicitacao(),
                                      "id_vaga": s.get_id_vaga(),
                                      "inicio": s.get_inicio(),
                                      "fim": s.get_fim()}

                    acordo_output.append(acordo)
        except:
            return None
        else:
            return acordo_output

    @staticmethod
    def list_past_by_motorista(cpf):
        acordoDAO = AcordoDAO()
        acordos_output = []
        
        try:
            acordos = acordoDAO.list()
            solicitacaoDAO = SolicitacaoDAO()
            vagaDAO = VagaDAO()

            for a in acordos:
                s = solicitacaoDAO.get(a.get_id_solicitacao())
                v = vagaDAO.get(s.get_id_vaga())

                now = datetime.datetime.now()
                if s.get_cpf_motorista() == cpf and s.get_fim() < now:
                    acordo = {"id_acordo": a.get_id_acordo(),
                                      "id_solicitacao": a.get_id_solicitacao(),
                                      "id_vaga": s.get_id_vaga(),
                                      "inicio": s.get_inicio(),
                                      "fim": s.get_fim(),
                                      "cpf_proprietario": v.get_cpf_proprietario()}
                    acordos_output.append(acordo)
        except:
            return None
        else:
            return acordos_output

    
    @staticmethod
    def list_future_by_proprietario(cpf):
        acordoDAO = AcordoDAO()
        acordos_output = []
        
        try:
            acordos = acordoDAO.list()
            solicitacaoDAO = SolicitacaoDAO()
            vagaDAO = VagaDAO()

            for a in acordos:
                s = solicitacaoDAO.get(a.get_id_solicitacao())
                v = vagaDAO.get(s.get_id_vaga())

                now = datetime.datetime.now()
                if v.get_cpf_proprietario() == cpf and s.get_inicio() > now:
                    acordo = {"id_acordo": a.get_id_acordo(),
                                      "id_solicitacao": a.get_id_solicitacao(),
                                      "id_vaga": s.get_id_vaga(),
                                      "inicio": s.get_inicio(),
                                      "fim": s.get_fim()}
                    acordos_output.append(acordo)
        except:
            return None
        else:
            return acordos_output

    @staticmethod
    def list_past_by_proprietario(cpf):
        acordoDAO = AcordoDAO()
        acordos_output = []
        
        try:
            acordos = acordoDAO.list()
            solicitacaoDAO = SolicitacaoDAO()
            vagaDAO = VagaDAO()

            for a in acordos:
                s = solicitacaoDAO.get(a.get_id_solicitacao())
                v = vagaDAO.get(s.get_id_vaga())

                now = datetime.datetime.now()
                if v.get_cpf_proprietario() == cpf and s.get_fim() < now:
                    acordo = {"id_acordo": a.get_id_acordo(),
                                      "id_solicitacao": a.get_id_solicitacao(),
                                      "id_vaga": s.get_id_vaga(),
                                      "inicio": s.get_inicio(),
                                      "fim": s.get_fim(),
                                      "cpf_motorista": s.get_cpf_motorista()}
                    acordos_output.append(acordo)
        except:
            return None
        else:
            return acordos_output

    @staticmethod
    def insert_nota_to_proprietario(id_acordo, nota):
        acordoDAO = AcordoDAO()
        vagaDAO = VagaDAO()
        solicitacaoDAO = SolicitacaoDAO()

        solicitacao = solicitacaoDAO.get(acordoDAO.get(id_acordo).get_id_solicitacao())
        vaga = vagaDAO.get(solicitacao.get_id_vaga())
        acordoDAODoc = AcordoDAODoc()

        try:
            acordoDoc = acordoDAODoc.get(id_acordo)
            acordoDoc.set_nota_MP(nota)
            acordoDAODoc.update(acordoDoc, vaga.get_cpf_proprietario(), solicitacao.get_cpf_motorista(), solicitacao.get_id_vaga())
        except:
            return False
        else:
            return True

    @staticmethod
    def insert_nota_to_motorista(id_acordo, nota):
        acordoDAO = AcordoDAO()
        vagaDAO = VagaDAO()
        solicitacaoDAO = SolicitacaoDAO()

        solicitacao = solicitacaoDAO.get(acordoDAO.get(id_acordo).get_id_solicitacao())
        vaga = vagaDAO.get(solicitacao.get_id_vaga())

        acordoDAODoc = AcordoDAODoc()

        try:
            acordoDoc = acordoDAODoc.get(id_acordo)
            acordoDoc.set_nota_PM(nota)
            acordoDAODoc.update(acordoDoc, vaga.get_cpf_proprietario(), solicitacao.get_cpf_motorista(), solicitacao.get_id_vaga())
        except:
            return False
        else:
            return True
