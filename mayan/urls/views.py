from django.http import HttpResponse
from django.http import JsonResponse
import requests
from mayan.apps.documents.tasks.document_tasks import PROCESSING_FILE_QUEUE
from mayan.apps.documents.models import Document
from django.shortcuts import render
import markdown

BlockUrl = 'http://13.233.48.180:3000/files'


def simple_string_view(request):
    """
    A simple Django view that returns a string.
    """
    return HttpResponse("Hello, this is a simple string response.")

def chatbot_response(user_message):
    client=""
    # Define a conversation history to provide context
    conversation_history = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": user_message},
    ]

    # Generate a response from the chatbot
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation_history,
    )

    # Extract the assistant's reply from the response
    assistant_response = response['choices'][0]['text'].strip()

    # Update the conversation history for future turns
    conversation_history.append({"role": "assistant", "content": assistant_response})

    # Return the assistant's response
    return {'response': assistant_response}


def chatbot_res(request):
    if request.method == 'GET':
        query = request.GET.get('message', '')
        print("Without id")
        # Define the URL and payload
        url = "http://13.233.48.180:8080/v2/response"
        payload = {"query": query, "namespace":""}
        print(payload)
        # Send a POST request with the payload
        response = requests.post(url, json=payload, timeout=1200)

        # Check the response status code
        if response.status_code == 200:
            data = response.json()  # Extract JSON data from the response
            print(data['response']['response'])
            unique_labels = set()
            unique_data = []
            
            # print(data)

            # for item in data['metadata']:
            #     label = item['label']
            #     if label not in unique_labels:
            #         unique_data.append(item)
            #         unique_labels.add(label)
            # print(data)
            try:
                # print(data['metadata'])
                bot_content = data['response']['response'].replace('code 404: ', '')
                md_content = markdown.markdown(bot_content)
                out_str = f"""
                    <div style="display: flex;flex-direction: column;align-items: flex-start;">
                        <div>{md_content}</div>
                        <ul style="margin-left: 20px;">"""
            
                # for i in unique_data:
                #     out_str += f"""
                #         <li style="margin-bottom: 5px;"><a target="_blank" onclick="window.location.href='/#/documents/documents/{i['id']}/preview/'" style="text-decoration: none;">"""+i['label']+"""</a></li>
                #     """

                out_str += "</ul></div>"
                data['response'] = out_str
            except:
                data=data
            print(data)
            return JsonResponse(data)  # Return the JSON response
        else:
            return JsonResponse({"error": "Failed to send data."}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=400)

def chatbot_res_with_id(request, doc_id):
    if request.method == 'GET':
        query = request.GET.get('message', '')
        print("With id ,", doc_id)
        # Define the URL and payload
        url = "http://13.233.48.180:8080/v2/response/"+str(doc_id)
        payload = {"query": query, "namespace":""}
        print(payload)

        # Send a POST request with the payload
        response = requests.post(url, json=payload, timeout=1200)

        # Check the response status code
        if response.status_code == 200:
            data = response.json()  # Extract JSON data from the response
            unique_labels = set()
            unique_data = []
            print(data)
            

            # for item in data['metadata']:
            #     label = item['label']
            #     if label not in unique_labels:
            #         unique_data.append(item)
            #         unique_labels.add(label)
            # print(data)
            try:
                # print(data['metadata'])
                bot_content = data['response']['response'].replace('code 404: ', '')
                md_content = markdown.markdown(bot_content)
                
                out_str = f"""
                    <div style="display: flex;flex-direction: column;align-items: flex-start;">
                        <div>{md_content}</div>
                        <ul style="margin-left: 20px;">"""

                # for i in unique_data:
                #     out_str += f"""
                #         <li style="margin-bottom: 5px;"><a target="_blank" onclick="window.location.href='/#/documents/documents/{i['id']}/preview/'" style="text-decoration: none;">"""+i['label']+"""</a></li>
                #     """

                out_str += "</ul></div>"
                data['response'] = out_str
            except:
                data=data
            return JsonResponse(data)  # Return the JSON response
        else:
            return JsonResponse({"error": "Failed to send data."}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=400)

def check_process(request, doc_id):
    if int(doc_id) in  PROCESSING_FILE_QUEUE:
        return JsonResponse({"file": True}, status=200)
    else:
        return JsonResponse({"file": False}, status=404)

def document_details(request):
    output_data = []
    response = requests.get(BlockUrl)
    if response.status_code == 200:
        data = response.json()
        obj1 = Document.objects.all()
        for i in obj1:
            print("Doc id is : ", i.id)
        # obj = Document.objects.get(id=3)
        output_data.append(obj1)
        for document in data:
            try:
                obj = Document.objects.get(id=document['id'])
                output_data.append(obj)
                output_data.append(obj)
                output_data.append(obj)
            except:
                print("match does't exist at : ", document['id'])
    context = {
        'objs': output_data,
    }
    print(context)

    return render(request, 'document_details.html', context)


def document_unverified(request):
    compromised_documents = [1113]  

    response = requests.get(BlockUrl)
    print(response.json())
    if response.status_code == 200:
        api_data = response.json()  

        api_document_ids = {document['id'] for document in api_data}

        all_documents = Document.objects.all()

        for document in all_documents:
            if document.id not in api_document_ids:
                compromised_documents.append(document)

    else:
        print(f"Failed to fetch data from API. Status code: {response.status_code}")

    context = {
        'compromised_docs': compromised_documents,
    }
    print(context)

    return render(request, 'document_unverified.html', context)
