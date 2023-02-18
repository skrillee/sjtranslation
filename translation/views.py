# -*- coding: utf-8 -*-
from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse
from django.http import JsonResponse
from xml.etree import ElementTree as ET
import xlrd
import os.path
from sjtanslation import settings


def file_extension(path):
    return os.path.splitext(path)[1]


def find_samenumber(list_excel, list_xml):
    diff_data = set(list_xml).difference(set(list_excel)) #差集，在list2中但不在list1中的元素
    return diff_data


class Translation(APIView):
    """
        Return information of authentication process
        User authentication related services
    """

    def post(self, request):
        responses = {
            'code': 1000,
            'message': None
        }
        try:

            excel_file = request.FILES.get("excel_file", None)
            xml_file = request.FILES.get("xml_file", None)
            sheet_name = request._request.POST.get('sheet_name', None)
            language = request._request.POST.get('language', None)
            if not os.path.exists(settings.UPLOAD_ROOT):
                os.makedirs(settings.UPLOAD_ROOT)
            excel_file_load = settings.UPLOAD_ROOT + "\\" + excel_file.name
            with open(excel_file_load, 'wb') as f:
                for i in excel_file.readlines():
                    f.write(i)
            if xml_file is None:
                return HttpResponse("no files for upload!")
            else:
                scroe_dict = {}
                if excel_file:
                    data = xlrd.open_workbook(excel_file_load)
                    sheet_list = data.sheets()
                    for sheet in sheet_list:
                        if sheet.name == sheet_name:
                            colnumber_b = ord('B') - ord('A')
                            colnumber_g = ord(language) - ord('A')
                            for i in range(100):  # 前一百行
                                scroe_dict[sheet.cell(i, colnumber_b).value] = sheet.cell(i, colnumber_g).value
                tree = ET.parse(xml_file)
                root = tree.getroot()
                result_list = []
                for child in root:
                    try:
                        # xml_data_value_list.append((child.text).encode('utf-8').decode("utf-8"))
                        child_key = child.attrib['name']
                        child_value = child.text
                        if scroe_dict[child_key] != child_value:
                            result_list.append(child_key)
                    except:
                        print('_____child_text_______')
                        print(child.text)
                    for node in child:
                        try:
                            # xml_data_value_list.append((node.text).encode('utf-8').decode("utf-8"))
                            node_key = node.attrib['name']
                            node_value = node.text
                            if scroe_dict[node_key] != node_value:
                                result_list.append(node_key)
                        except:
                            print('_____node_text_______')
                            print(node.text)
                responses['manifest_dict'] = result_list
            return JsonResponse(responses, json_dumps_params={'ensure_ascii': False})
        except Exception as e:
            responses['code'] = 3002
            responses['message'] = "请求异常"
        return JsonResponse(responses)

    def get(self, request):
        return render(request, 'index.html')
