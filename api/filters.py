# filters.py
import django_filters
from django_filters import rest_framework as filters
from django.db.models import Q
from .models import Usuario, EnvioMaterial, Perfil, EtapaEscolar, Disciplina, StatusEnvio


class UsuarioFilter(filters.FilterSet):
    """
    Advanced filtering for Usuario model
    """
    nome_usuario = filters.CharFilter(lookup_expr='icontains', help_text='Filtrar por nome (contém)')
    matricula = filters.CharFilter(lookup_expr='icontains', help_text='Filtrar por matrícula (contém)')
    cpf = filters.CharFilter(lookup_expr='exact', help_text='Filtrar por CPF exato')
    perfil_nome = filters.CharFilter(
        field_name='id_perfil__nome_perfil', 
        lookup_expr='icontains',
        help_text='Filtrar por nome do perfil'
    )
    
    # Date range for creation (if you add created_at field)
    # created_after = filters.DateFilter(field_name='created_at', lookup_expr='gte')
    # created_before = filters.DateFilter(field_name='created_at', lookup_expr='lte')
    
    class Meta:
        model = Usuario
        fields = {
            'id_perfil': ['exact'],
            'nome_usuario': ['exact', 'icontains'],
            'matricula': ['exact', 'icontains'],
        }


class EnvioMaterialFilter(filters.FilterSet):
    """
    Advanced filtering for EnvioMaterial model
    """
    # Basic filters
    ano_referencia = filters.NumberFilter(help_text='Filtrar por ano de referência')
    mes_referencia = filters.NumberFilter(help_text='Filtrar por mês de referência (1-12)')
    
    # Date range filters
    data_envio_escola_gte = filters.DateFilter(
        field_name='data_envio_escola', 
        lookup_expr='gte',
        help_text='Data de envio da escola maior ou igual'
    )
    data_envio_escola_lte = filters.DateFilter(
        field_name='data_envio_escola', 
        lookup_expr='lte',
        help_text='Data de envio da escola menor ou igual'
    )
    data_limite_envio_gte = filters.DateFilter(
        field_name='data_limite_envio', 
        lookup_expr='gte',
        help_text='Data limite maior ou igual'
    )
    data_limite_envio_lte = filters.DateFilter(
        field_name='data_limite_envio', 
        lookup_expr='lte',
        help_text='Data limite menor ou igual'
    )
    
    # Range filters
    ano_range = filters.NumericRangeFilter(
        field_name='ano_referencia',
        help_text='Filtrar por faixa de anos (ex: 2020,2024)'
    )
    
    # Related field filters
    etapa_nome = filters.CharFilter(
        field_name='id_etapa__nome_etapa', 
        lookup_expr='icontains',
        help_text='Filtrar por nome da etapa escolar'
    )
    disciplina_nome = filters.CharFilter(
        field_name='id_disciplina__nome_disciplina', 
        lookup_expr='icontains',
        help_text='Filtrar por nome da disciplina'
    )
    usuario_nome = filters.CharFilter(
        field_name='id_usuario__nome_usuario', 
        lookup_expr='icontains',
        help_text='Filtrar por nome do usuário'
    )
    status_descricao = filters.CharFilter(
        field_name='id_status__descricao_status', 
        lookup_expr='icontains',
        help_text='Filtrar por descrição do status'
    )
    
    # Multiple choice filters
    etapas = filters.ModelMultipleChoiceFilter(
        field_name='id_etapa',
        queryset=EtapaEscolar.objects.all(),
        help_text='Filtrar por múltiplas etapas'
    )
    disciplinas = filters.ModelMultipleChoiceFilter(
        field_name='id_disciplina',
        queryset=Disciplina.objects.all(),
        help_text='Filtrar por múltiplas disciplinas'
    )
    status_list = filters.ModelMultipleChoiceFilter(
        field_name='id_status',
        queryset=StatusEnvio.objects.all(),
        help_text='Filtrar por múltiplos status'
    )
    
    # Boolean filters for special conditions
    tem_observacoes = filters.BooleanFilter(
        method='filter_tem_observacoes',
        help_text='Filtrar envios que têm ou não têm observações'
    )
    atrasado = filters.BooleanFilter(
        method='filter_atrasado',
        help_text='Filtrar envios atrasados'
    )
    pendente_validacao = filters.BooleanFilter(
        method='filter_pendente_validacao',
        help_text='Filtrar envios pendentes de validação'
    )
    
    # Custom search filter
    search = filters.CharFilter(
        method='filter_search',
        help_text='Busca geral em múltiplos campos'
    )
    
    class Meta:
        model = EnvioMaterial
        fields = {
            'id_etapa': ['exact', 'in'],
            'id_disciplina': ['exact', 'in'],
            'id_usuario': ['exact', 'in'],
            'id_status': ['exact', 'in'],
            'mes_referencia': ['exact', 'gte', 'lte'],
            'ano_referencia': ['exact', 'gte', 'lte'],
        }
    
    def filter_tem_observacoes(self, queryset, name, value):
        """
        Filter submissions that have or don't have observations
        """
        if value is True:
            return queryset.exclude(Q(observacoes_gerencia__isnull=True) | Q(observacoes_gerencia=''))
        elif value is False:
            return queryset.filter(Q(observacoes_gerencia__isnull=True) | Q(observacoes_gerencia=''))
        return queryset
    
    def filter_atrasado(self, queryset, name, value):
        """
        Filter overdue submissions
        """
        from django.utils import timezone
        today = timezone.now().date()
        
        if value is True:
            return queryset.filter(
                data_limite_envio__lt=today,
                id_status__in=[1, 2]  # Pending or in progress
            )
        elif value is False:
            return queryset.exclude(
                data_limite_envio__lt=today,
                id_status__in=[1, 2]
            )
        return queryset
    
    def filter_pendente_validacao(self, queryset, name, value):
        """
        Filter submissions pending validation
        """
        if value is True:
            return queryset.filter(
                data_envio_escola__isnull=False,
                data_validacao_gerencia__isnull=True
            )
        elif value is False:
            return queryset.exclude(
                data_envio_escola__isnull=False,
                data_validacao_gerencia__isnull=True
            )
        return queryset
    
    def filter_search(self, queryset, name, value):
        """
        General search across multiple fields
        """
        if value:
            return queryset.filter(
                Q(id_usuario__nome_usuario__icontains=value) |
                Q(id_disciplina__nome_disciplina__icontains=value) |
                Q(id_etapa__nome_etapa__icontains=value) |
                Q(observacoes_gerencia__icontains=value) |
                Q(id_usuario__matricula__icontains=value)
            ).distinct()
        return queryset


