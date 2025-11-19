import os
from django.core.exceptions import ValidationError

def validate_max_file_size(value):
    limit = 10 * 1024 * 1024  # 10 MB
    if value.size > limit:
        raise ValidationError("O arquivo não pode ter mais que 10MB.")

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1].lower()
    allowed_extensions = [".pdf", ".doc", ".docx", ".zip"]
    if ext not in allowed_extensions:
        raise ValidationError("Tipo de arquivo não permitido. Use PDF, DOC, DOCX ou ZIP.")
