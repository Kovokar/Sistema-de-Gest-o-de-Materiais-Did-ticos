import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from api.models import Perfil, Usuario, EtapaEscolar, Disciplina, StatusEnvio, EnvioMaterial


class Command(BaseCommand):
    help = "Popula o banco de dados com dados iniciais (seed)."

    def handle(self, *args, **kwargs):
        # Criando Perfis
        admin = Perfil.objects.get_or_create(nome_perfil="Administrador")[0]
        prof = Perfil.objects.get_or_create(nome_perfil="Professor")[0]
        coord = Perfil.objects.get_or_create(nome_perfil="Coordenador")[0]
        self.stdout.write(self.style.SUCCESS("Perfis criados ✅"))

        # Criando Usuários
        usuarios_data = [
            {"matricula": "2023001", "cpf": "123.456.789-00", "nome_usuario": "João Silva", "telefone": "(11) 91234-5678", "id_perfil": prof},
            {"matricula": "2023002", "cpf": "987.654.321-00", "nome_usuario": "Maria Oliveira", "telefone": "(11) 99876-5432", "id_perfil": coord},
            {"matricula": "2023003", "cpf": "111.222.333-44", "nome_usuario": "Carlos Souza", "telefone": "(21) 93456-7890", "id_perfil": admin},
        ]

        usuarios = []
        for data in usuarios_data:
            user, created = Usuario.objects.get_or_create(
                matricula=data["matricula"],
                defaults={
                    "cpf": data["cpf"],
                    "nome_usuario": data["nome_usuario"],
                    "telefone": data["telefone"],
                    "id_perfil": data["id_perfil"],
                }
            )
            if created:
                user.set_password("senha123")  # gera hash seguro
                user.save()
            usuarios.append(user)

        self.stdout.write(self.style.SUCCESS("Usuários criados ✅"))

        # Criando Etapas Escolares
        etapas = [
            EtapaEscolar.objects.get_or_create(nome_etapa="Educação Infantil")[0],
            EtapaEscolar.objects.get_or_create(nome_etapa="Ensino Fundamental I")[0],
            EtapaEscolar.objects.get_or_create(nome_etapa="Ensino Fundamental II")[0],
            EtapaEscolar.objects.get_or_create(nome_etapa="Ensino Médio")[0],
        ]
        self.stdout.write(self.style.SUCCESS("Etapas criadas ✅"))

        # Criando Disciplinas
        disciplinas = [
            Disciplina.objects.get_or_create(nome_disciplina="Matemática")[0],
            Disciplina.objects.get_or_create(nome_disciplina="Português")[0],
            Disciplina.objects.get_or_create(nome_disciplina="História")[0],
            Disciplina.objects.get_or_create(nome_disciplina="Geografia")[0],
            Disciplina.objects.get_or_create(nome_disciplina="Biologia")[0],
        ]
        self.stdout.write(self.style.SUCCESS("Disciplinas criadas ✅"))

        # Criando Status de Envio
        status = [
            StatusEnvio.objects.get_or_create(descricao_status="Pendente")[0],
            StatusEnvio.objects.get_or_create(descricao_status="Enviado")[0],
            StatusEnvio.objects.get_or_create(descricao_status="Validado")[0],
            StatusEnvio.objects.get_or_create(descricao_status="Rejeitado")[0],
        ]
        self.stdout.write(self.style.SUCCESS("Status de Envio criados ✅"))

        # Criando Envios de Material
        for _ in range(10):
            EnvioMaterial.objects.get_or_create(
                id_etapa=random.choice(etapas),
                id_disciplina=random.choice(disciplinas),
                id_usuario=random.choice(usuarios),
                id_status=random.choice(status),
                mes_referencia=random.randint(1, 12),
                ano_referencia=2025,
                data_envio_escola=timezone.now().date(),
                observacoes_gerencia="Envio automático de teste",
            )
        self.stdout.write(self.style.SUCCESS("Envios de Material criados ✅"))

        self.stdout.write(self.style.SUCCESS("🎉 Seed finalizado com sucesso!"))
