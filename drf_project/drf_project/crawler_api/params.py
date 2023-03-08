from pydoc import describe
from drf_yasg import openapi

def get_param(name, desc, type, required=None, default=None):
    type_map = {
        'int': openapi.TYPE_INTEGER,
        'str': openapi.TYPE_STRING,
        'bool': openapi.TYPE_BOOLEAN
    }
    target_type = type_map[type]
    is_require = True if required == True else False
    return openapi.Parameter(name, openapi.TYPE_OBJECT, description=desc, 
                            type=target_type, required=is_require, default=default)
    


projectid_param=get_param("project_id","프로젝트 식별 ID",'int',True)
projecttitle_param=get_param("project_title","프로젝트 이름 (중복 불가)","str",True)
projectmode_param=get_param("project_mode","프로젝트 모드 (keyword/tag)","str",True)
projectkeyword_param=get_param("project_keyword","프로젝트 모드가 keyword일 때 수집할 검색어 목록 (쉼표로 구분하여 작성)","str",False)

crawler_param=get_param("crawler_id","크롤러 식별 ID","int",True)