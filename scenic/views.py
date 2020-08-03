from django.shortcuts import render


def get_scenic_detail_page(request, scenic_id):

    return render(request, 'scenic/detail.html')
