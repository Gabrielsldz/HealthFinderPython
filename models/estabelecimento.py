from pydantic import BaseModel
from typing import Optional

class estabelecimento(BaseModel):
    codigo_cnes: int
    numero_cnpj_entidade: Optional[str] = None
    nome_razao_social: Optional[str] = None
    nome_fantasia: Optional[str] = None
    natureza_organizacao_entidade: Optional[str] = None
    tipo_gestao: Optional[str] = None
    descricao_nivel_hierarquia: Optional[str] = None
    descricao_esfera_administrativa: Optional[str] = None
    codigo_tipo_unidade: int
    codigo_cep_estabelecimento: Optional[str] = None
    endereco_estabelecimento: Optional[str] = None
    numero_estabelecimento: Optional[str] = None
    bairro_estabelecimento: Optional[str] = None
    numero_telefone_estabelecimento: Optional[str] = None
    latitude_estabelecimento_decimo_grau: Optional[float] = None
    longitude_estabelecimento_decimo_grau: Optional[float] = None
    endereco_email_estabelecimento: Optional[str] = None
    numero_cnpj: Optional[str] = None
    codigo_identificador_turno_atendimento: Optional[str] = None
    descricao_turno_atendimento: Optional[str] = None
    estabelecimento_faz_atendimento_ambulatorial_sus: Optional[str] = None
    codigo_estabelecimento_saude: Optional[str] = None
    codigo_uf: int
    codigo_municipio: int
    descricao_natureza_juridica_estabelecimento: Optional[str] = None
    codigo_motivo_desabilitacao_estabelecimento: Optional[str] = None
    estabelecimento_possui_centro_cirurgico: Optional[int] = None
    estabelecimento_possui_centro_obstetrico: Optional[int] = None
    estabelecimento_possui_centro_neonatal: Optional[int] = None
    estabelecimento_possui_atendimento_hospitalar: Optional[int] = None
    estabelecimento_possui_servico_apoio: Optional[int] = None
    estabelecimento_possui_atendimento_ambulatorial: Optional[int] = None
    codigo_atividade_ensino_unidade: Optional[str] = None
    codigo_natureza_organizacao_unidade: Optional[str] = None
    codigo_nivel_hierarquia_unidade: Optional[str] = None
    codigo_esfera_administrativa_unidade: Optional[str] = None