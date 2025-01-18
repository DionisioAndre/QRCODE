import qrcode
from io import BytesIO
from django.http import JsonResponse, FileResponse
from rest_framework.decorators import api_view
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from .models import Evento
from .serializers import QRCodeDataSerializer


# Função para gerar o QR Code e salvar o evento
@api_view(['POST'])
def generate_qrcode(request):
    serializer = QRCodeDataSerializer(data=request.data)
    if serializer.is_valid():
        # Cria o evento
        evento = Evento.objects.create(
            morador=serializer.validated_data['morador'],
            tipo_evento=serializer.validated_data['tipo_evento'],
            data_evento=serializer.validated_data['data_evento'],
            hora_inicio=serializer.validated_data['hora_inicio'],
            hora_fim=serializer.validated_data['hora_fim'],
            local=serializer.validated_data['local'],
            convidado=serializer.validated_data['convidado'],
        )

        # Gerar o QR Code com os dados do evento
        qr_data = f"Morador: {evento.morador}\nEvento: {evento.tipo_evento}\nData: {evento.data_evento}\nInício: {evento.hora_inicio}\nFim: {evento.hora_fim}\nLocal: {evento.local}\nConvidado: {evento.convidado}"
        img = qrcode.make(qr_data)

        # Converter imagem do QR Code para BytesIO
        img_io = BytesIO()
        img.save(img_io)
        img_io.seek(0)

        # Gerar o PDF
        pdf_io = BytesIO()
        c = canvas.Canvas(pdf_io, pagesize=letter)
        img_reader = ImageReader(img_io)
        c.drawImage(img_reader, 100, 600, 200, 200)
        c.save()
        pdf_io.seek(0)

        # URL do PDF gerado
        pdf_url = f"http://127.0.0.1:8000/api/download_pdf/{evento.id}/"

        return JsonResponse({
            "id": evento.id,
            "qr_image": qr_data,  # QR code gerado como texto
            "pdf_url": pdf_url    # URL para download do PDF
        })

    else:
        return JsonResponse(serializer.errors, status=400)


# Função para baixar o PDF gerado
@api_view(['GET'])
def download_pdf(request, evento_id):
    try:
        evento = Evento.objects.get(id=evento_id)

        # Gerar o QR Code com os dados do evento
        qr_data = f"Morador: {evento.morador}\nEvento: {evento.tipo_evento}\nData: {evento.data_evento}\nInício: {evento.hora_inicio}\nFim: {evento.hora_fim}\nLocal: {evento.local}\nConvidado: {evento.convidado}"
        img = qrcode.make(qr_data)

        # Gerar o PDF com o QR Code
        pdf_io = BytesIO()
        c = canvas.Canvas(pdf_io, pagesize=letter)

        # Usar ImageReader para passar o objeto BytesIO para o canvas
        img_io = BytesIO()
        img.save(img_io)
        img_io.seek(0)
        img_reader = ImageReader(img_io)

        # Posição e tamanho do QR Code no PDF
        c.drawImage(img_reader, 100, 600, 200, 200)
        c.save()

        pdf_io.seek(0)

        # Retornar o PDF como resposta
        return FileResponse(pdf_io, as_attachment=True, filename=f"qrcode_evento_{evento.id}.pdf")

    except Evento.DoesNotExist:
        return JsonResponse({"error": "Evento não encontrado"}, status=404)


# Função para listar todos os eventos
@api_view(['GET'])
def get_events(request):
    eventos = Evento.objects.all()
    serializer = QRCodeDataSerializer(eventos, many=True)
    return JsonResponse(serializer.data, safe=False)


# Função para obter detalhes de um evento específico
@api_view(['GET'])
def get_event_detail(request, evento_id):
    try:
        evento = Evento.objects.get(id=evento_id)
        serializer = QRCodeDataSerializer(evento)
        return JsonResponse(serializer.data)
    except Evento.DoesNotExist:
        return JsonResponse({"error": "Evento não encontrado"}, status=404)


# Função para criar um evento
@api_view(['POST'])
def create_event(request):
    serializer = QRCodeDataSerializer(data=request.data)
    if serializer.is_valid():
        evento = serializer.save()
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)


# Função para editar um evento
@api_view(['PUT'])
def edit_event(request, evento_id):
    try:
        evento = Evento.objects.get(id=evento_id)
    except Evento.DoesNotExist:
        return JsonResponse({"error": "Evento não encontrado"}, status=404)

    serializer = QRCodeDataSerializer(evento, data=request.data, partial=True)
    if serializer.is_valid():
        evento = serializer.save()
        return JsonResponse(serializer.data)
    return JsonResponse(serializer.errors, status=400)


# Função para deletar um evento
@api_view(['DELETE'])
def delete_event(request, evento_id):
    try:
        evento = Evento.objects.get(id=evento_id)
        evento.delete()
        return JsonResponse({"message": "Evento deletado com sucesso!"}, status=204)
    except Evento.DoesNotExist:
        return JsonResponse({"error": "Evento não encontrado"}, status=404)
