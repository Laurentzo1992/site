import os

from django.core.exceptions import ValidationError

IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
DOCUMENT_EXTENSIONS = IMAGE_EXTENSIONS + [
    '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.zip', '.mp4',
]

IMAGE_MAX_SIZE = 5 * 1024 * 1024
DOCUMENT_MAX_SIZE = 20 * 1024 * 1024


def validate_image_extension(file):
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in IMAGE_EXTENSIONS:
        raise ValidationError(
            "Format d'image non autorisé (%(ext)s). Formats acceptés : %(allowed)s"
            % {'ext': ext, 'allowed': ', '.join(IMAGE_EXTENSIONS)}
        )


def validate_document_extension(file):
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in DOCUMENT_EXTENSIONS:
        raise ValidationError(
            "Type de fichier non autorisé (%(ext)s). Extensions acceptées : %(allowed)s"
            % {'ext': ext, 'allowed': ', '.join(DOCUMENT_EXTENSIONS)}
        )


def validate_image_size(file):
    if file.size > IMAGE_MAX_SIZE:
        raise ValidationError("L'image dépasse la taille maximale autorisée (5 Mo).")


def validate_document_size(file):
    if file.size > DOCUMENT_MAX_SIZE:
        raise ValidationError("Le fichier dépasse la taille maximale autorisée (20 Mo).")
