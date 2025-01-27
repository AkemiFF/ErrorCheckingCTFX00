from django.http import JsonResponse
# Create your views here.
from django.shortcuts import get_object_or_404, render

from utils.docker_manager import DockerManager

from .models import Defi

docker_manager = DockerManager()

def start_challenge(request, challenge_id):
    challenge = get_object_or_404(Defi, id=challenge_id)

    if challenge.is_active:
        return JsonResponse({'error': 'Challenge is already running.'}, status=400)

    container = docker_manager.start_container(challenge.name, challenge.port)
    if container:
        challenge.is_active = True
        challenge.save()
        return JsonResponse({'message': f'Challenge {challenge.name} started.'})
    return JsonResponse({'error': 'Failed to start challenge.'}, status=500)


# def test(request):
#     container = docker_manager.start_container('calc', 8887)
#     if container:
       
#         return JsonResponse({'message': f'Challenge calc started.'})
#     return JsonResponse({'error': 'Failed to start challenge.'}, status=500)

def test(request):
    # build = docker_manager.build_image('calc', "beginner")
    # if build:
    container = docker_manager.start_container('calc', 8887)

    if container:
       
        return JsonResponse({'message': f'Challenge calc started.'})
    return JsonResponse({'error': 'Failed to start challenge.'}, status=500)

import requests
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def proxy_to_docker(request, port,path):
    
    try:
        # print(path)
        docker_url = f"http://127.0.0.1:{port}/{path}" 
      
        response = requests.request(
            method=request.method,
            url=docker_url,
            headers={
                'Content-Type': request.META.get('CONTENT_TYPE', 'application/json'),
                'Accept': 'application/json'
            },
            data=request.body  
        )
        
        return HttpResponse(response.content, status=response.status_code)
    
    except requests.ConnectionError:
        return JsonResponse({'error': 'Unable to connect to Docker container'}, status=500)

def stop_test(request):
    docker_manager.stop_container('calc')
    return JsonResponse({'message': 'Container stopped.'})