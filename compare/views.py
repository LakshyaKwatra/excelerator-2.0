from django.shortcuts import render
from upload.models import Upload
from .forms import ComparisonForm
from django.http import HttpResponse
from django.conf import settings
import os
import json
import pandas as pd


# def compare_files(request):
#     target_data = get_object_data(Upload.objects.last())
#     target_data_str = str(target_data)
#     return render(request, 'compare/compare-files.html', {'target_data': target_data})
#
# def compare_files(request):
#     context = {}
#     form = ComparisonForm()
#     context['form'] = form
#     file1sheet1strings = get_file1_sheet1_strings()
#     file1sheet2strings = get_file1_sheet2_strings()
#     file2sheet1strings = get_file2_sheet1_strings()
#     file2sheet2strings = get_file2_sheet2_strings()
#
#     json_file1sheet1strings = json.dumps(file1sheet1strings)
#     json_file1sheet2strings = json.dumps(file1sheet2strings)
#     json_file2sheet1strings = json.dumps(file2sheet1strings)
#     json_file2sheet2strings = json.dumps(file2sheet2strings)
#
#     context['json_file1sheet1strings'] = json_file1sheet1strings
#     context['json_file1sheet2strings'] = json_file1sheet2strings
#     context['json_file2sheet1strings'] = json_file2sheet1strings
#     context['json_file2sheet2strings'] = json_file2sheet2strings
#
#     return render(request, 'compare/compare-files.html', context)


def compare_files(request):
    context = {}
    form = ComparisonForm()
    object_data = get_object_data(Upload.objects.last())
    json_object_data = json.dumps(object_data)
    context['json_object_data'] = json_object_data
    context['form'] = form
    return render(request, 'compare/compare-files.html', context)

def get_object_data(object):
    target_object = object
    file1 = target_object.file1
    file2 = target_object.file2
    file1name = file1.name
    file2name = file2.name
    file1path = os.path.join(settings.MEDIA_ROOT, file1name)
    file2path = os.path.join(settings.MEDIA_ROOT, file2name)
    file1format = file1name.split('.')[-1]
    file2format = file2name.split('.')[-1]
    file1_is_xl = file1format == 'xls' or file1format == 'xlsx'
    file2_is_xl = file2format == 'xls' or file2format == 'xlsx'
    file1dict = None
    file2dict = None
    file1df = None
    file2df = None
    file1sheets = None
    file2sheets = None
    file1dropdown = None
    file2dropdown = None
    file1dropdown_dict = None
    file2dropdown_dict = None
    if not file1_is_xl:
        file1df = get_xsv_df(file1path, file1format)
        file1dropdown = render_dropdown(file1df)
    else:
        file1dict = get_xl_df_dict(file1path)
        file1sheets = list(file1dict.keys())
        file1dropdown_dict = get_dropdown_dict(file1dict)

    if not file2_is_xl:
        file2df = get_xsv_df(file2path, file2format)
        file2dropdown = render_dropdown(file2df)
    else:
        file2dict = get_xl_df_dict(file2path)
        file2sheets = list(file2dict.keys())
        file2dropdown_dict = get_dropdown_dict(file2dict)

    target_data = {
        "file1name": file1name,
        "file2name": file2name,
        "file1path": file1path,
        "file2path": file2path,
        "file1format": file1format,
        "file2format": file2format,
        "file1_is_xl": file1_is_xl,
        "file2_is_xl": file2_is_xl,
        "file1sheets": file1sheets,
        "file2sheets": file2sheets,
        "file1dropdown": file1dropdown,
        "file2dropdown": file2dropdown,
        "file1dropdown_dict": file1dropdown_dict,
        "file2dropdown_dict": file2dropdown_dict
    }
    return target_data


def get_xsv_df(filepath, fileformat):
    if fileformat == 'csv':
        df = clean_df(pd.read_csv(filepath))
    elif fileformat == 'tsv':
        df = clean_df(pd.read_csv(filepath, sep='\t'))
    return df


def get_xl_df_dict(filepath):
    xl_file = pd.ExcelFile(filepath)
    df_dict = pd.read_excel(xl_file, None)
    for sheet in df_dict:
        df_dict[sheet] = clean_df(df_dict[sheet])
    return df_dict


def clean_df(df):
    df = df.dropna(how='all', axis=1).dropna(how='all', axis=0).fillna('')
    df = df.applymap(str)
    df.columns = df.columns.astype(str)
    return df


def get_dropdown_dict(df_dict):
    dropdown_dict = {}
    for sheet in df_dict:
        dropdown_dict[sheet] = render_dropdown(df_dict[sheet])
    return dropdown_dict


def render_dropdown(df):
    col_head_dict = fill_cols(df)[0]
    dd_fields = []
    for key in col_head_dict:
        buff = ''
        for field in col_head_dict[key]:
            if field != '' and 'Unnamed:' not in field:
                if buff == '':
                    buff += field
                else:
                    buff += ' ➤ '
                    buff += field
        dd_fields.append(buff)
    return dd_fields


def fill_cols(df):
    col_head_dict = {}
    skip_rows = 0
    for j in range(len(df.columns)):
        col_head_dict[j + 1] = [df.columns[j]]
    if col_check(col_head_dict):
        return col_head_dict, skip_rows
    else:
        for i in range(len(df)):
            for j in range(len(df.columns)):
                col_head_dict[j + 1].append(df.loc[df.index[i]][df.columns[j]])
            skip_rows += 1
            if col_check(col_head_dict):
                return col_head_dict, skip_rows


def col_check(col_head_dict):
    for col in col_head_dict:
        if len(set(col_head_dict[col])) < 1:
            return False
        if len(set(col_head_dict[col])) == 1 and (col_head_dict[col][0] == '' or 'Unnamed:' in col_head_dict[col][0]):
            return False
        if len(set(col_head_dict[col])) == 2 and (col_head_dict[col][0] == '' or col_head_dict[col][1] == '') and (
                'Unnamed:' in col_head_dict[col][0] or 'Unnamed:' in col_head_dict[col][1]):
            return False
    return True
