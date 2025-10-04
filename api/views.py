# views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from django.db.models import Count, Q
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample
from drf_spectacular.openapi import OpenApiTypes
from django.core.mail import EmailMessage
from .serializers import FileUploadSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


from .models import *
from .serializers import *


class HelloView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print(request.user)
        return Response({'message': f'Olá, {request.user}!'})


@extend_schema_view(
    list=extend_schema(
        summary="Listar perfis",
        description="Retorna uma lista paginada de todos os perfis disponíveis no sistema.",
        tags=["Perfis"]
    ),
    create=extend_schema(
        summary="Criar perfil",
        description="Cria um novo perfil no sistema.",
        tags=["Perfis"]
    ),
    retrieve=extend_schema(
        summary="Obter perfil",
        description="Retorna os detalhes de um perfil específico.",
        tags=["Perfis"]
    ),
    update=extend_schema(
        summary="Atualizar perfil",
        description="Atualiza completamente um perfil existente.",
        tags=["Perfis"]
    ),
    partial_update=extend_schema(
        summary="Atualizar parcialmente perfil",
        description="Atualiza parcialmente um perfil existente.",
        tags=["Perfis"]
    ),
    destroy=extend_schema(
        summary="Excluir perfil",
        description="Remove um perfil do sistema.",
        tags=["Perfis"]
    ),
)
class PerfilViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Perfil model with full CRUD operations
    """
    permission_classes = [IsAuthenticated]
    queryset = Perfil.objects.all()
    serializer_class = PerfilSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['nome_perfil']
    ordering_fields = ['id_perfil', 'nome_perfil']
    ordering = ['id_perfil']


@extend_schema_view(
    list=extend_schema(
        summary="Listar usuários",
        description="Retorna uma lista paginada de todos os usuários do sistema.",
        parameters=[
            OpenApiParameter(
                name='search',
                type=OpenApiTypes.STR,
                description='Busca por nome, matrícula ou CPF'
            ),
            OpenApiParameter(
                name='id_perfil',
                type=OpenApiTypes.INT,
                description='Filtrar por ID do perfil'
            ),
        ],
        tags=["Usuários"]
    ),
    create=extend_schema(
        summary="Criar usuário",
        description="Cria um novo usuário no sistema.",
        examples=[
            OpenApiExample(
                'Exemplo de criação',
                value={
                    "id_perfil": 1,
                    "nome_usuario": "João Silva",
                    "matricula": "12345",
                    "cpf": "123.456.789-00",
                    "confirm_senha": "senha123",
                    "senha": "senha123",
                    "telefone": "(85) 99999-9999"
                }
            )
        ],
        tags=["Usuários"]
    ),
    retrieve=extend_schema(
        summary="Obter usuário",
        description="Retorna os detalhes de um usuário específico.",
        tags=["Usuários"]
    ),
    update=extend_schema(
        summary="Atualizar usuário",
        description="Atualiza completamente um usuário existente.",
        tags=["Usuários"]
    ),
    partial_update=extend_schema(
        summary="Atualizar parcialmente usuário",
        description="Atualiza parcialmente um usuário existente.",
        tags=["Usuários"]
    ),
    destroy=extend_schema(
        summary="Excluir usuário",
        description="Remove um usuário do sistema.",
        tags=["Usuários"]
    ),
)
class UsuarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para o modelo de usuário
    """
    queryset = Usuario.objects.select_related('id_perfil').all()
    serializer_class = UsuarioSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['nome_usuario', 'matricula', 'cpf']
    ordering_fields = ['id_usuario', 'nome_usuario', 'matricula']
    ordering = ['id_usuario']
    filterset_fields = ['id_perfil']

    def get_serializer_class(self):
        if self.action == 'create':
            return UsuarioCreateSerializer
        return UsuarioSerializer

    @extend_schema(
        summary="Obter usuários por perfil",
        description="Retorna uma lista de usuários filtrados por ID do perfil.",
        parameters=[
            OpenApiParameter(
                name='perfil_id',
                type=OpenApiTypes.INT,
                description='ID do perfil para filtrar os usuários',
                required=True
            )
        ],
        tags=["Usuários"],
        responses={200: UsuarioSerializer(many=True)}
    )
    @action(detail=False, methods=['get'])
    def by_perfil(self, request):
        perfil_id = request.query_params.get('perfil_id')
        if perfil_id:
            usuarios = self.queryset.filter(id_perfil=perfil_id)
            serializer = self.get_serializer(usuarios, many=True)
            return Response(serializer.data)
        return Response({'error': 'perfil_id parameter is required'}, 
                        status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    list=extend_schema(
        summary="Listar etapas escolares",
        description="Retorna uma lista de todas as etapas escolares (séries) disponíveis.",
        tags=["Etapas Escolares"]
    ),
    create=extend_schema(
        summary="Criar etapa escolar",
        description="Cria uma nova etapa escolar no sistema.",
        tags=["Etapas Escolares"]
    ),
    retrieve=extend_schema(
        summary="Obter etapa escolar",
        description="Retorna os detalhes de uma etapa escolar específica.",
        tags=["Etapas Escolares"]
    ),
    update=extend_schema(
        summary="Atualizar etapa escolar",
        description="Atualiza completamente uma etapa escolar existente.",
        tags=["Etapas Escolares"]
    ),
    partial_update=extend_schema(
        summary="Atualizar parcialmente etapa escolar",
        description="Atualiza parcialmente uma etapa escolar existente.",
        tags=["Etapas Escolares"]
    ),
    destroy=extend_schema(
        summary="Excluir etapa escolar",
        description="Remove uma etapa escolar do sistema.",
        tags=["Etapas Escolares"]
    ),
)
class EtapaEscolarViewSet(viewsets.ModelViewSet):
    """
    ViewSet for EtapaEscolar model with full CRUD operations
    """
    permission_classes = [IsAuthenticated]
    queryset = EtapaEscolar.objects.all()
    serializer_class = EtapaEscolarSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['nome_etapa']
    ordering_fields = ['id_etapa', 'nome_etapa']
    ordering = ['id_etapa']


