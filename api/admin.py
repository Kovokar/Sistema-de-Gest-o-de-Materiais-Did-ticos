# admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Perfil, Usuario, EtapaEscolar, Disciplina, StatusEnvio, EnvioMaterial


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    """
    Admin configuration for Perfil model
    """
    list_display = ['id_perfil', 'nome_perfil', 'total_usuarios']
    list_display_links = ['id_perfil', 'nome_perfil']
    search_fields = ['nome_perfil']
    ordering = ['id_perfil']
    
    def total_usuarios(self, obj):
        """Display total users for this profile"""
        count = obj.usuario_set.count()
        if count > 0:
            url = reverse('admin:material_didatico_usuario_changelist') + f'?id_perfil__exact={obj.id_perfil}'
            return format_html('<a href="{}">{} usuários</a>', url, count)
        return '0 usuários'
    
    total_usuarios.short_description = 'Total de Usuários'


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    """
    Admin configuration for Usuario model
    """
    list_display = [
        'id_usuario', 'nome_usuario', 'matricula', 'cpf', 
        'get_perfil_nome', 'telefone', 'total_envios'
    ]
    list_display_links = ['id_usuario', 'nome_usuario']
    list_filter = ['id_perfil', 'id_perfil__nome_perfil']
    search_fields = ['nome_usuario', 'matricula', 'cpf', 'id_perfil__nome_perfil']
    ordering = ['nome_usuario']
    readonly_fields = ['id_usuario']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome_usuario', 'matricula', 'id_perfil')
        }),
        ('Dados Pessoais', {
            'fields': ('cpf', 'telefone')
        }),
        ('Acesso', {
            'fields': ('senha',),
            'classes': ('collapse',)
        }),
    )
    
    def get_perfil_nome(self, obj):
        """Display profile name"""
        return obj.id_perfil.nome_perfil if obj.id_perfil else '-'
    get_perfil_nome.short_description = 'Perfil'
    get_perfil_nome.admin_order_field = 'id_perfil__nome_perfil'
    
    def total_envios(self, obj):
        """Display total submissions for this user"""
        count = obj.enviomaterial_set.count()
        if count > 0:
            url = reverse('admin:material_didatico_enviomaterial_changelist') + f'?id_usuario__exact={obj.id_usuario}'
            return format_html('<a href="{}">{} envios</a>', url, count)
        return '0 envios'
    
    total_envios.short_description = 'Total de Envios'


@admin.register(EtapaEscolar)
class EtapaEscolarAdmin(admin.ModelAdmin):
    """
    Admin configuration for EtapaEscolar model
    """
    list_display = ['id_etapa', 'nome_etapa', 'total_envios']
    list_display_links = ['id_etapa', 'nome_etapa']
    search_fields = ['nome_etapa']
    ordering = ['id_etapa']
    
    def total_envios(self, obj):
        """Display total submissions for this school stage"""
        count = obj.enviomaterial_set.count()
        if count > 0:
            url = reverse('admin:material_didatico_enviomaterial_changelist') + f'?id_etapa__exact={obj.id_etapa}'
            return format_html('<a href="{}">{} envios</a>', url, count)
        return '0 envios'
    
    total_envios.short_description = 'Total de Envios'


@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    """
    Admin configuration for Disciplina model
    """
    list_display = ['id_disciplina', 'nome_disciplina', 'total_envios']
    list_display_links = ['id_disciplina', 'nome_disciplina']
    search_fields = ['nome_disciplina']
    ordering = ['nome_disciplina']
    
    def total_envios(self, obj):
        """Display total submissions for this subject"""
        count = obj.enviomaterial_set.count()
        if count > 0:
            url = reverse('admin:material_didatico_enviomaterial_changelist') + f'?id_disciplina__exact={obj.id_disciplina}'
            return format_html('<a href="{}">{} envios</a>', url, count)
        return '0 envios'
    
    total_envios.short_description = 'Total de Envios'


@admin.register(StatusEnvio)
class StatusEnvioAdmin(admin.ModelAdmin):
    """
    Admin configuration for StatusEnvio model
    """
    list_display = ['id_status', 'descricao_status', 'total_envios', 'status_color']
    list_display_links = ['id_status', 'descricao_status']
    search_fields = ['descricao_status']
    ordering = ['id_status']
    
    def total_envios(self, obj):
        """Display total submissions with this status"""
        count = obj.enviomaterial_set.count()
        if count > 0:
            url = reverse('admin:material_didatico_enviomaterial_changelist') + f'?id_status__exact={obj.id_status}'
            return format_html('<a href="{}">{} envios</a>', url, count)
        return '0 envios'
    
    total_envios.short_description = 'Total de Envios'
    
    def status_color(self, obj):
        """Display status with color coding"""
        color_map = {
            1: '#ffc107',  # Pending - Yellow
            2: '#28a745',  # Approved - Green
            3: '#dc3545',  # Rejected - Red
            4: '#17a2b8',  # In Review - Blue
        }
        color = color_map.get(obj.id_status, '#6c757d')  # Default gray
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            color, obj.descricao_status
        )
    
    status_color.short_description = 'Status Visual'