class PerfilFilter(filters.FilterSet):
    """
    Simple filtering for Perfil model
    """
    nome_perfil = filters.CharFilter(
        lookup_expr='icontains',
        help_text='Filtrar por nome do perfil (contém)'
    )
    
    class Meta:
        model = Perfil
        fields = ['nome_perfil']


class EtapaEscolarFilter(filters.FilterSet):
    """
    Simple filtering for EtapaEscolar model
    """
    nome_etapa = filters.CharFilter(
        lookup_expr='icontains',
        help_text='Filtrar por nome da etapa (contém)'
    )
    
    class Meta:
        model = EtapaEscolar
        fields = ['nome_etapa']


class DisciplinaFilter(filters.FilterSet):
    """
    Simple filtering for Disciplina model
    """
    nome_disciplina = filters.CharFilter(
        lookup_expr='icontains',
        help_text='Filtrar por nome da disciplina (contém)'
    )
    
    class Meta:
        model = Disciplina
        fields = ['nome_disciplina']


class StatusEnvioFilter(filters.FilterSet):
    """
    Simple filtering for StatusEnvio model
    """
    descricao_status = filters.CharFilter(
        lookup_expr='icontains',
        help_text='Filtrar por descrição do status (contém)'
    )
    
    class Meta:
        model = StatusEnvio
        fields = ['descricao_status']