from django.test import SimpleTestCase, TestCase, Client
from django.urls import reverse, resolve
from main.views import *

class TestUrls(SimpleTestCase):
    def test_dashboard_url_is_resolved(self):
        url = reverse('main:dashboard')
        self.assertEquals(resolve(url).func, dashboard)

    def test_signup_url_is_resolved(self):
        url = reverse('main:signup')
        self.assertEquals(resolve(url).func, signup_view)
    def test_login_url_is_resolved(self):
        url = reverse('main:login')
        self.assertEquals(resolve(url).func, login_view)
    def test_logout_url_is_resolved(self):
        url = reverse('main:logout')
        self.assertEquals(resolve(url).func, logout_view)

    def test_team_list_url_is_resolved(self):
        url = reverse('main:team_list')
        self.assertEquals(resolve(url).func.view_class, TeamList)
    def test_project_list_url_is_resolved(self):
        url = reverse('main:project_list')
        self.assertEquals(resolve(url).func.view_class, ProjectList)
    def test_user_list_url_is_resolved(self):
        url = reverse('main:user_list')
        self.assertEquals(resolve(url).func.view_class, UserList)
        
    def test_user_detail_url_is_resolved(self):
        url = reverse('main:user_detail', args=['username'])
        self.assertEquals(resolve(url).func.view_class, UserDetail)

    def test_team_detail_url_is_resolved(self):
        url = reverse('main:team_detail', args=['team_namespace'])
        self.assertEquals(resolve(url).func.view_class, TeamDetail)
    def test_project_detail_is_resolved(self):
        url = reverse('main:project_detail', args=['team_namespace', 'project_namespace'])
        self.assertEquals(resolve(url).func.view_class, ProjectDetail)
    def test_issue_detail_is_resolved(self):
        url = reverse('main:issue_detail', args=['team_namespace', 'project_namespace', 0])
        self.assertEquals(resolve(url).func.view_class, IssueDetail)

    def test_project_form_is_resolved(self):
        url = reverse('main:project_form', args=['team_namespace'])
        self.assertEquals(resolve(url).func.view_class, ProjectFormView)
    def test_issue_form_is_resolved(self):
        url = reverse('main:issue_form', args=['team_namespace', 'project_namespace'])
        self.assertEquals(resolve(url).func.view_class, IssueFormView)

    def test_issue_delete_is_resolved(self):
        url = reverse('main:issue_delete', args=['team_namespace', 'project_namespace', 0])
        self.assertEquals(resolve(url).func.view_class, IssueDelete)
    def test_project_delete_is_resolved(self):
        url = reverse('main:project_delete', args=['team_namespace', 'project_namespace'])
        self.assertEquals(resolve(url).func.view_class, ProjectDelete)
    def test_team_delete_is_resolved(self):
        url = reverse('main:team_delete', args=['team_namespace'])
        self.assertEquals(resolve(url).func.view_class, TeamDelete)

class TestViews(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.homepage_url = reverse('homepage')
        self.authors_q_url = reverse('author_q', args=['some-author'])

        self.author1 = Author.objects.create(
            name = 'some-author',
            address = 'TestAdress',
            city = 'TestCity',
            country = 'TestCountry'
        )

    def test_project_homepage_GET(self):
        client = Client()

        response = client.get(self.homepage_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'base_generic.html')

    def test_project_authors_GET(self):
        client = Client()

        response = client.get(self.authors_q_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/book_list.html')
