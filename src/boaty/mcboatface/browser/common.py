from zope.publisher.browser import BrowserView
from Products.CMFPlone.PloneBatch import Batch
from plone import api



class StudentList(BrowserView):
    """
    student list
    """
    def getQuery(self):
        sort_on = self.sort_on()
        path = '/'.join(self.context.getPhysicalPath())
        query_dict = {'path': path, 'portal_type': 'Student',
                      'depth': 1, 'sort_on': sort_on, 'sort_order': 'reverse'}
        age = self.get_age()
        if age not in [None, '']:
            query_dict['age'] = age
        gender = self.get_gender()
        if gender not in [None, '']:
            query_dict['gender'] = gender
        
        return query_dict

    def getStudents(self):
        b_start = self.batch_start()
        b_size = self.batch_size()
        query = self.getQuery()
        result = self.context.portal_catalog.searchResults(
           query
        )
        batch = Batch(result, b_size, int(b_start), orphan=0)
        total = len(result)
        return [batch, total]
    
    def get_age(self):
        value = self.request.get('age', None)
        return value
    
    def get_gender(self):
        value = self.request.get('gender', None)
        return value
    
    def sort_on(self):
        value = self.request.get('sort_on', 'created')
        return str(value)

    def batch_start(self):
        value = self.request.get('b_start', 0)
        return int(value)

    def batch_size(self):
        b_size = 10
        if self.context.REQUEST.get('b_size', 10) not in (None, '', 10):
            b_size = self.context.REQUEST.get('b_size')
            if b_size == 'all':
                b_size = 1000
            else:
                b_size = int(b_size)

        if self.context.REQUEST.get('filterBy') == 'lockable' or self.context.REQUEST.get('filterBy') == 'confirmable':
            b_size = 1000
            self.context.REQUEST.set('b_size', 'all')

        return b_size

class StudentPortfolios(StudentList):
    """"""

    def __call__(self):
        query = self.context.REQUEST.get("something")
        # do something with query

        return self.index()

class StudentDashboard(BrowserView):
    """"""
    def get_username(self):
        user = api.user.get_current()
        return user.getId()