@admin.register(EnvioMaterial)
class EnvioMaterialAdmin(admin.ModelAdmin):
    """
    Admin configuration for EnvioMaterial model
    """
    list_display = [
        'id_envio', 'get_usuario_nome', 'get_disciplina_nome', 
        'get_etapa_nome', 'mes_referencia', 'ano_referencia',
        'get_status_display', 'data_envio_escola', 'data_limite_envio',
        'is_overdue'
    ]
    list_display_links = ['id_envio']
    list_filter = [
        'ano_referencia', 'mes_referencia', 'id_status',
        'id_etapa', 'id_disciplina', 'data_envio_escola'
    ]
    search_fields = [
        'id_usuario__nome_usuario', 'id_usuario__matricula',
        'id_disciplina__nome_disciplina', 'id_etapa__nome_etapa',
        'observacoes_gerencia'
    ]
    ordering = ['-ano_referencia', '-mes_referencia', '-id_envio']
    readonly_fields = ['id_envio', 'mes_referencia_display']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': (
                'id_usuario', 'id_etapa', 'id_disciplina', 
                'mes_referencia', 'mes_referencia_display', 'ano_referencia'
            )
        }),
        ('Status e Controle', {
            'fields': ('id_status', 'observacoes_gerencia')
        }),
        ('Datas de Controle', {
            'fields': (
                'data_envio_escola', 'data_envio_see',
                'data_validacao_gerencia', 'data_envio_formador',
                'data_limite_envio'
            ),
            'classes': ('collapse',)
        }),
    )
    
    date_hierarchy = 'data_envio_escola'
    
    def get_usuario_nome(self, obj):
        """Display user name"""
        return obj.id_usuario.nome_usuario if obj.id_usuario else '-'
    get_usuario_nome.short_description = 'Usuário'
    get_usuario_nome.admin_order_field = 'id_usuario__nome_usuario'
    
    def get_disciplina_nome(self, obj):
        """Display subject name"""
        return obj.id_disciplina.nome_disciplina if obj.id_disciplina else '-'
    get_disciplina_nome.short_description = 'Disciplina'
    get_disciplina_nome.admin_order_field = 'id_disciplina__nome_disciplina'
    
    def get_etapa_nome(self, obj):
        """Display school stage name"""
        return obj.id_etapa.nome_etapa if obj.id_etapa else '-'
    get_etapa_nome.short_description = 'Etapa'
    get_etapa_nome.admin_order_field = 'id_etapa__nome_etapa'
    
    def get_status_display(self, obj):
        """Display status with color coding"""
        if not obj.id_status:
            return '-'
        
        color_map = {
            1: '#ffc107',  # Pending
            2: '#28a745',  # Approved
            3: '#dc3545',  # Rejected
            4: '#17a2b8',  # In Review
        }
        color = color_map.get(obj.id_status.id_status, '#6c757d')
        
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 6px; border-radius: 3px; font-size: 11px;">{}</span>',
            color, obj.id_status.descricao_status
        )
    
    get_status_display.short_description = 'Status'
    get_status_display.admin_order_field = 'id_status__descricao_status'
    
    def is_overdue(self, obj):
        """Check if submission is overdue"""
        from django.utils import timezone
        
        if not obj.data_limite_envio:
            return '-'
        
        today = timezone.now().date()
        if obj.data_limite_envio < today and obj.id_status.id_status in [1, 4]:  # Pending or In Review
            return format_html(
                '<span style="color: #dc3545; font-weight: bold;">⚠️ Atrasado</span>'
            )
        elif obj.data_limite_envio == today:
            return format_html(
                '<span style="color: #ffc107; font-weight: bold;">⏰ Vence hoje</span>'
            )
        else:
            return format_html(
                '<span style="color: #28a745;">✅ No prazo</span>'
            )
    
    is_overdue.short_description = 'Situação do Prazo'
    
    def mes_referencia_display(self, obj):
        """Display month name in Portuguese"""
        return obj.mes_referencia_display if obj else '-'
    mes_referencia_display.short_description = 'Mês (Nome)'
    
    # Custom actions
    actions = ['mark_as_approved', 'mark_as_rejected', 'mark_as_pending']
    
    def mark_as_approved(self, request, queryset):
        """Mark selected submissions as approved"""
        # Assuming status ID 2 is "Approved"
        approved_status = StatusEnvio.objects.filter(id_status=2).first()
        if approved_status:
            updated = queryset.update(id_status=approved_status)
            self.message_user(request, f'{updated} envios marcados como aprovados.')
        else:
            self.message_user(request, 'Status "Aprovado" não encontrado.', level='ERROR')
    
    mark_as_approved.short_description = 'Marcar como aprovado'
    
    def mark_as_rejected(self, request, queryset):
        """Mark selected submissions as rejected"""
        # Assuming status ID 3 is "Rejected"
        rejected_status = StatusEnvio.objects.filter(id_status=3).first()
        if rejected_status:
            updated = queryset.update(id_status=rejected_status)
            self.message_user(request, f'{updated} envios marcados como rejeitados.')
        else:
            self.message_user(request, 'Status "Rejeitado" não encontrado.', level='ERROR')
    
    mark_as_rejected.short_description = 'Marcar como rejeitado'
    
    def mark_as_pending(self, request, queryset):
        """Mark selected submissions as pending"""
        # Assuming status ID 1 is "Pending"
        pending_status = StatusEnvio.objects.filter(id_status=1).first()
        if pending_status:
            updated = queryset.update(id_status=pending_status)
            self.message_user(request, f'{updated} envios marcados como pendentes.')
        else:
            self.message_user(request, 'Status "Pendente" não encontrado.', level='ERROR')
    
    mark_as_pending.short_description = 'Marcar como pendente'


# Customize admin site headers
admin.site.site_header = "Sistema de Material Didático"
admin.site.site_title = "Material Didático Admin"
admin.site.index_title = "Painel de Administração"