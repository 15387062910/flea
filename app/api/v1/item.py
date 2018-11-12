"""
    app/api/v1/item.py:
    item相关API
        /api/v1/item/   GET   								返回所有物品信息
        /api/v1/item/page/<int:page_num>   GET              访问部分物品信息 page_num指定返回范围
        /api/v1/item/<int:item_id>   GET   					返回某个物品详细信息
        /api/v1/item/<int: user_id>  POST    				发布物品信息
        /api/v1/item/<int:item_id>   PUT   					修改某个物品信息
        /api/v1/item/<int: item_id>  DELETE   				删除某个物品信息

        /api/v1/item/search/<search_key>/<int:page_num>	    GET			    搜索物品
        /api/v1/item/upload_img                             POST   			上传图片  返回图片地址
"""
from . import Redprint
from app.req_res import *
from app.req_res.req_transfer import Transfer
from app.utils.file import allowed_file, save_upload_img
from app.models.item import Item
from app.models.user import User

item = Redprint("item")


@item.route('/', methods=['GET'])
def get_items():
    """
    返回所有物品基本信息及物品对应的发布者id
    :return:
    """
    try:
        items = Item.all()
        data = [dict(i) for i in items]
        print(data)
        return dict(code=1, msg='get all item data successfully', data=data)
    except Exception as e:
        print(e)
        return ItemNotFound() if isinstance(e, NotFound) else SomethingError()
    # return '返回所有物品信息'


@item.route('/page/<int:page_num>', methods=['GET'])
def get_items2(page_num):
    """
    返回部分物品信息
    :return:
    """
    try:
        items = Item.page(page_num)
        data = [dict(i) for i in items]
        print(data)
        return dict(code=1, msg='get a part of item data successfully', data=data)
    except Exception as e:
        print(e)
        return ItemNotFound() if isinstance(e, NotFound) else SomethingError()
    # return '返回部分物品信息'


@item.route('/<int:item_id>', methods=['GET'])
def return_item(item_id):
    """
    根据物品id得到物品的信息
    :param item_id: 物品id
    :return:
    """
    try:
        i = Item.query.filter_by(id=item_id).first_or_404()
        return dict(code=1, msg='get a item data successfully', data=dict(i))
    except Exception as e:
        print(e)
        return ItemNotFound() if isinstance(e, NotFound) else SomethingError()
    # return '返回某个物品信息'


@item.route('/<int:user_id>', methods=['POST'])
def post_item(user_id):
    try:
        req = Transfer()
        data = req.handle_post()
        print('data: ', data)
        User.query.get(user_id)
        if Item.create_item(data, user_id):
            return PostSuccess()
    except Exception as e:
        print(e)
        return UserNotFound() if isinstance(e, NotFound) else SomethingError()
    # return '发布物品信息'


@item.route('/<int:item_id>', methods=['PUT'])
def edit_item(item_id):
    """
    更新item
    :param item_id:
    :return:
    """
    try:
        i = Item.query.get(item_id)
        transfer = Transfer()
        data = transfer.handle_post()
        print('edit_item', data)
        if i.edit_item(data):
            return UpdateSuccess()
        else:
            return UpdateFail()
    except Exception as e:
        print(e)
        return ItemNotFound() if isinstance(e, NotFound) else SomethingError()
    # return '修改物品信息'


@item.route('/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """
    删除item
    :param item_id:
    :return:
    """
    try:
        i = Item.query.get(item_id)
        i.delete()
    except Exception as e:
        print(e)
        return ItemNotFound() if isinstance(e, NotFound) else SomethingError()
    else:
        return DeleteSuccess()
    # return '删除物品信息'


@item.route('/search/<search_key>/<int:page_num>', methods=['GET'])
def search_item(search_key, page_num):
    """
    搜索item get实现
    :return:
    """
    # todo 待测试
    try:
        key = '%{}%'.format(search_key)
        print("key and page_num: ", key, page_num)
        data = Item.search_item(key, page_num)
        print(data)
        return dict(code=1, msg='search items successfully', data=data)
    except Exception as e:
        print(e)
        return ItemNotFound() if isinstance(e, NotFound) else SomethingError()
    # return '搜索物品信息'


@item.route('/search/', methods=['POST'])
def search_item2():
    """
    搜索item post实现
    :return:
    """
    # todo 待测试
    try:
        req = Transfer()
        data = req.handle_post()
        key = '%{}%'.format(data["search_key"])
        page_num = int(data["page_num"])
        print("key and page_num: ", key, page_num)
        data = Item.search_item(key, page_num)
        print(data)
        return dict(code=1, msg='search items successfully', data=data)
    except Exception as e:
        print(e)
        return ItemNotFound() if isinstance(e, NotFound) else SomethingError()
    # return '搜索物品信息'


@item.route('/upload_img', methods=['POST'])
def upload_img():
    """
    上传图片，返回图片地址
    :return: 图片地址
    """
    # todo 待测试
    try:
        print(request.files)
        transfer = Transfer()
        file = transfer.handle_file()
        if file and allowed_file(file.filename):
            data = save_upload_img(file, file.filename)
            return dict(code=1, msg='upload img successfully', data=data)
        else:
            return ParameterException()
    except Exception as e:
        print(e)
    except FileNameException:
        return FileNameException()
    except ChoiceImgException:
        return ChoiceImgException()
    except ImgLargeException:
        return ImgLargeException()
    return SomethingError()
    # return "图片地址"


