# models.py
from django.db import models
from django.core.validators import RegexValidator


class BaseModel(models.Model):
    """
    Abstract base model to include common fields
    """
    created_by = models.CharField(max_length=100, null=True, blank=True, verbose_name="Criado por")
    updated_by = models.CharField(max_length=100, null=True, blank=True, verbose_name="Atualizado por")
    deleted_by = models.CharField(max_length=100, null=True, blank=True, verbose_name="Deletado por")
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True,verbose_name="Atualizado em")
    deleted_at = models.DateTimeField(blank=True, null=True, default=None, verbose_name="Deletado em")
    class Meta:
        abstract = True


class Perfil(BaseModel):
    """
    Model representing user profiles/roles
    """
    id_perfil = models.AutoField(primary_key=True)
    nome_perfil = models.CharField(max_length=100, verbose_name="Nome do Perfil")
    
    class Meta:
        db_table = 'Perfil'
        verbose_name = "Perfil"
        verbose_name_plural = "Perfis"
    
    def __str__(self):
        return self.nome_perfil


class Usuario(BaseModel):
    """
    Model representing system users
    """
    # CPF validator
    cpf_validator = RegexValidator(
        regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',
        message="CPF deve estar no formato XXX.XXX.XXX-XX"
    )
    
    # Phone validator
    phone_validator = RegexValidator(
        regex=r'^\(\d{2}\)\s\d{4,5}-\d{4}$',
        message="Telefone deve estar no formato (XX) XXXXX-XXXX"
    )
    
    id_usuario = models.AutoField(primary_key=True)
    id_perfil = models.ForeignKey(
        Perfil, 
        on_delete=models.CASCADE,
        db_column='Id_Perfil',
        verbose_name="Perfil"
    )
    nome_usuario = models.CharField(max_length=100, verbose_name="Nome do Usuário")
    matricula = models.CharField(max_length=50, unique=True, verbose_name="Matrícula")
    cpf = models.CharField(
        max_length=14, 
        unique=True, 
        validators=[cpf_validator],
        verbose_name="CPF"
    )
    senha = models.CharField(max_length=100, verbose_name="Senha")
    telefone = models.CharField(
        max_length=20, 
        validators=[phone_validator],
        blank=True, 
        null=True,
        verbose_name="Telefone"
    )
    
    class Meta:
        db_table = 'Usuario'
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
    
    def __str__(self):
        return f"{self.nome_usuario} - {self.matricula}"


class EtapaEscolar(BaseModel):
    """
    Model representing school stages/grades
    """
    id_etapa = models.AutoField(primary_key=True)
    nome_etapa = models.CharField(max_length=100, verbose_name="Nome da Etapa")
    
    class Meta:
        db_table = 'Etapa_Escolar'
        verbose_name = "Etapa Escolar"
        verbose_name_plural = "Etapas Escolares"
    
    def __str__(self):
        return self.nome_etapa


class Disciplina(BaseModel):
    """
    Model representing academic subjects
    """
    id_disciplina = models.AutoField(primary_key=True)
    nome_disciplina = models.CharField(max_length=100, verbose_name="Nome da Disciplina")
    
    class Meta:
        db_table = 'Disciplina'
        verbose_name = "Disciplina"
        verbose_name_plural = "Disciplinas"
    
    def __str__(self):
        return self.nome_disciplina


class StatusEnvio(BaseModel):
    """
    Model representing submission status
    """
    id_status = models.AutoField(primary_key=True)
    descricao_status = models.CharField(max_length=100, verbose_name="Descrição do Status")
    
    class Meta:
        db_table = 'Status_Envio'
        verbose_name = "Status de Envio"
        verbose_name_plural = "Status de Envio"
    
    def __str__(self):
        return self.descricao_status


class EnvioMaterial(BaseModel):
    """
    Model representing material submissions
    """
    MONTH_CHOICES = [
        (1, 'Janeiro'), (2, 'Fevereiro'), (3, 'Março'), (4, 'Abril'),
        (5, 'Maio'), (6, 'Junho'), (7, 'Julho'), (8, 'Agosto'),
        (9, 'Setembro'), (10, 'Outubro'), (11, 'Novembro'), (12, 'Dezembro')
    ]
    
    id_envio = models.AutoField(primary_key=True)
    id_etapa = models.ForeignKey(
        EtapaEscolar, 
        on_delete=models.CASCADE,
        db_column='Id_Etapa',
        verbose_name="Etapa Escolar"
    )
    id_disciplina = models.ForeignKey(
        Disciplina, 
        on_delete=models.CASCADE,
        db_column='Id_Disciplina',
        verbose_name="Disciplina"
    )
    id_usuario = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE,
        db_column='Id_Usuario',
        verbose_name="Usuário"
    )
    id_status = models.ForeignKey(
        StatusEnvio, 
        on_delete=models.CASCADE,
        db_column='Id_Status',
        verbose_name="Status"
    )
    mes_referencia = models.IntegerField(
        choices=MONTH_CHOICES,
        verbose_name="Mês de Referência"
    )
    ano_referencia = models.IntegerField(verbose_name="Ano de Referência")
    observacoes_gerencia = models.TextField(
        blank=True, 
        null=True,
        verbose_name="Observações da Gerência"
    )
    data_envio_escola = models.DateField(
        blank=True, 
        null=True,
        verbose_name="Data de Envio da Escola"
    )
    data_envio_see = models.DateField(
        blank=True, 
        null=True,
        verbose_name="Data de Envio SEE"
    )
    data_validacao_gerencia = models.DateField(
        blank=True, 
        null=True,
        verbose_name="Data de Validação da Gerência"
    )
    data_envio_formador = models.DateField(
        blank=True, 
        null=True,
        verbose_name="Data de Envio ao Formador"
    )
    data_limite_envio = models.DateField(
        blank=True, 
        null=True,
        verbose_name="Data Limite de Envio"
    )
    
    class Meta:
        db_table = 'Envio_material'
        verbose_name = "Envio de Material"
        verbose_name_plural = "Envios de Material"
        # Add unique constraint to prevent duplicate submissions
        unique_together = ['id_etapa', 'id_disciplina', 'id_usuario', 'mes_referencia', 'ano_referencia']
    
    def __str__(self):
        return f"Envio {self.id_envio} - {self.id_disciplina} - {self.mes_referencia}/{self.ano_referencia}"
    
    @property
    def mes_referencia_display(self):
        """Returns the month name in Portuguese"""
        months = dict(self.MONTH_CHOICES)
        return months.get(self.mes_referencia, self.mes_referencia)