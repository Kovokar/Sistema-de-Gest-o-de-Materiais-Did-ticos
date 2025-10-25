# views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from django.db.models import Count, Q
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample, OpenApiResponse
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

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """
        Retorna as informações do usuário autenticado
        """
        usuario = request.user  # Usuário autenticado via token/session
        serializer = self.get_serializer(usuario)
        return Response(serializer.data)
    
    @extend_schema(
        summary="Criar usuário com perfil de Professor automaticamente",
        description=(
            "Cria um novo usuário atribuindo automaticamente o perfil de Professor. "
            "Não é necessário enviar o campo `id_perfil`, pois ele é definido pelo sistema."
        ),
        tags=["Usuários"],
        request=UsuarioCreateSerializer,
        responses={
            201: UsuarioSerializer,
            400: OpenApiTypes.OBJECT,
        },
        examples=[
            {
                "matricula": "3456789",
                "cpf": "987.654.321-00",
                "nome_usuario": "Professor João",
                "senha": "1234",
                "confirm_senha": "1234",
                "telefone": "(11) 99999-8888"
            }
        ],
    )
    @action(detail=False, methods=['post'], url_path='create-professor')
    def create_professor(self, request):
        """
        Cria um novo usuário com perfil de professor automaticamente.
        """
        try:
            perfil_professor = Perfil.objects.get(nome_perfil__iexact='professor')
        except Perfil.DoesNotExist:
            return Response(
                {'error': 'Perfil de professor não encontrado.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Copia os dados do request e força o id_perfil do professor
        data = request.data.copy()
        data['id_perfil'] = perfil_professor.id

        serializer = UsuarioCreateSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UsuarioSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        'id', 'mes_referencia', 'ano_referencia', 
        'data_envio_escola', 'data_limite_envio'
    ]
    ordering = ['-id']
    
    @extend_schema(
        summary="Criar envio de material",
        description=(
            "Cria um novo registro de envio de material didático.\n\n"
            "- Se `mes_referencia` não for informado, o sistema usará o mês atual.\n"
            "- `data_limite_envio` deve ser enviada no formato **DD-MM-YYYY**."
        ),
        request=EnvioMaterialSerializer,
        responses={201: EnvioMaterialSerializer},
        tags=["Envio de Materiais"]
    )
    @action(detail=False, methods=['post'])
    def perform_create(self, serializer):
        """
        Preenche automaticamente mês/ano se não forem enviados.
        """
        now = timezone.now()

        # Se o mês não foi informado, pega o mês e ano atuais
        mes = serializer.validated_data.get('mes_referencia') or now.month
        ano = serializer.validated_data.get('ano_referencia') or now.year

        serializer.save(
            mes_referencia=mes,
            ano_referencia=ano,
            data_envio_formador=datetime.now().date()
        )
    
    @extend_schema(
    summary="Validar ou rejeitar um envio de material",
    description=(
        "Define o status do envio como **Validado** ou **Rejeitado** com base no campo `validado`. "
        "Registra também a observação da gerência e a data da validação."
    ),
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "validado": {"type": "boolean", "example": True},
                "observacoes_gerencia": {"type": "string", "example": "Material revisado e aprovado."}
            },
            "required": ["validado"]
        }
    },
    responses={200: EnvioMaterialSerializer, 400: OpenApiResponse(description="Parâmetro inválido")},
    tags=["Envios de Material"]
)
    @action(detail=True, methods=['post'])
    def validar(self, request, pk=None):
        """
        Valida ou rejeita um envio de material.

        Corpo esperado:
        {
            "validado": true,
            "observacoes_gerencia": "Comentário opcional"
        }
        """
        try:
            envio = EnvioMaterial.objects.get(pk=pk)
        except EnvioMaterial.DoesNotExist:
            return Response({"error": "Envio não encontrado"}, status=status.HTTP_404_NOT_FOUND)

        validado = request.data.get("validado")
        observacoes = request.data.get("observacoes_gerencia", "")

        if validado is None:
            return Response(
                {"error": "O campo 'validado' é obrigatório (true/false)."},
                status=status.HTTP_400_BAD_REQUEST
            )

        status_dict = {s['descricao_status']: s['id'] for s in StatusEnvio.objects.filter(deleted_at__isnull=True).values('id', 'descricao_status')}

        # Define status (1 = pendente, 2 = aprovado, 3 = rejeitado)
        envio.id_status_id = status_dict['Validado'] if validado else status_dict['Rejeitado']
        envio.observacoes_gerencia = observacoes
        envio.data_validacao_gerencia = datetime.now().date()
        envio.save()

        serializer = EnvioMaterialSerializer(envio)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @extend_schema(
    summary="Mudar status de um envio de material",
    description=(
        "Altera o status do envio para o `status_id` fornecido. "
        "Também permite atualizar a observação da gerência."
    ),
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "status_id": {"type": "integer", "example": 2},
                "observacoes_gerencia": {"type": "string", "example": "Atualizando status manualmente."}
            },
            "required": ["status_id"]
        }
    },
    responses={200: EnvioMaterialSerializer, 400: OpenApiResponse(description="Parâmetro inválido")},
    tags=["Envios de Material"]
)
    @action(detail=True, methods=['post'])
    def mudar_status(self, request, pk=None):
        """
        Muda o status de um envio de material para o status_id fornecido.
        """
        try:
            envio = EnvioMaterial.objects.get(pk=pk)
        except EnvioMaterial.DoesNotExist:
            return Response({"error": "Envio não encontrado"}, status=status.HTTP_404_NOT_FOUND)

        try:
            status_obj = StatusEnvio.objects.get(pk=request.data.get("status_id"))
        except StatusEnvio.DoesNotExist:
            return Response({"error": "Status não encontrado"}, status=status.HTTP_404_NOT_FOUND)


        observacoes = request.data.get("observacoes_gerencia", "")
        envio.observacoes_gerencia = observacoes
        envio.id_status = status_obj
        envio.save()

        serializer = EnvioMaterialSerializer(envio)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def get_serializer_class(self):
        """
        Return different serializers for different actions
        """
        # if self.action == 'list':
        #     print("List action - using resumo serializer")
        #     return EnvioMaterialResumoSerializer
        return EnvioMaterialSerializer
    
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
    
    @action(detail=False, methods=['get'])
    def pending(self, request):
        """
        Get pending submissions
        """
        pending_status = request.query_params.get('status_id', 1)
        envios = self.queryset.filter(id_status=pending_status)
        serializer = EnvioMaterialSerializer(envios, many=True)
        return Response(serializer.data)
    
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
            total_envios=Count('id'),
            envios_pendentes=Count('id', filter=Q(id_status=1)),
            envios_aprovados=Count('id', filter=Q(id_status=2)),
            envios_rejeitados=Count('id', filter=Q(id_status=3))
        )
        
        stats['mes_referencia'] = int(mes) if mes else None
        stats['ano_referencia'] = int(ano) if ano else None
        
        serializer = EnvioMaterialStatsSerializer(data=stats)
        serializer.is_valid()
        return Response(serializer.data)
    
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
