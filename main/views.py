from django.shortcuts import render
from .models import Post
from django.views import generic
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.conf import settings
from .forms import SeuFormulario

def home(request):
    form = SeuFormulario(request.POST or None)  # Instancie o formulário e passe os dados do POST, se houver
    if request.method == 'POST' and form.is_valid():
        nome = form.cleaned_data['nome']
        email = form.cleaned_data['email']
        telefone = form.cleaned_data['telefone']
        mensagem = form.cleaned_data['mensagem']

        # Lógica para enviar o email
        send_mail(
            'Assunto do Email',
            f'Nome: {nome}\nEmail: {email}\nTelefone: {telefone}\nMensagem: {mensagem}',
            settings.DEFAULT_FROM_EMAIL,
            ['seu-email@example.com'],  # Insira o email de destino aqui
            fail_silently=False,
        )

        # Retorne a resposta após o envio do email (pode ser uma página de confirmação, por exemplo)
        return render(request, 'confirmacao.html')

    context = {'form': form}
    return render(request, 'index.html', context)


def membros(request):
    return render(request, 'membros.html')


class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'blog.html'


class PostList2(generic.ListView):
    template_name = 'membros.html'

    def get_queryset(self):
        try:
            idd = Post.objects.latest('display_id')
            iddd = idd.display_id
        except Post.DoesNotExist:
            iddd = None

        if iddd is not None:
            queryset = Post.objects.filter(display_id__gt=iddd-3, status=1).order_by('-display_id')
        else:
            queryset = Post.objects.none()

        return queryset


class DetailView(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'


def enviar_email(request):
    if request.method == 'POST':
        form = SeuFormulario(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            email = form.cleaned_data['email']
            telefone = form.cleaned_data['telefone']
            mensagem = form.cleaned_data['mensagem']

            # Lógica para enviar o e-mail
            send_mail(
                'Assunto do E-mail',
                f'Nome: {nome}\nE-mail: {email}\nTelefone: {telefone}\nMensagem: {mensagem}',
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )

            return render(request, 'main/sucesso.html')
    else:
        form = SeuFormulario()

    return render(request, 'main/index.html', {'form': form})
