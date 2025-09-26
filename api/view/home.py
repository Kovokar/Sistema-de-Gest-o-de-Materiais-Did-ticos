# views/home.py
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.conf import settings


def home_view(request):
    """
    Home page view that displays all available API routes
    """
    # Get base URL
    base_url = request.build_absolute_uri('/')[:-1]  # Remove trailing slash
    
    # Define all available routes with descriptions
    routes = {
        'Documentação da API': [
            {
                'name': '📖 Swagger UI (Interativo)',
                'url': reverse('swagger-ui'),
                'description': 'Interface interativa para testar todos os endpoints da API'
            },
            {
                'name': '📚 ReDoc (Documentação)',
                'url': reverse('redoc'),
                'description': 'Documentação completa e elegante da API'
            },
            {
                'name': '🔧 Schema OpenAPI',
                'url': reverse('schema'),
                'description': 'Schema OpenAPI 3.0 em formato JSON'
            },
        ],
        'Administração': [
            {
                'name': '⚙️ Painel Admin',
                'url': '/admin/',
                'description': 'Interface administrativa do Django'
            },
            {
                'name': '🔐 Autenticação API',
                'url': '/api-auth/',
                'description': 'Login/logout para API navegável'
            },
        ],
        'Endpoints da API': [
            {
                'name': '🏠 API Root',
                'url': '/api/',
                'description': 'Endpoint raiz com links para todos os recursos'
            },
            {
                'name': '👤 Perfis',
                'url': '/api/perfis/',
                'description': 'Gestão de perfis de usuário (roles/funções)'
            },
            {
                'name': '👥 Usuários',
                'url': '/api/usuarios/',
                'description': 'Gestão completa de usuários do sistema'
            },
            {
                'name': '🎓 Etapas Escolares',
                'url': '/api/etapas-escolares/',
                'description': 'Gestão de etapas escolares (séries)'
            },
            {
                'name': '📖 Disciplinas',
                'url': '/api/disciplinas/',
                'description': 'Gestão de disciplinas acadêmicas'
            },
            {
                'name': '📊 Status de Envio',
                'url': '/api/status-envio/',
                'description': 'Gestão de status dos envios'
            },
            {
                'name': '📚 Envios de Material',
                'url': '/api/envios-material/',
                'description': 'Gestão de envios de material didático'
            },
        ],
        'Endpoints Especiais': [
            {
                'name': '👥 Usuários por Perfil',
                'url': '/api/usuarios/by_perfil/',
                'description': 'Filtrar usuários por perfil específico'
            },
            {
                'name': '📚 Envios por Usuário',
                'url': '/api/envios-material/by_user/',
                'description': 'Envios de material por usuário específico'
            },
            {
                'name': '📅 Envios por Período',
                'url': '/api/envios-material/by_period/',
                'description': 'Envios filtrados por mês e ano'
            },
            {
                'name': '⏳ Envios Pendentes',
                'url': '/api/envios-material/pending/',
                'description': 'Lista de envios com status pendente'
            },
            {
                'name': '📊 Estatísticas',
                'url': '/api/envios-material/stats/',
                'description': 'Estatísticas de envios por período'
            },
            {
                'name': '⚠️ Envios em Atraso',
                'url': '/api/envios-material/overdue/',
                'description': 'Envios que passaram do prazo limite'
            },
        ]
    }
    
    # System info
    system_info = {
        'django_version': getattr(settings, 'DJANGO_VERSION', 'N/A'),
        'debug_mode': settings.DEBUG,
        'base_url': base_url,
        'api_version': '1.0.0'
    }
    
    context = {
        'routes': routes,
        'system_info': system_info,
        'base_url': base_url,
    }
    
    return render(request, 'home.html', context)