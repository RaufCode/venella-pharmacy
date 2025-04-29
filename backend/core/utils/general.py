import string, random, sys, io, os
from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpRequest
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from core.models.accounts import UserAccount


def generate_otp(otp_length):
    """
    Generate a one time pin with specified length
    """
    return "".join([random.choice(string.digits) for i in range(otp_length)])


def get_user_from_jwttoken(request: HttpRequest) -> UserAccount:
    "Return a user object when a valid jwt token is set in the request header"
    jwt = JWTAuthentication()
    try:
        user = jwt.get_user(
            jwt.get_validated_token((jwt.get_raw_token(jwt.get_header(request))))
        )
    except Exception as e:
        raise AuthenticationFailed(detail="Authorization header is required")
    return user


def password_generator():
    """Generate a random password for a new organizational account"""
    return "".join(
        [random.choice(string.ascii_letters + string.digits) for i in range(8)]
    )


def validate_posted_data(data: dict, fields: list[str]):
    """Validate against missing fields in posted data"""
    err: bool = False
    errors: dict = {}
    for field in fields:
        if not data.get(field):
            err = True
            errors.update({field: ["this field is required"]})

    return err, errors


def client_address(request: HttpRequest):
    """Get the address of the client that made the request to the server"""
    scheme = request.scheme
    client = request.headers.get("Referer")
    host = request.get_host()
    client_addr = f"{client}" if client else f"{scheme}://{host}/"
    return client_addr


def absolute_media_url_builder(request: HttpRequest, media_url: str):
    return request.build_absolute_uri(media_url)


class InMemoryUploadedFileHandler:

    def __init__(self) -> None:
        pass

    def from_img(self, image, file_name=None):
        """Create a Django InMemoryUploadedFile object"""
        image_buffer = io.BytesIO()
        image.save(image_buffer, format="PNG")
        image_buffer.seek(0)

        seal_image = InMemoryUploadedFile(
            image_buffer,
            field_name="ImageField",
            name=file_name if file_name else "seal_image.png",
            content_type="PNG",
            size=sys.getsizeof(image_buffer),
            charset=None,
        )

        return seal_image

    def from_img_path(self, image_path):
        """Create an InMemoryUploadedFile image object from path"""

        file_name = os.path.split(image_path)[-1]
        with open(image_path, "rb") as f:
            image_data = f.read()

            # Create a BytesIO buffer to hold the image data in memory and write to the buffer
            buffer = BytesIO()
            buffer.write(image_data)

            # Create an InMemoryUploadedFile object with the buffer, file name, content type, and size
            uploaded_image = InMemoryUploadedFile(
                buffer, None, file_name, "image/jpeg", buffer.tell(), None
            )

            # Seek to the beginning of the buffer
            uploaded_image.seek(0)

            return uploaded_image

    def from_file_path(self, file_path, file_name=None):
        """Create an InMemoryUploadedFile object from a file directory"""
        with open(file_path, "rb") as f:
            pdf_data = f.read()

        f_name = file_name if file_name else os.path.split(file_path)[-1]

        pdf_file_io = io.BytesIO(pdf_data)
        content_type = "application/pdf"

        pdf_file = InMemoryUploadedFile(
            pdf_file_io,
            field_name="file",
            name=f_name,
            content_type=content_type,
            size=sys.getsizeof(pdf_data),
            charset=None,
        )
        return pdf_file

    def from_bytesio(self, file_bytesio: io.BytesIO, file_name=None):
        """Create an InMemoryUploadedFile object from an in-memory io stream"""

        pdf_file_io = file_bytesio
        content_type = "application/pdf"
        f_name = file_name if file_name else "seal_file.pdf"

        pdf_file = InMemoryUploadedFile(
            pdf_file_io,
            field_name=None,
            name=f_name,
            content_type=content_type,
            size=sys.getsizeof(pdf_file_io),
            charset=None,
        )
        return pdf_file
