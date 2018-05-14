from django.test import TestCase
import django.core.mail as dmail
from django.urls import resolve
from .models import User
from .forms import RegisterForm
from .auth import get_send_activation_email_url, send_activation_email
from django.http import HttpRequest
from django.db.utils import IntegrityError
#from pdb import set_trace

# Create your tests here.

##### HELPER FUNCTIONS ######


class UserModelTest(TestCase):

    def setUp(self):
         ## The only way to create a user is through a form. This form
        data = {'email'     : 'test@test.com',
                'password1' : 'hullaballo',
                'password2' : 'hullaballo'}
        form = RegisterForm(data=data)
        self.assertTrue(form.is_valid())
        user = form.save(commit=False) #don't save the model bound to form, return it
        user.is_active = False
        user.save()
        self.user1 = user


    def test_user_creation_email_send(self):
        user = self.user1

        #Need to make a request
        #sned_activation_email uses this to get the current domain..
        request = self.client.get('/')  
        request.get_host = lambda : 'testserver' #have to add this function. The test request doesn't have it.
        #Test sending email directly using a function
        email = send_activation_email(request,user)
        self.assertEqual(dmail.outbox[0].body,email.body)
        print(email.body)

        #Test sending email by requesting the url that does so
        url = get_send_activation_email_url(user)
        request = self.client.get(url)
        print(request)
        print(dmail.outbox[1].body)
        print(email.body)
        self.assertEqual(dmail.outbox[1].body,email.body)

    def test_user_creation_confirm_like(self):
        



    def test_bchaccount_creation(self):
        pass
        #raise Exception('Need to create a BCHaccount class!')

# class ItemModelTest(TestCase):
#     def test_saving_and_retreiving_items(self):
#         lists, items = get_random_lists()
#         print('Got random lists')

#         self.assertEqual(len(lists),len(items))
#         for i in range(len(lists)):
#             got_items = lists[i].item_set.all()
#             got_items = [got_items[j] for j in range(len(got_items))]
#             self.assertEqual(len(got_items),len(items[i]))
#             for test_item in items[i]:
#                 self.assertTrue(test_item in got_items)
#         print('OK: Random lists have all the correct items')

#     def test_model_relations1(self):
#         item = Item()
#         try:
#             item.save()
#         except IntegrityError as e:
#             self.assertIn('NOT NULL constraint failed',str(e))
#         print("OK: Can't save item without being linked to model")
#         list_ = List()
#         item.list = list_

#         try:
#             item.save()
#         except:
#             pass
#         else:
#             raise Exception('Was allowed to save item linked to unsaved list')
#         print("OK: Can't save item linked to unsaved list")

#         #TODO: figure how to reset the db here. It still is upset over the 
#         #bad queuries above.


#     def test_model_relations2(self):
#         item = Item()
#         list_ = List()
#         list_.save()
#         item.list = list_

#         item.save()
#      #   item.save()



#         # saved_list = List.objects.first()
#         # self.assertEqual(saved_list,list_)

#         # saved_items = Item.objects.all()
#         # self.assertEqual(saved_items.count(),2)

#         # self.assertEqual(saved_items[0].text,'The first ever list item')
#         # self.assertEqual(saved_items[0].list,list_)
#         # self.assertEqual(saved_items[1].text,'Second list item')
#         # self.assertEqual(saved_items[1].list,list_)

#         # ###Confirm that reverse search also works
#         # self.assertEqual(list_.item_set.all()[0],saved_items[0])
#         # self.assertEqual(list_.item_set.all()[1],saved_items[1])

#         # set_trace()



# class ListViewTest(TestCase):

#     def test_displays_all_items(self):
#         list_ = List.objects.create()
#         Item.objects.create(text='itemey 1', list=list_)
#         Item.objects.create(text='itemey 2', list=list_)

#         response = self.client.get( ('/lists/%i/' % list_.id) )

#         self.assertContains(response, 'itemey 1')
#         self.assertContains(response, 'itemey 2')