@extend_schema_view(
    list=extend_schema(
        summary="Listar disciplinas",
        description="Retorna uma lista de todas as disciplinas disponíveis no sistema.",
        tags=["Disciplinas"]
    ),
    create=extend_schema(
        summary="Criar disciplina",
        description="Cria uma nova disciplina no sistema.",
        tags=["Disciplinas"]
    ),
    retrieve=extend_schema(
        summary="Obter disciplina",
        description="Retorna os detalhes de uma disciplina específica.",
        tags=["Disciplinas"]
    ),
    update=extend_schema(
        summary="Atualizar disciplina",
        description="Atualiza completamente uma disciplina existente.",
        tags=["Disciplinas"]
    ),
    partial_update=extend_schema(
        summary="Atualizar parcialmente disciplina",
        description="Atualiza parcialmente uma disciplina existente.",
        tags=["Disciplinas"]
    ),
    destroy=extend_schema(
        summary="Excluir disciplina",
        description="Remove uma disciplina do sistema.",
        tags=["Disciplinas"]
    ),
)
class DisciplinaViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Disciplina model with full CRUD operations
    """
    permission_classes = [IsAuthenticated]
    queryset = Disciplina.objects.all()
    serializer_class = DisciplinaSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['nome_disciplina']
    ordering_fields = ['id_disciplina', 'nome_disciplina']
    ordering = ['id_disciplina']


@extend_schema_view(
    list=extend_schema(
        summary="Listar status de envio",
        description="Retorna uma lista de todos os status de envio disponíveis.",
        tags=["Status de Envio"]
    ),
    create=extend_schema(
        summary="Criar status de envio",
        description="Cria um novo status de envio no sistema.",
        tags=["Status de Envio"]
    ),
    retrieve=extend_schema(
        summary="Obter status de envio",
        description="Retorna os detalhes de um status de envio específico.",
        tags=["Status de Envio"]
    ),
    update=extend_schema(
        summary="Atualizar status de envio",
        description="Atualiza completamente um status de envio existente.",
        tags=["Status de Envio"]
    ),
    partial_update=extend_schema(
        summary="Atualizar parcialmente status de envio",
        description="Atualiza parcialmente um status de envio existente.",
        tags=["Status de Envio"]
    ),
    destroy=extend_schema(
        summary="Excluir status de envio",
        description="Remove um status de envio do sistema.",
        tags=["Status de Envio"]
    ),
)
class StatusEnvioViewSet(viewsets.ModelViewSet):
    """
    ViewSet for StatusEnvio model with full CRUD operations
    """
    permission_classes = [IsAuthenticated]
    queryset = StatusEnvio.objects.all()
    serializer_class = StatusEnvioSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['descricao_status']
    ordering_fields = ['id_status', 'descricao_status']
    ordering = ['id_status']


class EnvioMaterialFilter(filters.FilterSet):
    """
    Custom filter for EnvioMaterial
    """
    ano_referencia = filters.NumberFilter()
    mes_referencia = filters.NumberFilter()
    data_envio_escola_gte = filters.DateFilter(field_name='data_envio_escola', lookup_expr='gte')
    data_envio_escola_lte = filters.DateFilter(field_name='data_envio_escola', lookup_expr='lte')
    data_limite_envio_gte = filters.DateFilter(field_name='data_limite_envio', lookup_expr='gte')
    data_limite_envio_lte = filters.DateFilter(field_name='data_limite_envio', lookup_expr='lte')
    
    class Meta:
        model = EnvioMaterial
        fields = [
            'id_etapa', 'id_disciplina', 'id_usuario', 'id_status',
            'ano_referencia', 'mes_referencia'
        ]


@extend_schema_view(
    list=extend_schema(
        summary="Listar envios de material",
        description="Retorna uma lista paginada de todos os envios de material didático.",
        parameters=[
            OpenApiParameter(
                name='search',
                type=OpenApiTypes.STR,
                description='Busca por nome do usuário, disciplina, etapa ou observações'
            ),
            OpenApiParameter(
                name='id_etapa',
                type=OpenApiTypes.INT,
                description='Filtrar por ID da etapa escolar'
            ),
            OpenApiParameter(
                name='id_disciplina',
                type=OpenApiTypes.INT,
                description='Filtrar por ID da disciplina'
            ),
            OpenApiParameter(
                name='id_usuario',
                type=OpenApiTypes.INT,
                description='Filtrar por ID do usuário'
            ),
            OpenApiParameter(
                name='id_status',
                type=OpenApiTypes.INT,
                description='Filtrar por ID do status'
            ),
            OpenApiParameter(
                name='ano_referencia',
                type=OpenApiTypes.INT,
                description='Filtrar por ano de referência'
            ),
            OpenApiParameter(
                name='mes_referencia',
                type=OpenApiTypes.INT,
                description='Filtrar por mês de referência (1-12)'
            ),
        ],
        tags=["Envios de Material"]
    ),
    create=extend_schema(
        summary="Criar envio de material",
        description="Registra um novo envio de material didático.",
        examples=[
            OpenApiExample(
                'Exemplo de criação',
                value={
                    "id_etapa": 1,
                    "id_disciplina": 1,
                    "id_usuario": 1,
                    "id_status": 1,
                    "mes_referencia": 3,
                    "ano_referencia": 2024,
                    "observacoes_gerencia": "Material aprovado",
                    "data_limite_envio": "2024-03-15"
                }
            )
        ],
        tags=["Envios de Material"]
    ),
    retrieve=extend_schema(
        summary="Obter envio de material",
        description="Retorna os detalhes de um envio de material específico.",
        tags=["Envios de Material"]
    ),
    update=extend_schema(
        summary="Atualizar envio de material",
        description="Atualiza completamente um envio de material existente.",
        tags=["Envios de Material"]
    ),
    partial_update=extend_schema(
        summary="Atualizar parcialmente envio de material",
        description="Atualiza parcialmente um envio de material existente.",
        tags=["Envios de Material"]
    ),
    destroy=extend_schema(
        summary="Excluir envio de material",
        description="Remove um envio de material do sistema.",
        tags=["Envios de Material"]
    ),
)
class EnvioMaterialViewSet(viewsets.ModelViewSet):
    """
    ViewSet for EnvioMaterial model with full CRUD operations
    """
    permission_classes = [IsAuthenticated]
    queryset = EnvioMaterial.objects.select_related(
        'id_etapa', 'id_disciplina', 'id_usuario', 'id_status'
    ).all()
    serializer_class = EnvioMaterialSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_class = EnvioMaterialFilter
    search_fields = [
        'id_usuario__nome_usuario', 'id_disciplina__nome_disciplina',
        'id_etapa__nome_etapa', 'observacoes_gerencia'
    ]
    ordering_fields = [
        'id_envio', 'mes_referencia', 'ano_referencia', 
        'data_envio_escola', 'data_limite_envio'
    ]
    ordering = ['-id_envio']
    
    def get_serializer_class(self):
        """
        Return different serializers for different actions
        """
        # if self.action == 'list':
        #     print("List action - using resumo serializer")
        #     return EnvioMaterialResumoSerializer
        return EnvioMaterialSerializer
    
    @extend_schema(
        summary="Obter envios por usuário",
        description="Retorna uma lista de envios de material filtrados por ID do usuário.",
        parameters=[
            OpenApiParameter(
                name='user_id',
                type=OpenApiTypes.INT,
                description='ID do usuário para filtrar os envios',
                required=True
            )
        ],
        tags=["Envios de Material"],
        responses={200: EnvioMaterialSerializer(many=True)}
    )
    @action(detail=False, methods=['get'])
    def by_user(self, request):
        """
        Get material submissions by user
        """
        user_id = request.query_params.get('user_id')
        if user_id:
            envios = self.queryset.filter(id_usuario=user_id)
            serializer = EnvioMaterialSerializer(envios, many=True)
            return Response(serializer.data)
        return Response({'error': 'user_id parameter is required'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        summary="Obter envios por período",
        description="Retorna uma lista de envios de material filtrados por mês e ano de referência.",
        parameters=[
            OpenApiParameter(
                name='mes',
                type=OpenApiTypes.INT,
                description='Mês de referência (1-12)',
                required=True
            ),
            OpenApiParameter(
                name='ano',
                type=OpenApiTypes.INT,
                description='Ano de referência',
                required=True
            )
        ],
        tags=["Envios de Material"],
        responses={200: EnvioMaterialSerializer(many=True)}
    )
    @action(detail=False, methods=['get'])
    def by_period(self, request):
        """
        Get material submissions by month and year
        """
        mes = request.query_params.get('mes')
        ano = request.query_params.get('ano')
        
        if mes and ano:
            envios = self.queryset.filter(
                mes_referencia=mes, 
                ano_referencia=ano
            )
            serializer = EnvioMaterialSerializer(envios, many=True)
            return Response(serializer.data)
        return Response({'error': 'mes and ano parameters are required'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        summary="Obter envios pendentes",
        description="Retorna uma lista de envios de material com status pendente.",
        parameters=[
            OpenApiParameter(
                name='status_id',
                type=OpenApiTypes.INT,
                description='ID do status considerado como pendente (padrão: 1)'
            )
        ],
        tags=["Envios de Material"],
        responses={200: EnvioMaterialSerializer(many=True)}
    )
    @action(detail=False, methods=['get'])
    def pending(self, request):
        """
        Get pending submissions
        """
        pending_status = request.query_params.get('status_id', 1)
        envios = self.queryset.filter(id_status=pending_status)
        serializer = EnvioMaterialSerializer(envios, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        summary="Obter estatísticas de envios",
        description="Retorna estatísticas dos envios por período.",
        parameters=[
            OpenApiParameter(
                name='mes',
                type=OpenApiTypes.INT,
                description='Mês de referência (opcional)'
            ),
            OpenApiParameter(
                name='ano',
                type=OpenApiTypes.INT,
                description='Ano de referência (opcional)'
            )
        ],
        tags=["Envios de Material"],
        responses={200: EnvioMaterialStatsSerializer()}
    )
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        Get submission statistics
        """
        mes = request.query_params.get('mes')
        ano = request.query_params.get('ano')
        
        queryset = self.queryset
        
        if mes:
            queryset = queryset.filter(mes_referencia=mes)
        if ano:
            queryset = queryset.filter(ano_referencia=ano)
        
        # Count by status (assuming status IDs: 1=pending, 2=approved, 3=rejected)
        stats = queryset.aggregate(
            total_envios=Count('id_envio'),
            envios_pendentes=Count('id_envio', filter=Q(id_status=1)),
            envios_aprovados=Count('id_envio', filter=Q(id_status=2)),
            envios_rejeitados=Count('id_envio', filter=Q(id_status=3))
        )
        
        stats['mes_referencia'] = int(mes) if mes else None
        stats['ano_referencia'] = int(ano) if ano else None
        
        serializer = EnvioMaterialStatsSerializer(data=stats)
        serializer.is_valid()
        return Response(serializer.data)
    
    @extend_schema(
        summary="Obter envios em atraso",
        description="Retorna envios que passaram da data limite.",
        tags=["Envios de Material"],
        responses={200: EnvioMaterialSerializer(many=True)}
    )
    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """
        Get overdue submissions
        """
        from django.utils import timezone
        today = timezone.now().date()
        
        envios = self.queryset.filter(
            data_limite_envio__lt=today,
            id_status__in=[1, 2]  # Only pending or in-progress submissions
        )
        serializer = EnvioMaterialSerializer(envios, many=True)
        return Response(serializer.data)
    
# app/views.py

class FileUploadView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            file = serializer.validated_data["file"]

            try:
                mail = EmailMessage(
                    subject="Arquivo enviado pelo sistema",
                    body="Segue o arquivo em anexo.",
                    from_email=None,  # usa DEFAULT_FROM_EMAIL
                    to=[email],
                )
                mail.attach(file.name, file.read(), file.content_type)
                mail.send()

                return Response({"message": "Arquivo enviado com sucesso!"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
