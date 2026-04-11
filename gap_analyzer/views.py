from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import JobDescriptionSerializer
from .utils import find_missing_skills
from .models import CompanyDetails, SkillGap
from analyzer.models import Resume

class GapAnalysisView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = JobDescriptionSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data

            # Step 1 - get user skills from DB
            try:
                resume = Resume.objects.filter(
                    user=request.user
                ).latest('uploaded_at')
                user_skills = [s.strip() for s in resume.skills.split(',')]
            except Resume.DoesNotExist:
                return Response(
                    {"error": "Please upload your resume first"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Step 2 - compare directly
            result = find_missing_skills(user_skills, data['company_skills'])

            # Step 3 - save temporarily
            company = CompanyDetails.objects.create(
                user=request.user,
                company_name=data['company_name'],
                role=data['role'],
                company_skills=", ".join(data['company_skills'])
            )

            SkillGap.objects.create(
                user=request.user,
                company=company,
                missing_skills=", ".join(result['missing']),
                verdict=result['verdict']
            )

            # Step 4 - return response
            return Response({
                "missing_skills": result['missing'],
                "verdict": result['verdict'],
                "message": result['message']
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)