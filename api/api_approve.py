from config import HOST_URL


class ApiApprove:
    # 初始化
    def __init__(self,session):
        self.session = session
        # 1. 认证url
        self.__url_approve = HOST_URL + "/member/realname/approverealname"
        # 2. 获取认证信息url
        self.__url_approve_info = HOST_URL + "/member/member/getapprove"

    # 认证
    def api_approve(self, realname, card_id):
        data = {
            "realname":realname,
            "card_id":card_id
        }
        # files={"x":"y"} 附加文件，目的使用多种消息格式传递数据
        # 附加files后，传递数据类型为：form+files，为多消息体数据
        return self.session.post(self.__url_approve, data=data, files={"x": "y"})

    # 获取认证信息
    def api_approve_info(self):
        return self.session.post(self.__url_approve_info)
