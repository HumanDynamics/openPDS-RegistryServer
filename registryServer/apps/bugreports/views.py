import uuid
import settings
from django.http import HttpResponse

def writeReport(request):
    if request.method == "POST":
        filename = str(uuid.uuid4()) + ".report"
        with open(settings.SERVER_UPLOAD_DIR + filename, "wb") as bugFile:
            bugFile.write(request.body)
    return HttpResponse("success")
