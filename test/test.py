import unittest
from vk import User
import vk_api


class MyTestCase(unittest.TestCase):
    def setUp(self):
        print("method setUp")
        self.token = "user_token"
        self.vk_session = vk_api.VkApi(token=self.token)
        self.vk = self.vk_session.get_api()
        self.vk_auth = self.vk_session.get_api()
        self.users_id = self.vk_auth.users.get(fields="bdate, sex, city, relation")
        self.uid = self.users_id[0].get('id')
        self.search_terms = {'age_from': 39, 'age_to': 43, 'city': 'Москва', 'sex': 2}

    def tearDown(self):
        print("method tearDown")

    def test_users_id(self):
        self.assertListEqual(User.users_id(self), self.users_id)

    def test_requirements(self):
        list_requirements = [{"sex": 1, "bdate": "25.4.1980", "city": {"id": 1, "title": "Москва"}, "relation": 1}]
        self.assertDictEqual(User.requirements(list_requirements), self.search_terms)

    def test_user_search(self):
        self.assertDictEqual(User.user_search(self, self.search_terms, [])[0],
                             {109630621: 'https://vk.com/id109630621'})

    def test_top_photo(self):
        list_candidates = [{225090124: 'https://vk.com/id225090124'}]
        top_photo_result = [{225090124: 'https://vk.com/id225090124', 'url_photo': [
            {336916735: 'https://sun9-69.userapi.com/impf/CtX3CBMkQbl8iM6uDpZlB8osCy2tvtj878pQ7A/R3fLme8IObs.jpg?'
                        'size=1059x909&quality=96&sign=502f032bdc768d38b11b3d2dc1e03608&c_uniq_tag='
                        '_n-meHj7Ltd7yQBIFWkFW_x9avVZReqCCZHOZMgaPjw&type=album'},
            {343291494: 'https://sun9-49.userapi.com/impf/KXj5i_33CDE_iFCh7s9U9MSYpzxqtx1ofUcGpQ/mhedl_Hk04g.jpg?'
                        'size=719x1080&quality=96&sign=383cae46cde4e317007b8ec0c7f0f525&c_uniq_tag='
                        '076nMOSXvoRPSdlZ4uCYAJpnLkbll4nvgDC3fm-1S0Q&type=album'},
            {379014038: 'https://sun9-73.userapi.com/impf/c627231/v627231124/1287d/rRNHmg062zs.jpg?'
                        'size=715x882&quality=96&sign=703cc3381d205807d6f5221ed857c38f&c_uniq_tag='
                        'gX4TSpwfwa8zuEK1Zl2Os_DRSxaAHJ5FIx6Pr-247bo&type=album'}]}]

        self.assertListEqual(User.top_photo(self, list_candidates), top_photo_result)


if __name__ == '__main__':
    unittest.main()