from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import ResumeUploadSerializer
from .utils import extract_text, extract_sections
from .models import Resume

class ResumeUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ResumeUploadSerializer(data=request.data)

        if serializer.is_valid():
            file = request.FILES['resume']

            raw_text = extract_text(file)
            sections = extract_sections(raw_text)

            resume = Resume.objects.create(
                user=request.user,
                name=sections['name'],
                skills=sections['skills'],
                projects=sections['projects']
            )

            return Response({
                "message": "Resume uploaded successfully",
                "resume_id": resume.id,
                "name": resume.name,
                "skills": resume.skills,
                "projects": resume.projects
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)