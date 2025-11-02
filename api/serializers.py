# serializers.py
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.openapi import OpenApiTypes
from .models import Perfil, Usuario, EtapaEscolar, Disciplina, StatusEnvio, EnvioMaterial
from datetime import datetime


class PerfilSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Perfil
    
    Campos:
    - id_perfil: ID único do perfil
    - nome_perfil: Nome descritivo do perfil/função
    """
    class Meta:
        model = Perfil
        fields = ['id', 'nome_perfil']


class UsuarioSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Usuario
    
    Campos principais:
    - nome_usuario: Nome completo do usuário
    - matricula: Matrícula única do usuário
    - cpf: CPF no formato XXX.XXX.XXX-XX
    - telefone: Telefone no formato (XX) XXXXX-XXXX
    """
    perfil_nome = serializers.CharField(
        source='id_perfil.nome_perfil', 
        read_only=True,
        help_text="Nome do perfil associado ao usuário"
    )
    
    class Meta:
        model = Usuario
        fields = [
            'id', 'id_perfil', 'perfil_nome', 'nome_usuario', 
            'matricula', 'cpf', 'password', 'telefone'
        ]
        extra_kwargs = {
            'password': {
                'write_only': True,
                'help_text': 'Password do usuário (apenas escrita)'
            },
            'cpf': {
                'help_text': 'CPF no formato XXX.XXX.XXX-XX'
            },
            'telefone': {
                'help_text': 'Telefone no formato (XX) XXXXX-XXXX'
            }
        }
    
    def create(self, validated_data):
        # You might want to hash the password here
        # from django.contrib.auth.hashers import make_password
        # validated_data['senha'] = make_password(validated_data['senha'])
        return super().create(validated_data)


class EtapaEscolarSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo EtapaEscolar
    
    Campos:
    - id: ID único da etapa escolar
    - nome_etapa: Nome da etapa/série escolar
    """
    class Meta:
        model = EtapaEscolar
        fields = ['id', 'nome_etapa']


class DisciplinaSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Disciplina
    
    Campos:
    - id: ID único da disciplina
    - nome_disciplina: Nome da disciplina acadêmica
    """
    class Meta:
        model = Disciplina
        fields = ['id', 'nome_disciplina']


class StatusEnvioSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo StatusEnvio
    
    Campos:
    - id: ID único do status
    - descricao_status: Descrição do status de envio
    """
    class Meta:
        model = StatusEnvio
        fields = ['id', 'descricao_status']


class EnvioMaterialSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo EnvioMaterial.
    Retorna as datas no formato DD-MM-YYYY.
    """
    etapa_nome = serializers.CharField(source='id_etapa.nome_etapa', read_only=True)
    disciplina_nome = serializers.CharField(source='id_disciplina.nome_disciplina', read_only=True)
    usuario_nome = serializers.CharField(source='id_usuario.nome_usuario', read_only=True)
    status_descricao = serializers.CharField(source='id_status.descricao_status', read_only=True)
    mes_referencia_display = serializers.CharField(read_only=True)

    # 👇 Aceita entrada em DD-MM-YYYY ou ISO
    data_limite_envio = serializers.DateField(
        input_formats=['%d-%m-%Y', '%Y-%m-%d'],
        required=False,
        help_text="Data limite no formato DD-MM-YYYY"
    )

    mes_referencia = serializers.IntegerField(required=False, allow_null=True)
    ano_referencia = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = EnvioMaterial
        fields = [
            'id', 'id_etapa', 'etapa_nome', 'id_disciplina', 'disciplina_nome',
            'id_usuario', 'usuario_nome', 'id_status', 'status_descricao',
            'mes_referencia', 'mes_referencia_display', 'ano_referencia',
            'observacoes_gerencia', 'data_envio_escola', 'data_envio_see',
            'data_validacao_gerencia', 'data_envio_formador', 'data_limite_envio'
        ]
        extra_kwargs = {
            'mes_referencia': {'help_text': 'Mês de referência (1-12)', 'required': False},
            'ano_referencia': {'help_text': 'Ano de referência (ex: 2024)', 'required': False},
        }

    def to_representation(self, instance):
        """
        Formata todas as datas no formato DD-MM-YYYY ao retornar os dados.
        """
        data = super().to_representation(instance)

        # Lista dos campos de data que você quer formatar
        date_fields = [
            'data_envio_escola',
            'data_envio_see',
            'data_validacao_gerencia',
            'data_envio_formador',
            'data_limite_envio'
        ]

        for field in date_fields:
            value = data.get(field)
            if value:
                try:
                    # Caso venha no formato ISO, converte para DD-MM-YYYY
                    parsed_date = datetime.strptime(value, '%Y-%m-%d').date()
                    data[field] = parsed_date.strftime('%d-%m-%Y')
                except Exception:
                    # Se já estiver no formato correto ou for nulo, ignora
                    pass

        return data
# Additional serializers for specific use cases
class UsuarioCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para criação de usuários
    Inclui validações adicionais e hash seguro de senha
    """
    senha = serializers.CharField(write_only=True, help_text="Senha do usuário")
    confirm_senha = serializers.CharField(write_only=True, help_text="Confirmação da senha")
    
    class Meta:
        model = Usuario
        fields = [
            'id_perfil', 'nome_usuario', 'matricula', 'cpf', 
            'senha', 'confirm_senha', 'telefone'
        ]
        extra_kwargs = {
            'senha': {'write_only': True}
        }
    
    def validate(self, attrs):
        if attrs.get('senha') != attrs.get('confirm_senha'):
            raise serializers.ValidationError("As senhas não coincidem")
        return attrs

    def create(self, validated_data):
        senha = validated_data.pop('senha')
        validated_data.pop('confirm_senha', None)

        user = Usuario(**validated_data)
        user.set_password(senha) 
        user.save()
        return user


class EnvioMaterialResumoSerializer(serializers.ModelSerializer):
    """
    Serializer resumido para listagem de envios
    Inclui apenas os campos essenciais para performance
    """
    etapa_nome = serializers.CharField(source='id_etapa.nome_etapa', read_only=True)
    disciplina_nome = serializers.CharField(source='id_disciplina.nome_disciplina', read_only=True)
    usuario_nome = serializers.CharField(source='id_usuario.nome_usuario', read_only=True)
    status_descricao = serializers.CharField(source='id_status.descricao_status', read_only=True)
    
    class Meta:
        model = EnvioMaterial
        fields = [
            'id', 'etapa_nome', 'disciplina_nome', 'usuario_nome',
            'status_descricao', 'mes_referencia', 'ano_referencia',
            'data_envio_escola', 'data_limite_envio'
        ]


class EnvioMaterialStatsSerializer(serializers.Serializer):
    """
    Serializer para estatísticas de envios
    """
    total_envios = serializers.IntegerField()
    envios_pendentes = serializers.IntegerField()
    envios_aprovados = serializers.IntegerField()
    envios_rejeitados = serializers.IntegerField()
    mes_referencia = serializers.IntegerField()
    ano_referencia = serializers.IntegerField()
    

class FileUploadSerializer(serializers.Serializer):
    email = serializers.EmailField()
    file = serializers.FileField()